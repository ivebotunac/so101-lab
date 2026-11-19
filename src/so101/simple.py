"""Student API for the SO-101 follower arm: plain functions, angles in degrees.

Runs on the real arm when config/robot.yaml names a follower port, otherwise on a
simulated arm that prints each motion. SO101_SIM=1 forces the simulation.

Zero degrees is the middle of a joint's calibrated range. The gripper goes from
0 (closed) to 100 (open).
"""

import atexit
import json
import os
import time
from pathlib import Path

JOINTS = ("shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper")

CONFIG = Path(__file__).resolve().parents[2] / "config" / "robot.yaml"
MAX_SPEED = 90.0        # degrees per second
MAX_TEMPERATURE = 65    # °C, the motor protects itself near 71
LIMIT_MARGIN = 3.0      # degrees kept free before each end of a joint
STEP = 0.02             # seconds between two targets sent to the motors

CALIBRATION = Path.home() / ".cache/huggingface/lerobot/calibration/robots/so_follower"

_arm = None


def _limits(ranges):
    """Turn calibrated ranges, {joint: (range_min, range_max)}, into limits in degrees."""
    limits = {}
    for joint, (range_min, range_max) in ranges.items():
        if joint == "gripper":
            limits[joint] = (0.0, 100.0)
            continue
        half = (range_max - range_min) / 2 * 360 / 4095
        half = round(min(half - LIMIT_MARGIN, 170.0), 1)
        limits[joint] = (-half, half)
    return limits


class _SimulatedArm:
    simulated = True
    # Nominal ranges, used only when no arm is connected.
    limits = {
        "shoulder_pan": (-100.0, 100.0),
        "shoulder_lift": (-90.0, 90.0),
        "elbow_flex": (-90.0, 90.0),
        "wrist_flex": (-90.0, 90.0),
        "wrist_roll": (-150.0, 150.0),
        "gripper": (0.0, 100.0),
    }

    def __init__(self):
        self.angles = {joint: 0.0 for joint in JOINTS}
        # With a calibration on this computer the dry run has the real arm's limits.
        files = sorted(CALIBRATION.glob("*.json"))
        if files:
            calibration = json.loads(files[0].read_text())
            self.limits = _limits({j: (c["range_min"], c["range_max"]) for j, c in calibration.items()})

    def read(self, joint):
        return self.angles[joint]

    def write(self, targets):
        self.angles.update(targets)

    def temperature(self, joint):
        return 30

    def release(self):
        pass


class _RealArm:
    simulated = False

    def __init__(self, port, robot_id):
        from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig

        calibrate = (
            f"lerobot-calibrate --robot.type=so101_follower --robot.port={port} --robot.id={robot_id}"
        )
        # Torque stays on at exit, so the arm holds its pose instead of falling.
        config = SO101FollowerConfig(port=port, id=robot_id, disable_torque_on_disconnect=False)
        self.robot = SO101Follower(config)
        if not self.robot.calibration:
            raise RuntimeError(f"The arm is not calibrated. Run:\n  {calibrate}")
        self.robot.connect(calibrate=False)
        if not self.robot.is_calibrated:
            self.robot.disconnect()
            raise RuntimeError(f"The calibration file does not match the motors. Run:\n  {calibrate}")
        atexit.register(self.robot.disconnect)

        self.limits = _limits(
            {joint: (c.range_min, c.range_max) for joint, c in self.robot.calibration.items()}
        )

    def read(self, joint):
        return self.robot.bus.read("Present_Position", joint, num_retry=2)

    def write(self, targets):
        self.robot.send_action({f"{joint}.pos": angle for joint, angle in targets.items()})

    def temperature(self, joint):
        return self.robot.bus.read("Present_Temperature", joint, normalize=False, num_retry=2)

    def release(self):
        self.robot.bus.disable_torque()


def _config():
    try:
        import yaml
    except ImportError:
        return {}
    return yaml.safe_load(CONFIG.read_text())["follower"]


