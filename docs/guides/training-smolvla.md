# Training and evaluating SmolVLA

The lab trains one policy family: SmolVLA, fine-tuned from `lerobot/smolvla_base`. It is
trained only for skills that need learning: contact, fine motor control, speed. Gestures and
pointing need no training, see [motion without training](motion-without-training.md), and a
simple pick and place can be done by a reasoning model, see
[Gemini ER and Argon](gemini-argon.md).

## Why SmolVLA and not ACT

| | ACT | SmolVLA |
|---|---|---|
| What it is | Behavior cloning with action chunking | A VLM (SmolVLM2) plus an action expert trained with flow matching |
| Parameters | about 80M | 450M |
| Language | None, one model per task | A text instruction selects the task |
| Pretraining | None | About 10M frames from 487 community datasets, mostly SO-100 and SO-101 |
| Training on an A100 | About 1.5 h for 100k steps at batch 64 | About 4 h for 20k steps |
| Inference | About 5 ms | About 99 ms, with asynchronous inference available |

Numbers from the SmolVLA blog on a real SO-100: pick and place 80 percent against 70 for
ACT, stacking 75 against 65, sorting 78 against 68. Transfer to an SO-101: 76.5 against
48.3. Pretraining moves SmolVLA from 51.7 to 78.3 percent.

## It does not work without fine-tuning

The base model officially requires fine-tuning, with about 50 episodes recommended. This
arm's calibration is not the one it saw, the cameras are not where its cameras were, and the
feature keys have to match. The typical result without a good fine-tune is an arm that moves
convincingly toward the object and grasps air. Four hours on an A100 are the entry ticket,
not an optional cost.

## Train

```bash
lerobot-train \
  --policy.path=lerobot/smolvla_base \
  --dataset.repo_id=${HF_USER}/so101-pickplace \
  --rename_map='{"observation.images.scene": "observation.images.camera1", "observation.images.wrist": "observation.images.camera2"}' \
  --batch_size=64 --steps=20000 \
  --policy.device=cuda \
  --output_dir=outputs/train/smolvla_so101 \
  --job_name=smolvla_so101 \
  --policy.repo_id=${HF_USER}/smolvla_so101
```

- **`--policy.path`, never `--policy.type=smolvla`.** The second trains from scratch, needs
  about 200k steps and throws away the pretraining that is the reason for choosing SmolVLA.
- **`--rename_map` maps this lab's camera names to `camera1`, `camera2`, `camera3`.**
  Without it training stops with a feature mismatch.
- Experiment tracking is switched on with a flag; check the current LeRobot documentation
  for which tracker the installed release supports.

Resume after a dropped session:

```bash
lerobot-train --config_path=${HF_USER}/smolvla_so101 --resume=true
```

### How many steps

```
steps_per_epoch = ceil(total_frames / (gpu_count * batch_size))
total_steps     = steps_per_epoch * epochs
```

50 episodes of about 30 s at 30 fps is about 45,000 frames, so about 700 steps per epoch at
batch 64. 20k steps is the official baseline. More steps do not repair bad demonstrations;
compare checkpoints by rollouts in a fixed scene.

### Where to train

| | Colab with an A100 | HF Jobs |
|---|---|---|
| How | A notebook, cell by cell | `--job.target=a10g-small` on the same command |
| Setup | Install on every session | `hf auth login` only |
| Dataset | Has to be on the Hub | A local one is pushed to a private repo |
| Interruptions | Possible, needs resume | The job keeps running |
| Cost | Compute units | Per second, see `hf jobs hardware` |

The first training goes through Colab, where every step is visible, which also suits
students. Routine runs move to HF Jobs. In Colab the token is a Colab Secret, never a cell,
and the A100 is not left running while the notebook is being edited. Notebooks:
https://huggingface.co/docs/lerobot/notebooks

## Evaluate

```bash
lerobot-rollout \
  --strategy.type=base \
  --policy.path=${HF_USER}/smolvla_so101 \
  --robot.type=so101_follower --robot.port=<FOLLOWER_PORT> --robot.id=ive_follower \
  --robot.cameras="{ scene: {...}, wrist: {...} }" \
  --rename_map='{"observation.images.scene": "observation.images.camera1", "observation.images.wrist": "observation.images.camera2"}' \
  --task="<the exact string used when recording>" \
  --duration=60
```

- The camera configuration and the `--rename_map` are identical to recording and training.
- `--inference.type=rtc` gives smoother motion with a slow policy.
- `--task` is a process argument and cannot change during a rollout. A robot that switches
  tasks restarts the rollout or uses the Python API.
- There is no validation curve for a real robot. A checkpoint is chosen by testing it on the
  arm. Held-out episodes are a partial answer.
- Define the protocol before testing, for example 50 attempts from a fixed position and 50
  from random positions inside a 10 by 10 cm zone, on the same checkpoint.
- Every run gets a row in [experiments](../experiments.md).
- Below 50 percent after 50 demonstrations, examine the setup first: light, cameras,
  calibration. Do not record more blindly.

## Time budget

Assembly and calibration take a weekend. 50 episodes are 2 to 4 hours of recording. Training
is about 4 hours. Evaluation and debugging take the longest. The real work is the loop of
record, train, run, and re-record the weak cases.
