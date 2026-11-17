# Grounded Labelling Pipeline: evaluation card

> Card version 1.3 · Data as of 2026-11-17 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-15 – 2026-11-17 | Liang Liyuan | Python, Pandas, DuckDB (SQL), BM25 and local embedding retrieval (Qwen3-Embedding-0.6B), evidence-check, Lark Base (workflows and the AI Agent step), Message Batches API | [Code and report](https://github.com/llia0031-dotcom/grounded-labelling-pipeline) |

**Problem**: How checkable answers become a review workflow a team runs daily: unsure cases go to people, and prompts ship with canary release and rollback.

**What I did**: I turned Grounded Review into a four-step review workflow: the model decides, evidence-check verifies the quotes, ads that fail the check or that the model is unsure of go to a human review queue, and reviewed ads come back as regression items; plus a policy retrieval evaluation, a knowledge-base Q&A that answers only from the policy library, prompt versions, canary and rollback rules, weekly reports computed in SQL and a launch checklist, with judging and review workflows built in a Lark Base.

**Results**: 

- Wrong decisions that went live: v1 17/332 → v2 9/332; sent to review 6/332 → 72/332
- Round one rolled back at 10% under the rules written beforehand; two rules were wrong and have been fixed
- Round two, with the fixed rules on newly written ads, reached 100% without a rollback; in the replay v2 became the production version

## Summary

A review and labelling workflow built around Grounded Review. Each ad is decided by the model with quotes, the quotes are checked by evidence-check, and ads that fail the check, cannot be read or that the model is unsure of go to a human review queue; reviewed ads that differ from the model become new regression items. Prompts are versioned; a new version passes a regression test, then a canary release under rules written beforehand, and rolls back when a rule fires. A knowledge-base Q&A answers only from the policy library and says so when no clause covers the question. Traffic is a replay of Grounded Review's test items, not real users; reviewer decisions in the replay are the items' fixed answers.

- **Place in the portfolio**: Operations
- **Link to the core component**: Every quote goes through the evidence-check script; it imports Grounded Review's code read-only and replays its stored answers.
- **Models used**: Triage and the knowledge-base Q&A use claude-haiku-5-5 (evaluations through the Message Batches API); the AI Agent step in the Lark workflows uses the platform model Seed 1.8, and the chat bot uses claude-haiku-5-5; Chinese clause retrieval uses the policy library's BM25, English uses the local embedding model Qwen3-Embedding-0.6B.

## Uses

- A review team's daily flow: the model decides and quotes, quotes are checked, unsure or failed cases go to a review queue, and reviewed cases become regression items.
- A prompt release flow: regression test, canary under written rules, rollback when one fires, and weekly metrics on wrong decisions that went live, review rate and cost.

## Out of scope

- A replay of test items, not real users. Reviewer decisions are the items' fixed answers.
- The Lark platform model and claude-haiku-5-5 are not compared on one item set; this only shows the workflow runs in Lark.
- Does not replace reviewers: unsure, failed and unreadable ads all go to people.
- The "AI Agent" step in Lark is one model call inside a fixed flow, with no tools or memory.
- The bot's Q&A and usage log have only been tested; there is no real usage.

## Evaluation data

### Regression test: triage prompt v1 vs v2 (332 replayed requests)

Stored answers to Grounded Review's held-out, harder and real-ad items, replayed request by request; answers to the written items were fixed when they were written, and the real ads' answers come from regulators' and courts' rulings. v2's adoption criteria were preregistered.

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

### Canary round two: fixed rules on newly written ads

120 newly written text ads (60 Chinese, 60 English), two runs each, 240 requests; the fixed rollback rules and predictions were preregistered. The canary went to full release in three steps, comparing the canary's cumulative requests with production.

| Field | Value |
|---|---|
| Date | 2026-11-16 |
| Items and answers | 240 requests |
| Runs | Two runs per ad, 1 run per version |
| Model and send mode | claude-haiku-5-5, Message Batches API (half price) |
| Frozen before the run | `docs/PREREGISTRATION-ROUND2.md` |

### The workflow in Lark: the platform AI Agent step (25 Chinese ads)

Ads added to a Lark Base are decided by the platform's AI Agent step and written back; quote checks are added by script, and unsure or failed answers go to the review queue. 25 Chinese text ads with answers fixed at writing; the plan was written before the run.

| Field | Value |
|---|---|
| Date | 2026-11-16 |
| Items and answers | 25 ads, one run each |
| Runs | 1 run |
| Model and send mode | Lark Base AI Agent step (Seed 1.8) |
| Frozen before the run | `docs/LARK-AGENT-PLAN.md` |

### Policy retrieval: right clause in the top three (124 labelled violations)

Grounded Review's 32 policy clauses searched with its BM25; one query per labelled violation, with the right clauses fixed in the labels. Searching with the ad text is compared with searching with the model's answer.

| Field | Value |
|---|---|
| Date | 2026-11-15 |
| Items and answers | 124 labelled violations |
| Runs | Deterministic retrieval, 1 run |
| Model and send mode | No model calls; v1's stored first-run answers |

### Prompt v3 on newly written ads: not adopted

Another 120 newly written text ads, two runs each, 240 requests; some were written as needing a human, the rest have clear answers. Adoption rules and predictions were preregistered; a regression ran on the 332 round-one requests.

| Field | Value |
|---|---|
| Date | 2026-11-17 |
| Items and answers | 240 requests (plus 332 in the regression) |
| Runs | Two runs per ad, 1 run per version |
| Model and send mode | claude-haiku-5-5, Message Batches API (half price) |
| Frozen before the run | `docs/PREREGISTRATION-ROUND3.md` |

### Prompt v4 on another set of newly written ads: not adopted

Another 120 newly written text ads, two runs each, 240 requests; some were written as needing a human. The adoption rules are word for word those of round three, and the predictions were frozen before the run; a regression ran on the 332 round-one requests.

| Field | Value |
|---|---|
| Date | 2026-11-17 |
| Items and answers | 240 requests (plus 332 in the regression) |
| Runs | Two runs per ad, 1 run per version |
| Model and send mode | claude-haiku-5-5, Message Batches API (half price) |
| Frozen before the run | `docs/PREREGISTRATION-ROUND4.md` |

### Policy knowledge-base Q&A: answers only from retrieved clauses (80 questions)

80 questions, half Chinese and half English, some not answerable from the library; answers fixed when the questions were written; two runs each, 160 requests. The plan and predictions were written before the run. A right answer has the right verdict, cites the right clause and passes the quote check; for a question the library cannot answer it must say so and cite nothing.

| Field | Value |
|---|---|
| Date | 2026-11-17 |
| Items and answers | 160 requests |
| Runs | 2 runs per question |
| Model and send mode | claude-haiku-5-5, Message Batches API; BM25 for Chinese, Qwen3-Embedding-0.6B for English, top 5 clauses |
| Frozen before the run | `docs/KBQA-PLAN.md` |

### English clause retrieval on a local embedding model (labels not used to choose it)

Several retrieval methods were compared on the round-one labels to choose one, then checked on the round-two and round-three labels that were not used for the choice; queries are the model's answers, English only. Chinese stays on BM25.

| Field | Value |
|---|---|
| Date | 2026-11-17 |
| Items and answers | 40 round-two and 23 round-three English violation labels |
| Runs | Deterministic retrieval, 1 run |
| Model and send mode | Qwen3-Embedding-0.6B (quantised, fastembed), run locally, no API calls |

### Two Lark workflows: judging and review (60 Chinese ads, two passes)

The first workflow judges, checks every quote, routes the ad and records why; the second writes the review back and records disagreements as regression items. 60 Chinese round-two text ads ran twice: the first pass followed the plan written beforehand, the second ran after seeing the first and fixing the quote check, so it is not preregistered. The script's check and the platform's check are compared side by side.

| Field | Value |
|---|---|
| Date | 2026-11-17 |
| Items and answers | 60 ads |
| Runs | 2 passes (the second after the fix) |
| Model and send mode | Lark Base workflows; the AI Agent step uses the platform model Seed 1.8 on the free allowance |
| Frozen before the run | `docs/LARK-AGENT-PLAN.md` section 8 (first pass) |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Regression test: triage prompt v1 vs v2 (332 replayed requests)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Wrong decisions that went live (v1) | 17/332 (5.1%, 95% CI 3.2–8.0%) | lower is better | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions.json) |
| Wrong decisions that went live (v2) | 9/332 (2.7%, 95% CI 1.4–5.1%) | lower is better | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions.json) |
| Sent to human review (v1) | 6/332 (1.8%, 95% CI 0.8–3.9%) | context only | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions.json) |
| Sent to human review (v2) | 72/332 (21.7%, 95% CI 17.6–26.4%) | context only | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions.json) |
| Decisions right (v1) | 315/332 (94.9%, 95% CI 92.0–96.8%) | higher is better | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions.json) |
| Decisions right (v2) | 312/332 (94.0%, 95% CI 90.9–96.1%) | higher is better | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions.json) |

