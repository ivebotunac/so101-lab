# State of the stack, November 2026

A fact check of everything the guides rely on, run on 2026-11-11 through a web research
task and then checked against primary sources where that was cheap. Each finding says how
far it was checked.

## LeRobot 0.7.0

Checked against the GitHub releases API: `v0.7.0` was published on 2026-11-05, `v0.6.1` on
2026-08-03, `v0.6.0` on 2026-07-06.

Reported from the release notes, not re-read here:

- Trackio replaces Weights & Biases. `--wandb.*` becomes `--trackio.*`, the W&B `entity` and
  `mode` flags have no equivalent, and a remote job needs `--trackio.space_id`. The current
  SmolVLA documentation does use `--trackio.enable=true`.
- Checkpoints are no longer uploaded as tracking artifacts by default.
- A bare `pip install lerobot` no longer brings dataset or training dependencies; extras
  have to be named.
- `lerobot.async_inference` and the `async` extra are gone. Remote inference is the `remote`
  extra, `lerobot-policy-server`, and `lerobot-rollout --inference.type=remote`.
- `lerobot-rollout --interactive=true` adds `/start`, `/subtask`, `/vqa`, `/autosteer` and
  `/stop`.
- macOS 14 or newer is required, macOS 15 for MPS.

Sources: https://github.com/huggingface/lerobot/releases and
https://huggingface.co/blog/lerobot/lerobot-release-v070

## Gemini 4 Argon

Checked against the pricing page: `gemini-4-argon`, paid tier only, 2 USD input and 10 USD
output per million tokens through 2026-11-30, then 4 and 20 USD from 2026-12-01. Thinking
tokens are billed as output. Batch and flex are half price.

Reported from Google's robotics article and developer guide:

- The SO-101 demo draws a 2 cm grid at `grid_z` over the wrist camera image, with +X up, +Y
  left and +Z as height above the table.
- Its primitives: `look_at`, `deproject`, `grasp`, `place`, `place_until_contact`, `goto`,
  `move_by`, `move_until_contact`, `open_gripper`, `close_gripper`, `home`, `done`.
- The 58.9 s, 22.9 s and 17.4 s figures are task iteration times, not API latency. Hard
  reasoning can take minutes; the guide recommends `background=True` or an HTTP timeout of
  15 to 20 minutes.
- No public harness for the SO-101 was found, from Google or anyone else.

Sources: https://ai.google.dev/gemini-api/docs/pricing and
https://developers.googleblog.com/gemini-4-argon-for-robotics/

## Gemini Robotics ER 2

Checked against the pricing page: both `gemini-robotics-er-2-preview` and
`gemini-robotics-er-2-streaming-preview` cost 1 USD input and 5 USD output per million
tokens through 2026-12-31, then 2 and 10 USD. Both have a free tier, whose data is used to
improve Google's products. Both are still previews.

Reported from the model pages: both take text, image, video and audio and return text only.
The streaming model supports the Live API and function calling but not structured output,
code execution, caching or batch. Limits are 131,072 input and 65,536 output tokens.

Not confirmed: rate limits and the exact rule on API key restrictions.

## Policies on the SO-101

"Benchmarking Vision-Language-Action Models on SO-101: Failure and Recovery Analysis",
https://arxiv.org/abs/2606.08881. The abstract was read: pi0.5, SmolVLA, Wall-X and ACT
fine-tuned on a physical SO-101, four tasks. The numbers below are as reported by the
research task from the paper's HTML, with 100 demonstrations per task and 20 trials each:

| Model | Average success | Recovery rate |
|---|---|---|
| ACT | 33.75% | 6.45% |
| SmolVLA | 32.5% | 3.23% |
| Wall-X | 51.25% | 20.51% |
| pi0.5 | 56.25% | 30.77% |

Every model scored 10 percent or less on colour sorting. This puts SmolVLA level with ACT
and well under pi0.5 on this arm, which bears on the lab's SmolVLA-only decision.

`aviadarn/so101-lerobot` reports, in MuJoCo only, ACT success against the number of
demonstrations on 50 held-out layouts: 10% at 25, 34% at 50, 44% at 100, 54% at 200, 50% at
300. A curation heuristic did worse than random selection.

## Voice

Reported from the OpenAI and Google pricing pages, not re-read here:

- OpenAI lists `gpt-realtime-2.1` at 32 USD audio input and 64 USD audio output per million
  tokens, `gpt-realtime-2.1-mini` at 10 and 20 USD, and a separate full-duplex model
  `gpt-live-1` at 0.05 USD per session minute with backend model and tool use billed on
  top. `gpt-live-1` uses `v1/live/sessions`, not `v1/realtime`.
- Gemini Live lists `gemini-3.8-live` at about 0.005 USD per minute of audio in and 0.018
  USD per minute of audio out. Its native transport is a WebSocket; WebRTC comes through
  LiveKit or Pipecat.
- No source measures Croatian speech to speech quality for either. OpenAI's text to speech
  documentation lists Croatian, which says nothing about the realtime models.

## Repositories

Checked through the GitHub API on 2026-11-11:

| Repository | What it is | Last push |
|---|---|---|
| `Ekumen-OS/GeminiRobotics-SO101` | Gemini Robotics ER 2 demo with the SO-101 | 2026-10-31 |
| `fouad1233/SO101_Speech_controlled_robotic_arm_with_smolvla` | Voice controlled SO-101 | 2026-05-06 |
| `aviadarn/so101-lerobot` | SO-101 pick and place in MuJoCo with ACT | 2026-09-29 |
| `anshuman-dev/ros-mcp-plugin` | MCP server and ROS 2 bridge for the SO-101 | 2026-04-26 |
| `RoboColosseum/robocolosseum-finetune-so101` | Evaluation of fine-tuned VLA policies on the SO-101 | 2026-11-04 |
| `Arjunros/gemini-so100` | Gemini with an SO-100, no description | 2026-08-29 |

`johannstark/GeminiRobotics-SO101` returns 404; the Ekumen-OS repository carries the same
name.

## What this changed in the lab

The guides were updated for LeRobot 0.7.0, the Argon and ER 2 prices and the Argon
primitive set. The SmolVLA-only decision was not changed; the benchmark is recorded as an
open question in `docs/decisions.md`.
