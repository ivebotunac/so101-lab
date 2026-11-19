# Setting up the arm for teaching

From a boxed kit to an arm that runs the programs in [`teaching/`](../../teaching/README.md).
Only the follower arm is used: no leader arm, no camera. The functions and the lessons are
described in that folder's README.

## What is needed

- The follower arm, clamped to the table, on its **12 V** supply. The voltage is printed on
  the adapter as its output and on the sticker of each motor. The follower is the arm with
  the claws; the leader, with the handle and trigger, stays in its box together with its 5 V
  supply, so the two supplies cannot be swapped.
- One USB cable to the computer.
- Free space around the arm. What the joints are shown during calibration is all the arm
  will ever use, so a small table only needs a shorter sweep.

## Install

From the root of the repo, with [uv](https://docs.astral.sh/uv/):

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -e '.[arm]'
source .venv/bin/activate
```

This installs LeRobot 0.7.0 with the Feetech motor support and nothing for datasets or
training; those come with the [full setup](setup-macos.md).

## Connect and calibrate, once

1. Plug in the 12 V supply, then the USB cable.
2. Find the port: `lerobot-find-port`. It asks for the USB cable to be unplugged and names
   the port that disappeared. On macOS, `ls /dev/tty.usbmodem*` lists it directly.
3. Write the port into `config/robot.yaml` under `follower.port`.
4. Calibrate:

   ```bash
   lerobot-calibrate --robot.type=so101_follower --robot.port=<FOLLOWER_PORT> --robot.id=ive_follower
   ```

   The motors go limp, so hold the arm.

   - Move every joint to the middle of its range, the gripper half open, and press Enter.
   - Move each joint slowly from one end of its travel to the other, the gripper included.
     `wrist_roll` is skipped, it turns a full circle. The table on screen shows MIN and MAX
     for each motor changing as the joint moves.
   - Press Enter. The calibration is saved under the id `ive_follower`.

   When a calibration already exists the command first offers to keep it; `c` and Enter
   starts a new one. The video is at
   https://huggingface.co/docs/lerobot/so101#calibration-video.

Calibration sets where zero is and how far each joint travels, and writes those ends into
the motors. Three things follow:

- **The sweep is the workspace.** A joint moved through half of its travel is limited to
  that half. On a crowded table this is the way to keep the arm inside the free space.
- **The pose the arm lies in when it is off has to be inside the sweep.** Fold the arm all
  the way during calibration; otherwise the motors start outside their own limits.
- **A joint that was not moved does not move.** A gripper left alone gets a range of zero.

It is repeated only after the arm has been taken apart or moved to a table with different
free space. If the command reports missing motors, the motor ids were never written; that
is `lerobot-setup-motors`, step 2 of the [full setup](setup-macos.md).

## First motion

```bash
python teaching/check_arm.py     # reads six angles and temperatures, moves nothing
python teaching/first_move.py    # rolls the wrist by 15 degrees and back
```

`check_arm.py` switches the motors on, so the arm stiffens and holds its pose from then on.
Keep a hand on the plug of the power supply for the first runs.

## The rest pose

`rest()` and `teaching/park_arm.py` fold the arm before the motors switch off. The pose they
go to is `follower.rest_pose` in `config/robot.yaml`: the angles `check_arm.py` printed
while the arm lay folded on the table, before anything moved it. After a new calibration,
read them again and replace the six numbers.

## A session

1. Power, then USB. `python teaching/check_arm.py` shows that the arm answers.
2. A new program goes to the simulated arm first: `SO101_SIM=1 python <file>`. The simulated
   arm has the real arm's limits once a calibration exists on the computer, so a program
   that passes there is not refused by the motors.
3. The same command without `SO101_SIM=1` runs it on the arm.
4. `python teaching/park_arm.py` ends the session. Then the power can be unplugged.

During a long session, `check_arm.py` every few minutes shows the temperatures. The
functions refuse to move a motor above 65 °C.

## When something is wrong

| What happens | Why | What to do |
|---|---|---|
| `The arm is not calibrated` | No calibration file under the id in `config/robot.yaml` | Calibrate |
| `The calibration file does not match the motors` | The motors hold another calibration | Calibrate, or keep the file when the command offers it |
| `ValueError: ... can go from ... to ...` | The angle is outside what calibration recorded | Use a smaller angle, or calibrate with a wider sweep |
| A program prints `[sim]` lines and the arm stands still | No port in `config/robot.yaml`, or `SO101_SIM=1` is set | Write the port, unset the variable |
| The port is not found | Cable, power, or a board that needs the CH340 driver | See the [full setup](setup-macos.md) |
| The arm drops when a program starts | The motors were off and the arm was not resting | Start from the rest pose, or hold the arm |
