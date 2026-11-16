# Grounded Labelling Pipeline: evaluation card

> Card version 1.0 · Data as of 2026-11-16 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-15 – 2026-11-16 | Liang Liyuan | Python, Pandas, BM25, evidence-check, Lark Base, Message Batches API | [Code and report](https://github.com/Jason-d-e/grounded-labelling-pipeline) |

**Problem**: How checkable answers become a review workflow a team runs daily: unsure cases go to people, and prompts ship with canary release and rollback.

**What I did**: I turned Grounded Review into a four-step review workflow: the model decides, evidence-check verifies the quotes, ads that fail the check or that the model is unsure of go to a human review queue, and reviewed ads come back as regression items; plus a policy retrieval evaluation, prompt versions, canary and rollback rules, weekly reports and a launch checklist, with the review queue syncable to Lark Base.

**Results**: 

- Wrong decisions that went live: v1 17/332 → v2 9/332; sent to review 6/332 → 72/332
- Under the rollback rules written beforehand, the canary rolled back at 10%; two rules were wrong, now reviewed

## Summary

A review and labelling workflow built around Grounded Review. Each ad is decided by the model with quotes, the quotes are checked by evidence-check, and ads that fail the check, cannot be read or that the model is unsure of go to a human review queue; reviewed ads that differ from the model become new regression items. Prompts are versioned; a new version passes a regression test, then a canary release under rules written beforehand, and rolls back when a rule fires. Traffic is a replay of Grounded Review's test items, not real users; reviewer decisions in the replay are the items' fixed answers.

- **Place in the portfolio**: Operations
- **Link to the core component**: Every quote goes through the evidence-check script; it imports Grounded Review's code read-only and replays its stored answers.
- **Models used**: claude-haiku-5-5 through the Message Batches API; retrieval uses the policy library's BM25.

## Uses

- A review team's daily flow: the model decides and quotes, quotes are checked, unsure or failed cases go to a review queue, and reviewed cases become regression items.
- A prompt release flow: regression test, canary under written rules, rollback when one fires, and weekly metrics on wrong decisions that went live, review rate and cost.

## Out of scope

- Not live traffic: requests replay Grounded Review's test items, and reviewer decisions are the items' fixed answers.
- Does not replace reviewers: unsure, failed and unreadable ads all go to people.

## Evaluation data

### Regression test: triage prompt v1 vs v2 (332 replayed requests)

Stored answers to Grounded Review's held-out, harder and real-ad items, replayed request by request; each request's answer was fixed when the item was written. v2's adoption criteria were preregistered.

| Field | Value |
|---|---|
| Date | 2026-11-15 |
| Items and answers | 332 requests, 1 run per version |
| Runs | 1 run per version |
| Model and send mode | claude-haiku-5-5, Message Batches API (half price) |
| Frozen before the run | `docs/PREREGISTRATION.md` |

### Canary replay under the rules written beforehand (a replay, not real users)

The same requests replayed week by week, split between v1 (production) and v2 (canary) by a hash of the request id; rollback rules written beforehand: a higher share of wrong decisions let through, a review rate more than 15 points higher, accuracy more than 5 points lower, or cost more than fifteen percent higher.

| Field | Value |
|---|---|
| Date | 2026-11-15 |
| Items and answers | Four weeks, 332 requests |
| Runs | 1 replay |
| Model and send mode | No model calls; stored answers replayed |
| Frozen before the run | `docs/PREREGISTRATION.md` and `docs/CANARY-POSTMORTEM.md` |

### Policy retrieval: right clause in the top three (124 labelled violations)

Grounded Review's 32 policy clauses searched with its BM25; one query per labelled violation, with the right clauses fixed in the labels. Searching with the ad text is compared with searching with the model's answer.

| Field | Value |
|---|---|
| Date | 2026-11-15 |
| Items and answers | 124 labelled violations |
| Runs | Deterministic retrieval, 1 run |
| Model and send mode | No model calls; v1's stored first-run answers |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Regression test: triage prompt v1 vs v2 (332 replayed requests)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Wrong decisions that went live (v1) | 17/332 (5.1%, 95% CI 3.2–8.0%) | lower is better | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions.json) |
| Wrong decisions that went live (v2) | 9/332 (2.7%, 95% CI 1.4–5.1%) | lower is better | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions.json) |
| Sent to human review (v1) | 6/332 (1.8%, 95% CI 0.8–3.9%) | context only | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions.json) |
| Sent to human review (v2) | 72/332 (21.7%, 95% CI 17.6–26.4%) | context only | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions.json) |
| Decisions right (v1) | 315/332 (94.9%, 95% CI 92.0–96.8%) | higher is better | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions.json) |
| Decisions right (v2) | 312/332 (94.0%, 95% CI 90.9–96.1%) | higher is better | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions.json) |

v2 lets fewer wrong decisions through at the cost of far more human review; all four adoption criteria are met.

### Canary replay under the rules written beforehand (a replay, not real users)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Canary share when a rule fired | 10% | context only | [`grounded-labelling-pipeline/data/canary.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/canary.json) |
| That week, canary: wrong decisions that went live | 1/10 (10.0%, 95% CI 1.8–40.4%) | lower is better | [`grounded-labelling-pipeline/data/canary.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/canary.json) |
| That week, production: wrong decisions that went live | 6/80 (7.5%, 95% CI 3.5–15.4%) | lower is better | [`grounded-labelling-pipeline/data/canary.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/canary.json) |

Three rules fired at the first step, it rolled back, and production stayed at v1. The review found two wrong rules: the review-rate rule contradicted v2's purpose, and rates were compared when the canary had only 10 requests. The fixed rules were written after seeing the results; replayed on the same requests they reach full release, which proves nothing; a canary on new traffic is needed.

### Policy retrieval: right clause in the top three (124 labelled violations)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Searching with the ad text: right clause in the top three | 66/124 (53.2%, 95% CI 44.5–61.8%) | higher is better | [`grounded-labelling-pipeline/data/retrieval.csv`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/retrieval.csv) |
| Searching with the model's answer: right clause in the top three | 110/124 (88.7%, 95% CI 81.9–93.2%) | higher is better | [`grounded-labelling-pipeline/data/retrieval.csv`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/retrieval.csv) |

## Grader calibration

- No grader is used: decisions are scored against the items' fixed answers, and reviewer decisions in the replay are those answers.

## Limitations and failure cases

- Traffic replays test items rather than real users, and reviewer decisions are the items' fixed answers, not real reviewers.
  - Recommendation: After launch, track wrong decisions let through and review volume per version on real requests, and feed QA samples back as regression items.
- v2 lets fewer wrong decisions through, but human review rose from 6/332 to 72/332, often on clear ads the model called unsure.
  - Recommendation: Next, reduce "unsure" on clear ads, again through a regression test before a canary.
- Two rollback rules were wrong; the fixed rules were written after seeing the results, so reaching full release on the same requests is not evidence.
  - Recommendation: Align rollback rules with the change's purpose and adoption criteria, check only hard conditions on small steps, and rerun the canary on newly written items.

## Versions

- **1.0** (2026-11-16) First card, from the result files in the public grounded-labelling-pipeline repository.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.
