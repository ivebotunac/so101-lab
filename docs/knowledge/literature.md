# Literature

Leads for reading, not conclusions.

## Surveys, start here

| Paper | Year | Why |
|---|---|---|
| [VLA Models for Robotics: A Review Towards Real-World Applications](https://doi.org/10.1109/access.2025.3609980) | 2025 | A full-stack review of VLA, https://vla-survey.github.io |
| [Foundation models in robotics](https://doi.org/10.1177/02783649241281508) | 2024 | The canonical survey |
| [A survey on integration of LLMs with intelligent robots](https://doi.org/10.1007/s11370-024-00550-5) | 2024 | Tutorial-level prompting examples, good for teaching |
| [A Survey of Robot Intelligence with LLMs](https://doi.org/10.3390/app14198868) | 2024 | Reward design, low-level control, planning |
| [Embodied Learning for Object-centric Manipulation](https://doi.org/10.1007/s11633-025-1542-8) | 2025 | Perception and policy learning for manipulation |
| [Survey on RL of VLA Models](https://doi.org/10.36227/techrxiv.176531955.54563920/v1) | 2025 | Reinforcement learning on top of VLA, preprint |
| [Multimodal fusion and VLMs for robot vision](https://doi.org/10.1016/j.inffus.2025.103652) | 2025 | VLM perception |
| [VLM-based human-robot collaboration](https://doi.org/10.1007/s42524-025-4136-9) | 2025 | Collaboration examples for teaching |

## System papers

- **ELLMER**, [Nature Machine Intelligence 2025](https://doi.org/10.1038/s42256-025-01005-x):
  GPT-4 with retrieval and force and visual feedback for long-horizon tasks. The closest
  related work to a reasoner that orchestrates skills on an arm.
- **Benchmarking VLA Models on SO-101: Failure and Recovery Analysis**,
  https://arxiv.org/abs/2606.08881: pi0.5, SmolVLA, Wall-X and ACT fine-tuned on a physical
  SO-101, with a failure taxonomy and recovery metrics. The closest thing to a reference
  result for this arm.
- **Robot Learning: A Tutorial**, https://arxiv.org/abs/2510.12403: a good base for teaching.
- [Touch and vision for robotic housekeeping](https://doi.org/10.1038/s41467-024-51261-5),
  Nature Communications 2024.
- [Survey on LLM-Enhanced RL](https://doi.org/10.1109/tnnls.2024.3497992), IEEE TNNLS 2024.
- [Survey on LLM based autonomous agents](https://doi.org/10.1007/s11704-024-40231-1).

## Primary VLA papers

| Paper | arXiv |
|---|---|
| pi0.5 | 2504.16054 |
| OpenVLA | 2406.09246 |
| SmolVLA | 2506.01844 |
| GR00T N1 | 2503.14734 |
| Gemini Robotics 1.5 | 2510.03342 |
| HIL-SERL | 2410.21845 |
| UMI | 2402.10329 |
| FAST | 2501.09747 |
| AnySkin | 2409.08276 |

## Directions the field is moving in

1. Reinforcement learning fine-tuning on top of VLA models.
2. Synthetic data from world models and from reasoners that build a simulated twin.
3. Hierarchical systems of a reasoner and a controller, which is where this lab sits.
