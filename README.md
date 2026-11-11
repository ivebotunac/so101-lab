# so101-lab

A working lab around one [SO-101](https://github.com/TheRobotStudio/SO-ARM100) Pro robot arm
and [LeRobot](https://github.com/huggingface/lerobot). It is used for three things:

- **Teaching.** Plain Python examples that move a motor or read an angle, for students who
  are learning to program and have not met AI yet.
- **Learning robotics.** A ladder of small labs, from one motor to a trained policy.
- **Research.** Trials with vision-language-action models, reasoning models that control the
  arm without training, and voice commands.

## The setup

| Part | Detail |
|---|---|
| Follower arm | SO-101 Pro, 6 x Feetech STS3215 at 12 V |
| Leader arm | SO-101, 6 x Feetech STS3215 at 5 V |
| Wrist camera | on the follower's gripper |
| Scene camera | on the laptop, sees the whole workspace |
| Microphone | on the laptop, for voice commands |
| Computer | macOS on Apple Silicon for control and recording, cloud GPU for training |

## Start here

1. [Setup on macOS](docs/guides/setup-macos.md): install, motors, calibration,
   teleoperation, cameras.
2. [Recording datasets](docs/guides/recording-datasets.md): the protocol and the commands.
3. [Training SmolVLA](docs/guides/training-smolvla.md): fine-tuning and evaluation.
4. [Motion without training](docs/guides/motion-without-training.md): gestures, pointing,
   the gripper as a mouth.
5. [Gemini ER and Argon](docs/guides/gemini-argon.md): a reasoning model that drives the arm
   through primitives.
6. [Voice control](docs/guides/voice-control.md): speech, skills, memory, perception.

Background reading is in [docs/knowledge](docs/knowledge): concepts, hardware, motion and
kinematics, resources, literature, and a [reading list](docs/knowledge/reading-list.md) of
tutorials and projects by topic. The target system and the order of work are in
[docs/architecture.md](docs/architecture.md), the reasons in
[docs/decisions.md](docs/decisions.md).

## Layout

```
config/          ports, calibration ids, camera indexes
docs/guides/     how to do something, with commands
docs/knowledge/  why it works that way
src/so101/       the library: motors, motion, kinematics, perception, safety, voice, agents
teaching/        student examples, no AI
labs/            the learning ladder, one folder per step
experiments/     dated open-ended trials
research/        dated notes on new models, papers and releases
behaviors/       robot skills as data
```

Folders appear as their first content does. Commands and numbers reflect LeRobot 0.7.0, the
release they were checked against; LeRobot moves fast, so check its documentation when a
command fails.
