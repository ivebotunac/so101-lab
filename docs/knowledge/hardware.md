# Hardware: SO-101 Pro

The SO-101 is the second generation of the SO-ARM100 by TheRobotStudio and Hugging Face,
with better cable routing, easier assembly and tuned leader gear ratios. Each arm has 6
degrees of freedom and 6 Feetech STS3215 smart servos. STL files, the bill of materials and
the URDF and MJCF models: https://github.com/TheRobotStudio/SO-ARM100

## The Pro kit has two power supplies

The Pro difference is the follower: 6 STS3215 at 12 V, up to about 30 kg·cm, instead of
7.4 V at 16.5 to 19.5 kg·cm, with the same 1/345 gearing. The leader keeps 7.4 V motors.

- **Leader on the 5 V supply, follower on the 12 V supply. Never swap them.**
- Mark the adapters with labels or colour before switching anything on.
- A weak supply shows up as random motor resets.

## Gear ratios

All six follower motors are 1/345, for maximum torque. The leader is pushed by hand, so it
mixes ratios:

| Joint | Ratio |
|---|---|
| J1 shoulder pan | 1/191 |
| J2 shoulder lift | 1/345 |
| J3 elbow flex | 1/191 |
| J4 wrist flex | 1/147 |
| J5 wrist roll | 1/147 |
| J6 gripper | 1/147 |

The motors look identical from outside. Write F1 to F6 and L1 to L6 on the housings before
assembly. A swapped motor in the leader is one of the most common mistakes.

## Why a smart servo matters

A hobby servo accepts "go to this angle" and cannot be asked anything. The STS3215 has a
microcontroller, a magnetic encoder and serial communication, so it reports position, speed,
load, current, voltage and temperature. For learning this is decisive, because noise in the
readings becomes noise in the model.

| Item | Value |
|---|---|
| Encoder | 12-bit magnetic, 4096 steps per turn, about 0.088 degrees, no sliding contact |
| Communication | Half duplex serial bus, daisy chain, id 0 to 253 |
| Backlash | 0.5 degrees or less |
| Feedback | Position, speed, load, current, voltage, temperature |

Positions from 0 to 4095 in LeRobot come from that resolution. The angle of a joint from a
raw position is `(position - 2048) * 360 / 4096`.

## Bus and ids

All six motors share one line and are told apart by id, 1 to 6. Every motor ships with id 1,
so during setup each is connected alone and given its id before joining the chain. Two
motors with the same id on the line produce chaos.

## Registers

| Register | Address | Note |
|---|---|---|
| Mode | 33 | 0 position, 1 velocity, 2 PWM, 3 step |
| Torque_Enable | 40 | 0 limp, 1 holding |
| Goal_Position | 42 | Target position |
| Present_Position | 56 | Actual position |
| Present_Load | 60 | Relative torque, 1000 is 100 percent |
| Present_Temperature | 63 | Degrees Celsius |
| Present_Current | 69 | 1 unit is 6.5 mA |

Switch torque off before writing to EEPROM. LeRobot's `FeetechMotorsBus` uses the same
register names.

## Current as a sense of touch

`Present_Current` rises when the arm meets resistance. It is the cheapest force feedback
there is: if the current jumps while the gripper closes, something has been caught.

## Why the arm dies without power

The STS3215 has no mechanical brake and holds position only with active torque. When torque
is switched off, during calibration or a disconnect, the arm falls. So: table clamps for
both arms, a hand ready to hold the arm, and no arm left stretched out under load, which
heats the motor.

## Temperature

Static holding settles around 48 °C. Intense oscillation reaches about 71 °C, where the
motor enters protection. During long sessions read the temperatures every few minutes.

## Calibration is an agreement about zero

The encoder knows the angle of the shaft and not what that angle means for this arm, which
depends on how it was assembled. Calibration settles that with the software. Consequences:

- repeat it after every disassembly,
- a dataset recorded on one calibration is not valid for another, because the same number
  is a different physical angle,
- the same holds for other people's datasets and for base models.

## Cameras

- The lab uses a scene camera and a wrist camera. Ordinary USB cameras are enough.
- SmolVLA expects its cameras as `camera1`, `camera2`, `camera3`; the lab's names are mapped
  to those with `--rename_map`.
- Two identical cameras get their USB paths swapped by the operating system.
- Lighting matters more than resolution: a fixed desk lamp and a consistent scene.
- RealSense or OAK-D only once depth is needed.

## Typical traps

1. A wrong calibration makes everything wrong.
2. Swapped power supplies on a Pro kit, swapped motors in the leader.
3. Overheating, above all the gripper in continuous work.
4. The arm falls without torque.
5. Backlash: do not expect absolute precision, least of all with the arm stretched out.
6. The gripper wears out from too much grasping force. Limit force and speed.

## Later extensions

Tactile sensing with AnySkin (https://arxiv.org/abs/2409.08276), the LeKiwi mobile base, and
the dual-arm XLeRobot (https://github.com/Vector-Wangel/XLeRobot).
