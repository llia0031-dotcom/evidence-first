# Evaluation protocol

[中文](eval-protocol.md)

This protocol writes down, in one place, the practice the projects already follow. In one sentence: **write the answers and the plan first, freeze them, then run; re-test every new version, and record how the scores moved and why a version was or was not adopted.**

Evaluation has three layers, run in order; if a layer fails, the next one does not run:

| Layer | When it runs | What it answers | Cost |
|---|---|---|---|
| 1. Rule checks | On every change | Are the output's format, quotes and numbers intact? | None |
| 2. Model grading | Calibrated first, then on every new version | Quality rules cannot check: can the advice be used as is, was a judgement misread? | Small |
| 3. Canary comparison | Last, after the first two pass | With the new version serving part of the requests, did any metric get worse? | Depends on traffic |

---

## 0. Preregistration: the common ground of every evaluation

Before running, write these five things into the project's `PREREGISTRATION.md` and record the file fingerprints (first 12 characters of SHA-256):

1. **Items and answers.** Answers are fixed when the items are written, never added after seeing results. State honestly when the items were written (for example "written after the first round's results").
2. **Scoring script.** Scoring rules are code and are frozen; if scoring changes after the run, the old results no longer count as the same evaluation.
3. **What is tested.** Prompt, code, model id and settings (effort, maximum length, tool list, output format).
4. **Predictions.** Roughly what each arm will score and which will be better; afterwards each one is marked "held" or "did not hold".
5. **Decision rules.** Written before the run: what result means adopt and what means do not adopt, for example "failures on the new problem fall to zero and nothing that was right gets worse".

After the run:

- The files really did not change: recompute the fingerprints and compare them with the preregistration.
- Anything changed after the run goes into a "changes after the run" section at the end of the preregistration; the earlier text is not edited.
- Anything not run is marked **NOT RUN** with the reason, never "omitted" or left blank.
- Frozen results are not re-run just to change how requests are sent (for example moving to the batch API); when comparing with old results, the change of sending method is stated.

What each project does today:

| Project | Preregistration | What was frozen |
|---|---|---|
| evidence-check | `eval/v2/PREREGISTRATION.md`, `eval/v3/`, `eval/v4/` | Items, skill text, checking script, scoring script; skill v0.2 was final before the held-out items were written |
| Grounded Review | `eval/PREREGISTRATION.md` (one section each for the held-out set, v1.1, v1.2, v1.3, the hard set and real ads) | Items, prompt code, scoring script, images; every new version of the advice prompt gets a newly written set |
| Sellpoint Check | `testset/*/PREREGISTRATION.md`, `testset/SUGGEST_PLAN.md`, `testset/ARM_A2_PLAN.md` | Items, judging prompts, each version of the advice prompt |
| Resume screening | `eval/PREREGISTRATION.md`, one each from `eval/v2/` to `eval/verify/` | Resumes, answers, prompts; later rounds check fingerprints and stop if a prompt changed |
| Voice agent evaluation | `eval/PREREGISTRATION.md` (main plan and twelve addenda) | Items, audio list, scoring script, the settings of each improvement |
| Text on product images | `data/freeze.json`, `data/实验/freeze.json` | Tasks and rubric, frozen before generation |
| Grounded Labelling Pipeline | `docs/PREREGISTRATION.md`, one each for rounds two to four, and plans for the knowledge-base Q&A and the Lark workflows | Items, prompts, adoption rules, canary rollback rules and predictions; round four's adoption rules are word for word those of round three |
| Grounded Business Review | `eval/PREREGISTRATION.md` | Items, rules, prompts, model and settings, scoring script; file fingerprints frozen before the run (`eval/frozen.json`) and unchanged afterwards |
| Cairn, TraceDesk | No preregistration file | Items and answers were written before the runs, but no fingerprints were frozen; the cards say so under limitations |

## 1. Rule checks: on every change

Rule checks are deterministic code with no model calls and no cost, so they run on every change and in CI.

**What they check:**

