# Evidence-backed resume screening: evaluation card

> Card version 1.2 · Data as of 2026-11-15 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-13 – 2026-11-14 | Liang Liyuan | Node.js, Python, evidence-check 0.2.0, Message Batches API | [Code and report](https://github.com/Jason-d-e/evidence-screening) |

**Problem**: When a model screens resumes, every met / not-met verdict should carry a resume quote; does that make it more accurate, and do verdicts change when name, gender or school change.

**What I did**: I wrote fictional jobs and resumes with answers fixed in advance and compared plain scoring, quotes, and quotes plus the script; after finding that the check discarded correct verdicts I rewired it twice; then tested with trap-laden new resumes, planted errors and an independent second review.

**Results**: 

- Advance decisions changed by a name swap: plain 0/240, with quotes 0/240
- Correct "met" verdicts lost to the check: 70/424 → 10/424 (resume facts split out) → 0/424 (self-check before submitting)
- Second review catches planted misreadings: 80/80

## Summary

Tests whether having the model attach a resume quote to every met / not-met verdict, checked by the evidence-check script, makes screening more accurate and more stable when name, gender, school, career gaps or marital details change. All jobs and resumes are fictional and answers were fixed when the resumes were written. Four rounds: accuracy and stability, a better way to wire the check, messier resumes with traps, plus planted-error tests and an independent second review.

- **Place in the portfolio**: Scenario: judgement
- **Link to the core component**: Uses a frozen copy of the evidence-check 0.2.0 script to check every quote.
- **Models used**: claude-haiku-5-5; from round three on, the Message Batches API.

## Uses

- Give a recruiting team a first pass with grounds: every "met" links to the resume text.
- A pre-launch check: swap names, gender, school and similar details and see whether decisions change.

## Out of scope

- Not an audit of any product, only a small controlled test; no real people's resumes.
- The total score is not for ranking or cut-offs, and keyword matching must not decide on its own.
- Re-test on your own jobs and resumes before going live.

## Evaluation data

### Round 1: accuracy and stability (228 resume versions)

4 jobs and 24 base resumes, each varied by name, gender, school, career gap, marital status and prompt injection: 228 versions. Compared keyword matching, plain scoring, with quotes, and with quotes plus the script check. Hashes of 11 files frozen before the run.

| Field | Value |
|---|---|
| Date | 2026-11-13 |
| Items and answers | 228 versions, 2 runs per arm, 1,368 calls |
| Runs | 2 runs per arm, pooled |
| Model and send mode | claude-haiku-5-5, standard API |
| Frozen before the run | `eval/PREREGISTRATION.md` |

### Round 2: a better way to wire the check (12 new resumes)

The model first separates resume facts and quotes, and the script checks only those; another arm calls the checker itself before submitting. 12 new resumes, 48 versions, frozen before the run.

| Field | Value |
|---|---|
| Date | 2026-11-13 |
| Items and answers | 48 versions, 4 arms × 2 runs, 384 conversations |
| Runs | 2 runs per arm, pooled |
| Model and send mode | claude-haiku-5-5, standard API |
| Frozen before the run | `eval/v2/PREREGISTRATION.md` |

### Round 3: messier resumes with traps (24)

24 messier new resumes with 40 planted traps (used but did not build, below the threshold, already graduated and so on); answers fixed at writing, frozen before the run.

| Field | Value |
|---|---|
| Date | 2026-11-14 |
| Items and answers | 24 resumes, 40 traps, 3 arms × 2 runs |
| Runs | 2 runs per arm, pooled |
| Model and send mode | claude-haiku-5-5, Message Batches API (half price) |
| Frozen before the run | `eval/v3/PREREGISTRATION.md` |

### Planted errors: what the script stops

Errors planted into existing correct answers: changed numbers, added numbers, dropped characters, lines from another resume, and misreadings where the quote is real but the verdict is wrong. No model calls.

| Field | Value |
|---|---|
| Date | 2026-11-14 |
| Items and answers | 409 base answers |
| Runs | Deterministic script, 1 run |
| Model and send mode | No model calls, no cost |
| Frozen before the run | `eval/seeded/PREREGISTRATION.md` |

### Independent second review

Every "met" gets an independent second review: one arm sees the reason, one sees only the quote. Tested on 103 right answers and 40 planted misreadings from round three.

| Field | Value |
|---|---|
| Date | 2026-11-14 |
| Items and answers | 143 items, 2 runs per arm |
| Runs | 2 runs per arm, pooled |
| Model and send mode | claude-haiku-5-5, Message Batches API (half price) |
| Frozen before the run | `eval/verify/PREREGISTRATION.md` |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Round 1: accuracy and stability (228 resume versions)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Requirements right (plain) | 2728/2736 (99.7%, 95% CI 99.4–99.9%) | higher is better | [`evidence-screening/eval/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/results/run-2026-11-13.summary.json) |
| Requirements right (with quotes) | 2735/2736 (100.0%, 95% CI 99.8–100.0%) | higher is better | [`evidence-screening/eval/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/results/run-2026-11-13.summary.json) |
| Requirements right (quotes + script) | 2379/2736 (87.0%, 95% CI 85.6–88.2%) | higher is better | [`evidence-screening/eval/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/results/run-2026-11-13.summary.json) |
| Requirements right (keyword matching) | 2510/2736 (91.7%, 95% CI 90.6–92.7%) | higher is better | [`evidence-screening/eval/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/results/run-2026-11-13.summary.json) |
| Advance decision changed by a name swap (plain) | 0/240 (0.0%, 95% CI 0.0–1.6%) | lower is better | [`evidence-screening/eval/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/results/run-2026-11-13.summary.json) |
| Advance decision changed by a name swap (with quotes) | 0/240 (0.0%, 95% CI 0.0–1.6%) | lower is better | [`evidence-screening/eval/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/results/run-2026-11-13.summary.json) |
| Advance decision changed by a school swap (with quotes) | 0/48 (0.0%, 95% CI 0.0–7.4%) | lower is better | [`evidence-screening/eval/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/results/run-2026-11-13.summary.json) |

Quotes alone cost no accuracy, but wiring the script straight onto "met" verdicts discards correct ones: the model's verdict often restates the job's threshold number, which the resume quote does not contain.

### Round 2: a better way to wire the check (12 new resumes)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Correct "met" lost to the check (quotes + script) | 70/424 (16.5%, 95% CI 13.3–20.3%) | lower is better | [`evidence-screening/eval/v2/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/v2/results/run-2026-11-13.summary.json) |
| Correct "met" lost to the check (resume facts split out + script) | 10/424 (2.4%, 95% CI 1.3–4.3%) | lower is better | [`evidence-screening/eval/v2/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/v2/results/run-2026-11-13.summary.json) |
| Correct "met" lost to the check (self-check + script) | 0/424 (0.0%, 95% CI 0.0–0.9%) | lower is better | [`evidence-screening/eval/v2/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/v2/results/run-2026-11-13.summary.json) |

### Round 3: messier resumes with traps (24)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Traps judged not met (self-check arm) | 80/80 (100.0%, 95% CI 95.4–100.0%) | higher is better | [`evidence-screening/eval/v3/results/run-2026-11-14.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/v3/results/run-2026-11-14.summary.json) |
| Traps judged not met (plain) | 80/80 (100.0%, 95% CI 95.4–100.0%) | higher is better | [`evidence-screening/eval/v3/results/run-2026-11-14.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/v3/results/run-2026-11-14.summary.json) |
| Requirements right (self-check + script) | 286/288 (99.3%, 95% CI 97.5–99.8%) | higher is better | [`evidence-screening/eval/v3/results/run-2026-11-14.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/v3/results/run-2026-11-14.summary.json) |

### Planted errors: what the script stops

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Added numbers stopped | 409/409 (100.0%, 95% CI 99.1–100.0%) | higher is better | [`evidence-screening/eval/seeded/results/seeded-2026-11-14.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/seeded/results/seeded-2026-11-14.json) |
| Lines from another resume stopped | 409/409 (100.0%, 95% CI 99.1–100.0%) | higher is better | [`evidence-screening/eval/seeded/results/seeded-2026-11-14.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/seeded/results/seeded-2026-11-14.json) |
| Misreadings stopped | 0/40 (0.0%, 95% CI 0.0–8.8%) | higher is better | [`evidence-screening/eval/seeded/results/seeded-2026-11-14.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/seeded/results/seeded-2026-11-14.json) |

Quote checking stops fabrication, not misreading; that is why a second review is needed.

### Independent second review

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Misreadings caught (reason visible) | 80/80 (100.0%, 95% CI 95.4–100.0%) | higher is better | [`evidence-screening/eval/verify/results/run-2026-11-14.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/verify/results/run-2026-11-14.summary.json) |
| Misreadings caught (quote only) | 79/80 (98.8%, 95% CI 93.3–99.8%) | higher is better | [`evidence-screening/eval/verify/results/run-2026-11-14.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/verify/results/run-2026-11-14.summary.json) |
| Right answers wrongly flagged (reason visible) | 0/206 (0.0%, 95% CI 0.0–1.8%) | lower is better | [`evidence-screening/eval/verify/results/run-2026-11-14.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/verify/results/run-2026-11-14.summary.json) |

## Grader calibration

- Requirement verdicts are scored by script against answers fixed when the resumes were written; no grader is used.
- The independent second review was checked on known answers first: planted misreadings caught 80/80, false alarms on right answers 0/206.

## Limitations and failure cases

- Resumes are fictional and short and come from the same author as the answers; one model, one setting.
  - Recommendation: Before launch, re-test on anonymised real resumes and the team's own jobs.
- The misreadings were written in, and the review uses the same model as the screening.
  - Recommendation: Use a model from another provider for the review, or review a sample by hand.
- One cell of the answer key is disputed, and it is where round three's only wrong cell sits.
  - Recommendation: Mark disputed answers and report them separately from the main metric.

## Versions

- **1.0** (2026-11-15) First card; the project is not public. A low-effort round still being scored is not included.
- **1.1** (2026-11-15) Added when, team, stack, links and "problem / what I did / results" at the top, the way portfolio case studies open; the evaluation sections are unchanged.
- **1.2** (2026-11-16) The project is public: link to the code and report added; the demo page is not online yet.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.
