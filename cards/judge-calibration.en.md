# Judge Calibration: evaluation card

> Card version 1.2 · Data as of 2026-11-18 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-18 | Liang Liyuan | Python, Message Batches API, Cohen's kappa with bootstrap intervals, a quality-check agent with two tools | [Code and report](https://github.com/llia0031-dotcom/judge-calibration) |

**Problem**: A model judge is convenient, but how far can it be trusted, which checks can it take, which belong to a script, and which must stay with people?

**What I did**: I measured one model judge against three standards kept apart: answers fixed when the items were built, regulator and court decisions, and the human ratings that ship with public datasets; then set which checks go to a script, a judge or a person, and built a quality-check agent with an acceptance standard. The plan, frozen files and predictions were written before the runs.

**Results**: 

- Agreed with the answers fixed at item-building time on 702/711; planted errors caught 385/390
- Regulator and court decisions: 33/35 where the ad itself shows it, only 6/11 where outside evidence decides
- Rules, then the judge, unsure items to people: errors missed 2/390 against 7/390 with the judge alone; sent to people 49/711

## Summary

Measures how far one model judge can be trusted, against three standards kept apart: items with answers fixed when they were built (review opinions, resume verdicts, revision advice), regulator and court decisions on real ads, and the human ratings that ship with public datasets (Judge's Verdict, SummEval, WMT MQM Chinese to English). The results sort checks into three kinds: for a script, for the judge, and for people; the judge alone is compared with rules first, then the judge, with unsure items sent to people. Last, a quality-check agent with two tools gets an acceptance standard tested on simulated batches. No human ratings were collected for this project.

- **Place in the portfolio**: Operations
- **Link to the core component**: The items come from the stored answers of Grounded Review, resume screening and Sellpoint Check; the rule-checkable part goes to a script, the way evidence-check does it.
- **Models used**: The judge is claude-haiku-5-5 (effort medium, Message Batches API); claude-sonnet-5-5 serves as a second judge on 120 items.

## Uses

- Deciding which checks an evaluation team can hand to a model judge: calibrate on fixed answers first, then see how far it holds against outside standards.
- Quality checks in production: rules first, then the judge, unsure items to people, with batch acceptance.

## Out of scope

- Does not evaluate models other than the judge, nor show a judge is reliable on other tasks; a new task needs a new calibration.
- Published human ratings have their own definitions and noise; agreeing with them does not make the judge right.

## Evaluation data

### Judge prompts v1 to v4 (development split)

Four judge prompts compared on the development split by mean balanced accuracy over the three item families; the chosen one was frozen before the test split ran.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | Development split |
| Runs | 1 run per item per version |
| Model and send mode | claude-haiku-5-5, effort medium, Message Batches API |
| Frozen before the run | `eval/PREREGISTRATION.md` |

### Items with fixed answers (test split, majority of three judgments)

Review opinions, resume verdicts and revision advice taken from the stored answers of Grounded Review, resume screening and Sellpoint Check, with planted errors in quotes, clauses, format and conclusions; answers fixed when the items were built.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | 711 items |
| Runs | Three judgments per item, majority taken |
| Model and send mode | claude-haiku-5-5, effort medium, Message Batches API; prompt v2 |
| Frozen before the run | `eval/PREREGISTRATION.md` |

### Regulator and court decisions (46 real ads)

30 UK ASA rulings and 16 Chinese regulator or court cases, split by whether the decision can be read from the ad itself.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | 46 ads |
| Runs | Three judgments per ad, majority taken |
| Model and send mode | claude-haiku-5-5, effort medium, Message Batches API |
| Frozen before the run | `eval/PREREGISTRATION.md` |

### Human ratings that ship with public datasets

Judge's Verdict (200 items, three annotators), SummEval (30 news articles with 4 summaries each, 120 per dimension, three experts) and WMT MQM Chinese to English (240 segments). All human ratings come with the datasets.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | 200 Judge's Verdict items; 120 SummEval summaries per dimension; 240 WMT MQM segments |
| Runs | Three judgments per item |
| Model and send mode | claude-haiku-5-5, effort medium, Message Batches API |
| Frozen before the run | `eval/PREREGISTRATION.md` |

### Rules, judge and a review queue (711 items)

The same items with fixed answers, comparing the judge alone (A) with rules first, then one judgment, unsure items sent to a queue (B).

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | 711 items, 390 of them wrong |
| Runs | 1 run per arm |
| Model and send mode | claude-haiku-5-5, effort medium, Message Batches API |
| Frozen before the run | `eval/PREREGISTRATION.md` |

### Does padding or assurance sway the judge? (368 items)

The same items with irrelevant padding or assurance phrases added to the answer, to see whether verdicts change; repeating the judgment measures the noise floor.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | 368 items |
| Runs | 1 run per change |
| Model and send mode | claude-haiku-5-5, effort medium, Message Batches API |
| Frozen before the run | `eval/PREREGISTRATION.md` |

### Quality-check agent and acceptance standard

239 review records (119 wrong, 120 right), comparing a script alone with a quality-check agent using two tools; the acceptance standard is tested on simulated batches of 100 records at several error rates.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | 239 records; simulated batches |
| Runs | 1 run per record |
| Model and send mode | claude-haiku-5-5, effort medium, Message Batches API |
| Frozen before the run | `eval/PREREGISTRATION.md` |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Judge prompts v1 to v4 (development split)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Mean balanced accuracy (v1) | 0.860 | higher is better | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| Mean balanced accuracy (v2) | 0.976 | higher is better | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |

v2 was best and adopted; v3 tied at a higher cost and v4 was stricter, failing some right answers; neither was adopted.

### Items with fixed answers (test split, majority of three judgments)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Agreement with the fixed answers | 702/711 (98.7%, 95% CI 97.6–99.3%) | higher is better | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| Planted errors caught | 385/390 (98.7%, 95% CI 97.0–99.5%) | higher is better | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| Cohen's kappa | 0.974 | higher is better | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |

On items with clear answers the judge is almost always right and catches most planted errors. The 9 disagreements left are all the judge's errors; of the original 12, 3 came from items first built without the product listing and 2 from required statements left out of the answer key when the items were built, and both were corrected and run again (corrections 1 and 2).

### Regulator and court decisions (46 real ads)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Agreement with regulator and court decisions | 39/46 (84.8%, 95% CI 71.8–92.4%) | higher is better | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| Readable from the ad itself | 33/35 (94.3%, 95% CI 81.4–98.4%) | higher is better | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| Turning on outside evidence | 6/11 (54.5%, 95% CI 28.0–78.7%) | higher is better | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |

Where the decision shows in the ad itself the judge is mostly right; where it rests on outside evidence (test reports, licences, actual effects) it is right about half the time.

### Human ratings that ship with public datasets

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Judge's Verdict: exact agreement with each annotator (mean) | 67.3% | higher is better | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| Judge's Verdict: exact agreement between annotators (mean) | 64.3% | context only | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| SummEval fluency: Spearman with experts | 0.408 | higher is better | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| SummEval consistency: Spearman with experts | 0.682 | higher is better | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| WMT MQM Chinese to English: weighted kappa | 0.290 | higher is better | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |

On right-or-wrong items the judge agrees with annotators about as well as they agree with one another; on subjective quality (fluency, coherence) and translation error severity it is far from people.

### Rules, judge and a review queue (711 items)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Judge alone: errors missed | 7/390 (1.8%, 95% CI 0.9–3.7%) | lower is better | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| Rules, judge, review queue: errors missed | 2/390 (0.5%, 95% CI 0.1–1.9%) | lower is better | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| Rules, judge, review queue: sent to people | 49/711 (6.9%, 95% CI 5.3–9.0%) | lower is better | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| Judge alone: cost per 1,000 items | US$0.304 | lower is better | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| Rules, judge, review queue: cost per 1,000 items | US$0.244 | lower is better | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| First judgments marked sure: error rate | 3/662 (0.5%, 95% CI 0.2–1.3%) | lower is better | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| First judgments marked unsure: error rate | 10/49 (20.4%, 95% CI 11.5–33.6%) | context only | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |

Rules first, then the judge, with unsure items to people, misses fewer errors at a lower cost; the items the judge marks unsure are the ones it gets wrong most, which makes them the right ones to send.

### Does padding or assurance sway the judge? (368 items)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Verdicts changed by padding | 0/368 (0.0%, 95% CI 0.0–1.0%) | lower is better | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| Verdicts changed by assurances | 2/368 (0.5%, 95% CI 0.1–2.0%) | lower is better | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |

Padding changed no verdict; assurances changed 2/368, all borderline good answers, and let no wrong one through; the prediction that they would sway the judge did not hold.

### Quality-check agent and acceptance standard

| Metric | Result | Direction | Source file |
|---|---|---|---|
| QC agent: wrong records caught | 119/119 (100.0%, 95% CI 96.9–100.0%) | higher is better | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| QC agent: correct records flagged | 7/120 (5.8%, 95% CI 2.9–11.6%) | lower is better | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| Batches with a two-percent error rate accepted (target: at least nine in ten) | 86.6% | higher is better | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| Batches with a ten-percent error rate accepted (target: at most one in ten) | 9.4% | lower is better | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| Predictions written beforehand that held | 8/12 (66.7%, 95% CI 39.1–86.2%) | context only | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| Total API cost (batch prices) | US$2.63 | lower is better | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |

The agent caught every wrong record with few false flags, but is weak on missing labels: before the answer keys were corrected, six "correct" records in fact lacked a required statement and it flagged one, and its instructions do not ask whether a record is complete. The acceptance standard meets one target of two: too few two-percent batches pass (target: at least nine in ten), while ten-percent batches meet theirs (at most one in ten); one more false flag flips the outcome, so it sits close to both.

## Grader calibration

- The judge itself is what is tested: agreement with each standard is computed by script; "human ratings" means only those shipped with the public datasets, and none were collected for this project.

## Limitations and failure cases

- The items come from the same set of projects' stored answers and the errors are planted; "argued to a wrong conclusion" samples were produced by `eval/gen_flips.py` with the same model, so a bias towards its own writing is not ruled out.
  - Recommendation: Before use, calibrate again on real records with settled outcomes, with error samples from other sources.
- Only 46 regulator and court decisions, 11 of them turning on outside evidence; the intervals are wide.
  - Recommendation: Leave such decisions to people, or gather the outside evidence before handing them to a judge.
- The acceptance standard passed only 86.6% of two-percent batches, short of the at-least-nine-in-ten target set beforehand; ten-percent batches passed 9.4%, meeting theirs. The agent's false flags blur the flag rate, and looking back, no flag-rate threshold alone meets both targets.
  - Recommendation: Count only flags confirmed on review towards the threshold (not yet tested), then test again on simulated batches.

## Versions

- **1.0** (2026-11-18) First card, from the result files in the public judge-calibration repository.
- **1.1** (2026-11-18) Follows the project's correction 1: the revision-advice items were first built without the product listing; with it added the family was judged again, and the affected numbers are recomputed from the corrected result files, with the account of the disagreements rewritten. The prompt-version choice is unchanged.
- **1.2** (2026-11-18) Follows the project's correction 2: a few answer keys had left out a required statement, and with it added the results were recomputed; the agent's false flags, the acceptance rates for both batch levels and the total cost come from the new result files, and the account of the disagreements and the acceptance verdict are rewritten. Agreement with the fixed answers is unchanged.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.

Sources and licences of third-party data, models and code are listed in the [project repository](https://github.com/llia0031-dotcom/judge-calibration).
