# A dance: three figures made of poses, repeated in loops, with a random finish.
import random

from gestures import celebrate, clap
from so101.simple import home, move, pose


def sway(times=2):
    """Lean left and right with the whole arm."""
    print(f"sway(): the arm leans left and right, {times} times")
    for i in range(times):
        print(f"  sway {i + 1} of {times}")
        pose(shoulder_pan=30, wrist_roll=40, elbow_flex=20, speed=70)
        pose(shoulder_pan=-30, wrist_roll=-40, elbow_flex=20, speed=70)
    pose(shoulder_pan=0, wrist_roll=0, elbow_flex=0, speed=70)


def pump(times=3):
    """Elbow up and down, the gripper opens at the top."""
    print(f"pump(): the elbow goes up and down, {times} times")
    for i in range(times):
        print(f"  pump {i + 1} of {times}")
        pose(elbow_flex=50, gripper=80, speed=90)
        pose(elbow_flex=10, gripper=10, speed=90)


def twist(times=2):
    """The wrist rolls while the base turns the other way."""
    print(f"twist(): the wrist and the base turn against each other, {times} times")
    for i in range(times):
        print(f"  twist {i + 1} of {times}")
        pose(shoulder_pan=-25, wrist_roll=80, wrist_flex=20, speed=90)
        pose(shoulder_pan=25, wrist_roll=-80, wrist_flex=-20, speed=90)
    pose(shoulder_pan=0, wrist_roll=0, wrist_flex=0, speed=90)


def random_figure():
    """Pick one of the three figures by chance."""
    number = random.randint(1, 3)
    print(f"random_figure(): the number is {number}")
    if number == 1:
        sway(times=1)
    elif number == 2:
        pump(times=2)
    else:
        twist(times=1)


rounds = int(input("How many rounds (1 to 3)? "))
if rounds < 1 or rounds > 3:
    rounds = 1

print("home(): the arm goes to its starting pose")
home()
for number in range(1, rounds + 1):
    print(f"Round {number} of {rounds}")
    sway()
    pump()
    twist()
    clap(times=2)

print("Free style:")
for i in range(3):
    random_figure()

move("wrist_roll", 0)
celebrate()