v2 lets fewer wrong decisions through at the cost of far more human review; all four adoption criteria are met.

### Canary replay under the rules written beforehand (a replay, not real users)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Canary share when a rule fired | 10% | context only | [`grounded-labelling-pipeline/data/canary.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/canary.json) |
| That week, canary: wrong decisions that went live | 1/10 (10.0%, 95% CI 1.8–40.4%) | lower is better | [`grounded-labelling-pipeline/data/canary.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/canary.json) |
| That week, production: wrong decisions that went live | 6/80 (7.5%, 95% CI 3.5–15.4%) | lower is better | [`grounded-labelling-pipeline/data/canary.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/canary.json) |

Three rules fired at the first step, it rolled back, and production stayed at v1. The review found two wrong rules: the review-rate rule contradicted v2's purpose, and rates were compared when the canary had only 10 requests. The fixed rules were written after seeing the results; replayed on the same requests they reach full release, which proves nothing; a canary on new traffic is needed.

### Canary round two: fixed rules on newly written ads

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Canary share reached without a rollback | 100% | context only | [`grounded-labelling-pipeline/data/canary-round2.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/canary-round2.json) |
| Decisions right (v1) | 239/240 (99.6%, 95% CI 97.7–99.9%) | higher is better | [`grounded-labelling-pipeline/data/versions-round2.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-round2.json) |
| Decisions right (v2) | 240/240 (100.0%, 95% CI 98.4–100.0%) | higher is better | [`grounded-labelling-pipeline/data/versions-round2.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-round2.json) |
| Sent to human review (v2) | 36/240 (15.0%, 95% CI 11.0–20.1%) | context only | [`grounded-labelling-pipeline/data/versions-round2.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-round2.json) |
| At full release, canary: wrong decisions that went live (cumulative) | 0/101 (0.0%, 95% CI 0.0–3.7%) | lower is better | [`grounded-labelling-pipeline/data/canary-round2.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/canary-round2.json) |
| At full release, production: wrong decisions that went live (cumulative) | 1/150 (0.7%, 95% CI 0.1–3.7%) | lower is better | [`grounded-labelling-pipeline/data/canary-round2.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/canary-round2.json) |
| v2 cost per request, relative to v1 (predicted at most 1.05×; this prediction did not hold) | 1.0503× | lower is better | [`grounded-labelling-pipeline/data/versions-round2.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-round2.json) |

No rule fired at any step and v2 was promoted to production. Both versions were almost always right on these ads, so this round shows the release process works; the evidence that v2 lets fewer errors through still comes from round one.

### The workflow in Lark: the platform AI Agent step (25 Chinese ads)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Written back to the table | 25/25 (100.0%, 95% CI 86.7–100.0%) | higher is better | [`grounded-labelling-pipeline/data/lark-agent-eval1.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/lark-agent-eval1.json) |
| Decisions right | 25/25 (100.0%, 95% CI 86.7–100.0%) | higher is better | [`grounded-labelling-pipeline/data/lark-agent-eval1.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/lark-agent-eval1.json) |
| Quote check failed, sent to review | 2/25 (8.0%, 95% CI 2.2–25.0%) | context only | [`grounded-labelling-pipeline/data/lark-agent-eval1.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/lark-agent-eval1.json) |
| Platform model said it was unsure | 0/25 (0.0%, 95% CI 0.0–13.3%) | context only | [`grounded-labelling-pipeline/data/lark-agent-eval1.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/lark-agent-eval1.json) |
| Reference: triage model's stored answers saying unsure | 13/50 (26.0%, 95% CI 15.9–39.6%) | context only | [`grounded-labelling-pipeline/data/lark-agent-eval1.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/lark-agent-eval1.json) |

