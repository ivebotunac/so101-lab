# Research

What the lab reads and watches about robot learning, and what it took from each source:
papers, videos, Reddit and forum threads, blog posts, repositories and releases. The field
moves every month, so this folder is where a new idea is written down before the lab tries
it.

A note records what a source says and how far that was checked. What turns out to hold
moves on: an explanation into [`docs/knowledge/`](../docs/knowledge), a command into
[`docs/guides/`](../docs/guides), a choice into [`docs/decisions.md`](../docs/decisions.md).

## Layout

One folder per topic, one file per source. A topic folder appears with its first note.

| Folder | Covers |
|---|---|
| `stack-reviews/` | A periodic check of everything the guides rely on: releases, prices, flags, benchmarks. One file per review, named by month: `2026-11.md` |
| `vla/` | Vision-language-action models and policies on the SO-101: SmolVLA, pi0.5, GR00T, ACT |
| `speech/` | Realtime speech models and the voice loop: latency, barge-in, Croatian |
| `reasoning-models/` | Models that plan and drive the arm through tools: Gemini Robotics ER, Gemini Argon, LLMs over MCP |
| `vision/` | Cameras, VLM pointing, hand-eye calibration, faces |
| `simulation/` | MuJoCo, Isaac Lab, ManiSkill, sim-to-real |
| `hardware/` | The arm, servos, grippers, sensors, other kits |
| `teaching/` | How others teach programming and robotics with an arm like this one |

A new topic gets a row here when its folder is created.

## A note

The file is named after the source, in lowercase with hyphens, prefixed by its kind when
that helps: `smolvla-paper.md`, `video-lerobot-calibration-walkthrough.md`,
`reddit-so101-gripper-overheating.md`, `repo-geminirobotics-so101.md`.

```markdown
# <Title of the source>

- Kind: paper | video | thread | post | repository | release
- Link: <url>
- Read: <YYYY-MM-DD>
- Checked: <how far the claims were verified: read only, run, reproduced on this arm>

## What it says

The claims, with numbers, in the source's own terms.

## What it means for this lab

What to try, what it changes, or why it changes nothing.
```

A note is final state: when a later source corrects it, the note is rewritten and its
`Read` date moves.

## Notes

- [Stack review, November 2026](stack-reviews/2026-11.md): LeRobot 0.7.0, Gemini Argon and
  ER 2, SmolVLA against ACT and pi0.5 on a physical SO-101, realtime speech prices, and
  active SO-101 repositories.
