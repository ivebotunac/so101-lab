# Concepts

## From classical robotics to robot learning

In classical robotics an engineer writes the model of the world, the controller and every
action by hand. That works in a factory where everything is fixed and falls apart on a
table with changing light and objects in different places. Robot learning turns it around:
the robot learns from data, as a language model learns from text.

## VLM: image and text in, text out

A vision encoder cuts the image into patches and turns them into visual tokens. They are
projected into the same space as text tokens, joined with the prompt, and an ordinary
autoregressive decoder does the rest.

The capability that matters for robotics is **pointing**: instead of a description the model
returns coordinates, "the cube is at (412, 305)". That is the bridge from understanding an
image to the physical world, because a coordinate can become a target for the arm.

## VLA: a VLM that speaks to motors

A vision-language-action model replaces the text output with an action head. Instead of
words it produces joint commands, six numbers for the SO-101, many times a second. Actions
are decoded in three ways:

1. **Discrete action tokens** (OpenVLA): actions are binned like words. The FAST tokenizer
   compresses them.
2. **Flow matching or diffusion head** (pi0, SmolVLA, GR00T): continuous, smooth actions.
3. **Action chunking** (ACT, SmolVLA): a chunk of, say, 50 future steps is predicted at once.

## Imitation learning

There is no internet full of motion. The cheapest source is demonstration: a person moves
the leader arm, the follower repeats, and pairs of (images and angles) to (next angles) are
recorded. Training is supervised learning of that mapping.

The problem is **compounding error**: small mistakes accumulate and the robot drifts off the
path it knows. Action chunking and generative action heads reduce it.

## Dual system: brain and spine

One model cannot think deeply and drive motors 30 times a second.

- **System 2** is the slow planner, a VLM such as Gemini Robotics ER or Argon. It looks at
  the scene, plans and picks a skill.
- **System 1** is fast motor control, a small policy such as ACT or SmolVLA that carries out
  one concrete task.

This lab is built on that split.

## Reasoner or controller

The easiest way not to get lost in the names. Every system is one of two things:

- a **reasoner**, whose output is text, coordinates, a plan or code: Gemini Robotics ER,
  Gemini 4 Argon,
- a **controller**, whose output is motor commands: pi0, SmolVLA, GR00T, OpenVLA, ACT.

Google has both under similar names: Gemini Robotics is a VLA for partners only, Gemini
Robotics ER is a reasoner with a public API. The reasoner is available here; controllers are
trained through LeRobot.

## Glossary

| Term | In short | Why it matters here |
|---|---|---|
| Teleoperation | The leader drives the follower; this is how demonstrations are recorded | The first step of every training |
| Proprioception | The robot's sense of its own state: angles, gripper | An input to every policy beside the cameras |
| Joint and Cartesian space | Joint angles against the position of the tip (x, y, z) | A VLA works in joint space, gestures and pointing in Cartesian |
| Sim2real | Train in simulation, transfer to the real arm | An alternative to recording, with a large domain gap |
| Cross-embodiment | One model for several kinds of robot | Zero-shot on a new arm still does not work |
| Success detection | A model judges whether the task succeeded | Reasoners can do it; needed for failing gracefully |

## Two sobering facts

1. **No VLA works zero-shot on your arm.** Zero percent success is documented for transfer
   to an embodiment the model did not see in fine-tuning. A foundation model in robotics is
   a good starting point for fine-tuning.
2. **Reading numbers in papers.** Always ask on which hardware, with how many
   demonstrations, and who ran the evaluation.

## Reading

- HF Robotics Course: https://huggingface.co/learn/robotics-course
- Robot Learning: A Tutorial: https://arxiv.org/abs/2510.12403
- SmolVLA: https://arxiv.org/abs/2506.01844
- OpenVLA: https://arxiv.org/abs/2406.09246
- FAST: https://arxiv.org/abs/2501.09747
