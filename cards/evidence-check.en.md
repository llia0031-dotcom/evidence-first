# evidence-check: evaluation card

> Card version 1.1 · Data as of 2026-11-15 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-12 – 2026-11-14 | Liang Liyuan | Python (standard library only), Agent Skill, promptfoo | [Code and report](https://github.com/llia0031-dotcom/evidence-check) |

**Problem**: Answers and drafts written from documents quietly shift dates and numbers or add facts no document states; every factual sentence should carry a word-for-word quote that a script checks.

**What I did**: I took TraceDesk's word-for-word quote and number rules out into a skill and checker anyone can install; found problems in a development run, wrote v0.2, and compared it with a plain prompt on frozen held-out items; then revised the rules twice (0.3.0, 0.4.0) from false alarms in real use and a list of known gaps, writing new items before each change.

**Results**: 

- Held-out: planted errors flagged 60/60, correct facts wrongly flagged 3/150
- Answers with an invented number: plain prompt 4/32 → skill v0.2 0/32
- Script 0.4.0: correct claims passing 0/11 → 11/11, changed numbers still all flagged 13/13

## Summary

An Agent Skill plus a checker script. The skill has the agent attach a word-for-word quote from the documents to every factual sentence; the script checks that the quote is really in the cited file (case, spacing, curly quotes and punctuation forgiven) and that every date, time, amount and count in the sentence also appears in its quotes, across Chinese and English numerals ("下午2点" matches 14:00). The script cannot judge meaning, so the skill also has the agent reread every passing claim. Two modes: answer from documents, and check a draft.

- **Place in the portfolio**: Core component
- **Link to the core component**: This is the core component: Sellpoint Check, Grounded Review and the screening study call its script; the matching and number rules were ported from TraceDesk.
- **Models used**: Evaluated with claude-haiku-5-5 (effort medium); the script itself calls no model and needs only Python 3.9+.

## Uses

- Answer from your own documents with a quote for every fact; claims that fail are fixed or dropped before anyone reads them.
- Check a draft: split it into claims, quote a source for each, run the script and report each problem with the document's words and one suggested fix.
- Serve as the quote-checking tool inside other agents, as Grounded Review and Sellpoint Check do.

## Out of scope

- Opinions and brainstorming, which have no source to check.
- Judging meaning: a real sentence can be cited for its opposite, and the script cannot tell.
- Sums, conversions and computed day counts or ratios: the script flags them on purpose for a person to check.

## Evaluation data

### Held-out evaluation v2 (144 conversations)

Documents for a fictional event: 16 questions (8 Chinese, 8 English) and 8 drafts with 30 planted errors (contradictions, numbers, invented facts, outdated values, computed values) and 75 correct facts. Skill v0.2 was frozen before the items were written; item and scorer hashes were frozen before the run. Three arms, plain prompt, skill v0.1 and skill v0.2, with one model, one set of documents and one output format.

| Field | Value |
|---|---|
| Date | 2026-11-12 |
| Items and answers | 24 items, 2 runs per arm, 3 arms, 144 conversations |
| Runs | 2 runs per arm, pooled; the runs are not independent, so intervals are too narrow |
| Model and send mode | claude-haiku-5-5, standard API |
| Frozen before the run | `eval/v2/PREREGISTRATION.md` (plan, expectations, hashes of 12 files) |

### Script 0.3.0: 36 new claims (script only)

Nine rules changed after false alarms in real use. 36 new claims were written before the change: correct claims should pass, claims with a changed number must be flagged, and claims beyond the script's reach are flagged on purpose. Script only, no model calls.

| Field | Value |
|---|---|
| Date | 2026-11-13 |
| Items and answers | 36 claims |
| Runs | Deterministic script, 1 run |
| Model and send mode | No model calls, no cost |
| Frozen before the run | `eval/v3/PREREGISTRATION.md` |

### Script 0.4.0: 28 new claims (script only)

Six rules added (rounding to at least two significant figures, Chinese ordinals and others). 28 new claims were written before the change; the v1–v3 items were rerun to confirm nothing regressed.

| Field | Value |
|---|---|
| Date | 2026-11-14 |
| Items and answers | 28 claims |
| Runs | Deterministic script, 1 run |
| Model and send mode | No model calls, no cost |
| Frozen before the run | `eval/v4/PREREGISTRATION.md` |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Held-out evaluation v2 (144 conversations)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Planted errors flagged (skill v0.2) | 60/60 (100.0%, 95% CI 94.0–100.0%) | higher is better | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |
| Correct facts wrongly flagged (plain + script) | 12/150 (8.0%, 95% CI 4.6–13.5%) | lower is better | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |
| Correct facts wrongly flagged (skill v0.2) | 3/150 (2.0%, 95% CI 0.7–5.7%) | lower is better | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |
| Answers with an invented number (plain prompt) | 4/32 (12.5%, 95% CI 5.0–28.1%) | lower is better | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |
| Answers with an invented number (skill v0.1) | 2/32 (6.2%, 95% CI 1.7–20.1%) | lower is better | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |
| Answers with an invented number (skill v0.2) | 0/32 (0.0%, 95% CI 0.0–10.7%) | lower is better | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |
| Cost of 48 conversations (plain prompt) | US$0.0520 | lower is better | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |
| Cost of 48 conversations (skill v0.2) | US$0.1603 | lower is better | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |

All three arms flag every planted error; the skill's effect shows in free answers, where it stops invented numbers.

### Script 0.3.0: 36 new claims (script only)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Correct claims passing (0.2.0) | 3/16 (18.8%, 95% CI 6.6–43.0%) | higher is better | [`evidence-check/eval/v3/results/script-only.md`](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/v3/results/script-only.md) |
| Correct claims passing (after the change) | 16/16 (100.0%, 95% CI 80.6–100.0%) | higher is better | [`evidence-check/eval/v3/results/script-only.md`](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/v3/results/script-only.md) |
| Changed numbers flagged (after the change) | 17/17 (100.0%, 95% CI 81.6–100.0%) | higher is better | [`evidence-check/eval/v3/results/script-only.md`](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/v3/results/script-only.md) |

### Script 0.4.0: 28 new claims (script only)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Correct claims passing (0.3.0) | 0/11 (0.0%, 95% CI 0.0–25.9%) | higher is better | [`evidence-check/eval/v4/results/script-only.md`](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/v4/results/script-only.md) |
| Correct claims passing (0.4.0) | 11/11 (100.0%, 95% CI 74.1–100.0%) | higher is better | [`evidence-check/eval/v4/results/script-only.md`](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/v4/results/script-only.md) |
| Changed numbers flagged (0.4.0) | 13/13 (100.0%, 95% CI 77.2–100.0%) | higher is better | [`evidence-check/eval/v4/results/script-only.md`](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/v4/results/script-only.md) |

## Grader calibration

- No grader is used: every score is computed by script against answers fixed when the items were written.

## Limitations and failure cases

- Items and skill come from the same author, on fictional documents; one model, two runs, one day.
  - Recommendation: When adding it to another agent, test again with that setting's own documents and errors.
- On its own the script misses contradictions in meaning: a real quote with the right numbers can be cited for the opposite claim.
  - Recommendation: That is why the skill makes the agent reread every passing claim; add an independent second check for more safety.
- Chinese quotes need at least four characters, so complete shorter phrases are blocked; translated group names and ordinals far from the quote are not yet recognised.
  - Recommendation: These are on the list for the next version, which will again get new items before the change.

## Versions

- **1.0** (2026-11-15) First card: skill v0.2, script 0.4.0.
- **1.1** (2026-11-15) Added when, team, stack, links and "problem / what I did / results" at the top, the way portfolio case studies open; the evaluation sections are unchanged.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.