The workflow runs in Lark: every ad was written back and decided right; two answers stitched non-adjacent clause sentences into one quote and the script sent them to review. The platform model never said it was unsure, while the triage model often did in its stored answers, so the review rate must be measured again after a model change.

### Policy retrieval: right clause in the top three (124 labelled violations)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Searching with the ad text: right clause in the top three | 66/124 (53.2%, 95% CI 44.5–61.8%) | higher is better | [`grounded-labelling-pipeline/data/retrieval.csv`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/retrieval.csv) |
| Searching with the model's answer: right clause in the top three | 110/124 (88.7%, 95% CI 81.9–93.2%) | higher is better | [`grounded-labelling-pipeline/data/retrieval.csv`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/retrieval.csv) |

### Prompt v3 on newly written ads: not adopted

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Clear ads sent to human review (v2) | 44/176 (25.0%, 95% CI 19.2–31.9%) | lower is better | [`grounded-labelling-pipeline/data/versions-v3-round3.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-v3-round3.json) |
| Clear ads sent to human review (v3) | 4/176 (2.3%, 95% CI 0.9–5.7%) | lower is better | [`grounded-labelling-pipeline/data/versions-v3-round3.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-v3-round3.json) |
| Ads that need a human, sent to people (v2) | 44/64 (68.8%, 95% CI 56.6–78.8%) | higher is better | [`grounded-labelling-pipeline/data/versions-v3-round3.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-v3-round3.json) |
| Ads that need a human, sent to people (v3) | 19/64 (29.7%, 95% CI 19.9–41.8%) | higher is better | [`grounded-labelling-pipeline/data/versions-v3-round3.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-v3-round3.json) |
| Regression (round one): wrong decisions that went live (v2) | 9/332 (2.7%, 95% CI 1.4–5.1%) | lower is better | [`grounded-labelling-pipeline/data/versions-v3.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-v3.json) |
| Regression (round one): wrong decisions that went live (v3) | 9/332 (2.7%, 95% CI 1.4–5.1%) | lower is better | [`grounded-labelling-pipeline/data/versions-v3.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-v3.json) |

