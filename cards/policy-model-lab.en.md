# Policy Model Lab: evaluation card

> Card version 1.0 · Data as of 2026-11-18 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-17 – 2026-11-18 | Liang Liyuan | Python, PyTorch, LoRA fine-tuning (Qwen3), local vision-language models (Qwen3.5, Qwen3-VL), SigLIP 2, mmBERT, OCR, Message Batches API | [Code and report](https://github.com/llia0031-dotcom/policy-model-lab) |

**Problem**: To review a short video ad against policy, what must a model see, and can a small model trained on synthetic ads do the job?

**What I did**: On a laptop GPU I ran three preregistered experiments: what a model needs to see of a short video ad (caption, cover, sampled frames, the whole video, text read off the frames) to review it well; whether small models fine-tuned on synthetic ads match a large model; and a check on 300 real short videos from another platform. A survey of the past year's research closes it.

**Results**: 

- Video ads: claude-haiku-5-5 with 16 frames was right on 86/96 and caught every violation (64/64); with the caption only it caught 25/64
- Locally, Qwen3.5-4B reading only the text from 16 frames was right on 80/96, the same as watching the whole video (80/96), in 2.4 s per item against 19.2 s
- Qwen3-1.7B fine-tuned on synthetic ads was right on 133/168 of Grounded Review's test items, too close to call against claude-haiku-5-5 (138/168; paired difference -3.0 points)

## Summary

Three experiments on reviewing short video ads against policy, all on one laptop GPU, with plans and predictions preregistered. The first compares what a model is shown of the same ad: caption, cover, sampled frames, the whole video, or text read off the frames. The second fine-tunes small models on synthetic ads and compares them with a large model on Grounded Review's test items, video text and real cases. The third checks 300 real short videos from another platform for a yes/no violation call. For the real videos and real cases only totals are published.

- **Place in the portfolio**: Scenario: judgement
- **Link to the core component**: The second experiment tests on Grounded Review's items and policy categories; its findings feed the triage step of the Grounded Labelling Pipeline.
- **Models used**: The large model is claude-haiku-5-5 (Message Batches API); locally Qwen3.5-4B, Qwen3-VL-2B, SigLIP 2, mmBERT and LoRA-tuned Qwen3-0.6B and Qwen3-1.7B.

## Uses

- Choosing inputs and models for a review team: read the text off the frames first, then decide whether a costlier model should see the picture.
- A pre-launch method: compare inputs and model sizes on one item set and check each prediction written beforehand.

## Out of scope

- The video ads are synthetic with answers fixed when written; the real videos come from another platform whose standard differs from this project's policy library.
- For the real videos and real cases only totals are published, no text or frames.
- Other programs were using the GPU while Qwen3-VL-2B ran, so its timings are not compared.

## Evaluation data

### Video ads: what the model is shown (96 videos)

96 synthetic video ads (half Chinese, half English), 64 violating and 32 compliant (some of them look-alike traps); answers fixed when written. Each ad is shown as caption, cover, 8 or 16 sampled frames, the whole video, or the text read off the frames.

| Field | Value |
|---|---|
| Date | 2026-11-17 |
| Items and answers | 96 videos |
| Runs | 1 run per input |
| Model and send mode | claude-haiku-5-5 through the Message Batches API; local models on one laptop GPU |
| Frozen before the run | `eval/PREREGISTRATION.md` |

### Small models fine-tuned on synthetic ads

Trained on synthetic ads and tested on unseen sets: Grounded Review's test items (168 decisions), the video ads' text, 46 real cases (totals only) and a synthetic validation set. Compared with the same model untuned, claude-haiku-5-5 and mmBERT; paired differences carry intervals from 4,000 bootstrap resamples.

| Field | Value |
|---|---|
| Date | 2026-11-17 |
| Items and answers | 168 decisions on Grounded Review's items; 46 real cases |
| Runs | 1 run per model |
| Model and send mode | Qwen3-1.7B with LoRA trained on one laptop GPU; claude-haiku-5-5 through the Message Batches API |
| Frozen before the run | `eval/PREREGISTRATION.md` |

### Real short videos from another platform: violating or not (300, totals only)

300 of the 1,000 KuaiMod test videos drawn with a fixed seed (173 fine, 127 violating), asking whether the video breaks the platform's community rules. Local models saw downscaled frames; claude-haiku-5-5 received the originals. No frame, title or text is shown.

| Field | Value |
|---|---|
| Date | 2026-11-17 |
| Items and answers | 300 videos |
| Runs | 1 run per model |
| Model and send mode | claude-haiku-5-5 through the Message Batches API; Qwen3.5-4B locally |
| Frozen before the run | `eval/PREREGISTRATION.md` |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Video ads: what the model is shown (96 videos)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Caption only: violations caught (claude-haiku-5-5) | 25/64 (39.1%, 95% CI 28.1–51.3%) | higher is better | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| 16 frames: decisions right (claude-haiku-5-5) | 86/96 (89.6%, 95% CI 81.9–94.2%) | higher is better | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| 16 frames: violations caught (claude-haiku-5-5) | 64/64 (100.0%, 95% CI 94.3–100.0%) | higher is better | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| Whole video: decisions right (Qwen3.5-4B, local) | 80/96 (83.3%, 95% CI 74.6–89.5%) | higher is better | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| Text from 16 frames only: decisions right (Qwen3.5-4B, local) | 80/96 (83.3%, 95% CI 74.6–89.5%) | higher is better | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| Whole video: median seconds per item (Qwen3.5-4B) | 19.2 s | lower is better | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| Frame text only: median seconds per item (Qwen3.5-4B) | 2.4 s | lower is better | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| 8 frames: compliant ads wrongly rejected (Qwen3-VL-2B) | 28/32 (87.5%, 95% CI 71.9–95.0%) | lower is better | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| 16 frames: decisions right (SigLIP 2) | 62/96 (64.6%, 95% CI 54.6–73.4%) | higher is better | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |

With the caption only most violations are missed; more frames catch more. Locally, Qwen3.5-4B reading only the text off the frames is as accurate as watching the whole video, much faster and with less GPU memory.

### Small models fine-tuned on synthetic ads

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Grounded Review's items: right (Qwen3-1.7B + LoRA) | 133/168 (79.2%, 95% CI 72.4–84.6%) | higher is better | [`policy-model-lab/results/text_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_summary.md) |
| Grounded Review's items: right (claude-haiku-5-5) | 138/168 (82.1%, 95% CI 75.7–87.2%) | higher is better | [`policy-model-lab/results/text_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_summary.md) |
| Paired difference: 1.7B + LoRA minus claude-haiku-5-5 (points) | -3.0 | context only | [`policy-model-lab/results/text_paired.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_paired.md) |
| Paired difference: tuned minus untuned (points) | 11.3 | higher is better | [`policy-model-lab/results/text_paired.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_paired.md) |
| Real cases: right (Qwen3-1.7B + LoRA) | 38/46 (82.6%, 95% CI 69.3–90.9%) | higher is better | [`policy-model-lab/results/text_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_summary.md) |
| Real cases: right (claude-haiku-5-5) | 33/46 (71.7%, 95% CI 57.5–82.7%) | higher is better | [`policy-model-lab/results/text_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_summary.md) |
| Synthetic validation: right (mmBERT) | 173/191 (90.6%, 95% CI 85.6–94.0%) | higher is better | [`policy-model-lab/results/text_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_summary.md) |
| Real cases: right (mmBERT) | 25/46 (54.3%, 95% CI 40.2–67.8%) | higher is better | [`policy-model-lab/results/text_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_summary.md) |
| Training time (minutes, Qwen3-1.7B + LoRA) | 46.2 | context only | [`policy-model-lab/results/train/qwen3-1.7b-lora.json`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/train/qwen3-1.7b-lora.json) |

The tuned 1.7B model is too close to call against claude-haiku-5-5 on Grounded Review's items and well above the untuned model; the further from the synthetic data the more it drops, and mmBERT is near half on real cases.

### Real short videos from another platform: violating or not (300, totals only)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Frames and text: right (Qwen3.5-4B, local) | 225/300 (75.0%, 95% CI 69.8–79.6%) | higher is better | [`policy-model-lab/results/kuaimod_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/kuaimod_summary.md) |
| Frames and text: right (claude-haiku-5-5) | 214/300 (71.3%, 95% CI 66.0–76.2%) | higher is better | [`policy-model-lab/results/kuaimod_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/kuaimod_summary.md) |
| Fine videos flagged (Qwen3.5-4B) | 45/173 (26.0%, 95% CI 20.0–33.0%) | lower is better | [`policy-model-lab/results/kuaimod_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/kuaimod_summary.md) |
| Fine videos flagged (claude-haiku-5-5) | 70/173 (40.5%, 95% CI 33.4–47.9%) | lower is better | [`policy-model-lab/results/kuaimod_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/kuaimod_summary.md) |

With frames and text the local Qwen3.5-4B was right slightly more often and claude-haiku-5-5 flagged more fine videos; the two received frames of different sizes and the standard comes from another platform, so this is indicative only.

## Grader calibration

- No grader is used: decisions are scored by script against answers fixed when the items were written (for real videos and cases, their original labels).

## Limitations and failure cases

- The video ads and training data are synthetic; the further from them, the more the tuned models drop (mmBERT on real cases: 25/46).
  - Recommendation: Before release, build items from the platform's own past decisions and test again; retrain with real data where needed.
- The real short videos come from another platform with a different standard, and the two models received frames of different sizes.
  - Recommendation: Re-test on the target platform's data and standard, with the same input size for every model.
- One run per model per item; some differences fall within the intervals and cannot be separated.
  - Recommendation: Add items and runs for the close comparisons before deciding.

## Versions

- **1.0** (2026-11-18) First card, from the result files in the public policy-model-lab repository.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.

Sources and licences of third-party data, models and code are listed in the [project repository](https://github.com/llia0031-dotcom/policy-model-lab).
