# Motion and kinematics

Intuition and practice, without heavy derivations. The mathematics is left to libraries.

## Two languages for one motion

- **Joint space.** Six numbers, the angle of each joint. The language of motors.
- **Cartesian or task space.** Where the tip of the gripper is (x, y, z) and how it is
  oriented. The language of tasks.

Kinematics translates between the two.

## Forward kinematics, the easy direction

Angles to the position of the tip. Walk along the arm from the base: rotate by the joint
angle, move by the length of the link, and so on to the tip. Each step is a 4 by 4
homogeneous matrix and forward kinematics is their product. There is always exactly one
answer. In practice: load the URDF into ikpy and call `forward_kinematics`.

## Inverse kinematics, the hard direction

Position to angles. It is hard for three reasons:

1. **Several solutions.** Elbow up or elbow down.
2. **No solution.** The point is outside the workspace.
3. **Singularities.** With the arm fully stretched, a tiny move of the tip demands wild
   swings of the joints.

The **Jacobian** is a matrix that says how far the tip moves when each joint turns a little.
Numerical IK solvers use it iteratively, and when it degenerates, that is the signature of a
singularity.

## Smoothness is physics, not looks

A jump from 10 to 60 degrees is in theory infinite acceleration, which means a jerk,
vibration and wear. So a trajectory is computed:

- **linear:** constant speed, jerks at start and stop,
- **cubic spline:** smooth position and speed,
- **trapezoidal velocity:** accelerate, hold, decelerate, the classic for motors,
- **minimum jerk:** minimises the third derivative, the way a human arm moves.

## PID: how the motor gets where it was told

- **P** pushes in proportion to the error. A large P is fast but overshoots and oscillates.
- **I** remembers accumulated error and removes a lasting offset. Too large gives slow
  oscillation.
- **D** brakes according to the rate of change. Too large amplifies noise.

On the SO-101: a limp arm that lags has gains that are too low, an arm that buzzes around
its target has gains that are too high.

## Where kinematics is needed

- **Needed:** scripted gestures in space, pointing at an object (a VLM gives the point, IK
  the angles), safety checks (is the target inside the workspace), and any harness that
  offers a primitive such as `goto(x, y, z)`.
- **Not needed:** VLA policies such as ACT and SmolVLA, which learn the mapping from images
  to angles directly in joint space.

Understanding both tells you when a problem is 20 lines of IK and when it is 50
demonstrations and a training run.

## Tools

- **ikpy**, the fastest start for FK and IK from a URDF: https://github.com/Phylliade/ikpy
- **lerobot-kinematics**, FK and IK for the SO-101 with MuJoCo and keyboard control of the
  end effector: https://github.com/box2ai-robotics/lerobot-kinematics
- **Robotics Toolbox for Python**: https://github.com/petercorke/robotics-toolbox-python
- **MuJoCo Menagerie**, model `trs_so_arm100`:
  https://github.com/google-deepmind/mujoco_menagerie
- **placo** for fast realtime IK. One community report on an SO-101 hit a state caching bug
  that made the arm drift and moved to MuJoCo solvers.
- Feetech tutorials: https://github.com/commanderfun/STS3215 and
  https://github.com/vassar-robotics/feetech-servo-sdk

Skip for now: DH tables by hand, dynamics, derivations of screw theory.

## A six week path

| Week | Work | Done when |
|---|---|---|
| 1 | Feetech SDK: move each motor, read position, current, temperature | All six joints are under control |
| 2 | Calibrate both arms, teleoperate | Leader and follower match |
| 3 | Forward kinematics with ikpy on the URDF | The predicted tip is within 1 to 2 cm of the real one |
| 4 | MuJoCo simulation | A real pose is reproduced in simulation |
| 5 | Inverse kinematics, the arm to a given point | Five points reliably, no limit exceeded |
| 6 | Smooth trajectories and the first scripted gesture | The gesture repeats without jerks |

## Watching

- QUT Robot Academy: https://petercorke.com/resources/robot-academy/
- Modern Robotics, chapters 2 to 6:
  https://www.youtube.com/playlist?list=PL917Z2qaUgvhLe1stf2rCEbI4zx7mDyuR
- RoboGrok, the most approachable IK: https://robogrok.com/
- PID intuitively: https://mikelikesrobots.github.io/blog/understand-pid-controllers/