Clear ads got far fewer needless reviews, but ads written as needing a human were also sent to people less often, a drop past the ten-point limit set beforehand, so v3 was not adopted and production stays on v2. Had it been rolled out, no canary rollback rule would have fired: what stopped it was the ads written as needing a human and the adoption standard written beforehand.

### Prompt v4 on another set of newly written ads: not adopted

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Clear ads sent to human review (v2) | 43/176 (24.4%, 95% CI 18.7–31.3%) | lower is better | [`grounded-labelling-pipeline/data/versions-v4-round4.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-v4-round4.json) |
| Clear ads sent to human review (v4) | 11/176 (6.2%, 95% CI 3.5–10.8%) | lower is better | [`grounded-labelling-pipeline/data/versions-v4-round4.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-v4-round4.json) |
| Ads that need a human, sent to people (v2) | 42/64 (65.6%, 95% CI 53.4–76.1%) | higher is better | [`grounded-labelling-pipeline/data/versions-v4-round4.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-v4-round4.json) |
| Ads that need a human, sent to people (v4) | 47/64 (73.4%, 95% CI 61.5–82.7%) | higher is better | [`grounded-labelling-pipeline/data/versions-v4-round4.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-v4-round4.json) |
| Clear ads decided wrongly and gone live (v2) | 0/176 (0.0%, 95% CI 0.0–2.1%) | lower is better | [`grounded-labelling-pipeline/data/versions-v4-round4.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-v4-round4.json) |
| Clear ads decided wrongly and gone live (v4) (both runs of the same trap item) | 2/176 (1.1%, 95% CI 0.3–4.0%) | lower is better | [`grounded-labelling-pipeline/data/versions-v4-round4.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-v4-round4.json) |
| Regression (round one): wrong decisions that went live (v2) | 9/332 (2.7%, 95% CI 1.4–5.1%) | lower is better | [`grounded-labelling-pipeline/data/versions-v4.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-v4.json) |
| Regression (round one): wrong decisions that went live (v4) | 13/332 (3.9%, 95% CI 2.3–6.6%) | lower is better | [`grounded-labelling-pipeline/data/versions-v4.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/versions-v4.json) |

