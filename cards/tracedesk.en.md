# TraceDesk Lite: evaluation card

> Card version 1.1 · Data as of 2026-11-15 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-03 – 2026-11-10 (Ctrl+V Hackathon) | Liang Liyuan, ZIzi821 | Node.js, React, promptfoo, Claude Haiku 5.5 | [Code](https://github.com/Jason-d-e/tracedesk-lite) · [Demo video](https://youtu.be/eEHcymuLP58) |

**Problem**: An FAQ assistant that answers only from given documents with word-for-word quotes, putting key facts such as deadlines first with their source.

**What I did**: We built an FAQ assistant for readers who find dense text hard: one sentence first, then a checklist, then the evidence; the server checks every quote and deadline; the prompt went from grounded-v2 to v2.4, with v2.2 to v2.4 each compared side by side with a plain prompt on the same cases (v2.2 on the development set, v2.3 and v2.4 on the check set).

**Results**: 

- 20 check cases: plain prompt 17/20, grounded-v2.4 20/20
- Deadlines with a source: plain prompt 17/20, v2.4 20/20

## Summary

An FAQ assistant that answers only from the given documents, designed for readers who find dense text hard: bottom line first, then steps and deadlines, each with a word-for-word quote. Quotes are checked before display and failures are withheld. The demo documents describe a fictional event, DemoClub. The evaluation compares a plain prompt with the grounded prompt series on the same model.

- **Place in the portfolio**: Scenario: grounded Q&A
- **Link to the core component**: evidence-check's matching and number rules were ported from this project's checker.
- **Models used**: claude-haiku-5-5 (effort medium).

## Uses

- Answer common questions from public material such as event or course documents, with key dates first and quoted.

## Out of scope

- Not a medical tool; there is no evidence that it helps readers with attention difficulties (no user testing was done).
- Cannot act for the user; it only answers what the documents state.

## Evaluation data

### Check run 1: plain prompt vs grounded-v2.3 (20 cases)

40 cases split into a development group and a check group of 20 each: answerable, not in the documents, needs clarification, conflicting versions and prompt injection. The check group was run only after the configuration was fixed. No hashes were frozen before the run.

| Field | Value |
|---|---|
| Date | 2026-11-09 |
| Items and answers | 20 check cases |
| Runs | 1 run per arm |
| Model and send mode | claude-haiku-5-5, standard API |

### Check run 2: plain prompt vs grounded-v2.4 (same 20 cases)

v2.4 was written after seeing run 1 and run on the same cases, so this is not a clean held-out result.

| Field | Value |
|---|---|
| Date | 2026-11-09 |
| Items and answers | 20 check cases |
| Runs | 1 run per arm |
| Model and send mode | claude-haiku-5-5, standard API |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Check run 1: plain prompt vs grounded-v2.3 (20 cases)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| All automatic checks passed (plain prompt) | 15/20 (75.0%, 95% CI 53.1–88.8%) | higher is better | `launchpad-tracedesk/eval/results/check-2026-11-09.summary.md` |
| All automatic checks passed (grounded-v2.3) | 19/20 (95.0%, 95% CI 76.4–99.1%) | higher is better | `launchpad-tracedesk/eval/results/check-2026-11-09.summary.md` |

### Check run 2: plain prompt vs grounded-v2.4 (same 20 cases)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| All automatic checks passed (plain prompt) | 17/20 (85.0%, 95% CI 64.0–94.8%) | higher is better | `launchpad-tracedesk/eval/results/check-v2.4-2026-11-09.summary.md` |
| All automatic checks passed (grounded-v2.4) | 20/20 (100.0%, 95% CI 83.9–100.0%) | higher is better | `launchpad-tracedesk/eval/results/check-v2.4-2026-11-09.summary.md` |
| Deadlines with a source (plain prompt) | 17/20 (85.0%, 95% CI 64.0–94.8%) | higher is better | `launchpad-tracedesk/eval/results/check-v2.4-2026-11-09.summary.md` |
| Deadlines with a source (grounded-v2.4) | 20/20 (100.0%, 95% CI 83.9–100.0%) | higher is better | `launchpad-tracedesk/eval/results/check-v2.4-2026-11-09.summary.md` |
| Cost of 20 cases (grounded-v2.4) | US$0.0134 | lower is better | `launchpad-tracedesk/eval/results/check-v2.4-2026-11-09.summary.md` |
| Cost of 20 cases (plain prompt) | US$0.0093 | lower is better | `launchpad-tracedesk/eval/results/check-v2.4-2026-11-09.summary.md` |

## Grader calibration

- Automatic checks are rule-based (checker v2); no grader is used.

## Limitations and failure cases

- Only 40 cases on fictional documents; the second run changed the prompt after seeing the first, so it is not a clean held-out result.
  - Recommendation: For the next version, freeze a new unseen set before comparing.
- The quote check proves the quote exists, not that it supports the answer; automatic checks also raise false alarms, so factual correctness needs a separate item-by-item check.
  - Recommendation: Add a meaning check, as evidence-check does by rereading every passing claim.
- The grounded prompt costs more: US$0.0134 for v2.4 against US$0.0093 for the plain prompt on the same 20 cases.
  - Recommendation: At volume, send shorter document excerpts or cache the unchanging part.

## Versions

- **1.0** (2026-11-15) First card; the live prompt is grounded-v2.4-access. The result files are internal; the public repository has the summary report.
- **1.1** (2026-11-15) Added when, team, stack, links and "problem / what I did / results" at the top, the way portfolio case studies open; the evaluation sections are unchanged.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.

Sources and licences of third-party data, models and code are listed in the [project repository](https://github.com/Jason-d-e/tracedesk-lite).
