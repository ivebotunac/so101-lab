# The arm in a programming course

Plain Python functions that move the follower arm, for students who are learning variables,
conditions, loops and functions. No leader arm, no camera, no AI: a line of code runs and a
joint turns.

## What is needed

- The follower arm, clamped to the table, on its **12 V** supply. The voltage is printed on
  the adapter as its output. The follower is the arm with the claws; the leader, with the
  handle and trigger, stays in its box together with its 5 V supply.
- One USB cable to the computer.

## Install

From the root of the repo, with [uv](https://docs.astral.sh/uv/):

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -e '.[arm]'
source .venv/bin/activate
```

This installs LeRobot 0.7.0 with the Feetech motor support and nothing for datasets or
training; those come with the [full setup](setup-macos.md). A computer without the arm needs
no install at all: `PYTHONPATH=src python3 teaching/05_loops.py` runs on the simulated arm.

## Connect and calibrate, once

1. Plug in the 12 V supply, then the USB cable.
2. Find the port: `lerobot-find-port`. It asks for the USB cable to be unplugged and names
   the port that disappeared.
3. Write the port into `config/robot.yaml` under `follower.port`.
4. Calibrate:

   ```bash
   lerobot-calibrate --robot.type=so101_follower --robot.port=<FOLLOWER_PORT> --robot.id=ive_follower
   ```

   The motors go limp, so hold the arm. Move every joint to the middle of its range, press
   Enter, then move each joint slowly through its whole range and press Enter again. The
   video is at https://huggingface.co/docs/lerobot/so101#calibration-video.

Calibration sets where zero is and how far each joint travels, and the functions below take
their limits from it. It is repeated only after the arm has been taken apart. If the command
reports missing motors, the motor ids were never written; that is
`lerobot-setup-motors`, step 2 of the [full setup](setup-macos.md).

## First motion

```bash
python teaching/00_check_arm.py     # reads six angles and temperatures, moves nothing
python teaching/01_first_move.py    # rolls the wrist by 15 degrees and back
```

Keep a hand on the power supply's plug for the first runs. `SO101_SIM=1` in front of any
command runs it on the simulated arm instead, which is the dry run before a new program
goes to the motors.

## The functions

```python
from so101.simple import move, read_angle, home
```

| Function | Does |
|---|---|
| `move(joint, angle, speed=45)` | Moves one joint to an angle in degrees and waits until it is there |
| `read_angle(joint)` | Returns the current angle |
| `lowest_angle(joint)`, `highest_angle(joint)` | Return the limits of a joint |
| `read_temperature(joint)` | Returns the motor temperature in °C |
| `open_gripper()`, `close_gripper()` | Open and close the claws |
| `home()` | Moves every joint to the middle of its range |
| `relax()` | Switches the motors off after three seconds; the arm falls, so hold it |

The joints are `shoulder_pan`, `shoulder_lift`, `elbow_flex`, `wrist_flex`, `wrist_roll` and
`gripper`. Zero degrees is the middle of a joint's calibrated range. The gripper is not in
degrees: 0 is closed and 100 is open.

- An angle outside the limits raises `ValueError` and nothing moves.
- Speed is in degrees per second and is capped at 90.
- A motor above 65 °C refuses to move until it cools.
- When a program ends the motors keep holding the pose. Finish a session with `home()` or,
  with a hand on the arm, `relax()`.

## Examples by lecture

| File | Topic |
|---|---|
| `teaching/03_variables.py` | A reading stored in a variable, an expression, an f-string, types |
| `teaching/04_conditions.py` | `if`, `elif`, `else` and `and` decide whether a joint may move |
| `teaching/05_loops.py` | `while`, `for`, `range()` and `break` repeat a motion |
| `teaching/06_functions.py` | `wave()`, `nod()`, default arguments, a return value, a program made of functions |