- **Is a quote really the source?** With the evidence-check script: a quote must come word for word from the file it cites, and the dates, times, amounts and quantities in the sentence must appear in the quote. In Sellpoint Check a failed quote is dropped and does not count as evidence; in Grounded Review a failed quote is stopped before the answer is shown.
- **Is the output format right?** Are all fields present, filled in the right place, free of template placeholders? Grounded Review's advice is an example: the rule checks found the corrected caption sometimes landing in the wrong field, which led to v1.2 and v1.3.
- **Is the scoring script itself right?** Scoring scripts carry a few examples with known answers and check themselves before a run (the voice evaluation's `score.py --check`).
- **Offline self-checks.** Each project's `tests/`, with no model calls.

**Rules:**

- If the rule checks fail, the next layer does not run.
- Rules check form, not meaning: a real quote can be used to support the opposite claim. That is left to the second layer.

## 2. Model grading: calibrate first, then run on every version

Some qualities cannot be checked by rules, for example "can the merchant apply this advice as is" or "was this 'met' verdict a misreading of the resume". For these a grader is used: one model call that scores against a rubric, kept separate from the system under test.

**Calibrate first:**

1. Prepare samples with known answers: advice known to be good or bad, planted errors, items whose answers were fixed when written.
2. Run the grader on them and publish its agreement with the known answers in the card's "grader calibration" section.
3. If agreement is too low, revise the rubric and calibrate again until it is high enough, and only then grade the system. The reference target is 90% or more.

What each project does:

| Project | What the grader scores | How it was calibrated |
|---|---|---|
| Sellpoint Check | Whether advice can be applied as is | Scored known good and bad advice first; each item scored twice independently, with the agreement between the two reported |
| Sellpoint Check | A second, independent judgement of each piece of evidence | Compared with the answers on items with known answers first |
| Resume screening | Whether a "met" verdict was misread | 40 planted misreadings mixed with right answers; how many were caught and how many false alarms |
| Grounded Review | Whether a revised version passes | Re-reviewed with the single-prompt arm; no separate calibration, which is listed as a limitation |
| Text on product images | Visual quality | Scored three times independently with agreement reported; not compared with blind ratings by buyers, which is listed as a limitation |

**Run on every version:**

- Every new version runs on newly written, frozen items and sits in the same table as the previous one.
- When the rubric, the grader's model or its prompt changes, calibrate again before use.
- When the grader and the system under test are the same model, that is listed as a limitation; where possible a model from a different vendor serves as a second grader.

## 3. Canary comparison: last

Only after the first two layers pass does a new version serve part of the requests, to see whether real metrics get worse. None of these projects has live traffic, so canary releases are shown only by replaying test items, and every page says "a replay, not real users".

**How:**

1. Versions are separate from releases: the `production` label points at the live version and `staging` at the candidate. A release moves production to the new version; a rollback moves it back (`prompts/labels.json`, `scripts/prompts.py`).
2. Requests are split by a hash of their id, so a request always lands in the same group; every request records which version served it.
3. The release steps are written in the release checklist, for example 10% → 50% → 100%; rollback conditions are checked at every step.
4. Rollback conditions are written before the start; when one fires, it rolls back, with no further debate.
5. The model version is locked together with the prompt; otherwise rolling back the prompt may not restore the old behaviour.

Demonstration: [`prompts/rollout/canary-replay.en.md`](../prompts/rollout/canary-replay.en.md) replays two real comparisons from Grounded Review: v1.3 triggers no rollback at any step and reaches full release; v1.2 trips both the malformed-field and the cost conditions at 50% and rolls back. The Grounded Labelling Pipeline ran several replays the same way: in round one the rules written beforehand rolled it back, and the post-mortem found the rules themselves were wrong; with fixed rules it reached full release on newly written ads. Its versions 3 and 4 failed at the adoption standard and never entered a canary; had they been rolled out, no rollback rule would have stopped them, so the adoption standard and the item design act earlier than a canary can. Checklist template: [`prompts/rollout/上线检查清单模板.md`](../prompts/rollout/上线检查清单模板.md) (in Chinese).

## 4. How numbers are reported

1. **Numbers are never copied by hand.** Every number in the evaluation cards and the prompt registry is computed by script from the projects' result files; each source file's fingerprint is kept in `cards/sources.lock.json`, and `python scripts/build_cards.py --check` fails when a file changes.
2. **Proportions carry a 95% interval and the number of runs.** Wilson intervals; where two runs of the same item are pooled, the card says "the two runs are not independent, so the interval is too narrow".
3. **Define the metric before giving the number; give its direction and date.** Every metric says "higher is better" or "lower is better", and every card says how recent its data is.
4. **A change to the items or the scoring rules is a new evaluation version.** It gets its own table; old and new scores are not subtracted.
5. **Comparisons are complete.** Old and new versions side by side on the same items, with every item that was right before and is wrong now listed.
6. **Limitations are stated as numbers, each with a piece of advice.**
7. **Cost is recorded as spent.** The cheapest current model by default; dozens of non-urgent calls or more go through the batch API (half price); calls in a real-time loop use the normal API.

## 5. References

- Hamel Husain, "Your AI Product Needs Evals" (2024): evaluation in three levels, unit tests, human and model evaluation, and A/B tests.
- Aman Khan, "Beyond vibe checks" (2025): calibrate the grader against an answer set first, then compare with a baseline on the same dataset.
- UK AISI, inspect_evals (MIT): changes that may affect scores bump the version and record before and after scores.
- openai/evals (MIT): test the grader itself on a labelled set.
- Hugging Face model card template (Apache-2.0): the sections of the evaluation cards.
- Langfuse prompt management docs, promptfoo (MIT): release labels, regression checks and CI.
