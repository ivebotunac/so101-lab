# Voice control

The arm takes spoken commands through the laptop microphone and answers by voice and by
motion. This guide holds what is known before the first line of that code is written.

## Latency rules everything

Human conversation tolerates a pause of half a second to a second. A talking robot is
therefore a pipeline with a time budget per stage: voice activity detection, speech to text,
the language model, text to speech, with motion running in parallel. Speech-to-speech APIs
shorten the chain and tie the robot to the cloud. The target is under 1.5 s to the first
audio.

## Options for realtime speech

| Option | When |
|---|---|
| OpenAI Realtime over WebRTC | The first choice here. Mature speech to speech, function calling while the robot is speaking |
| Gemini Live with ER 2 streaming | When the same model does perception and planning; its motion calls are blocking |
| Local: Pipecat or LiveKit Agents with faster-whisper and a TTS | Privacy and full control |
| Moshi (Kyutai) | Open source full duplex, about 200 ms, weaker with tools |

The lab compares these rather than committing to one. A language marked as supported and a
voice that is pleasant to listen to are different things for a small language, so each
candidate gets a 15 minute live test in the target language before anything is built on it.
For a fully local pipeline in a small language, check that the TTS model covers it; Meta
MMS-TTS and Piper are the usual candidates.

## Barge-in and echo

- The robot's voice enters its own microphone. Without echo cancellation the robot thinks
  someone is interrupting it. WebRTC brings echo cancellation, which is why WebRTC is used
  and a raw WebSocket is not.
- Turn detection: a voice activity threshold under about 600 ms cuts people off in the
  middle of a thought.
- Keep the microphone and the speaker physically apart.

## Skills

Describing every capability in one prompt costs thousands of tokens and confuses the model.
The Agent Skills pattern (https://agentskills.io) discloses in three layers:

1. **Discovery.** The model sees only a name and a one-sentence description.
2. **Activation.** When it picks a skill, the full `SKILL.md` is loaded.
3. **Execution.** Only then are scripts and resources touched.

A skill is a folder under `behaviors/`: when to use it, parameters, preconditions, the
success criterion, safety limits, and its data such as keyframes. A tool is one Python
module with a `name`, a model-facing `description`, a JSON Schema for parameters, an async
`__call__` and a `needs_response` flag, the pattern Reachy Mini uses.

Kinds of skills for this arm: gestures, pointing, trained policies as tools, perception,
memory, web search, and `idle_do_nothing`.

## Memory

Structure, not a transcript: episodic (what happened), semantic (facts about people),
procedural (learned skills), and for a robot also the record of actions: which skill, which
parameters, whether it succeeded. Candidates: mem0 (https://github.com/mem0ai/mem0) and
Letta (https://github.com/letta-ai/letta).

## Perception in two modes

- **Reflexes are computer vision.** InsightFace computes a face embedding and compares it
  against a FAISS index in milliseconds, locally. Face tracking with a PID loop makes the
  arm "look at" the speaker.
- **Thinking is a VLM.** "What is the person holding?", "is the table tidy?". Slower and
  paid per call.

## Privacy and the EU AI Act

- Face embeddings are a special category of data under GDPR article 9. They need explicit
  consent and a data protection impact assessment: enrol only people who consented, process
  on the device, delete on request.
- The EU AI Act, article 5(1)(f), forbids inferring emotions in educational institutions. A
  robot in a classroom may recognise who someone is, with consent, and never how they feel.
  Features such as affective dialogue stay off.
- Cloud models receive the images sent to them. Crop to the table.

## Web search in a voice loop

Speak a filler ("let me check") the moment a search starts, so the listener hears something
within a second. Retrieve only when needed, answer in 40 to 60 words, cap each result at
300 to 500 characters.

## The five things that hurt

They all come down to time and to who owns the arm.

1. **Who owns the arm right now?** Idle breathing, face tracking, a gesture and a policy all
   write to the same motors. This needs a layered motion arbiter with priorities, a queue
   and interruption rules, designed and not improvised.
2. **Blocking calls in the voice loop.** A tool returns "motion started" at once, the motion
   runs in its own task, and completion arrives as an event. The skill layer is async from
   the first day.
3. **Barge-in and echo.**
4. **Sync of speech and motion.** The nod lands on "of course", not two seconds later.
5. **What happens when a policy fails.** Success detection by a reasoning model and a
   graceful spoken way out.

Reference implementation:
https://github.com/pollen-robotics/reachy_mini_conversation_app

## Where these projects die

Not from complexity but from integrating everything at once. The cure is a vertical slice:
"wave to me", voice, orchestrator, one tool, the arm waves, "there, hi". Once that slice
works, every new skill is an entry in the tool registry, not a new integration project.
