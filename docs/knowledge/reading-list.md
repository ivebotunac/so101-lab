# Reading list

Tutorials, courses, repositories and write-ups beyond the basics in
[resources](resources.md), grouped by what the lab does. Every link answered on 2026-11-11.
The descriptions and numbers are each source's own claims, collected by a research run and
not reproduced here. Almost none of these were written for LeRobot 0.7.0, so read them for
the idea and check every command against the current API before running it.

## Read first

1. LeRobot v0.7.0 release notes, the current baseline:
   https://github.com/huggingface/lerobot/releases/tag/v0.7.0
2. NVIDIA, calibrating the SO-101 and checking offsets against the mechanical end stops:
   https://docs.nvidia.com/learning/physical-ai/sim-to-real-so-101/latest/07-calibrating-so101.html
3. The STS3215 tutorial and register reference: https://github.com/commanderfun/STS3215
4. ECE4560 assignment 3, reading a position and making a bounded joint move:
   https://maegantucker.com/ECE4560/assignment3-so101
5. ECE4560 assignments 7 and 8, from geometric IK to pick and place:
   https://maegantucker.com/ECE4560/assignment7-so101 and
   https://maegantucker.com/ECE4560/assignment8-so101
6. A MuJoCo environment for the SO-101 that runs on Apple Silicon:
   https://github.com/isaka1022/so101-sim2real
7. Hand-eye calibration with measured error:
   https://docs.cyberwave.com/feature-reference/hand-eye-calibration
8. The SO-101 VLA benchmark: https://arxiv.org/abs/2606.08881
9. Imitation learning then RL on a real SO-101, with success against the number of
   demonstrations: https://github.com/atomictan/lerobot-so101
10. Gemini Robotics ER 2 driving an SO-101 through tool calls:
    https://ekumenlabs.com/blog/posts/give-robot-arm-a-brain/

## Assembly, calibration and hardware faults

| Source | What it gives |
|---|---|
| https://docs.nvidia.com/learning/physical-ai/sim-to-real-so-101/latest/07-calibrating-so101.html | Finding ports, calibrating, and a script that checks the offsets against the end stops |
| https://www.twinworks.com/community/so-101.html | Replacing the gripper servo; a new servo reports id 1 where the arm expects id 6 |
| https://github.com/TheRobotStudio/SO-ARM100/issues/134 | A report of about 1 degree of real backlash and 1.8 to 2.6 degrees of position error under a 1.5 kg load |
| https://robonine.com/testing-of-feetech-sts3215-servomotor-backlash-repeatability-and-torque | A bench test: about 0.87 degrees of backlash, repeatability of about 0.3 mm |
| https://gitlab.fhnw.ch/robots/intro-to-robotics/-/blob/main/docs/so101.md | A university course's notes on the SO-101: id conflicts, slow servos, jumps to a stale goal, undervoltage, overheating |

No source measures how often grippers wear out or motors overheat. Those remain things to
watch, not known rates.

## Direct control from Python, and teaching

| Source | What it gives |
|---|---|
| https://github.com/commanderfun/STS3215 | A multi-part tutorial on the servo with the vendor SDK: ports, torque, position, speed, acceleration, load, errors, and a register reference. Tested on macOS |
| https://maegantucker.com/ECE4560/assignment3-so101 | ECE4560, joint space: `read_position.py`, `set_position.py`, 50 Hz commands, linear interpolation between poses |
| https://maegantucker.com/ECE4560/assignment4-so101 | ECE4560, the arm in MuJoCo: the XML model and position actuators |
| https://maegantucker.com/ECE4560/assignment9-so101 | ECE4560, cubic trajectories; the hardware takes position commands, not velocity |
| https://calwoo.github.io/notes/curricula/robotics/curriculum/ | A self-study curriculum on a physical SO-101, from data collection through ACT, Diffusion Policy, pi0 and SmolVLA to a capstone |

ECE4560 is the closest existing course to the `teaching/` track here: an undergraduate
sequence on the SO-101 that goes read a joint, move a joint, interpolate, simulate, IK, pick
and place.

