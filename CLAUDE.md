# CLAUDE.md

A lab for one SO-101 Pro robot arm: a leader arm, a follower arm, a wrist camera on the
follower and a scene camera on the laptop. The repo holds everything done with that arm,
from plain Python examples for first-year students to VLA training, zero-shot control with
reasoning models and voice commands.

Everything here is in English and in Python. `README.md` maps the repo.

## This repo will be public

It is private now and will be opened later, history included. Nothing private goes into a
commit: no home directory paths, no credentials, no personal accounts, no names of private
repos or private notes. Ports and camera indexes are machine facts, not secrets, and live in
`config/robot.yaml`. Keys live in a gitignored `.env`; `.env.example` lists them blank.

## Hardware facts that cost money when forgotten

- **Leader runs on 5 V, follower on 12 V.** Swapping the supplies destroys motors.
- **STS3215 servos have no brake.** With torque off the arm falls. Both arms are clamped to
  the table and a hand is ready whenever torque is released.
- **Calibration is an agreement about zero.** A dataset, a keyframe file and a trained policy
  are valid only for the calibration they were made on. The calibration ids are
  `ive_follower` and `ive_leader` and are the same in every command.
- **The gripper overheats first.** Motors go into protection near 71 °C. Long sessions read
  `Present_Temperature`.

## Rules for code that moves the arm

- Nothing runs on hardware before a dry run: print or simulate the targets, then move.
- Once anything other than a person decides a motion (an LLM, a policy, a voice command),
  it goes through the safety layer in `src/so101/safety/`: joint, speed and workspace
  limits, a timeout, a software e-stop, and an action ledger so that a network retry never
  repeats a physical motion.
- A model never sends raw joint angles. It calls named primitives with validated arguments.
- A task string for a policy is verbatim: the string used at rollout is the exact
  `--dataset.single_task` used at recording. Free language is the orchestrator's job.
- SmolVLA is fine-tuned with `--policy.path=lerobot/smolvla_base`, never
  `--policy.type=smolvla`, which trains from scratch.

## LeRobot changes fast

The lab is pinned to LeRobot 0.7.0. Command names and flags have changed between releases
(`lerobot-record` for evaluation became `lerobot-rollout`, SmolVLA training gained a required
`--rename_map`, Trackio replaced Weights & Biases). The commands in `docs/guides/` were
checked against the LeRobot documentation when written. Before
changing or adding one, check the current documentation instead of writing it from memory.

## Where things go

| What | Where |
|---|---|
| How to do something, with commands | `docs/guides/` |
| Why something works the way it does | `docs/knowledge/` |
| A decision and its reason | `docs/decisions.md` |
| One line per training or evaluation run | `docs/experiments.md` |
| Code that survives | `src/so101/` |
| Student lessons, fun programs and arm tools, no AI | `teaching/`, indexed by its `README.md` |
| How the coding assistant writes and runs them | `.claude/skills/arm-teach/` |
| A step of the learning ladder | `labs/<nn>-<name>/` with goal, command and done-when |
| An open-ended trial with a result | `experiments/<date>-<name>/` |
| A note on a new model, paper or release | `research/<date>-<name>.md` |
| A robot skill as data | `behaviors/<name>/` |

A folder is created when its first file is. Datasets and checkpoints live on the Hugging
Face Hub, never in the repo. When code from a lab is needed a second time, it moves to
`src/so101/`.
