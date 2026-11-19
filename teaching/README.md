# Teaching

Python programs that move a robot arm, for students in their first programming course. No
AI and no camera: a line of code runs and a joint turns. Every program here uses only what
the course has covered by that lecture.

Without the arm, every program runs on a simulated arm that prints each motion. With the
arm, [the setup guide](../docs/guides/teaching-arm.md) covers power, the port and
calibration.

## Running a program

From the root of the repo:

```bash
source .venv/bin/activate
python teaching/lessons/05_loops.py              # on the arm
SO101_SIM=1 python teaching/lessons/05_loops.py  # on the simulated arm
```

Without an installed environment the simulated arm still works:
`PYTHONPATH=src python3 teaching/lessons/05_loops.py`. The programs under `fun/` are run
from their own folder: `cd teaching/fun && python dance.py`.

## The arm in one picture

The arm has five joints and a gripper. Zero degrees is the middle of a joint's range, and an
angle is positive to one side of it and negative to the other.

| Joint | Moves |
|---|---|
| `shoulder_pan` | the whole arm, left and right around the base |
| `shoulder_lift` | the upper arm, forward and back |
| `elbow_flex` | the forearm, up and down |
| `wrist_flex` | the gripper, up and down |
| `wrist_roll` | the gripper, around its own axis |
| `gripper` | the claws, from 0 (closed) to 100 (open) |

## The functions

```python
from so101.simple import move, pose, read_angle, home
```

| Function | Does |
|---|---|
| `move(joint, angle, speed=45)` | Moves one joint to an angle in degrees and waits until it is there |
| `pose(speed=45, elbow_flex=30, wrist_roll=-20)` | Moves several joints at once, each named as a keyword argument |
| `home()` | Moves every joint to the middle of its range |
| `read_angle(joint)` | Returns the current angle of a joint |
| `lowest_angle(joint)`, `highest_angle(joint)` | Return the limits of a joint |
| `read_temperature(joint)` | Returns the temperature of the joint's motor in °C |
| `open_gripper()`, `close_gripper()` | Open and close the claws |
| `rest()` | Folds the arm into its rest pose and switches the motors off |
| `relax()` | Switches the motors off where the arm stands; it falls, so hold it |

What the arm refuses:

- An angle outside the limits raises `ValueError` and nothing moves.
- A speed above 90 degrees per second is lowered to 90.
- A motor above 65 °C raises `RuntimeError` until it cools.

When a program ends the motors keep holding the last pose.
`python teaching/park_arm.py` ends a session.

## Lessons

One file per lecture, each ending with a few tasks under `# Try it:`.

| File | Lecture | The arm shows |
|---|---|---|
| `lessons/01_first_program.py` | The first program | Statements run top to bottom; a sensor reading is a value |
| `lessons/02_algorithms.py` | Algorithms | Sequence, decision and repetition; the order of steps |
| `lessons/03_variables.py` | Variables, types, operators, input and output | Assignment, `int`, `float`, `str`, `bool`, swapping, `//` and `%`, `input()`, f-strings |
| `lessons/04_conditions.py` | Conditions | `if`, `elif`, `else`, nested conditions, `and`, `or`, `not` |
| `lessons/05_loops.py` | Loops | `while`, `for`, `range()`, an accumulator, `break`, `continue`, nested loops |
| `lessons/06_functions.py` | Functions | `def`, parameters, default arguments, `return`, local variables, `random` |
| `lessons/07_review.py` | Review of lectures 1 to 6 | The arm driven from the keyboard: commands, checks, Euclid's algorithm |

## Fun

Programs for showing what the arm can do. They use the same functions and nothing beyond
lecture 6, so each one can be read in class.

| File | Does |
|---|---|
| `fun/gestures.py` | The gestures the others import: `wave`, `nod`, `shake`, `shrug`, `bow`, `clap`, `look_around`, `think`, `celebrate`, `sleep`, `wake_up` |
| `fun/show.py` | Every gesture, one after another |
| `fun/greet.py` | Asks for a name, waves once per letter and bows |
| `fun/dance.py` | Three dance figures in loops, then three picked at random |
| `fun/oracle.py` | Answers yes or no questions with a nod, a shake or a shrug |
| `fun/guess_the_angle.py` | Turns the base to a secret angle; the player guesses it |

## Tools

| File | Does |
|---|---|
| `check_arm.py` | Prints the angle and temperature of every joint, moves nothing |
| `first_move.py` | Rolls the wrist by 15 degrees and back, the first test after calibration |
| `park_arm.py` | Folds the arm and switches the motors off |
