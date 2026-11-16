# Sellpoint Check: evaluation card

> Card version 1.2 · Data as of 2026-11-15 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-12 – 2026-11-14 | Liang Liyuan | Node.js, DuckDB, Orama, evidence-check, Message Batches API | [Code](https://github.com/Jason-d-e/sellpoint-check) · [Design case study](https://jason-d-e.github.io/sellpoint-check/design/case/en/) · [Clickable prototype](https://jason-d-e.github.io/sellpoint-check/design/prototype/product-en.html) |

**Problem**: Which listing claims do buyer reviews confirm: buyers see only confirmed claims with quotes, and the rest go privately to the merchant with suggested rewrites.

**What I did**: I designed claim checking as a feature the platform and merchants share: buyers see only confirmed claims, the rest go privately to the merchant; compared three evidence-finding methods on accuracy and cost; and iterated the merchant advice six times, testing each version on new frozen items before deciding.

**Results**: 

- 60 claims with known answers: adopted method 60/60, per-review judging 58/60, retrieval first 52/60
- Real data: 2.8% of the calls and 17% of the cost of per-review judging
- Rewrite advice v5 on real data, two independent gradings: 142/151, 143/151

## Summary

The listing's claims are split out, buyer reviews are searched for quotes that support or refute each one, every quote is checked word for word by the evidence-check script, and each claim is labelled supported, refuted, mixed or not mentioned. The buyer page shows only supported claims with their quotes; the rest go to the merchant's private claim check with quotes and a suggested rewrite. The evaluation compares three ways of finding evidence: retrieve then judge (A), judge review by review and aggregate (B, after the PRAISE paper), and all reviews in one call (C, adopted).

- **Place in the portfolio**: Scenario: judgement
- **Link to the core component**: Calls the evidence-check script directly: a quote that fails is dropped and does not count as evidence.
- **Models used**: claude-haiku-5-5 (effort medium); the retrieval arms use local embedding models and Orama hybrid search (from Cairn).

## Uses

- A platform shows only review-confirmed claims, with quotes, on product and store pages.
- A merchant sees privately which claims reviews do not confirm, the buyers' words, and a suggested rewrite.

## Out of scope

- Does not publish refuted or mixed labels, judge violations or trigger penalties.
- Does not judge claims buyers cannot observe, such as ingredient amounts or lab results.
- Skips products with too few reviews; the first version does not touch recommendation ranking.
- The real review data used for research has no commercial licence, and review text is not redistributed.

## Evaluation data

### Constructed set v1 (60 claims, known answers)

12 fictional products and 433 reviews, answers fixed at writing, with trap reviews that look like evidence but are not. Written after the real-data run by the same author; frozen before the run.

| Field | Value |
|---|---|
| Date | 2026-11-12 |
| Items and answers | 60 claims |
| Runs | 1 run per method |
| Model and send mode | claude-haiku-5-5, standard API |
| Frozen before the run | `testset/PREREGISTRATION.md` (item fingerprint, expectations) |

### Real data (30 products, no answer key)

30 beauty products, 538 reviews and 210 claims from the public research dataset Amazon Reviews 2023 (Beauty). There is no answer key, so the comparison covers cost and calls, and every piece of evidence gets a second, independent judgement.

| Field | Value |
|---|---|
| Date | 2026-11-12 |
| Items and answers | 30 products, 210 claims |
| Runs | 1 run per method; A and C were run a second time to measure repeatability |
| Model and send mode | claude-haiku-5-5, standard API |

### Chinese set (50 claims, slang and sarcasm)

10 fictional products and 312 Chinese reviews with slang, sarcasm and traps; answers fixed at writing, frozen before the run.

| Field | Value |
|---|---|
| Date | 2026-11-14 |
| Items and answers | 50 claims |
| Runs | 1 run per method |
| Model and send mode | claude-haiku-5-5, standard API |
| Frozen before the run | `testset/zh/PREREGISTRATION.md` |

### English set v2 (50 claims, long reviews, typos, sarcasm)

10 fictional products and 490 reviews, harder than v1; answers fixed at writing, frozen before the run.

| Field | Value |
|---|---|
| Date | 2026-11-14 |
| Items and answers | 50 claims |
| Runs | 1 run per method |
| Model and send mode | claude-haiku-5-5, Message Batches API (half price) |
| Frozen before the run | `testset/v2/PREREGISTRATION.md` |

### Retrieval upgrade A2: 180 claims A had not seen

A2 switches to Orama hybrid search with sentence windows. It is compared with A and C on four newly written sets (mixed, mixed 2, spoken, spoken 2); plan and decision rule written before the run.

| Field | Value |
|---|---|
| Date | 2026-11-14 |
| Items and answers | 180 claims across four sets |
| Runs | 1 run per method |
| Model and send mode | claude-haiku-5-5, mostly Message Batches API |
| Frozen before the run | `testset/ARM_A2_PLAN.md` |

### Rewrite advice (merchant view): v1 and the adopted v5

40 claims with known answers and 151 unconfirmed claims from the real data. Each suggestion is graded twice, independently, against a rubric (can the merchant apply it as is). Versions 2 to 6 were each tested on a set written for them; see the prompt registry. Only v1 and v5 on the same real data are listed here.

| Field | Value |
|---|---|
| Date | 2026-11-14 |
| Items and answers | 40 test claims; 151 real claims |
| Runs | Generated once per version, graded twice |
| Model and send mode | claude-haiku-5-5; v1–v3 standard API, v4–v6 Message Batches API |
| Frozen before the run | `testset/SUGGEST_PLAN.md` and each set's PREREGISTRATION |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Constructed set v1 (60 claims, known answers)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Correct: all reviews in one call (C, adopted) | 60/60 (100.0%, 95% CI 94.0–100.0%) | higher is better | [`sellpoint-check/results/score-testset.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset.json) |
| Correct: per-review judging (B) | 58/60 (96.7%, 95% CI 88.6–99.1%) | higher is better | [`sellpoint-check/results/score-testset.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset.json) |
| Correct: retrieve then judge (A) | 52/60 (86.7%, 95% CI 75.8–93.1%) | higher is better | [`sellpoint-check/results/score-testset.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset.json) |
| Trap reviews cited as evidence (C) | 0/11 (0.0%, 95% CI 0.0–25.9%) | lower is better | [`sellpoint-check/results/score-testset.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset.json) |

### Real data (30 products, no answer key)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Calls: C as a share of B | 2.8% | lower is better | [`sellpoint-check/results/compare-run.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/compare-run.json) |
| Cost: C as a share of B | 17% | lower is better | [`sellpoint-check/results/compare-run.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/compare-run.json) |
| Second judgement agrees: C's supporting evidence | 184/208 (88.5%, 95% CI 83.4–92.1%) | higher is better | [`sellpoint-check/results/audit-run.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/audit-run.json) |
| Second judgement agrees: C's refuting evidence | 86/94 (91.5%, 95% CI 84.1–95.6%) | higher is better | [`sellpoint-check/results/audit-run.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/audit-run.json) |
| Second judgement agrees: A's supporting evidence | 143/173 (82.7%, 95% CI 76.3–87.6%) | higher is better | [`sellpoint-check/results/audit-run.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/audit-run.json) |
| C labels identical across two runs | 92.9% (n=210) | higher is better | [`sellpoint-check/results/repeat-run.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/repeat-run.json) |
| Reference: the second judgement against known answers | 95.8% (n=72) | higher is better | [`sellpoint-check/results/audit-testset.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/audit-testset.json) |

### Chinese set (50 claims, slang and sarcasm)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Correct (C) | 50/50 (100.0%, 95% CI 92.9–100.0%) | higher is better | [`sellpoint-check/results/score-testset-zh.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-zh.json) |
| Correct (B) | 47/50 (94.0%, 95% CI 83.8–97.9%) | higher is better | [`sellpoint-check/results/score-testset-zh.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-zh.json) |
| Correct (A) | 44/50 (88.0%, 95% CI 76.2–94.4%) | higher is better | [`sellpoint-check/results/score-testset-zh.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-zh.json) |

### English set v2 (50 claims, long reviews, typos, sarcasm)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Correct (C) | 50/50 (100.0%, 95% CI 92.9–100.0%) | higher is better | [`sellpoint-check/results/score-testset-v2.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-v2.json) |
| Correct (B) | 48/50 (96.0%, 95% CI 86.5–98.9%) | higher is better | [`sellpoint-check/results/score-testset-v2.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-v2.json) |
| Correct (A) | 46/50 (92.0%, 95% CI 81.2–96.8%) | higher is better | [`sellpoint-check/results/score-testset-v2.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-v2.json) |

### Retrieval upgrade A2: 180 claims A had not seen

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Correct (A) | 167/180 (92.8%, 95% CI 88.0–95.7%) | higher is better | [`sellpoint-check/results/score-testset-mixed.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-mixed.json)<br>[`sellpoint-check/results/score-testset-mixed2.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-mixed2.json)<br>[`sellpoint-check/results/score-testset-voice.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-voice.json)<br>[`sellpoint-check/results/score-testset-voice2.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-voice2.json) |
| Correct (A2) | 173/180 (96.1%, 95% CI 92.2–98.1%) | higher is better | [`sellpoint-check/results/score-testset-mixed.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-mixed.json)<br>[`sellpoint-check/results/score-testset-mixed2.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-mixed2.json)<br>[`sellpoint-check/results/score-testset-voice.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-voice.json)<br>[`sellpoint-check/results/score-testset-voice2.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-voice2.json) |
| Correct (C) | 177/180 (98.3%, 95% CI 95.2–99.4%) | higher is better | [`sellpoint-check/results/score-testset-mixed.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-mixed.json)<br>[`sellpoint-check/results/score-testset-mixed2.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-mixed2.json)<br>[`sellpoint-check/results/score-testset-voice.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-voice.json)<br>[`sellpoint-check/results/score-testset-voice2.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/score-testset-voice2.json) |

A2 beats A, but C stays adopted; A2 is the fallback when there are too many reviews for one call.

### Rewrite advice (merchant view): v1 and the adopted v5

| Metric | Result | Direction | Source file |
|---|---|---|---|
| v1, test set, first grading: usable as is | 35/40 (87.5%, 95% CI 73.9–94.5%) | higher is better | [`sellpoint-check/results/suggest-testset.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset.json) |
| v1, test set, second grading | 32/40 (80.0%, 95% CI 65.2–89.5%) | higher is better | [`sellpoint-check/results/suggest-testset.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset.json) |
| v1, real data, first grading | 140/151 (92.7%, 95% CI 87.4–95.9%) | higher is better | [`sellpoint-check/results/suggest-run.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-run.json) |
| v5, real data, first grading | 142/151 (94.0%, 95% CI 89.1–96.8%) | higher is better | [`sellpoint-check/results/suggest-run-v5.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-run-v5.json) |
| v5, real data, second grading | 143/151 (94.7%, 95% CI 89.9–97.3%) | higher is better | [`sellpoint-check/results/suggest-run-v5.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-run-v5.json) |
| v3: new copy free of "buyers say" phrasing | 140/151 (92.7%, 95% CI 87.4–95.9%) | higher is better | [`sellpoint-check/results/suggest-run-v3.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-run-v3.json) |
| v5: new copy free of "buyers say" phrasing | 151/151 (100.0%, 95% CI 97.5–100.0%) | higher is better | [`sellpoint-check/results/suggest-run-v5.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-run-v5.json) |
| Grader calibration: first pass on advice of known quality | 31/32 (96.9%, 95% CI 84.3–99.4%) | higher is better | [`sellpoint-check/results/suggest-testset.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset.json) |
| Grader calibration: second pass | 30/32 (93.8%, 95% CI 79.9–98.3%) | higher is better | [`sellpoint-check/results/suggest-testset.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset.json) |
| Chinese set (v2 comparison): v1 usable as is | 30/34 (88.2%, 95% CI 73.4–95.3%) | higher is better | [`sellpoint-check/results/suggest-testset-zh.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset-zh.json) |
| Chinese set (v2 comparison): v2 usable as is | 32/34 (94.1%, 95% CI 80.9–98.4%) | higher is better | [`sellpoint-check/results/suggest-testset-zh-v2.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset-zh-v2.json) |
| Mixed set (v3 comparison): v2 in the right language | 20/40 (50.0%, 95% CI 35.2–64.8%) | higher is better | [`sellpoint-check/results/suggest-testset-mixed-v2.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset-mixed-v2.json) |
| Mixed set (v3 comparison): v3 in the right language | 40/40 (100.0%, 95% CI 91.2–100.0%) | higher is better | [`sellpoint-check/results/suggest-testset-mixed-v3.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset-mixed-v3.json) |
| Mixed set 2 (v4 comparison): v3 usable as is | 38/39 (97.4%, 95% CI 86.8–99.5%) | higher is better | [`sellpoint-check/results/suggest-testset-mixed2-v3.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset-mixed2-v3.json) |
| Mixed set 2 (v4 comparison): v4 usable as is | 36/39 (92.3%, 95% CI 79.7–97.3%) | higher is better | [`sellpoint-check/results/suggest-testset-mixed2-v4.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset-mixed2-v4.json) |
| Spoken set 2 (v6 comparison): v5 usable as is | 29/32 (90.6%, 95% CI 75.8–96.8%) | higher is better | [`sellpoint-check/results/suggest-testset-voice2-v5.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset-voice2-v5.json) |
| Spoken set 2 (v6 comparison): v6 usable as is | 26/32 (81.2%, 95% CI 64.7–91.1%) | higher is better | [`sellpoint-check/results/suggest-testset-voice2-v6.json`](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset-voice2-v6.json) |

## Grader calibration

- Claim labels are scored by script against answers fixed when the items were written; no grader is used.
- Real data has no answer key, so every piece of evidence gets a second, independent judgement. That judgement was first checked on items with known answers: 95.8% agree.
- Rewrite advice is graded twice, independently, by a rubric grader. The grader was first calibrated on advice written in advance with known quality: 31/32 and 30/32 right. The grader and the advice generator use the same model (claude-haiku-5-5), which is a limit.

## Limitations and failure cases

- Test reviews are shorter and cleaner than real ones, and the items were written by the same author after the real-data run.
  - Recommendation: Before launch, repeat the real-data evaluation on the platform's own licensed reviews.
- Real data has no answer key: agreement between the first and second judgements (C: 88% for supporting and 91% for refuting evidence) shows consistency, not correctness.
  - Recommendation: Sample cases for human review at launch and turn the reviewed cases into new test items.
- The advice grader uses the same model as the generator, and agreement between the two gradings is moderate.
  - Recommendation: Use a model from another provider as a second grader, or grade a sample by hand.
- evidence-check requires Chinese quotes of at least four characters, which blocked two complete three-character review titles.
  - Recommendation: Let the checker accept a short quote when it is the whole review.

## Versions

- **1.0** (2026-11-15) First card; the project is not public.
- **1.1** (2026-11-15) Added when, team, stack, links and "problem / what I did / results" at the top, the way portfolio case studies open; the evaluation sections are unchanged.
- **1.2** (2026-11-16) The project is public: links to the code, design case study and clickable prototype added.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.

Sources and licences of third-party data, models and code are listed in the [project repository](https://github.com/Jason-d-e/sellpoint-check).
