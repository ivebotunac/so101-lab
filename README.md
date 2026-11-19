# so101-lab

A robotics lab built around one [SO-101](https://github.com/TheRobotStudio/SO-ARM100) robot
arm and [LeRobot](https://github.com/huggingface/lerobot), kept by Ive Botunac, PhD, assistant
professor at the Department of Mechatronics and Robotics, University of Zadar, Croatia.

The lab has two halves. **Teaching** uses the arm to teach first-year students the basics of
programming in Python. **Research** follows what is new in robot learning and tries it on the
same arm: vision-language-action models, models that see and point, reasoning models that
drive the arm through tools, and voice.

## Teaching

The arm is part of the course *Osnove programiranja* (Introduction to Programming) in the
first year of the undergraduate programme in Mechatronics and Robotics. The idea is simple:
every idea in the course becomes a motion. A variable holds an angle, a condition decides
whether a joint may move, a loop repeats a wave, a function gives a gesture its name. The
programs use no AI and no camera, so what a student reads in the code is all that happens.

- **One lesson per lecture.** [`teaching/lessons/`](teaching/lessons) follows the course week
  by week, and each lesson uses only what the course has covered by then. Every lesson ends
  with tasks: predict, change one thing, write one small thing.
- **Simulation first, then the arm.** Every program runs on a simulated arm that prints each
  motion, at home and without any install. The same file then moves the real arm in class.
- **Something to show.** [`teaching/fun/`](teaching/fun) has gestures, a dance, a greeting, a
  yes-or-no oracle and a guessing game, all written with what the students already know.

[`teaching/README.md`](teaching/README.md) lists the functions, the lessons and the
programs. [Setting up the arm for teaching](docs/guides/teaching-arm.md) gets a boxed arm
ready for class.

Try it without an arm:

```bash
git clone https://github.com/ivebotunac/so101-lab.git
cd so101-lab
PYTHONPATH=src python3 teaching/lessons/05_loops.py
```

## Research

The field moves every month, so the lab reads continuously: papers, videos, Reddit and forum
threads, blog posts, repositories and releases. Each source gets a note in
[`research/`](research/README.md), sorted by topic, and a periodic stack review checks that
what the guides rely on still holds. What proves itself moves into the guides and the
knowledge base.

The directions:

- **Vision-language-action models.** SmolVLA fine-tuned on this arm's own demonstrations
  for a few tabletop skills: [training SmolVLA](docs/guides/training-smolvla.md).
- **Seeing and pointing.** A vision-language model finds an object in the camera image and
  the arm points at it, with no training.
- **Reasoning models.** A model plans and calls named, validated motions instead of sending
  raw angles: [Gemini Robotics ER and Argon](docs/guides/gemini-argon.md).
- **Voice.** A realtime speech model listens and answers while the arm gestures:
  [voice control](docs/guides/voice-control.md).

The target system and the order of work are in [the architecture](docs/architecture.md), the
reasons behind each choice in [the decision log](docs/decisions.md).

## The setup

| Part | Detail |
|---|---|
| Follower arm | SO-101 Pro, 6 x Feetech STS3215 at 12 V |
| Leader arm | SO-101, 6 x Feetech STS3215 at 5 V, used for teleoperation and recording |
| Wrist camera | on the follower's gripper |
| Scene camera | on the laptop, sees the whole workspace |
| Microphone | on the laptop, for voice commands |
| Computer | macOS on Apple Silicon for control and recording, a cloud GPU for training |

Teaching needs only the follower arm, its power supply and a USB cable.

## Installation

The lab runs on macOS with Apple Silicon and Python 3.12, managed with
[uv](https://docs.astral.sh/uv/). It is pinned to LeRobot 0.7.0. Other systems are likely to
work and are not tested.

For teaching, from the root of the repo:

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -e '.[arm]'
source .venv/bin/activate
cp config/robot.local.example.yaml config/robot.local.yaml   # then write your arm's port
```

For recording datasets and training, follow [setup on macOS](docs/guides/setup-macos.md).
API keys for the research guides go into `.env`, copied from `.env.example`. Both `.env` and
`config/robot.local.yaml` are gitignored.

## Guides

1. [Setting up the arm for teaching](docs/guides/teaching-arm.md): power, port, calibration,
   a session.
2. [Setup on macOS](docs/guides/setup-macos.md): the full install, motors, calibration of
   both arms, teleoperation, cameras.
3. [Recording datasets](docs/guides/recording-datasets.md): the protocol and the commands.
4. [Training SmolVLA](docs/guides/training-smolvla.md): fine-tuning and evaluation.
5. [Motion without training](docs/guides/motion-without-training.md): gestures, pointing,
   the gripper as a mouth.
6. [Gemini ER and Argon](docs/guides/gemini-argon.md): a reasoning model that drives the arm
   through primitives.
7. [Voice control](docs/guides/voice-control.md): speech, skills, memory, perception.

Background is in [`docs/knowledge/`](docs/knowledge): concepts, hardware, motion and
kinematics, resources, literature, and a [reading list](docs/knowledge/reading-list.md) of
tutorials and projects by topic.

## Working with Claude Code

The repo is set up for [Claude Code](https://claude.com/claude-code). Start it in the root
of the repo: [`CLAUDE.md`](CLAUDE.md) gives it the hardware facts and the rules for code that
moves the arm, and two skills in [`.claude/skills/`](.claude/skills) do the recurring work.

| Skill | Does |
|---|---|
| [`arm-teach`](.claude/skills/arm-teach/SKILL.md) | Writes a lesson for a lecture, a gesture or a fun program, runs it on the simulated arm, and on the real arm only after a yes for that run |
| [`research-note`](.claude/skills/research-note/SKILL.md) | Turns a paper, video, thread, repository or release into a note under `research/`, and runs the monthly stack review |

Both are plain instructions and can be read as a description of how the work is done here,
with or without Claude Code.

## Layout

```
.claude/skills/  instructions for Claude Code: lessons and research notes
config/          the arm's calibration ids and rest pose; the port goes into robot.local.yaml
docs/guides/     how to do something, with commands
docs/knowledge/  why it works that way
research/        notes on papers, videos, threads and releases, by topic
src/so101/       the Python library; simple.py is the student API
teaching/        lessons by lecture, fun programs and arm tools
```

Planned, created with their first content: `labs/` for the learning ladder in the
architecture, `experiments/` for dated trials, `behaviors/` for robot skills as data.

## Safety

- **The leader runs on 5 V, the follower on 12 V.** Swapping the supplies destroys motors.
- **The servos have no brake.** With the motors off the arm falls, so both arms are clamped
  to the table and a hand is ready whenever the motors are switched off.
- **A new program runs on the simulated arm first.** `SO101_SIM=1` in front of the command.
- **The arm refuses** angles outside its calibrated range, speeds above 90 degrees per second
  and motion with a motor above 65 °C.

## Licence

The code, including every program in `teaching/`, is under the [MIT licence](LICENSE). The
written material in `docs/`, `research/` and the README files is under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The SO-101 is designed by [TheRobotStudio](https://github.com/TheRobotStudio/SO-ARM100) and
Hugging Face; LeRobot is by [Hugging Face](https://github.com/huggingface/lerobot).
