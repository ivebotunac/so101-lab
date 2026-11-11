# Resources

## Repositories, in the order worth cloning

| # | Repository | What it gives |
|---|---|---|
| 1 | https://github.com/huggingface/lerobot | The foundation: teleoperate, record, train, replay, rollout |
| 2 | https://github.com/IliaLarchenko/robot_MCP | An MCP server for the SO-101, an LLM drives the arm. Video: https://www.youtube.com/watch?v=EmpQQd7jRqs |
| 3 | https://github.com/Grigorij-Dudnik/RoboCrew | An LLM agent layer: gestures, VLA and sensors as tools, wake word, TTS |
| 4 | https://github.com/pollen-robotics/reachy_mini_conversation_app | Reference architecture: layered motion, tool registry, profiles |
| 5 | https://github.com/TheRobotStudio/SO-ARM100 | Hardware: STL, BOM, URDF and MJCF |
| 6 | https://github.com/box2ai-robotics/lerobot-kinematics | FK and IK for the SO-101, MuJoCo, keyboard control |

`robot_MCP` tracks an older LeRobot. To follow its video use release `v0.0.1`, and update
`MOTOR_NORMALIZED_TO_DEGREE_MAPPING` in its `config.py` after every recalibration, because
LeRobot now uses normalised joint states.

## Agent, voice, memory, perception

- Pipecat: https://github.com/pipecat-ai/pipecat
- LiveKit Agents: https://github.com/livekit/agents
- Moshi: https://github.com/kyutai-labs/moshi
- ElatoAI, realtime voice on an ESP32: https://github.com/akdeb/ElatoAI
- ROSA, the tool and guardrail pattern from NASA JPL: https://github.com/nasa-jpl/rosa
- mem0: https://github.com/mem0ai/mem0
- Letta: https://github.com/letta-ai/letta
- InsightFace: https://github.com/deepinsight/insightface
- Voyager, a skill library that grows through code: https://github.com/MineDojo/Voyager
- Gemini with an SO-101: https://github.com/johannstark/GeminiRobotics-SO101

## VLA and simulation

- SmolVLA base: https://huggingface.co/lerobot/smolvla_base
- openpi (pi0): https://github.com/physical-intelligence/openpi
- OpenVLA: https://github.com/openvla/openvla
- XLeRobot: https://github.com/Vector-Wangel/XLeRobot
- MuJoCo Menagerie: https://github.com/google-deepmind/mujoco_menagerie
- LeIsaac: https://github.com/lightwheelai/leisaac
- isaac_so_arm101: https://github.com/MuammerBay/isaac_so_arm101
- gym-hil: https://github.com/huggingface/gym-hil
- phosphobot, a web UI for record and train: https://github.com/phospho-app/phosphobot
- Awesome lists: https://github.com/Psi-Robot/Awesome-VLA-Papers and
  https://github.com/robotics-survey/Awesome-Robotics-Foundation-Models

## Courses, in order

1. HF Robotics Course, free, works without a robot:
   https://huggingface.co/learn/robotics-course
2. QUT Robot Academy, more than 200 short lessons:
   https://petercorke.com/resources/robot-academy/
3. Modern Robotics, chapters 2 to 6, free PDF:
   https://hades.mech.northwestern.edu/index.php/Modern_Robotics
4. RoboGrok: https://robogrok.com/
5. NVIDIA, Train an SO-101 From Sim-to-Real:
   https://docs.nvidia.com/learning/physical-ai/sim-to-real-so-101/latest/04-lerobot.html

## Books

1. Peter Corke, *Robotics, Vision and Control*, 3rd edition, in Python. The main
   recommendation.
2. Lynch and Park, *Modern Robotics*. Screw theory instead of DH; the preprint is free.
3. Imran and Gopalakrishnan, *AI for Robotics*, Apress 2025. VLA and embodied AI.

## Videos

| Video | Why |
|---|---|
| Trelis, Train an ACT Policy for the SO-101: https://www.youtube.com/watch?v=-tkEMLOLEwo | The most complete end to end walk, including training on a Mac |
| SO-ARM101 Assembly and Setup Guide: https://www.youtube.com/watch?v=70GuJf2jbYk | Assembly step by step |
| Nikodem Bartnik's SO-ARM101 series: https://www.youtube.com/user/nikodembartnik | Real problems and troubleshooting |
| Ilia Larchenko, MCP server for LLM control: https://www.youtube.com/watch?v=EmpQQd7jRqs | An LLM drives the arm |
| Ilia Larchenko, LeRobot at FOSSASIA 2025: https://www.youtube.com/watch?v=Tt8zDpZJyrM | An overview of the ecosystem |
| LycheeAI, SO-ARM101 with Isaac Sim: https://lycheeai-hub.com/project-so-arm101-x-isaac-sim-x-isaac-lab-tutorial-series | URDF, MoveIt2, sim2real |
| 3Blue1Brown, Essence of Linear Algebra | Intuition for matrices |

## Tutorials and community reports, valuable for their traps

- SmolVLA blog: https://huggingface.co/blog/smolvla
- How I Trained ACT on SO-101, on identical cameras, "cheating" by looking at the arm, and
  the missing eval set: https://huggingface.co/blog/sherryxychen/train-act-on-so-101
- Phospho, Train SmolVLA: https://docs.phospho.ai/learn/train-smolvla
- Seeed wiki, SO-ARM10x in LeRobot: https://wiki.seeedstudio.com/lerobot_so100m_new/
- Waveshare calibration:
  https://www.waveshare.com/wiki/SO-ARM100/101_Robotic_Arm_Calibration_and_Remote_Control
- XLeRobot, bimanual SmolVLA with three cameras:
  https://xlerobot.readthedocs.io/en/latest/software/getting_started/VLA_smol.html
- HIL-SERL on an SO-101: https://ggando.com/blog/so101-hil-serl/
- Gemini 4 Argon for Robotics: https://developers.googleblog.com/gemini-4-argon-for-robotics/
- Gemini Robotics documentation: https://ai.google.dev/gemini-api/docs/robotics-overview

## Communities

The LeRobot Discord, @LeRobotHF, and the LeRobot hackathons.