Better than v2 at both ends: fewer needless reviews of clear ads and more of the ads that need a human sent to people. But it is more often sure when wrong: one trap item was decided wrongly and went live in both runs (v2 decided it the same way but said it was unsure and sent it to people), and more wrong decisions got through in the round-one regression, so under the standard written beforehand it was not adopted and production stays on v2. That trap item's answer is debatable; as preregistered, it was not changed.

### Policy knowledge-base Q&A: answers only from retrieved clauses (80 questions)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Answered right | 134/160 (83.8%, 95% CI 77.3–88.7%) | higher is better | [`grounded-labelling-pipeline/data/kbqa-eval.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/kbqa-eval.json) |
| Said "not in the library" when it was not | 44/48 (91.7%, 95% CI 80.4–96.7%) | higher is better | [`grounded-labelling-pipeline/data/kbqa-eval.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/kbqa-eval.json) |
| Quotes that failed the check | 1/160 (0.6%, 95% CI 0.1–3.5%) | lower is better | [`grounded-labelling-pipeline/data/kbqa-eval.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/kbqa-eval.json) |
| Chinese questions: right clause in the top five (BM25) (predicted ninety percent or more; this prediction did not hold; counted per question, since retrieval is the same on both runs) | 23/28 (82.1%, 95% CI 64.4–92.1%) | higher is better | [`grounded-labelling-pipeline/data/retrieval-methods.csv`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/retrieval-methods.csv) |

Most questions were answered right, most questions the library cannot answer got "not in the library", and almost every quote passed the check. Of the predictions written beforehand only the one on Chinese retrieval failed; every "not in the library" on an answerable question came from retrieval missing the clause, not from an invented answer.

### English clause retrieval on a local embedding model (labels not used to choose it)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Round two, English: right clause in the top three (BM25) | 38/40 (95.0%, 95% CI 83.5–98.6%) | higher is better | [`grounded-labelling-pipeline/data/retrieval-methods.csv`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/retrieval-methods.csv) |
| Round two, English: right clause in the top three (embedding) | 39/40 (97.5%, 95% CI 87.1–99.6%) | higher is better | [`grounded-labelling-pipeline/data/retrieval-methods.csv`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/retrieval-methods.csv) |
| Round three, English: right clause in the top three (BM25) | 21/23 (91.3%, 95% CI 73.2–97.6%) | higher is better | [`grounded-labelling-pipeline/data/retrieval-methods.csv`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/retrieval-methods.csv) |
| Round three, English: right clause in the top three (embedding) | 23/23 (100.0%, 95% CI 85.7–100.0%) | higher is better | [`grounded-labelling-pipeline/data/retrieval-methods.csv`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/retrieval-methods.csv) |