## Kinematics

| Source | What it gives |
|---|---|
| https://github.com/TheRobotStudio/SO-ARM100/blob/main/Simulation/SO101/README.md | The official URDF and MuJoCo models; the README warns that some inertial values are not measured |
| https://github.com/huggingface/lerobot/blob/v0.7.0/src/lerobot/model/kinematics.py | LeRobot's own FK and IK, built on placo |
| https://maegantucker.com/ECE4560/assignment7-so101 | Geometric IK by hand: transforms, projections, triangle geometry, rejecting unreachable targets |
| https://github.com/TourEnduro/so101-ik-gamepad-control | ikpy with the URDF, a GUI and a gamepad; reports its reachable region as x 0.13 to 0.44 m, y within 0.3 m, z 0 to 0.44 m |
| https://github.com/wig-nesh/so101-inverse-kinematics | FK and IK with direct Feetech control, keyboard, mouse and hand tracking, circular paths |
| https://github.com/Z-Robotics-Lab/z-agent/blob/main/zeno/hardware/so101/ik_solver.py | A Pinocchio solver with damped least squares, 2 mm tolerance |

No tutorial was found that goes from a freshly calibrated URDF through IK to a measured
endpoint error on the real arm. That measurement is this lab's to make.

## Simulation

| Source | What it gives |
|---|---|
| https://github.com/isaka1022/so101-sim2real | A MuJoCo environment published as a LeRobot plugin, `SO101PickCube-v0`, documented for Apple Silicon. The passive viewer needs `mjpython` |
| https://github.com/physical-hardware-intelligence/phi | An open robot learning pipeline with a MuJoCo SO-101 model and Mac setup notes |
| https://github.com/aviadarn/so101-lerobot | A scripted expert, ACT training and evaluation in MuJoCo; 88 percent on unseen simulated layouts, trained partly on MPS |
| https://so101-bench.github.io/ | A real-to-sim-to-real benchmark: four tasks, 138 objects, 916 episodes, testing whether simulation preserves the ranking of policies |
| https://github.com/LightwheelAI/leisaac | Teleoperation and data collection in Isaac Lab with the SO-101 leader. NVIDIA GPUs only |
| https://docs.nvidia.com/learning/physical-ai/sim-to-real-so-101/latest/index.html | NVIDIA's sim-to-real course for the SO-101 |
| https://github.com/Luoyadan/lerobot_so101-sim2real | PPO sim-to-real in ManiSkill, written for LeRobot 0.3.4 |

On a Mac the route is MuJoCo. Isaac Sim and Isaac Lab do not run on Apple Silicon.

## Cameras and calibration

| Source | What it gives |
|---|---|
| https://docs.cyberwave.com/feature-reference/hand-eye-calibration | Wrist camera hand-eye calibration; 1.9 to 3.5 mm error in good runs, 7.7 to 24 mm when the samples are ill-conditioned |
| https://github.com/NBUT-hh/so101_ws/tree/main/so101_camera_calibration | A ROS 2 package with ChArUco intrinsics and hand-eye scripts, 20 to 30 poses collected by hand |
| https://github.com/google-gemini/robotics-pointing-sample | Google's sample that maps a pixel returned by a VLM onto the table plane with a ChArUco board and a homography |
| https://github.com/ggand0/vla-so101 | A working two-camera setup with a RealSense D405 and a Logitech C920 |

A homography maps a pixel to a point on the table plane and nothing else. No source
validates a depth camera pipeline on this arm from a depth pixel to a measured 3D error.

## Datasets and policies

