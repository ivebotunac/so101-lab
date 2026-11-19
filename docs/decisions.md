# Decisions

A log: one row per decision, newest last. A decision that is replaced gets a new row that
names the one it replaces.

| Date | Decision | Why |
|---|---|---|
| 2026-08 | Dual system: a reasoning model plans, LeRobot policies execute | One model cannot both plan and control at 30 Hz |
| 2026-08 | Skills follow the SKILL.md pattern | Progressive disclosure, skills as data, students can contribute |
| 2026-09-06 | SmolVLA only, from `smolvla_base`, with `--policy.path`. No ACT | Pretrained on SO-100 and SO-101, several tasks in one policy |
| 2026-09-06 | No community datasets in the fine-tune | They are already in the base model; the gap is this arm's domain |
| 2026-09-06 | SmolVLA for about three tabletop skills, not ten | Gestures and pointing need no training |
| 2026-09-06 | Gestures are keyframes and replay, not a VLA | Repeatable, timed, cheap |
| 2026-09-06 | OpenAI Realtime is the first candidate for voice, after a live test | Mature speech to speech, function calling during speech |
| 2026-09-06 | The gripper acts as a mouth | A robot without a face looks dead while speaking |
| 2026-09-06 | InsightFace for faces, mem0 for memory, IK with a homography for pointing | Existing solutions, local and cheap |
| 2026-09-06 | One repo with labs, a library and skills | The motion and safety layers are written once |
| 2026-09-06 | The safety adapter enters at step 4 of the ladder | The first time a model calls a motion |
| 2026-10-13 | Argon is the candidate for planning and zero-shot pick and place; training stays for contact and speed | Tasks describable by points need no training |
| 2026-11-11 | The repo also holds student examples on a simple API with a simulated arm | The same arm is used in a first-year programming course |
| 2026-11-11 | Robot skills live in `behaviors/`, not `skills/` | Keeps them apart from the coding assistant's skills |
| 2026-11-19 | The student API is plain functions in `so101.simple`, follower only, limits taken from the calibration | First-year students know functions and not classes; one arm, one supply and one cable set up fast |
| 2026-11-19 | The motors keep their torque when a student program ends | An arm that falls at the last line of every script wears out and frightens |
| 2026-11-19 | The repo is public under MIT for code and CC BY 4.0 for written material | Students and other labs can reuse the lessons and the guides |
| 2026-11-19 | Ports live in a gitignored `config/robot.local.yaml`; calibration ids are `lab_follower` and `lab_leader` | A clone on another computer falls back to the simulated arm instead of reaching for someone else's port |
| 2026-11-19 | Research notes are sorted by topic and named after their source; stack reviews are monthly | A dated file at the top of `research/` said when, not what |

## Lessons that shaped them

1. Most motion needs no training. The question is whether it depends on the scene and
   whether it needs contact.
2. No VLA works zero-shot on your arm. Fine-tuning is the entry ticket, about 50 episodes.
3. Calibration is an agreement about zero. A dataset and a model are valid only for the
   calibration they were made on.
4. Light and cameras decide the model. It sees only the frames.
5. A task string is verbatim. A policy picks a learned phrase; conversation belongs to the
   orchestrator.
6. The hardest part is not machine learning but realtime systems: ownership of the arm,
   async tools, barge-in, synchronisation, failing gracefully.
7. Projects die from integrating everything at once. Get to a vertical slice early.
8. With a reasoning model the hard part is classical robotics: camera to arm calibration,
   IK, precision.
9. Check secondary sources. Generated articles about new models are often wrong; primary
   documentation wins.
10. Before neural networks, spend time with manual control through the Python API and
    `lerobot-replay`.
11. Measure from the first day: success, time, number of calls, cost.

## Open questions

- Is a realtime speech model pleasant to listen to in Croatian?
- Argon's real latency and cost per move on this setup.
- Argon or ER 2 as the planner, or both in different roles?
- Which are the first two or three SmolVLA skills, and their task strings?
- Does SmolVLA-only still hold? A benchmark on a physical SO-101
  (https://arxiv.org/abs/2606.08881) puts SmolVLA level with ACT and pi0.5 well ahead. The
  first trained skill is the place to compare them on this arm.