On both sets of unused labels the right English clause reached the top three more often; round one was used to choose the method, so its numbers are optimistic and not reported.

### Two Lark workflows: judging and review (60 Chinese ads, two passes)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| First pass: the two quote checks agree | 49/60 (81.7%, 95% CI 70.1–89.4%) | higher is better | [`grounded-labelling-pipeline/data/lark-agent-eval2.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/lark-agent-eval2.json) |
| First pass: wrong decisions not sent to people | 0/60 (0.0%, 95% CI 0.0–6.0%) | lower is better | [`grounded-labelling-pipeline/data/lark-agent-eval2.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/lark-agent-eval2.json) |
| Second pass: the two quote checks agree | 60/60 (100.0%, 95% CI 94.0–100.0%) | higher is better | [`grounded-labelling-pipeline/data/lark-agent-eval3.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/lark-agent-eval3.json) |
| Second pass: the platform's route matches the rules | 60/60 (100.0%, 95% CI 94.0–100.0%) | higher is better | [`grounded-labelling-pipeline/data/lark-agent-eval3.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/lark-agent-eval3.json) |
| Second pass: reviews written back to the ad | 8/8 (100.0%, 95% CI 67.6–100.0%) | higher is better | [`grounded-labelling-pipeline/data/lark-agent-eval3.json`](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/data/lark-agent-eval3.json) |

On the first pass line breaks in the clauses blocked the platform's exact-text search, so the two checks disagreed on some ads, each time sending an extra ad to people and never letting one through; with line breaks handled, the second pass agreed on every check and route, and every review was written back. The second pass came after seeing the first, so it shows the fix works rather than testing a prediction.

## Grader calibration

- No grader is used: decisions are scored against the items' fixed answers, and reviewer decisions in the replay are those answers.

## Limitations and failure cases

- Traffic replays test items rather than real users, and reviewer decisions are the items' fixed answers, not real reviewers.
  - Recommendation: After launch, track wrong decisions let through and review volume per version on real requests, and feed QA samples back as regression items.
- v2 lets fewer wrong decisions through, but human review rose from 6/332 to 72/332, often on clear ads the model called unsure.
  - Recommendation: Version 3 relaxed "unsure" and sent fewer ads that need a human to people; version 4 improved both ends but was more often sure when wrong. The next version has to hold all three: fewer clear ads sent, no fewer ads that need a human, and no wrong decisions let through, again through a regression and new items before a canary.
- Round two reached full release on new traffic, but both versions were almost always right on those ads, so it did not show again that v2 lets fewer errors through; that evidence still comes from round one.
  - Recommendation: Find new ads that v1 misses (longer or vaguer ones) and compare again under the same rules.
- The Lark platform model never said it was unsure (0/25), while the triage model did in 13/50 stored answers; the bot's Q&A has only been tested, with no real usage.
  - Recommendation: After a model change, measure the review rate again before tuning the unsure threshold; test the bot on a batch of questions, then read its real usage log.
- Retrieval for Chinese questions is weak: the right clause was in the top five for only 23/28, and every "not in the library" on an answerable question came from retrieval missing it.
  - Recommendation: Try embedding or hybrid retrieval for Chinese too, checked first on questions not used to choose the method.

## Versions

- **1.0** (2026-11-16) First card, from the result files in the public grounded-labelling-pipeline repository.
- **1.1** (2026-11-16) Added canary round two (new traffic, v2 live), the Lark workflow evaluation and screenshots.
- **1.2** (2026-11-17) Added prompt v3 (not adopted), the knowledge-base Q&A, English retrieval on a local embedding model and the two Lark workflows; Lark screenshots replaced with the new ones.
- **1.3** (2026-11-17) Added prompt v4 (round four on newly written ads, not adopted); the Lark dashboard screenshot was replaced upstream.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.

Sources and licences of third-party data, models and code are listed in the [project repository](https://github.com/llia0031-dotcom/grounded-labelling-pipeline).
