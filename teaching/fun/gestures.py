# Gestures built from move() and pose(): the other scripts in this folder import them.
from so101.simple import close_gripper, home, move, open_gripper, pose


def wave(times=3, width=50):
    """Raise the forearm and roll the wrist left and right."""
    print(f"wave(): the wrist rolls left and right, {times} times")
    pose(elbow_flex=45, wrist_flex=-20)
    for i in range(times):
        print(f"  wave {i + 1} of {times}")
        move("wrist_roll", width, speed=90)
        move("wrist_roll", -width, speed=90)
    home()


def nod(times=2):
    """Yes: the wrist bends down and up."""
    print(f"nod(): yes, the wrist bends down and up, {times} times")
    for i in range(times):
        print(f"  nod {i + 1} of {times}")
        move("wrist_flex", 30, speed=90)
        move("wrist_flex", -5, speed=90)
    move("wrist_flex", 0)


def shake(times=2):
    """No: the base turns left and right."""
    print(f"shake(): no, the base turns left and right, {times} times")
    for i in range(times):
        print(f"  shake {i + 1} of {times}")
        move("shoulder_pan", 18, speed=90)
        move("shoulder_pan", -18, speed=90)
    move("shoulder_pan", 0)


def shrug():
    """Maybe: the arm leans back with an open gripper."""
    print("shrug(): maybe, the arm leans back with an open gripper")
    pose(shoulder_lift=-20, wrist_flex=-25, gripper=90, speed=90)
    pose(shoulder_lift=0, wrist_flex=0, gripper=10, speed=60)


def bow():
    """Lean forward, hold, and come back."""
    print("bow(): the arm leans forward, holds and comes back")
    pose(shoulder_lift=15, elbow_flex=20, wrist_flex=40, speed=40)
    pose(shoulder_lift=15, elbow_flex=20, wrist_flex=45, speed=10)
    home()


def clap(times=3):
    """Open and close the gripper quickly."""
    print(f"clap(): the gripper opens and closes, {times} times")
    for i in range(times):
        print(f"  clap {i + 1} of {times}")
        move("gripper", 70, speed=90)
        move("gripper", 10, speed=90)


def look_around():
    """Turn slowly to both sides, as if searching for something."""
    print("look_around(): the base turns slowly to both sides")
    pose(shoulder_pan=45, wrist_flex=-15, speed=40)
    move("wrist_roll", 25)
    pose(shoulder_pan=-45, wrist_roll=-25, speed=40)
    home()


def think():
    """Tilt the wrist and tap the gripper twice."""
    print("think(): the wrist tilts and the gripper taps")
    pose(elbow_flex=30, wrist_roll=35, speed=40)
    clap(times=2)
    home()


def celebrate():
    """Arm up, a fast roll of the wrist and a round of claps."""
    print("celebrate(): arm up, fast wrist and applause")
    pose(shoulder_lift=-15, elbow_flex=60, wrist_flex=-30, speed=90)
    for i in range(2):
        move("wrist_roll", 90, speed=90)
        move("wrist_roll", -90, speed=90)
    move("wrist_roll", 0, speed=90)
    clap()
    home()


def sleep():
    """Fold down slowly and close the gripper."""
    print("sleep(): the arm folds down")
    close_gripper()
    pose(shoulder_lift=-40, elbow_flex=70, wrist_flex=50, speed=25)


def wake_up():
    """Unfold from the sleeping pose and stretch the gripper."""
    print("wake_up(): the arm unfolds and stretches the gripper")
    home(speed=25)
    open_gripper()
    close_gripper()
