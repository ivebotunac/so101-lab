# Functions: a motion gets a name, parameters and a return value.
from so101.simple import close_gripper, highest_angle, home, lowest_angle, move, open_gripper


def wave(times=3, width=40):
    """Roll the wrist left and right."""
    for i in range(times):
        move("wrist_roll", width, speed=90)
        move("wrist_roll", -width, speed=90)
    move("wrist_roll", 0)


def nod(times=2):
    """Bend the wrist down and up."""
    for i in range(times):
        move("wrist_flex", 25, speed=60)
        move("wrist_flex", -10, speed=60)
    move("wrist_flex", 0)


def clap(times=2):
    """Open and close the gripper."""
    for i in range(times):
        open_gripper()
        close_gripper()


def clamp_angle(joint, angle):
    """Return the angle, or the nearest limit of the joint when it is outside."""
    if angle < lowest_angle(joint):
        return lowest_angle(joint)
    if angle > highest_angle(joint):
        return highest_angle(joint)
    return angle


def greet():
    """A program made of functions: each call is one motion."""
    move("shoulder_lift", clamp_angle("shoulder_lift", -20))
    wave()
    nod()
    clap(times=1)


home()
greet()
wave(times=2, width=20)             # the same function, a shy wave
print(clamp_angle("elbow_flex", 500))
home()
