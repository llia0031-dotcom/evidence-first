# Real-time voice agent evaluation: evaluation card

> Card version 1.2 · Data as of 2026-11-15 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-13 – 2026-11-15 | Liang Liyuan | Python, SenseVoice, local MCP tools, FireRedChat pVAD, Claude Haiku 5.5 | [Code and report](https://github.com/llia0031-dotcom/voice-agent-eval) |

**Problem**: Whether a voice assistant still gets the task right when the user pauses, interrupts, says "mm" or talks over background speech, with experience measured as latency, barge-in and false-stop numbers.

**What I did**: I wrote 42 conversations with pauses, barge-ins, backchannels and noise, answers fixed in advance, and built a local cascaded voice agent as the baseline; then tried fixes one at a time, each with its own preregistration addendum, and combined the ones that worked.

**Results**: 

- Strict pass: baseline (thinking on) 61/84, four fixes combined 62/84; text-only control 82/84
- First audio over background speech: 20.4 s → 4.56 s (primary-speaker VAD)
- Real barge-ins stopped 16/16, in 0.25 s

## Summary

Measures a cascaded real-time voice agent (voice activity detection → speech recognition → a model with tools → speech synthesis) on 42 scripted Chinese and English conversations covering pauses, interruptions, backchannels, noise and tool calls. Answers were fixed when the items were written; items, audio and scorer were frozen before the run. Three baseline settings and a text-only control come first; fixes are then tried one at a time on the same items (backchannels are not barge-ins, pause before cancelling, a shorter first speech chunk, confirm before deleting, listen only to the primary speaker), and the useful ones are combined.

- **Place in the portfolio**: Scenario: interaction
- **Link to the core component**: Follows evidence-check's preregistration practice; an offline check also compares spoken confirmations with tool results.
- **Models used**: claude-haiku-5-5 (effort low, standard streaming API: every call is in the real-time loop, so batch does not apply); SenseVoice for recognition; FireRedChat pVAD for primary-speaker detection.

## Uses

- Compare settings of a real-time voice agent: which holds up under pauses, barge-ins, backchannels and noise, and at what latency cost.
- Replay the same items before changing a setting, to see whether anything that worked breaks.

## Out of scope

- Not an evaluation of end-to-end speech models; none was compared.
- Does not represent real users: user speech is synthesised, time is simulated and echo cancellation is assumed perfect.

## Evaluation data

### Main run: three baseline settings and a text-only control (42 conversations)

42 conversations: tasks, pauses, barge-ins, backchannels, pink noise and background speech. Answers fixed at writing; items, audio manifest and scorer frozen before the run.

| Field | Value |
|---|---|
| Date | 2026-11-13 |
| Items and answers | 42 conversations, 2 runs per setting, 84 in all |
| Runs | 2 runs per setting, pooled; the runs are not independent, so intervals are too narrow |
| Model and send mode | claude-haiku-5-5, standard streaming API |
| Frozen before the run | `eval/PREREGISTRATION.md` (plan, expectations, file hashes) |

### Fixes one at a time (same 42 conversations)

Items, audio and scorer unchanged; each fix has its own preregistration addendum (change, expectation, file hashes). Only two adopted fixes and the combined setting are listed here; the rest are in section 6 of the project report.

| Field | Value |
|---|---|
| Date | 2026-11-14 |
| Items and answers | 42 conversations, 2 runs per setting |
| Runs | 2 runs per setting, pooled |
| Model and send mode | claude-haiku-5-5, standard streaming API |
| Frozen before the run | `eval/PREREGISTRATION.md`, addenda 1–11 |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Main run: three baseline settings and a text-only control (42 conversations)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Text-only control: strict pass | 82/84 (97.6%, 95% CI 91.7–99.3%) | context only | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| VAD baseline, thinking off: strict pass | 59/84 (70.2%, 95% CI 59.8–79.0%) | higher is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| VAD baseline, thinking on: strict pass | 61/84 (72.6%, 95% CI 62.3–81.0%) | higher is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| Thinking off: end of speech to first audio (clean task items) | 2.94 s (median, n=32, 95% CI 2.76–3.14) | lower is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| Thinking on: end of speech to first audio (clean task items) | 3.95 s (median, n=32, 95% CI 3.49–4.66) | lower is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| Thinking on: stopped on a real barge-in | 16/16 (100.0%, 95% CI 80.6–100.0%) | higher is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| Thinking on: kept talking through a backchannel | 0/8 (0.0%, 95% CI 0.0–32.4%) | higher is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| Reasoning said aloud with thinking off | 23/84 (27.4%, 95% CI 19.0–37.7%) | lower is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| Thinking on: first audio over background speech | 20.4 s (median, n=8, 95% CI 19.1–22.5) | lower is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |

### Fixes one at a time (same 42 conversations)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Primary-speaker VAD: strict pass | 63/84 (75.0%, 95% CI 64.8–83.0%) | higher is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| Primary-speaker VAD: first audio over background speech | 4.56 s (median, n=8, 95% CI 2.97–5.69) | lower is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| Pause, cancel only on a real barge-in: strict pass (under the original rule a pause counts as a stop, so backchannel items still fail) | 59/84 (70.2%, 95% CI 59.8–79.0%) | higher is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| Four fixes combined: strict pass | 62/84 (73.8%, 95% CI 63.5–82.0%) | higher is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| Four fixes combined: first audio (clean task items) | 3.83 s (median, n=32, 95% CI 3.38–4.12) | lower is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| Four fixes combined: stopped on a real barge-in | 16/16 (100.0%, 95% CI 80.6–100.0%) | higher is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| Four fixes combined: barge-in to stop | 0.25 s (median, n=16, 95% CI 0.25–0.28) | lower is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| Backchannel rule: kept talking through a backchannel | 4/8 (50.0%, 95% CI 21.5–78.5%) | higher is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| Plus fixed language: kept talking through a backchannel | 4/8 (50.0%, 95% CI 21.5–78.5%) | higher is better | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |

The four fixes together are the best setting tested; the remaining backchannel problem cannot be solved from transcribed text alone and needs the audio itself.

## Grader calibration

- No grader is used: scoring is a frozen rule-based script that ships six known-answer traces and must pass them first.
- Reasoning said aloud is detected with a fixed pattern.

## Limitations and failure cases

- User speech is synthesised and time is simulated; with 42 conversations and two runs per setting, a difference of one or two is noise.
  - Recommendation: Before launch, rerun with recorded human speech (for example a public dialogue speech set) and measure latency on a real network.
- Backchannels such as "mm-mm" still interrupt: the recogniser hears other words, and text alone cannot tell a backchannel from a short barge-in.
  - Recommendation: Use detection on the audio itself; an off-the-shelf acoustic backchannel model was tried offline and missed the preset bar, so it was not added.
- No end-to-end real-time speech model was compared.
  - Recommendation: Add an end-to-end model with a free tier and compare it on the same items and scorer.

## Versions

- **1.0** (2026-11-15) First card; the project is not public.
- **1.1** (2026-11-15) Added when, team, stack, links and "problem / what I did / results" at the top, the way portfolio case studies open; the evaluation sections are unchanged.
- **1.2** (2026-11-16) The project is public: link to the code and report added; source files link to the identical copies in the public repository.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.