def _follower_config():
    if os.environ.get("SO101_SIM") == "1":
        return None
    follower = _config()
    return follower if follower.get("port") else None


def _get_arm():
    global _arm
    if _arm is None:
        follower = _follower_config()
        if follower is None:
            print("[sim] No arm connected, motions are printed instead.")
            _arm = _SimulatedArm()
        else:
            _arm = _RealArm(follower["port"], follower["id"])
    return _arm


def _check_joint(joint):
    if joint not in JOINTS:
        raise ValueError(f"Unknown joint '{joint}'. The joints are: {', '.join(JOINTS)}.")


def _run(targets, speed):
    arm = _get_arm()
    if speed <= 0:
        raise ValueError(f"Speed must be above 0, got {speed}.")
    speed = min(speed, MAX_SPEED)

    for joint, angle in targets.items():
        _check_joint(joint)
        low, high = arm.limits[joint]
        if not low <= angle <= high:
            raise ValueError(f"{joint} can go from {low} to {high}, got {angle}.")
        temperature = arm.temperature(joint)
        if temperature > MAX_TEMPERATURE:
            raise RuntimeError(f"{joint} is at {temperature} °C. Let the arm cool down.")

    start = {joint: arm.read(joint) for joint in targets}
    if arm.simulated:
        for joint, angle in targets.items():
            print(f"[sim] {joint}: {start[joint]:.1f} -> {angle:.1f}")
        arm.write({joint: float(angle) for joint, angle in targets.items()})
        return

    longest = max(abs(angle - start[joint]) for joint, angle in targets.items())
    steps = max(1, int(longest / speed / STEP))
    for i in range(1, steps + 1):
        t = i / steps
        ease = t * t * (3 - 2 * t)  # slow start and slow stop
        arm.write({joint: start[joint] + (angle - start[joint]) * ease for joint, angle in targets.items()})
        time.sleep(STEP)
    time.sleep(0.2)  # let the motor settle on the target


def move(joint, angle, speed=45):
    """Move one joint to an angle in degrees and wait until it gets there."""
    _run({joint: angle}, speed)


def pose(speed=45, **angles):
    """Move several joints at once: pose(shoulder_pan=20, elbow_flex=30)."""
    _run(angles, speed)


def read_angle(joint):
    """Return the current angle of a joint in degrees."""
    _check_joint(joint)
    return round(_get_arm().read(joint), 1)


def lowest_angle(joint):
    """Return the smallest angle the joint accepts."""
    _check_joint(joint)
    return _get_arm().limits[joint][0]


def highest_angle(joint):
    """Return the largest angle the joint accepts."""
    _check_joint(joint)
    return _get_arm().limits[joint][1]


def read_temperature(joint):
    """Return the temperature of a joint's motor in °C."""
    _check_joint(joint)
    return _get_arm().temperature(joint)


def open_gripper():
    """Open the gripper."""
    _run({"gripper": 90}, 60)


def close_gripper():
    """Close the gripper, short of pressing the claws together."""
    _run({"gripper": 10}, 60)


def home(speed=30):
    """Move every joint to the middle of its range, all at once."""
    targets = {joint: 0.0 for joint in JOINTS}
    targets["gripper"] = 10.0
    _run(targets, speed)


def rest(speed=25):
    """Fold the arm into its rest pose from config/robot.yaml, then switch the motors off."""
    arm = _get_arm()
    targets = {}
    for joint, angle in (_config().get("rest_pose") or {}).items():
        low, high = arm.limits[joint]
        targets[joint] = min(max(angle, low), high)
    if targets:
        _run(targets, speed)
    if arm.simulated:
        print("[sim] motors off")
    else:
        arm.release()


def relax():
    """Switch the motors off. The arm falls, so hold it first."""
    arm = _get_arm()
    if arm.simulated:
        print("[sim] motors off")
        return
    print("Hold the arm: the motors switch off in 3 seconds.")
    time.sleep(3)
    arm.release()
