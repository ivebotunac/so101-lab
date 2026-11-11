# Motion without training

Most of what a conversational robot does with its arm needs no trained model.

## The deciding question

Does the motion depend on where something is in the scene, and does it need contact?

| Kind of motion | Example | How |
|---|---|---|
| Independent of the scene | wave, nod, shrug, "thinking", breathing | keyframes or replay, no training |
| Depends on a known coordinate | point at the cup, follow a face, pick and place of simple objects | VLM pointing or a reasoning model plus IK, no training |
| Contact and fine feedback | insert, wipe, rearrange, fold | training (SmolVLA) |

Roughly 80 percent of the repertoire sits in the first two rows.

## Why a VLA is the wrong tool for gestures

SmolVLA has no waving because its pretraining data is almost entirely tabletop manipulation.
Even with the data it would be wrong:

- **Not deterministic.** Flow matching is generative, so every wave differs a little. A
  gesture that comes out different each time reads as a fault, not as character.
- **Sensitive to the scene.** A cup on the table distorts the wave, because the model is
  conditioned on the image.
- **Latency.** About 99 ms per chunk instead of a known list of poses.
- **No sync with speech.** A nod exactly on "of course" needs control per frame.
- **Cost.** 50 demonstrations and 4 hours of A100 for a nondeterministic version of 20 lines
  of code, times fifteen gestures.

Pollen Robotics does the same in the Reachy Mini conversation app: recorded clips and
scripts, no VLA anywhere.

## Ways to author a motion

1. **Record and replay with the leader.** Act the gesture out, record one episode,
   `lerobot-replay` repeats it. Fifteen gestures in an afternoon. Valid for one calibration.
2. **Kinesthetic teaching.** Torque off on the follower, guide it by hand, a script reads
   `Present_Position` at 30 Hz. Release torque only on the joints being guided (for a wave:
   `wrist_flex`, `wrist_roll`, `shoulder_pan`) while `shoulder_lift` and `elbow_flex` hold
   the arm up.
3. **Keyframes in code.** A list of poses with ease-in and ease-out interpolation. A wave is
   an oscillation of `wrist_roll`, a nod of `wrist_flex`, a shrug of `shoulder_lift`.
   Amplitude and speed are parameters, so one gesture becomes a shy or an excited wave
   without a new recording.
4. **Teleoperation without a leader.** Phone, keyboard or gamepad.
5. **Authoring in simulation.** `lerobot-kinematics` moves the end effector with the
   keyboard in MuJoCo, and the same script then runs on the real arm.
6. **An LLM writes the gesture.** Through an MCP server for the arm, describe the motion in
   words, iterate, then freeze the result as keyframes. The LLM is no longer in the loop
   when the gesture plays.

Keyframes suit symmetric gestures, kinesthetic teaching or replay suit the ones that are
hard to describe in numbers, the simulator suits pointing and reaching.

Training SmolVLA without real demonstrations means simulation (Isaac Lab, MuJoCo), a project
of weeks with a real sim-to-real gap. For 50 episodes teleoperation wins.

## Pointing without training

```
image -> VLM: "point to the red cup" -> (412, 305)
      -> homography image to table   -> (x, y) on the table
      -> IK                          -> joint angles -> the arm points
```

On a table the step from 2D to 3D is easy because the surface is known: one homography, from
a checkerboard or from the arm touching 4 to 6 points. Arbitrary 3D positions need depth.

## The gripper as a mouth

The SO-101 has no head or face, so it looks dead while it speaks. A gripper that opens in
the rhythm of speech gives a point of focus and reads at once as "this is talking".

- The amplitude envelope of the audio going to the speaker sets the gripper opening, 10 to
  20 times a second. No model.
- Use the envelope, not the raw signal: RMS over a window of about 50 ms.
- Keep the amplitude small. 15 to 25 percent of full travel gives a convincing murmur, a
  wide open gripper looks hysterical.
- Compensate latency by shifting the envelope in time.
- Limit the speed and watch `Present_Temperature`. The gripper is the only motor that works
  nonstop.

## Patterns taken from Reachy Mini

- **Layered motion.** Primary motions (dance, emotion, goto, breathing) wait in a queue and
  a reactive wobble is blended over them. This solves ownership of the motors, it is not
  decoration.
- **Breathing as the idle motion.** A robot that stands perfectly still looks dead.
- **`idle_do_nothing` as an explicit tool.** The model must be able to choose to do nothing,
  otherwise every pause becomes a motion.

## Three layers of motion

| Layer | With | Why |
|---|---|---|
| Expression: wave, nod, breathing, mouth | replay and keyframes | repeatable, synchronised, free |
| Direction: point, follow a face, simple pick and place | reasoning model, homography, IK | depends on a coordinate, needs no learning |
| Manipulation: contact, fine motor control | SmolVLA | the only place training pays off |

The orchestrator does not see the difference: `play_gesture("wave")` and
`pick_and_place("cube", "bowl")` are both tools with a name, a description and parameters.
