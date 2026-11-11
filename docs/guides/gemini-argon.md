# Gemini Robotics ER and Gemini 4 Argon

Both are reasoners: they look, understand, plan and call functions. Neither drives motors.
The code in this repo executes what they ask for, after checking it.

Model ids, prices and limits change. The values below are from October 2026; read the
official documentation before relying on any of them.

- Robotics overview: https://ai.google.dev/gemini-api/docs/robotics-overview
- Argon for robotics: https://developers.googleblog.com/gemini-4-argon-for-robotics/
- Argon model page: https://ai.google.dev/gemini-api/docs/models/gemini-4-argon

## The Gemini Robotics family

- **ER (Embodied Reasoning).** A VLM for spatial reasoning: pointing as 2D points, bounding
  boxes, planning, object tracking, success detection, orchestration. Publicly available.
- **Gemini Robotics VLA.** End-to-end control, for selected partners only.

## ER 2

| Endpoint | Use |
|---|---|
| `gemini-robotics-er-2-preview` | Structured output, code execution, multi-step tool use |
| `gemini-robotics-er-2-streaming-preview` | Live API over WebSocket: 16 kHz PCM audio and JPEG up to 1 fps, for a voice loop |

- The API key must have restrictions; an unrestricted key returns 403.
- Function calls for physical motion are blocking, so a long motion stops the conversation.
- The API provides no safety stop and no collision checking. Arguments are validated here,
  and a network retry must never turn one motion into two.
- Google forbids safety-critical use. The safety layer is this repo's responsibility.
- An example of Gemini with an SO-101: https://github.com/johannstark/GeminiRobotics-SO101

The pattern: ER receives speech and an image, returns pointing and a plan, calls skills as
function calls, watches progress and replans.

## Argon

A model for reasoning and writing code, not a VLA. It does not send motor commands 30 times
a second. Every few seconds it looks at an image and calls a function such as
`grasp(x, y, z)`, which this repo's code executes. Argon is the engineer who draws where the
arm should go; a trained policy is the reflex in the arm.

Google's blog shows an SO-101 placing a LEGO brick into a box, improving over three
iterations from 58.9 s to 22.9 s to 17.4 s. Argon used a visual coordinate harness (the
wrist camera with a grid drawn over it) and action primitives (`grasp`, `place`, `goto`,
`move_until_contact`) served by a local HTTP server. The harness was not published; the
prompts were, in three phases: a dry run without moving, a hover with a check through the
wrist camera, then autonomous execution.

As of October 2026: `gemini-4-argon` on the paid tier of the Gemini API, through the
Interactions API and the `google-genai` SDK, at an introductory 2 USD per million input and
10 USD per million output tokens. Output is text only, the Live API is not supported, and
no production latency is published. Articles claiming latency under 50 ms and "actuation
tokens" did not match the official documentation.

### Three ways to use it

1. **Argon drives the arm zero-shot** through a harness: an HTTP server, IK and the safety
   layer. Argon never sends raw angles.
2. **Argon helps SmolVLA offline.** Hindsight labelling and a progress curve for recorded
   episodes, to drop the bad demonstrations. Synthetic data is the most demanding variant
   and comes last.
3. **Argon as the planner of the conversational robot.** A speech model handles the talking
   and calls Argon as a tool for tasks that need thought, such as "sort the bricks by
   colour".

### Is training still needed

Not for tasks that can be described by points in space: go above, descend, close, lift,
carry. IK handles the movement between points.

It is needed for contact and fine motor control (wiping, inserting, pushing), for speed and
smoothness (17 s per pick and place against a fluid policy), for moving objects, and for
working without internet and without a cost per move.

The leader arm stays useful for calibration, recording gestures, testing IK, future
demonstrations and teaching.

## Plan: clear the table into a box

### Physical setup

- The arm and the box are fixed, the box coordinates are written in code.
- Two cameras: the scene camera and the wrist camera for a check before the grasp.
- A matte single-colour surface, even light, objects that contrast with it.
- First objects: a LEGO brick, an eraser, a marker, a bottle cap, a small sponge. Avoid
  heavy, wide, flat (paper, cards) and slippery round objects.

### Calibration, the most important part

A coordinate system with its origin at the base of the arm, in centimetres. A homography for
the scene camera: the arm touches 4 to 6 points and each gets a pixel and a real position.
Most later misses come from here.

### The robot server, no AI in it

```
get_obs()            -> scene image, wrist image, gripper state
hover(x, y, yaw)     -> gripper 5 cm above the point
grasp(x, y, z, yaw)  -> descend, close, lift
drop_in_box()        -> move above the box and open
home()
```

The safety layer refuses anything outside the workspace, below the minimum height or above
the maximum speed. Grasp detection: a gripper that closes all the way holds nothing, so the
call returns `grasp_failed`.

### The agent loop

`google-genai` with function calling: image and task, a function call, execute it, return
the result and a new image, repeat until `done()`. A limit on steps and on cost per task is
mandatory.

### The prompt

It states the coordinate system, the position of the box, the gripper width, the list of
functions and the rules:

- first an inventory: JSON with each object, its position, orientation, grasp plan, and
  "can" or "cannot",
- one object at a time, starting with those that do not block others,
- always `hover` and check the wrist image before a grasp,
- after the drop, check that the object is gone from the table,
- at most 2 attempts per object, then skip it and say why.

### Order of testing

1. Access and latency: a photo of the table, coordinates of the objects, time and cost.
2. Inventory only, no arm: compare the coordinates with a ruler, error in centimetres.
3. Hover only: the arm hovers above each object, measure the offset.
4. One object: a LEGO brick into the box, 10 times.
5. Three to five different objects.
6. Self-improvement: logs and video of failures go back to Argon, which proposes changes.
7. The comparison: Argon zero-shot against SmolVLA with 50 episodes on the same tasks.

The stages without the arm and with hover only uncover most problems before anything can
break.

### What is hard

The AI part is the easier one: the agent loop and the prompt are a few hundred lines. The
hard part is classical robotics. A calibration error of 1 to 2 cm misses a small object, the
SO-101 has backlash and loses precision when stretched out, and the gripper is simple.
Calibration and IK are therefore solved as their own small project before Argon is
connected.

### What to watch

- Cost: a few cents per move with an image, tens of cents per task.
- Privacy: the images go to Google. Crop them to the table so that people stay out of frame.
- Hallucinated coordinates: the safety layer refuses everything outside the workspace,
  whatever the model says.