| Source | What it gives |
|---|---|
| https://arxiv.org/abs/2606.08881 | ACT, SmolVLA, Wall-X and pi0.5 on a physical SO-101, four tasks, 100 demonstrations each, with a failure taxonomy and recovery rates |
| https://github.com/atomictan/lerobot-so101 | ACT on one pick and drop task: 40 percent at 50 demonstrations, 60 at 75, 82.5 at 107, 96.7 at 118. Real-arm RL did not start learning in about 2,600 transitions |
| https://github.com/ljt228/pi05-so101-finetune | LoRA fine-tuning of pi0.5 on SO-101 data, on Linux with an NVIDIA GPU |
| https://github.com/Maelic/openpi-SO100 | pi0 fine-tuning for the SO-100 and SO-101; macOS unsupported |
| https://huggingface.co/blog/nvidia/gr00t-n1-5-so101-tuning | NVIDIA's guide to fine-tuning GR00T N1.5 on the SO-101, about 25 GB of VRAM |
| https://github.com/robocurve/gr00t-n1.7-so-101 | A LoRA fine-tune of GR00T N1.7 on 2,130 SO-101 episodes |
| https://github.com/RoboColosseum/robocolosseum-finetune-so101 | Scripts for five VLA models on five SO-101 tasks with a 25-trial evaluation plan; no results published yet |
| https://huggingface.co/blog/lerobot/lerobot-release-v070 | The 0.7.0 announcement: the remote policy server and interactive rollout |

The single-task repository and the four-task benchmark do not contradict each other. One
narrow, repeated task with more than 100 demonstrations reaches high success; a spread of
tasks does not.

## LLMs and reasoning models driving the arm

| Source | What it gives |
|---|---|
| https://github.com/Ekumen-OS/GeminiRobotics-SO101 | Gemini Robotics ER 2 with tool calling, camera input, a simulated and a real mode, and a homography from ArUco corners |
| https://ekumenlabs.com/blog/posts/give-robot-arm-a-brain/ | The write-up of that project |
| https://github.com/google-gemini/robotics-pointing-sample | Pixel to table coordinates, see cameras above |
| https://github.com/Tibe31/so101-mcp | An MCP server over an existing LeRobot setup with limit setting; no collision checking |
| https://github.com/anshuman-dev/ros-mcp-plugin | An MCP server and ROS 2 bridge, run in Docker |

No open reproduction of Google's Argon demo on the SO-101 was found.

## Voice

| Source | What it gives |
|---|---|
| https://github.com/carneym/assistive-arm | A local pipeline: wake word, voice activity detection, Whisper, an intent parser, an action, spoken feedback |
| https://github.com/jmeth/gemini | A web control panel for the SO-101 with voice triggers through the browser's speech API |
| https://github.com/fouad1233/SO101_Speech_controlled_robotic_arm_with_smolvla | Speech commands that select a SmolVLA task |
| https://docs.livekit.io/robotics/integrations/portal/examples/ | LiveKit's robotics transport with a two-arm SO-101 example: video, observations, actions |
| https://leobit.com/blog/real-time-voice-ai-gpt-live-vs-gemini-live-vs-elevenlabs/ | A comparison of realtime voice models with latency and word error rate; German, Spanish and French, no Croatian |

Nothing found connects OpenAI Realtime, Pipecat or Moshi to this arm, and nothing measures
a realtime voice model in Croatian.

## Safety

| Source | What it gives |
|---|---|
| https://github.com/leo-zhu-agibot/so101-deploylab | A harness that stresses a policy with latency, actuator noise and dropped observations, with bounded actions and slew-rate limits, and counts safety interventions |
| https://arxiv.org/abs/2503.07885 | RoboGuard: an LLM root of trust with temporal logic constraints; unsafe plans executed fall from over 92 to under 3 percent |
| https://github.com/adityakamath/so_arm_ros2 | A ROS 2 package for the arm whose README is plain that its e-stop is software only |

None of this is a safety-rated stop. A physical power cutoff within reach stays part of the
setup whatever the software does.

## Keeping up

- LeRobot releases: https://github.com/huggingface/lerobot/releases
- Community project feed: https://so101.builders/
- LeRobot hackathon write-up: https://42-ai.github.io/posts/LeRobotHackathonHighlights
- arXiv searches for "SO-101" and "low-cost VLA"
