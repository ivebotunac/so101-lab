# Setup on macOS

From an unopened kit to a follower arm that mirrors the leader. Ports, ids and camera
indexes are written into `config/robot.yaml` as they are found; the commands below show them
as `<FOLLOWER_PORT>` and `<LEADER_PORT>`.

## Before anything is plugged in

- Label the power supplies: **leader 5 V, follower 12 V**. Swapping them is the most
  expensive mistake of the first day.
- Label the motors F1 to F6 and L1 to L6. They look identical and the leader uses three
  different gear ratios, listed in [hardware](../knowledge/hardware.md).
- Clamp both arms to the table.

## 1. Software

The lab runs LeRobot 0.7.0, which needs Python 3.12, ffmpeg and macOS 14 or newer, macOS 15
for MPS.

```bash
brew install miniforge
conda create -y -n lerobot python=3.12
conda activate lerobot
conda install ffmpeg -c conda-forge

pip install 'lerobot[core_scripts,feetech,training]==0.7.0'
pip install 'lerobot[smolvla]==0.7.0'        # when SmolVLA is needed
```

- A bare `pip install lerobot` brings no dataset or training dependencies; the extras have
  to be named.
- `core_scripts` brings record, replay and calibrate. `feetech` adds the motor SDK.
  `training` adds what `lerobot-train` needs.
- LeRobot's own guide recommends `uv` when working from a clone of its source:
  `uv sync --locked --extra core_scripts --extra feetech --extra training`. The `uv` route
  needs PyTorch 2.10 or newer; the conda ffmpeg works with every PyTorch version.
- If the Mac does not see the board: a Waveshare board usually appears as
  `/dev/tty.usbmodem*`, some variants need the CH340 or CH343 driver.

## 2. Motor ids, before assembly

Id and baudrate are written to the motor's EEPROM once.

```bash
lerobot-find-port        # asks you to unplug the USB cable when it is ready

lerobot-setup-motors --robot.type=so101_follower --robot.port=<FOLLOWER_PORT>   # on 12 V
lerobot-setup-motors --teleop.type=so101_leader  --teleop.port=<LEADER_PORT>    # on 5 V
```

The script goes motor by motor starting from the gripper, and each motor must be the only
one connected. On a Waveshare board both jumpers sit on channel `B` (USB).

## 3. Assembly

- Official instructions, joint by joint: https://huggingface.co/docs/lerobot/so101
- Remove the support material from the printed parts and plug a 3-pin cable into each motor
  as it goes in.
- Video: https://www.youtube.com/watch?v=70GuJf2jbYk

## 4. Calibration

```bash
lerobot-calibrate --robot.type=so101_follower --robot.port=<FOLLOWER_PORT> --robot.id=ive_follower
lerobot-calibrate --teleop.type=so101_leader  --teleop.port=<LEADER_PORT>  --teleop.id=ive_leader
```

- Move every joint to the middle of its range, press Enter, then sweep each joint through
  its full range.
- The `id` is the calibration key. Use the same one in every later command.
- To recalibrate, delete the files under
  `~/.cache/huggingface/lerobot/calibration/robots` and `.../teleoperators`.
- Recalibrate after every disassembly. Datasets, keyframes and policies made on the old
  calibration stop being valid.

## 5. Teleoperation

```bash
lerobot-teleoperate \
  --robot.type=so101_follower --robot.port=<FOLLOWER_PORT> --robot.id=ive_follower \
  --teleop.type=so101_leader  --teleop.port=<LEADER_PORT>  --teleop.id=ive_leader \
  --display_data=true
```

## 6. Cameras

```bash
lerobot-find-cameras opencv    # prints the indexes and saves test frames to outputs/captured_images
```

- Give the terminal camera permission: System Settings, Privacy & Security.
- Without the Accessibility permission `lerobot-record` reads keys from the terminal, so
  keep the terminal focused while recording.
- The two cameras here are different models on purpose. Two identical cameras get their USB
  paths swapped by the operating system at random.
- Fixed, even lighting matters more than resolution.

## Diagnostics

- **Feetech timeout.** Look at the red LEDs along the chain. All steady from the gripper to
  the base means the wiring is fine. A chain that stops in the middle is a 3-pin cable or
  the power supply. A blinking LED is a motor in an error state, overload or wrong voltage.
- **Leader and follower do not match.** Recalibrate, then check for swapped motors.
- **Random resets.** Power supply.
- **Cameras swapped.** Check the indexes again with `lerobot-find-cameras`.

## Where training happens

Recording and teleoperation run well on the Mac. Training on MPS works but is slow. The
flow is: record on the Mac, push the dataset to the Hub, train on a cloud GPU, pull the
checkpoint back to the Mac for rollout. See [training SmolVLA](training-smolvla.md).
