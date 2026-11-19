---
name: arm-teach
description: Writes student lessons, gestures and fun programs under teaching/ and runs them, simulated first, on the real SO-101 arm only after a yes. Also checks and parks the arm. Use for a lesson or demo, to run something on the arm, to start or end a session. Triggers - napravi lekciju, nova gesta, pokreni na ruci, provjeri ruku, parkiraj ruku, write a lesson, run it on the arm. Not datasets or training.
---

# Teaching with the arm

`teaching/README.md` is what students read: the functions, the lessons and the fun programs.
`docs/guides/teaching-arm.md` is the setup: power, port, calibration, the rest pose and a
table of failures. Read the README before writing a program and the guide before touching
the hardware.

## The arm moves only on a yes

A program runs on the real arm when the user said yes to that run in the current turn, and
is at the arm. A yes for one program is not a yes for the next. Everything else runs with
`SO101_SIM=1`, which reaches no motor.

Reading is not moving, but it is not free either: `check_arm.py` connects, and connecting
switches the motors on, so an arm that was limp stiffens. Say so before the first connect of
a session.

## Running a program

All commands from the root of the repo.

1. **Dry run.** `SO101_SIM=1 .venv/bin/python <file>`, with every `input()` answered through
   a pipe: `printf '30\nquit\n' | SO101_SIM=1 .venv/bin/python <file>`. Programs under
   `teaching/fun/` import `gestures.py`, so they run from that folder:
   `( cd teaching/fun && SO101_SIM=1 ../../.venv/bin/python dance.py )`. The simulated arm
   takes its limits from the calibration on this computer, so a `ValueError` here is the
   refusal the motors would give. A program with branches is run once per branch.
2. **Ask.** Name the program, say what the arm will do in one sentence and how far it
   reaches, and wait.
3. **Run.** The same command without `SO101_SIM=1`. A program that waits for the keyboard is
   run by the user in their own terminal.
4. **Report** what the program printed and, after a long or fast one,
   `.venv/bin/python teaching/check_arm.py` for the temperatures.

A session ends with `.venv/bin/python teaching/park_arm.py`, which folds the arm and
switches the motors off. It moves the arm, so it needs its own yes. An arm left holding a
pose keeps its motors warm.

## Writing a lesson

A lesson is `teaching/lessons/NN_<topic>.py`, where NN is the lecture. Its shape:

- The first line is a comment: `# Lecture N, <topic>: <what the program shows>.`
- Imports from `so101.simple`, only the functions used.
- `home()` before the first motion and after the last.
- Sections of a few lines, each opened by a one-line comment that states the idea in the
  words of the lecture, not the motion: "continue skips one pass, break ends the whole loop".
- Printed text says what the student should notice.
- The last block is `# Try it:` with three or four numbered tasks: predict before running,
  change one thing, write one small thing.

The lesson uses only what the course has covered by that lecture:

| By lecture | Students have |
|---|---|
| 1 | `print()`, calling a function, comments, comparing two values |
| 2 | sequence, decision and repetition as ideas; flowcharts |
| 3 | variables, `int`, `float`, `str`, `bool`, arithmetic with `//` and `%`, `input()`, `int()` and `float()`, f-strings |
| 4 | `if`, `elif`, `else`, nesting, `and`, `or`, `not`, chained comparison |
| 5 | `while`, `for`, `range()`, `break`, `continue`, nested loops, accumulators |
| 6 | `def`, parameters, default and keyword arguments, `return`, local variables, `math`, `random` |

Lists, tuples, dictionaries, exceptions, files and classes come later in the course. A
lesson for a later lecture adds its row here and its line to the table in
`teaching/README.md`.

## Writing a gesture or a fun program

A gesture is a function in `teaching/fun/gestures.py` with a one-line docstring, built from
`move()` and `pose()`, ending where it started or in `home()`. A fun program is a file in
`teaching/fun/` that imports gestures and stays within lecture 6, so that it can be read
aloud in class. Both get a line in `teaching/README.md`.

## Angles that are safe to write

Zero is the middle of each joint's calibrated range and the limits differ per arm, so a
program asks for them with `lowest_angle()` and `highest_angle()` whenever it goes near an
end. Away from the ends:

- `shoulder_pan` and `wrist_roll` within 60 degrees of zero, `wrist_flex` within 45.
- `elbow_flex` from -30 to 70. Negative lowers the forearm toward the table.
- `shoulder_lift` from -40 to 20. Positive leans the arm forward, and forward plus a lowered
  forearm reaches the table, so the two are never combined at their ends.
- `speed` up to 90. Fast and wide repeated motions heat the motors; the gripper heats first.

The signs above were read on this lab's arm. After a new calibration, check them with one
small `move()` per joint before trusting a new gesture.

## When the library has to change

`src/so101/simple.py` stays plain functions with no classes in its public face, because
students read its docstrings. A new function there is added to the table in
`teaching/README.md` in the same change, and anything that touches how the motors are driven
is checked against the LeRobot version pinned in `pyproject.toml`, not written from memory.
