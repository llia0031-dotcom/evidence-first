# Grounded Review (ad-review agent): evaluation card

> Card version 1.3 · Data as of 2026-11-16 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-13 – 2026-11-16 | Liang Liyuan | Python, RapidOCR, BM25, evidence-check, Transformers (baselines), Message Batches API | [Code and report](https://github.com/llia0031-dotcom/grounded-review) · [Demo](https://llia0031-dotcom.github.io/grounded-review/en.html) · [Product plan](https://github.com/llia0031-dotcom/grounded-review/blob/main/product/PRD.md) |

**Problem**: An ad decision should name the rule and the exact words that break it, not just approve or reject.

**What I did**: I extracted 32 policy clauses from official sources, wrote a held-out set with traps, built an agent that looks up clauses, quotes them, revises and re-reviews over several turns, and compared it with a single prompt, a banned-word list and open-source moderation models; iterated the advice from v1 to v1.3; then switched to real ads judged by regulators and courts.

**Results**: 

- Held-out decisions right: single prompt 191/192, agent 187/192
- Real ads (UK ASA rulings): 49/60 and 51/60
- Advice fields filled wrongly: 6/36 → 0/36 (v1.3)

## Summary

An agent that reviews ads: it reads the caption and the words in the image, looks up 32 policy clauses, and approves or rejects. Every violation carries a category, the clause, the offending words and the clause text, and every quote must pass the evidence-check script before it counts. When the advertiser asks, it writes a corrected version and re-reviews the advertiser's own revision. The evaluation compares two arms: a single prompt with all material, and a tool-using agent.

- **Place in the portfolio**: Scenario: judgement
- **Link to the core component**: Every ad quote and clause quote goes through the evidence-check script; a quote that is not word for word in its source is stopped before the answer is shown.
- **Models used**: Both arms use claude-haiku-5-5 (effort medium) with one output format. Baselines: a banned-word list, CLIP, SigLIP 2, SafeGuard-VL-RL, Qwen3Guard-Gen-4B and Granite Guardian 3.3 8B (all run locally).

## Uses

- Give a reviewer a first decision with its grounds: which clause and which words, checkable against the source.
- Explain a rejection to the advertiser, suggest a fix and re-review the revision.
- Serve as a worked comparison of a tool-using agent against a single prompt.

## Out of scope

- Not a platform's full policy set: the library is a 32-clause excerpt and leaves out market-specific TikTok rules.
- Not a measurement on live traffic: the held-out and hard sets are written for the project, and the real ads are published descriptions in regulator rulings.
- Does not judge the advertiser's evidence: claims such as "clinically proven" depend on documents the model never sees.

## Evaluation data

### Held-out set v1 (96 written ads)

Image and text ads, half Chinese and half English, including traps that look like violations but comply. Answers were fixed when the items were written; item, code and scorer hashes were frozen before the run.

| Field | Value |
|---|---|
| Date | 2026-11-13 |
| Items and answers | 96 ads, two runs per arm, 192 decisions per arm |
| Runs | 2 runs per arm; proportions pool both runs, which are not independent, so intervals are too narrow |
| Model and send mode | claude-haiku-5-5, standard API |
| Frozen before the run | `eval/PREREGISTRATION.md` (plan, expectations, file hashes) |

### Held-out set v1, image ads: methods without a paid API

The 57 image ads of the held-out set, image only; every baseline runs once locally. SafeGuard-VL-RL was added after the plan was frozen, without a written expectation.

| Field | Value |
|---|---|
| Date | 2026-11-13 |
| Items and answers | 57 images |
| Runs | 1 run per method |
| Model and send mode | Local CPU, no cost |

### Harder set (24 ads)

Long captions, three-frame video screenshots and implied claims; written by the same author after the held-out results were known, answers fixed at writing, frozen before the run.

| Field | Value |
|---|---|
| Date | 2026-11-14 |
| Items and answers | 24 ads, 2 runs per arm |
| Runs | 2 runs per arm |
| Model and send mode | claude-haiku-5-5, Message Batches API (half price) |
| Frozen before the run | `eval/PREREGISTRATION.md`, harder-set section |

### Real ads (English): 30 published UK ASA rulings

Answers come from the regulator: upheld or not upheld. The arms read the ruling's description of the ad, not the ad, and the regulator's code differs from this project's policy library.

| Field | Value |
|---|---|
| Date | 2026-11-14 |
| Items and answers | 30 rulings (7 not upheld), 2 runs per arm |
| Runs | 2 runs per arm |
| Model and send mode | claude-haiku-5-5, Message Batches API (half price) |
| Frozen before the run | `eval/PREREGISTRATION.md`, real-ads section; item text is not published, only the summary |

### Real ads (Chinese): 16 published cases

12 cases penalised by market regulators and 4 found lawful by a regulator or court. Penalised items keep only the words the regulator quoted.

| Field | Value |
|---|---|
| Date | 2026-11-14 |
| Items and answers | 16 cases, 2 runs per arm |
| Runs | 2 runs per arm |
| Model and send mode | claude-haiku-5-5, Message Batches API (half price) |
| Frozen before the run | `eval/PREREGISTRATION.md`, real-ads section |

### Multi-turn mt2: v1 vs v1.1 (12 new ads)

Three turns: review, advice with a corrected version, re-review of the advertiser's own revision. Items were written after the prompt change and frozen before the run.

| Field | Value |
|---|---|
| Date | 2026-11-13 |
| Items and answers | 12 new ads, 2 runs per version, 24 conversations |
| Runs | 2 runs per version |
| Model and send mode | claude-haiku-5-5, standard API |
| Frozen before the run | `eval/PREREGISTRATION.md`, v1.1 section |

### Multi-turn mt3: v1.1 vs v1.2 (12 new ads)

Checks whether the corrected-caption field is filled in the wrong place; v1.2 sends malformed advice back once.

| Field | Value |
|---|---|
| Date | 2026-11-13 |
| Items and answers | 12 new ads, 3 runs per version, 36 conversations |
| Runs | 3 runs per version |
| Model and send mode | claude-haiku-5-5, standard API |
| Frozen before the run | `eval/PREREGISTRATION.md`, v1.2 section |

### Multi-turn mt4: v1.1 vs v1.3 (12 new ads)

v1.3 asks for the corrected caption before the explanation; items were written after v1.3 and frozen before the run. The run stopped once when the account ran out of credit and resumed with the same commands and unchanged files.

| Field | Value |
|---|---|
| Date | 2026-11-14 |
| Items and answers | 12 new ads, 3 runs per version, 36 conversations |
| Runs | 3 runs per version |
| Model and send mode | claude-haiku-5-5, standard API |
| Frozen before the run | `eval/PREREGISTRATION.md`, v1.3 section |

### Memory test: earlier confirmed decisions shown to the agent (24 new ads)

24 fictional text ads (12 Chinese, 12 English), each paired with an earlier decision on the same advertiser: half should follow it, half should not (fixed, qualified, history only, reworded, or a new violation). The memory is read-only; similar earlier decisions are attached to the review request with no extra model call. Ads, earlier decisions and answers were written together and preregistered before the run.

| Field | Value |
|---|---|
| Date | 2026-11-16 |
| Items and answers | 24 ads, 3 runs per arm |
| Runs | 3 runs per arm, pooled; runs are not independent, so intervals are too narrow |
| Model and send mode | claude-haiku-5-5, Message Batches API (half price) |
| Frozen before the run | `eval/PREREGISTRATION.md`, memory section |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Held-out set v1 (96 written ads)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Decisions right (single prompt) | 191/192 (99.5%, 95% CI 97.1–99.9%) | higher is better | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| Decisions right (agent) | 187/192 (97.4%, 95% CI 94.0–98.9%) | higher is better | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| Violations caught (single prompt) | 124/124 (100.0%, 95% CI 97.0–100.0%) | higher is better | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| Violations caught (agent) | 124/124 (100.0%, 95% CI 97.0–100.0%) | higher is better | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| Traps correctly approved (single prompt) | 59/60 (98.3%, 95% CI 91.1–99.7%) | higher is better | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| Traps correctly approved (agent) | 55/60 (91.7%, 95% CI 81.9–96.4%) | higher is better | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| Clauses cited correctly (single prompt) | 129/129 (100.0%, 95% CI 97.1–100.0%) | higher is better | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| Clauses cited correctly (agent) | 129/129 (100.0%, 95% CI 97.1–100.0%) | higher is better | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| Clause quotes passing the check (single prompt) | 224/225 (99.6%, 95% CI 97.5–99.9%) | higher is better | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| Clause quotes passing the check (agent) | 200/200 (100.0%, 95% CI 98.1–100.0%) | higher is better | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| Cost per ad (single prompt) | US$0.0010 | lower is better | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| Cost per ad (agent) | US$0.0023 | lower is better | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |

Both arms are near the ceiling on written items; the difference is that the agent rejected more traps.

### Held-out set v1, image ads: methods without a paid API

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Reference: rejecting everything | 37/57 (64.9%, 95% CI 51.9–76.0%) | context only | [`grounded-review/eval/results/test-2026-11-13.images.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.images.summary.json) |
| SafeGuard-VL-RL decisions right | 49/57 (86.0%, 95% CI 74.7–92.7%) | higher is better | [`grounded-review/eval/results/test-2026-11-13.images.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.images.summary.json) |
| CLIP zero-shot decisions right | 36/57 (63.2%, 95% CI 50.2–74.5%) | higher is better | [`grounded-review/eval/results/test-2026-11-13.images.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.images.summary.json) |
| SigLIP 2 zero-shot decisions right | 35/57 (61.4%, 95% CI 48.4–72.9%) | higher is better | [`grounded-review/eval/results/test-2026-11-13.images.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.images.summary.json) |
| Banned-word list decisions right | 27/57 (47.4%, 95% CI 35.0–60.1%) | higher is better | [`grounded-review/eval/results/test-2026-11-13.images.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.images.summary.json) |
| SafeGuard-VL-RL time per image (median, CPU) | 178.3 s | lower is better | [`grounded-review/eval/results/test-2026-11-13.images.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/test-2026-11-13.images.summary.json) |

None of these methods gives a clause or quote; only SafeGuard-VL-RL beats rejecting everything.

### Harder set (24 ads)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Decisions right (single prompt) | 48/48 (100.0%, 95% CI 92.6–100.0%) | higher is better | [`grounded-review/eval/results/hard-2026-11-14.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/hard-2026-11-14.summary.json) |
| Decisions right (agent) | 48/48 (100.0%, 95% CI 92.6–100.0%) | higher is better | [`grounded-review/eval/results/hard-2026-11-14.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/hard-2026-11-14.summary.json) |

Both arms are fully right: the set shows a ceiling, not a difference.

### Real ads (English): 30 published UK ASA rulings

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Decisions right (single prompt) | 49/60 (81.7%, 95% CI 70.1–89.4%) | higher is better | [`grounded-review/eval/results/real-2026-11-14.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/real-2026-11-14.summary.json) |
| Decisions right (agent) | 51/60 (85.0%, 95% CI 73.9–91.9%) | higher is better | [`grounded-review/eval/results/real-2026-11-14.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/real-2026-11-14.summary.json) |
| Violations caught (single prompt) | 43/46 (93.5%, 95% CI 82.5–97.8%) | higher is better | [`grounded-review/eval/results/real-2026-11-14.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/real-2026-11-14.summary.json) |
| Violations caught (agent) | 46/46 (100.0%, 95% CI 92.3–100.0%) | higher is better | [`grounded-review/eval/results/real-2026-11-14.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/real-2026-11-14.summary.json) |
| Not-upheld ads approved (single prompt) | 6/14 (42.9%, 95% CI 21.4–67.4%) | higher is better | [`grounded-review/eval/results/real-2026-11-14.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/real-2026-11-14.summary.json) |
| Not-upheld ads approved (agent) | 5/14 (35.7%, 95% CI 16.3–61.2%) | higher is better | [`grounded-review/eval/results/real-2026-11-14.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/real-2026-11-14.summary.json) |

Neither arm is perfect, and they stay close; the agent is stricter, catching more violations and rejecting more compliant ads. Most errors come from the regulator's rules differing from the policy library.

### Real ads (Chinese): 16 published cases

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Decisions right (single prompt) | 27/32 (84.4%, 95% CI 68.2–93.1%) | higher is better | [`grounded-review/eval/results/real-zh-2026-11-14.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/real-zh-2026-11-14.summary.json) |
| Decisions right (agent) | 26/32 (81.2%, 95% CI 64.7–91.1%) | higher is better | [`grounded-review/eval/results/real-zh-2026-11-14.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/real-zh-2026-11-14.summary.json) |

### Multi-turn mt2: v1 vs v1.1 (12 new ads)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Corrected version keeps template text (v1) | 3/24 (12.5%, 95% CI 4.3–31.0%) | lower is better | [`grounded-review/eval/results/multiturn-mt2-v1.jsonl`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/multiturn-mt2-v1.jsonl) |
| Corrected version keeps template text (v1.1) | 0/24 (0.0%, 95% CI 0.0–13.8%) | lower is better | [`grounded-review/eval/results/multiturn-mt2-v1.1.jsonl`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/multiturn-mt2-v1.1.jsonl) |

### Multi-turn mt3: v1.1 vs v1.2 (12 new ads)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Fields filled wrongly in the accepted advice (v1.1) | 4/36 (11.1%, 95% CI 4.4–25.3%) | lower is better | [`grounded-review/eval/results/multiturn-mt3-v1.1.jsonl`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/multiturn-mt3-v1.1.jsonl) |
| Fields filled wrongly in the accepted advice (v1.2) | 6/36 (16.7%, 95% CI 7.9–31.9%) | lower is better | [`grounded-review/eval/results/multiturn-mt3-v1.2.jsonl`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/multiturn-mt3-v1.2.jsonl) |

Sending it back does not help: the model repeats the fault, so v1.2 is dropped.

### Multi-turn mt4: v1.1 vs v1.3 (12 new ads)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Advice as submitted, fields filled wrongly (v1.1) | 6/36 (16.7%, 95% CI 7.9–31.9%) | lower is better | [`grounded-review/eval/results/multiturn-mt4-v1.1.jsonl`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/multiturn-mt4-v1.1.jsonl) |
| Advice as submitted, fields filled wrongly (v1.3) | 0/36 (0.0%, 95% CI 0.0–9.6%) | lower is better | [`grounded-review/eval/results/multiturn-mt4-v1.3.jsonl`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/multiturn-mt4-v1.3.jsonl) |
| Brand and price kept (v1.1) | 34/36 (94.4%, 95% CI 81.9–98.5%) | higher is better | [`grounded-review/eval/results/multiturn-mt4-v1.1.jsonl`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/multiturn-mt4-v1.1.jsonl) |
| Brand and price kept (v1.3) | 36/36 (100.0%, 95% CI 90.4–100.0%) | higher is better | [`grounded-review/eval/results/multiturn-mt4-v1.3.jsonl`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/multiturn-mt4-v1.3.jsonl) |
| Cost per three-turn conversation (v1.1) | US$0.0069 (n=36) | lower is better | [`grounded-review/eval/results/multiturn-mt4-v1.1.jsonl`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/multiturn-mt4-v1.1.jsonl) |
| Cost per three-turn conversation (v1.3) | US$0.0068 (n=36) | lower is better | [`grounded-review/eval/results/multiturn-mt4-v1.3.jsonl`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/multiturn-mt4-v1.3.jsonl) |

### Memory test: earlier confirmed decisions shown to the agent (24 new ads)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Decisions right (no memory) | 69/72 (95.8%, 95% CI 88.5–98.6%) | higher is better | [`grounded-review/eval/results/memory-2026-11-16.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/memory-2026-11-16.summary.json) |
| Decisions right (with memory) | 72/72 (100.0%, 95% CI 94.9–100.0%) | higher is better | [`grounded-review/eval/results/memory-2026-11-16.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/memory-2026-11-16.summary.json) |
| Earlier decision copied where it should not apply (with memory) | 0/36 (0.0%, 95% CI 0.0–9.6%) | lower is better | [`grounded-review/eval/results/memory-2026-11-16.report.md`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/memory-2026-11-16.report.md) |
| Cost per review with memory, relative to without | 0.89× | lower is better | [`grounded-review/eval/results/memory-2026-11-16.summary.json`](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/results/memory-2026-11-16.summary.json) |

With memory every decision is right; the errors without memory all come from one ad, so this demonstrates the mechanism rather than a rate. On ads where the earlier decision should not apply, it was never copied.

## Grader calibration

- Decisions, catches and clause citations are scored by script against answers fixed in advance; no grader is used.
- In the multi-turn task, whether a corrected version passes is judged by a separate single-prompt review. That review was not calibrated on its own; the nearest evidence is the same arm's 191/192 on the held-out set.

## Limitations and failure cases

- Written items hit the ceiling: both arms are near-perfect on the held-out set and fully right on the harder set, so they cannot separate the agent from the single prompt.
  - Recommendation: To separate them, use items the author did not write: more real rulings, longer videos, or rules the model has not seen.
- The agent rejects more traps: traps approved 55/60 against 59/60 for the single prompt, and it costs more.
  - Recommendation: Add positive examples or clause notes for compliant ads that look like violations (delivery guarantees, heritage listings, set prices).
- Most errors on real ads come from different rules: alcohol ads the ASA cleared lack the alcohol-content line TikTok requires, and both arms rejected them.
  - Recommendation: Keep the policy library identical to the rules being enforced; split it by market.
- Each multi-turn check uses 12 short text ads and one model; a difference of one or two conversations is noise.
  - Recommendation: Before the next advice prompt ships, test it on image ads and longer captions.
- The open-source moderation model takes minutes per image and gives no clause or quote; SafeGuard-VL-RL takes about 178.3 s per image.
  - Recommendation: Use open-source models as a cheap first filter and pass uncertain ads to the grounded review.
- The memory result rests on a single ad, and the short text ads and the store of earlier decisions were written together.
  - Recommendation: Before launch, test on real past decisions and longer ads; keep the memory read-only, with writes confirmed by a person.

## Versions

- **1.0** (2026-11-15) First card, following the public grounded-review repository: the public release has no Granite Guardian results on real ads, so neither does this card. The two text guardrails are compared only in report tables with no summary data file, so they are not on the card.
- **1.1** (2026-11-15) Added when, team, stack, links and "problem / what I did / results" at the top, the way portfolio case studies open; the evaluation sections are unchanged.
- **1.2** (2026-11-16) Added links to the demo and the product plan, and the memory test.
- **1.3** (2026-11-17) Wording corrected: the real-ad and held-out numbers are stated as decisions (two runs per ad), not as ad counts; the data date is now 2026-11-16, when the memory evaluation was added; Qwen3Guard and Granite Guardian added to the baselines. The two text guardrails' real-ad results are now in the report but have no summary data file, so they are still not on the card. Numbers unchanged.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.

Sources and licences of third-party data, models and code are listed in the [project repository](https://github.com/llia0031-dotcom/grounded-review).
