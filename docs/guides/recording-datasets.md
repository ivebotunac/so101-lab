# Recording datasets

A policy learns only what the cameras saw during the demonstrations. Most failed trainings
are failed recordings.

## Protocol

- At least 50 episodes. 25 has been shown not to be enough.
- 5 object positions, 10 episodes each, the same way of grasping every time.
- A narrow workspace of 10 to 15 cm. Community results: 50 demonstrations spread over 30 cm
  ended with the arm grasping air, about 75 clean episodes within 10 cm reached 80 percent.
- Fixed light, cameras taped in place, object positions marked on the table.
- Two different camera models.
- Do not look over your shoulder at the follower. Record while watching the camera feeds on
  the monitor, otherwise you demonstrate with information the model will not have.
- The task string is decided before the first episode and follows one convention.
- Add variation only after the basic case works reliably.

Fifty episodes is the minimum for a policy that does something, around 60 percent. One
community report reached 90 percent in distribution and 75 percent out of distribution with
25 demonstrations per position and rotations from -45 to +45 degrees, after three complete
cycles of record, train and evaluate.

## Record

```bash
hf auth login
HF_USER=$(NO_COLOR=1 hf auth whoami | awk -F': *' 'NR==1 {print $2}')

lerobot-record \
  --robot.type=so101_follower --robot.port=<FOLLOWER_PORT> --robot.id=ive_follower \
  --robot.cameras="{ scene: {type: opencv, index_or_path: <SCENE_INDEX>, width: 640, height: 480, fps: 30}, wrist: {type: opencv, index_or_path: <WRIST_INDEX>, width: 640, height: 480, fps: 30} }" \
  --teleop.type=so101_leader --teleop.port=<LEADER_PORT> --teleop.id=ive_leader \
  --dataset.repo_id=${HF_USER}/so101-test \
  --dataset.num_episodes=5 \
  --dataset.single_task="Grab the black cube" \
  --dataset.streaming_encoding=true \
  --display_data=true
```

- Keys: right arrow or `n` saves and moves on, left arrow or `r` repeats the episode, `ESC`
  or `q` stops, encodes and uploads.
- The dataset is stored under `~/.cache/huggingface/lerobot/{repo-id}`. To skip the upload
  add `--dataset.push_to_hub=False`.
- Useful lengths: `--dataset.episode_time_s=60`, `--dataset.reset_time_s=60`.
- With `--resume=true`, `num_episodes` is the number of additional episodes and
  `--dataset.root` is required.

Start with a 5 episode test dataset before recording 50.

## Two checks before investing hours

**Look at it.** Open https://huggingface.co/spaces/lerobot/visualize_dataset or run

```bash
lerobot-dataset-viz --repo-id "${HF_USER}/so101-test" --episode-index 0
```

Ask one question: could I do the task seeing only these camera views? If not, no training
fixes it. The state and action traces should run smoothly, with no frozen lines and no
missing streams. Do this for every episode before training.

**Replay it.** This uses no model and tests the hardware and the calibration.

```bash
lerobot-replay --robot.type=so101_follower --robot.port=<FOLLOWER_PORT> --robot.id=ive_follower \
  --dataset.repo_id=${HF_USER}/so101-test --dataset.episode=0
```

If the replay does not reproduce the motion, the problem is mechanical, not in the learning.

## Task strings are verbatim

The instruction given at rollout must be the same string as `--dataset.single_task`. One
published SO-101 model requires even a grammar mistake from its training data, letter for
letter. A task string is a choice from a set of learned phrases, not a conversation.

To fix the task of an existing dataset use `lerobot-edit-dataset` with the `modify_tasks`
operation.

## Several skills in one dataset

```bash
lerobot-edit-dataset \
  --repo_id ${HF_USER}/so101_all_skills \
  --operation.type merge \
  --operation.repo_ids "['${HF_USER}/so101_pickplace', '${HF_USER}/so101_handover']"
```

The datasets need identical feature keys, the same fps and the v3.0 format. Each skill keeps
its own task string.

## Other people's datasets

They are not added to the fine-tune. The base model already saw 487 community datasets, and
the fine-tune closes the gap of this arm's calibration, cameras, light and table, which
someone else's data cannot do. They are useful for two things: a short test training on
`lerobot/svla_so100_pickplace` to prove the pipeline works, and as a template of what a good
dataset looks like in the visualiser.
