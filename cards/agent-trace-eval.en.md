# Agent Trace Eval: evaluation card

> Card version 1.0 · Data as of 2026-11-18 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-18 | Liang Liyuan | Python, Message Batches API, step traces with rule checks, evidence-check, agentevals, Inspect AI logs | [Code and report](https://github.com/llia0031-dotcom/agent-trace-eval) |

**Problem**: Grading only the final answer of a tool-using agent is not enough: what did each step do, which errors do release checks stop, where does a failure start, and does a fix break something else?

**What I did**: I wrote 46 new tasks for three existing tool-using agents, ran each three times and recorded every step; scoring is written as rules over five stages (understanding, planning, tool calls, knowledge and citation, result), with release gates and a failure attribution table on top. After the base run, two fixes were registered with predictions before they ran, then re-tested on every task of their family.

**Results**: 

- Base task success: ad review 53/60, business review 47/54, creator workflow 21/24; all three trials 80%, 72%, 88%
- The gates guard form, not judgement: of 17 failed base trials, the gates caught 1 and let 16 through
- Skills against none: creator workflow success 21/24 against 8/24 (sign test p = 0.031)
- Registered fixes: advice tool called in a review turn 36/60 → 0/60; store closures located at the merchant 3/6 → 6/6, and the regression run caught another task getting worse

## Summary

Evaluates what a tool-using agent does at every step, not only its final answer. Three existing agents run unchanged (Grounded Review, Grounded Business Review, Creator Skills) on 46 new tasks: 20 ad review, 18 business review and 8 creator workflow, in three tiers from one-step tasks to multi-turn ones that need judgement, three trials each. Answers were fixed when the tasks were written, and tasks, answers, rubric code and configurations were hashed before the runs. Scoring is rule checks over the recorded steps in five stages; task success uses the result checks only, and process checks explain how the agent got there. Release gates (quote checks, number checks, the skills' own checking scripts) hold results for a person; the attribution table records where each failure starts, why, and how to fix it.

- **Place in the portfolio**: Operations
- **Link to the core component**: Quotes and numbers are checked with evidence-check's script; the agents are those of Grounded Review, Grounded Business Review and Creator Skills, run without code changes, and this adds what their own evaluations did not measure: the steps and the gates.
- **Models used**: claude-haiku-5-5 (effort medium) for all three agents and the judge; the first base trial used the standard API to measure latency, the other trials, fixes and comparisons the Message Batches API.

## Uses

- Pre-release evaluation of a tool-using agent: see at which step it goes wrong, which errors the gates stop and which need a person.
- Before changing a prompt or rule: write the predictions down, then re-test the whole family to confirm the fix breaks nothing else.

## Out of scope

- Does not show how the three agents do on real work; the tasks are synthetic or fictional, written for this bench.
- The fixes were checked only on the tasks they were written for; new tasks are needed to show they generalise.

## Evaluation data

### Base: three agents run unchanged

Ad review (Chinese and English ads, including three-turn reviews: review, advice, review of the next version), business review (a synthetic local-services platform with planted causes, quiet weeks, holidays and scoped requests) and a creator workflow (trend topics, a shot list and a subtitle check in one conversation). Answers fixed when the tasks were written, with each agent project's own validators and scorers.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | 46 tasks: 20 ad review, 18 business review, 8 creator workflow |
| Runs | 3 trials per task |
| Model and send mode | claude-haiku-5-5, effort medium; trial 1 standard API, trials 2 and 3 Message Batches API |
| Frozen before the run | `eval/PREREGISTRATION.md`, `eval/frozen.json` |

### Release gates and failure attribution (base)

The gates are the checks a deployment runs before release: quote checks, number checks and the skills' own checking scripts; what they hold goes to a person. For each failed trial the earliest failing check gives the stage, and the cause comes from a rule per check or a note written after reading the trace.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | The failed trials among 138 base trials |
| Runs | 3 trials per task |
| Model and send mode | claude-haiku-5-5, effort medium |
| Frozen before the run | `eval/PREREGISTRATION.md` |

### Skills against no skills (creator workflow)

The same 8 creator-workflow tasks, once with the three creator skills and their checking tools loaded and once without; paired by task, exact sign test.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | 8 tasks |
| Runs | 3 trials per task |
| Model and send mode | claude-haiku-5-5, effort medium, Message Batches API |
| Frozen before the run | `eval/PREREGISTRATION.md` |

### Two registered fixes and the regression run

After the base run, each fix adds two rules to the agent's instructions, with predictions and an adoption rule written before it ran. Ad review: one violation per phrase, under the most specific category; finish each request with the one tool it asks for. Business review: locate a store-closure cause at the merchant; name only slices the monitor flagged as causes. Each re-ran its whole family three times: the regression test.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | 20 ad review tasks; 18 business review tasks |
| Runs | 3 trials per task |
| Model and send mode | claude-haiku-5-5, effort medium, Message Batches API |
| Frozen before the run | `eval/PREREGISTRATION.md` (change log, 2026-11-18 20:48), `eval/frozen-changes.json` |

### Judge calibration and total spend

The 7 criteria rules cannot check are judged twice per answer against a written guide, first on 12 calibration answers with written verdicts, then on the base answers. Judged items do not affect task success.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | 12 calibration answers; 88 base answers |
| Runs | 2 judgements per answer |
| Model and send mode | claude-haiku-5-5, effort medium |
| Frozen before the run | `eval/PREREGISTRATION.md` |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Base: three agents run unchanged

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Ad review: task success | 53/60 (88.3%, 95% CI 77.8–94.2%) | higher is better | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| Business review: task success | 47/54 (87.0%, 95% CI 75.6–93.6%) | higher is better | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| Creator workflow: task success | 21/24 (87.5%, 95% CI 69.0–95.7%) | higher is better | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| Ad review: all three trials succeed (pass^3) | 80% | higher is better | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| Business review: all three trials succeed (pass^3) | 72% | higher is better | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| Creator workflow: all three trials succeed (pass^3) | 88% | higher is better | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| Ad review: tool calls correct | 351/387 (90.7%, 95% CI 87.4–93.2%) | higher is better | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| Ad review: advice tool called in a review turn (refused by the harness; it never failed a task) | 36/60 (60.0%, 95% CI 47.4–71.4%) | lower is better | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| Business review: held by the number check for a person | 9/54 (16.7%, 95% CI 9.0–28.7%) | context only | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |

The three families succeed at similar rates, and most failures start at the result: one phrase under two categories, a store closure located too coarsely, an ordinary specification rejected. Process faults are common even in successful trials: most ad review trials also called the advice tool in a review turn.

### Release gates and failure attribution (base)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Failed base trials | 17 | lower is better | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| Failures the gates caught | 1/17 (5.9%, 95% CI 1.0–27.0%) | higher is better | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| Failures the gates let through | 16/17 (94.1%, 95% CI 73.0–99.0%) | lower is better | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| Failures caused by the task or its answer key | 5/17 (29.4%, 95% CI 13.3–53.1%) | context only | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |

The gates caught almost nothing: every failed ad review cites real words and real clauses, and the reading is what is wrong; the business number check held more correct reports than failures, adding review load. Some failures are problems of the tasks or answer keys; they stay in the scores, with the reason stated.

### Skills against no skills (creator workflow)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Without skills: task success | 8/24 (33.3%, 95% CI 18.0–53.3%) | higher is better | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| Exact sign test over tasks, p | 0.031 | context only | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| Cost per trial with the skills, at the standard price, relative to without | 2.8× | context only | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |

Without the skills, shots are sized by feel, captions restore the script over what was actually said, and promotional cards were made on a fatal fire while citing real, current pages, so the source check passed them: a policy failure no form check can catch.

### Two registered fixes and the regression run

| Metric | Result | Direction | Source file |
|---|---|---|---|
| After the fix: advice tool called in a review turn | 0/60 (0.0%, 95% CI 0.0–6.0%) | lower is better | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| After the fix: change in output tokens per trial | -15% | lower is better | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| Ad review after the fix: task success | 54/60 (90.0%, 95% CI 79.9–95.3%) | higher is better | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| Ad review after the fix: tool calls correct | 345/345 (100.0%, 95% CI 98.9–100.0%) | higher is better | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| Before the fix: store closures located at the merchant | 3/6 (50.0%, 95% CI 18.8–81.2%) | higher is better | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| After the fix: store closures located at the merchant | 6/6 (100.0%, 95% CI 61.0–100.0%) | higher is better | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| Business review after the fix: task success | 48/54 (88.9%, 95% CI 77.8–94.8%) | higher is better | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| Business review after the fix: all three trials succeed (pass^3) | 83% | higher is better | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| Business review after the fix: tasks that got worse | 2 | lower is better | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |

Both fixes were adopted by the registered rule. Every ad prediction held; the gain is in the process, with no measured change in task success. The business fix located every store closure, but the flagged-slice rule did not hold, and a refund task was narrowed to one chain, finer than the event: a rule written from a failure has side effects, so the next step moves both rules from the prompt into code.

### Judge calibration and total spend

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Calibration: agreement with the written verdicts (after the correction) | 53/56 (94.6%, 95% CI 85.4–98.2%) | higher is better | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| Calibration: agreement with the written verdicts (as written) | 51/56 (91.1%, 95% CI 80.7–96.1%) | context only | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| Base answers: the two passes agree | 182/194 (93.8%, 95% CI 89.5–96.4%) | higher is better | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| Total spend (all runs, the judge and the smoke test) | US$1.48 | lower is better | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |

The two passes mostly agree. The judged items add two things rules cannot see: corrected ads that add new selling words needing proof pass the rule checks; and "keep watching" in quiet weeks fails, a gap in the guide rather than in the agent.

## Grader calibration

- The 7 criteria rules cannot check (whether advice is clear, follows from a stated cause, suits the account, and so on) are judged twice against a written guide; the judge is claude-haiku-5-5, the same model as the three agents under test.
- Calibration: agreement with 12 answers' written verdicts 53/56 (51/56 as written; one written verdict was itself wrong and was corrected); on base the two passes agree on 182/194. Judged items do not affect task success; no human ratings were collected.

## Limitations and failure cases

- Three trials per task over tasks written for this bench, so intervals are wide: business review task success 47/54 (87.0%, 95% CI 75.6–93.6%); per-task comparisons rest on three trials each.
  - Recommendation: Confirm the important findings with more trials and new tasks.
- The tasks are synthetic or fictional and come from the same project that runs them; two have a problem in the task or the key, kept in the scores.
  - Recommendation: Fix and re-run those two tasks, and build another set from real work with settled outcomes.
- The judge is the model under evaluation, and its guide has a gap on quiet weeks; judged items do not affect task success, and no human ratings were collected.
  - Recommendation: Close the gap in the guide and add a second judge from a different model.
- The fixes were checked only on the tasks they were written for; latency comes from the base standard-API trials only, one per task.
  - Recommendation: Test the fixes on new tasks, and re-test the refund tasks after the rules move into code.

## Versions

- **1.0** (2026-11-18) First card, from the result files in the public agent-trace-eval repository.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.

Sources and licences of third-party data, models and code are listed in the [project repository](https://github.com/llia0031-dotcom/agent-trace-eval).
