# Prompt registry

Every version of every prompt asset records its id, what changed, its real score on a frozen test set at the time, whether it was adopted, and why. Scores are computed by `scripts/prompts.py build` from the projects' result files, never typed in. An arrow compares old and new versions on the same items; scores from different test sets are not compared.

## Release labels

`production` is the version a project has adopted and uses from then on; `staging` is the candidate under test. A release moves production to the new version; a rollback moves it back (`python scripts/prompts.py rollback <asset>`). Labels start on 2026-11-15; earlier entries are back-filled from each project's records. None of these projects has live traffic; rollout is shown only by replaying test items, see [rollout/](rollout/).

| Asset | production | staging | Note |
|---|---|---|---|
| `evidence-check/skill` | v0.2 | v0.2 | The public repository and plugin ship v0.2. |
| `grounded-review/advice` | v1.3 | v1.3 | The project decided that new runs and demos use v1.3; the code default is still v1, and the demo shows stored v1 conversations. There is no live traffic. |
| `sellpoint-check/advice` | v5 | v5 | The project uses version 5. There is no live traffic. |
| `tracedesk/answer` | grounded-v2.4-access | grounded-v2.4-access | The demo and the public repository default to grounded-v2.4-access. |
| `cairn/answer` | cairn-monash-v2 | cairn-monash-v2 | The live demo uses cairn-monash-v2. |
| `evidence-pipeline/triage` | v2 | v2 | No live traffic; the canary is a replay of test items. |
| `evidence-pipeline/kb-qa` | v1 | v1 | No real usage; the evaluation is a replay of a question set, and the bot has only been asked a few test questions. |

## evidence-check: skill instructions (SKILL.md)

The skill instructions loaded into an agent: a word-for-word quote for every fact, run the checker, reread every passing claim. The checker script has its own versions (0.2.0 → 0.4.0); see the evaluation card.

- Location: `skills/evidence-check/SKILL.md` (evidence-check)
- Model lock: claude-haiku-5-5, effort medium in the evaluations

| Version | Date | Change | Score at the time | Decision | Why |
|---|---|---|---|---|---|
| **v0.1** | 2026-11-12 | First version of the skill.<br>`eval/v2/skill-versions/SKILL-v0.1.md` (fingerprint 9aec983a7522) | *Held-out v2: 16 questions and 8 drafts, 2 runs per arm*<br>Answers with an invented number: 2/32<br>Correct facts wrongly flagged: 2/150 | superseded | Development run v1 showed three problems: both false alarms were correct Chinese translations of English sources; the one missed error was a miscalculated duration; and it cost almost twice the plain prompt.<br>Source: [evidence-check/eval/EVALUATION.md](https://github.com/Jason-d-e/evidence-check/blob/main/eval/EVALUATION.md) |
| **v0.2** | 2026-11-12 | Paraphrase, summary and translation count as supported; only numbers the documents give; about a third shorter. Frozen before the held-out items were written.<br>`skills/evidence-check/SKILL.md` (fingerprint 8dcadfc8cd45, current) | *Held-out v2: 16 questions and 8 drafts, 2 runs per arm*<br>Answers with an invented number (v0.1 → v0.2): 2/32 → 0/32<br>Correct facts wrongly flagged (v0.2): 3/150<br>Cost of 48 conversations (v0.2): US$0.1603 | adopted | No invented numbers on the held-out set and slightly lower cost; one more false alarm, within noise.<br>Source: [evidence-check/eval/EVALUATION.md](https://github.com/Jason-d-e/evidence-check/blob/main/eval/EVALUATION.md) |

Label history: 2026-11-12 production ·→v0.1; 2026-11-12 staging ·→v0.2; 2026-11-12 production v0.1→v0.2

## Grounded Review: revision advice

The prompt, rules and output format the agent uses when the advertiser asks what is wrong and how to fix it. The review prompt itself is the same in every version.

- Location: `agent/review_agent.py` (grounded-review)
- Model lock: claude-haiku-5-5, effort medium

| Version | Date | Change | Score at the time | Decision | Why |
|---|---|---|---|---|---|
| **v1** | 2026-11-13 | First version: review, advice with a corrected version, re-review of the advertiser's version.<br>`SYSTEM`, `ADVICE_SCHEMA` and the advice question (`agent/review_agent.py`) | no stored evaluation | superseded | In multi-turn runs the corrected version sometimes kept template placeholders for a person to fill in.<br>Source: [grounded-review/eval/EVALUATION.md](https://github.com/Jason-d-e/grounded-review/blob/main/eval/EVALUATION.md) |
| **v1.1** | 2026-11-13 | The corrected version must be ready to publish with no blanks; missing information goes into the answer for the advertiser; a tool checks the corrected version.<br>v1 plus `ADVICE_RULES_V11` and the `check_revision` tool | *mt2: 12 new ads, 2 runs per version*<br>Placeholders left (v1 → v1.1): 3/24 → 0/24 | superseded | On 12 ads written for it, placeholders fell from 3/24 to 0/24; later the corrected caption was found to land in the wrong field at times.<br>Source: [grounded-review/eval/EVALUATION.md](https://github.com/Jason-d-e/grounded-review/blob/main/eval/EVALUATION.md) |
| **v1.2** | 2026-11-13 | Checks the advice fields and sends malformed advice back to the model once.<br>v1.1 plus sending malformed advice back once | *mt3: 12 new ads, 3 runs per version*<br>Fields wrong in the accepted advice (v1.1 → v1.2): 4/36 → 6/36 | not adopted | Sending it back does not help: the model repeats the fault; fields wrong 4/36 for v1.1 and 6/36 for v1.2, at a higher cost.<br>Source: [grounded-review/eval/EVALUATION.md](https://github.com/Jason-d-e/grounded-review/blob/main/eval/EVALUATION.md) |
| **v1.3** | 2026-11-14 | The output format asks for the corrected caption before the explanation; leaked markup is cleaned in code with no extra call.<br>`ADVICE_SCHEMA_V13` (corrected caption before the explanation) and `common.clean_advice` | *mt4: 12 new ads, 3 runs per version*<br>Advice fields filled wrongly (v1.1 → v1.3): 6/36 → 0/36<br>Brand and price kept (v1.1 → v1.3): 34/36 → 36/36<br>Cost per three-turn conversation (v1.1 → v1.3): US$0.0069 → US$0.0068 | adopted | On another 12 newly written ads, advice fields filled wrongly fell from 6/36 to 0/36; brand and price kept 36/36; cost unchanged.<br>Source: [grounded-review/eval/EVALUATION.md](https://github.com/Jason-d-e/grounded-review/blob/main/eval/EVALUATION.md) |

Label history: 2026-11-13 production ·→v1; 2026-11-13 staging ·→v1.1; 2026-11-13 production v1→v1.1; 2026-11-13 staging v1.1→v1.2; 2026-11-13 staging v1.2→v1.3; 2026-11-14 production v1.1→v1.3

## Sellpoint Check: rewrite advice for merchants

The suggested rewrite shown in the merchant's private view for claims reviews do not confirm. Each version is first compared with the previous one on a set written for it and frozen before the run, then checked on the same real data.

- Location: `pipeline/lib/suggest_prompts.mjs, suggest_v2.mjs … suggest_v6.mjs` (sellpoint-check)
- Model lock: claude-haiku-5-5, effort medium

| Version | Date | Change | Score at the time | Decision | Why |
|---|---|---|---|---|---|
| **v1** | 2026-11-13 | First version: for each unconfirmed claim, the reason, the buyers' words and a rewrite the merchant can apply as is.<br>`pipeline/lib/suggest_prompts.mjs` (fingerprint b5b2a58fdbde) | *40 claims with known answers; 151 real claims*<br>Test set usable as is (two gradings): 35/40 and 32/40<br>Real data: no refuted wording left: 136/151 | superseded | On real data some rewrites still kept wording the reviews refute.<br>Source: [sellpoint-check/results/suggest-run.md](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-run.md) |
| **v2** | 2026-11-14 | Three new rules plus a code check that sends back rewrites still containing refuted wording.<br>`pipeline/lib/suggest_v2.mjs` (fingerprint 279e9280f000) | *Chinese set, 34 claims (v1 vs v2); 151 real claims*<br>Chinese set usable as is, first grading (v1 → v2): 30/34 → 32/34<br>Real data: no refuted wording left (v1 → v2): 136/151 → 151/151<br>Advice in Chinese for Chinese listings (v2): 10/34 | adopted (later replaced by v3) | Refuted wording cleared and better on the new Chinese set, but most advice for Chinese listings was still in English.<br>Source: [sellpoint-check/results/suggest-testset-zh-v2.md](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset-zh-v2.md) |
| **v3** | 2026-11-14 | Mixed claims keep every confirmed part with its condition; the listing language is set in code; the send-back check is wider.<br>`pipeline/lib/suggest_v3.mjs` (fingerprint c346201974cd) | *Mixed set, 40 claims (v2 vs v3); 151 real claims*<br>Advice in the listing's language (v2 → v3): 20/40 → 40/40<br>Usable as is, first grading (v2 → v3): 37/40 → 37/40<br>Real data usable as is, first grading (v3): 143/151 | adopted (later replaced by v5) | Chinese merchants must get Chinese advice: on the new mixed set, advice in the right language went from half under v2 to all of it, with usable advice about level.<br>Source: [sellpoint-check/results/suggest-testset-mixed-v3.md](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset-mixed-v3.md) |
| **v4** | 2026-11-14 | A new field listing refuted words, four rules and more send-backs.<br>`pipeline/lib/suggest_v4.mjs` (fingerprint 7b0d5b8debfe) | *Mixed set 2, 39 claims (v3 vs v4); 151 real claims*<br>Usable as is, first grading (v3 → v4): 38/39 → 36/39<br>Real data usable as is, first grading (v4): 136/151 | not adopted | Asked to list refuted words first, the model tends to delete them wholesale; it removes too much and the score drops.<br>Source: [sellpoint-check/results/suggest-testset-mixed2-v4.md](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset-mixed2-v4.md) |
| **v5** | 2026-11-14 | The v3 prompt unchanged, plus a code check that sends back new copy containing "buyers say" phrasing.<br>`pipeline/lib/suggest_v5.mjs` (fingerprint 4f50d20090bd) | *Spoken set, 31 claims (v3 vs v5); 151 real claims*<br>Usable as is, first grading (v3 → v5): 31/31 → 29/31<br>Real data: no "buyers say" phrasing (v3 → v5): 140/151 → 151/151<br>Real data usable as is, first grading (v5): 142/151 | adopted | On real data, copy free of "buyers say" phrasing rose from 140/151 to 151/151, with usable advice level.<br>Source: [sellpoint-check/results/suggest-testset-voice-v5.md](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset-voice-v5.md) |
| **v6** | 2026-11-14 | A wider synonym list for "buyers say" and a "keep the limits" note on retries.<br>`pipeline/lib/suggest_v6.mjs` (fingerprint ce17fbc23ce9) | *Spoken set 2, 32 claims (v5 vs v6); 151 real claims*<br>Usable as is, first grading (v5 → v6): 29/32 → 26/32<br>Real data usable as is, first grading (v6): 139/151 | not adopted | "Keep the limits" made the model keep refuted specifics as if they were limits, and the score dropped; the advice stays at v5.<br>Source: [sellpoint-check/results/suggest-testset-voice2-v6.md](https://github.com/Jason-d-e/sellpoint-check/blob/main/results/suggest-testset-voice2-v6.md) |

Label history: 2026-11-13 production ·→v1; 2026-11-14 production v1→v2; 2026-11-14 production v2→v3; 2026-11-14 staging v3→v4; 2026-11-14 staging v4→v5; 2026-11-14 production v3→v5; 2026-11-14 staging v5→v6; 2026-11-14 staging v6→v5

## TraceDesk: grounded answers

The system prompt of the FAQ assistant: answer only from the documents, bottom line first, a word-for-word quote for each point, and a source for every deadline. The comparison is a plain prompt on the same model (baseline-v2).

- Location: `app/lib/prompts.js` (tracedesk)
- Model lock: claude-haiku-5-5, effort medium

| Version | Date | Change | Score at the time | Decision | Why |
|---|---|---|---|---|---|
| **grounded-v2-access** | 2026-11-09 | Output format v2: a one-line conclusion and a list of next steps.<br>Text not kept | no stored evaluation | superseded | Only smoke-tested; no evaluation result was stored.<br>Source: [tracedesk-lite/app/lib/prompts.js](https://github.com/Jason-d-e/tracedesk-lite/blob/main/app/lib/prompts.js) |
| **grounded-v2.1-access** | 2026-11-09 | Dates written in the reader's language.<br>Text not kept | no stored evaluation | superseded | Not evaluated on its own.<br>Source: [tracedesk-lite/app/lib/prompts.js](https://github.com/Jason-d-e/tracedesk-lite/blob/main/app/lib/prompts.js) |
| **grounded-v2.2-access** | 2026-11-09 | Writing-style rules adapted from i-have-adhd.<br>`app/lib/prompts.js` at public commit d78874c | *Development set, 20 cases (plain vs v2.2)*<br>All automatic checks passed (plain → v2.2): 17/20 → 19/20 | superseded | More answers passed the automatic checks than with the plain prompt on the development set; later, deadlines were sometimes not attached to their step.<br>Source: [tracedesk-lite/app/lib/prompts.js](https://github.com/Jason-d-e/tracedesk-lite/blob/main/app/lib/prompts.js) |
| **grounded-v2.3-access** | 2026-11-09 | A step's deadline must be attached to that step and its quote must state it.<br>`app/lib/prompts.js` at public commit 8064b58 | *Check set, 20 cases, run 1*<br>All automatic checks passed (plain → v2.3): 15/20 → 19/20 | superseded | Check run 1 passed more automatic checks than the plain prompt; deadlines in Chinese answers could still come out in English.<br>Source: [tracedesk-lite/EVALUATION.md](https://github.com/Jason-d-e/tracedesk-lite/blob/main/EVALUATION.md) |
| **grounded-v2.4-access** | 2026-11-09 | Deadlines also written in the reader's language.<br>`app/lib/prompts.js` at public commit 2951bef (current default) | *Check set, 20 cases, run 2*<br>All automatic checks passed (plain → v2.4): 17/20 → 20/20<br>Cost of 20 cases (plain → v2.4): US$0.0093 → US$0.0134 | adopted | Check run 2 passed every automatic check, but it came after seeing run 1 on the same cases, so it is not a clean held-out result.<br>Source: [tracedesk-lite/EVALUATION.md](https://github.com/Jason-d-e/tracedesk-lite/blob/main/EVALUATION.md) |

Label history: 2026-11-09 production ·→grounded-v2-access; 2026-11-09 production grounded-v2-access→grounded-v2.1-access; 2026-11-09 production grounded-v2.1-access→grounded-v2.2-access; 2026-11-09 production grounded-v2.2-access→grounded-v2.3-access; 2026-11-09 production grounded-v2.3-access→grounded-v2.4-access

## Cairn: answers from published rules

The system prompt Cairn answers with: conclusion first, deadlines and next steps, campus stated, no invented dates, fees or contacts.

- Location: `app/lib/prompt.js` (cairn)
- Model lock: claude-haiku-5-5

| Version | Date | Change | Score at the time | Decision | Why |
|---|---|---|---|---|---|
| **cairn-v1** | 2026-11-09 | The first version, over accessibility guidelines (WCAG).<br>`app/lib/prompt.js` at public commit f63aafa | no stored evaluation | retired | Retired when the corpus switched to student pages. |
| **cairn-monash-v1** | 2026-11-10 | Conclusion first, deadlines and next steps, campus stated, no invented dates, fees or contacts.<br>`app/lib/prompt.js` at public commit 921e557 | no stored evaluation | superseded | Replaced by v2 after the final readability review. |
| **cairn-monash-v2** | 2026-11-10 | The reader is told about "the pages", never "the passages"; no campus remark when a rule applies everywhere; no note on what the pages leave out once the question is answered; the campus is passed to the model, which never asks for it.<br>`app/lib/prompt.js` at public commit 45f0b13 (current) | no stored evaluation | adopted | From the readability review. Both versions were only smoke-tested, with results printed to the console and not stored, so no score is listed; the retrieval evaluation does not depend on the prompt.<br>Source: [cairn/app/lib/prompt.js](https://github.com/Jason-d-e/cairn/blob/main/app/lib/prompt.js) |

Label history: 2026-11-09 production ·→cairn-v1; 2026-11-10 production cairn-v1→cairn-monash-v1; 2026-11-10 production cairn-monash-v1→cairn-monash-v2

## Grounded Labelling Pipeline: first-pass decision

The first decision on each ad in the pipeline: approve or reject, which clause, which words of the ad. From v2 it also says whether it is sure; unsure answers go to human review. The pipeline's own registry holds the same asset with the same labels.

- Location: `pipeline/triage.py` (grounded-labelling-pipeline)
- Model lock: claude-haiku-5-5, effort medium, max_tokens 8000

| Version | Date | Change | Score at the time | Decision | Why |
|---|---|---|---|---|---|
| **v1** | 2026-11-15 | First version: the whole policy library, the image, the caption and the image's text in one request, answered in the review format.<br>Grounded Review's one-prompt arm as it is (`agent/oneshot.py`) | *Grounded Review's 166 items, 2 replays each*<br>Wrong decisions that went live: 17/332<br>Decisions right: 315/332 | superseded | Every wrong decision in the replay went live (17/332); the quote check only caught answers that were right but quoted badly.<br>Source: [grounded-labelling-pipeline/reports/compare-v1-v2.md](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/reports/compare-v1-v2.md) |
| **v2** | 2026-11-15 | The model says whether it is sure; unsure answers go to human review.<br>v1 plus one rule on when to be unsure (`triage.CERTAINTY_RULE`) and two output fields, `certainty` and `unsure_reason` | *Round one: Grounded Review's 166 items, 2 replays each; round two: 120 newly written text ads, 2 runs each*<br>Wrong decisions that went live (v1 → v2): 17/332 → 9/332<br>Sent to human review (v1 → v2): 6/332 → 72/332<br>Decisions right (v1 → v2): 315/332 → 312/332<br>Cost per request (v1 → v2): US$0.00062 → US$0.00063<br>Round two, new ads: decisions right (v1 → v2): 239/240 → 240/240 | adopted | It passed all four preregistered adoption rules on the regression set: wrong decisions that went live 17/332 → 9/332. The rollback rules written before the replay rolled it back at 10%; the post-mortem found two of those rules were wrong. With the fixed rules, a second canary on newly written ads fired no rule at any of its three steps, so v2 was adopted and production moved to it. Both versions were almost always right in round two, so that round shows the release process works; the evidence that v2 lets fewer errors through comes from round one.<br>Source: [grounded-labelling-pipeline/docs/CANARY-POSTMORTEM.md](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/docs/CANARY-POSTMORTEM.md) |
| **v3** | 2026-11-17 | Meant to send fewer clear ads to people: a text ad with no image, a sourced fact that cannot be checked, the advertiser's licence and targeting, and words a guidance clause plainly allows no longer count as unsure.<br>v2's rule on when to be unsure, rewritten (`triage.CERTAINTY_RULE_V3`): which cases count as unsure and which do not; the output format is unchanged | *Round three: another 120 newly written text ads, 2 runs each; regression: the 166 round-one items, 2 replays each*<br>Clear ads sent to human review (v2 → v3): 44/176 → 4/176<br>Ads that need a human, sent to people (v2 → v3): 44/64 → 19/64<br>Regression: wrong decisions that went live (v2 → v3): 9/332 → 9/332<br>Regression: sent to human review (v2 → v3): 72/332 → 30/332 | not adopted | On another set of newly written ads (adoption rules and predictions preregistered), clear ads sent to people fell from 44/176 to 4/176; but ads written as needing a human were also sent to people less often, 44/64 to 19/64, past the limit set beforehand, so it was not adopted and production stays on v2. In the round-one regression, wrong decisions that went live were 9/332 against 9/332. Had it been rolled out, no canary rollback rule would have fired; the adoption standard stopped it.<br>Source: [grounded-labelling-pipeline/reports/compare-v2-v3-round3.md](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/reports/compare-v2-v3-round3.md) |
| **v4** | 2026-11-17 | Meant to pass at both ends: fewer clear ads sent to people, and no fewer of those that need one. It names common boundary cases and adds a self-check: if another reading also holds, answer unsure.<br>v3's rule on when to be unsure plus one case: the decision turns on placing the ad's words inside or outside a rule and the words sit on the boundary (`triage.CERTAINTY_RULE_V4`); the output format is unchanged | *Round four: another 120 newly written text ads, 2 runs each; regression: the 166 round-one items, 2 replays each*<br>Clear ads sent to human review (v2 → v4): 43/176 → 11/176<br>Ads that need a human, sent to people (v2 → v4): 42/64 → 47/64<br>Clear ads decided wrongly and gone live (v2 → v4): 0/176 → 2/176<br>Regression: wrong decisions that went live (v2 → v4): 9/332 → 13/332 | not adopted | On another set of newly written ads (adoption rules word for word those of round three, predictions frozen before the run), it beat v2 at both ends: clear ads sent to people 43/176 → 11/176, ads that need a human sent to people 42/64 → 47/64. But it was more often sure when wrong: clear ads decided wrongly and gone live 0/176 → 2/176 (both runs of one trap item whose answer is debatable and, as preregistered, unchanged), and round-one regression escapes 9/332 → 13/332. Not adopted; production stays on v2. Had it been rolled out, no canary rollback rule would have fired.<br>Source: [grounded-labelling-pipeline/reports/compare-v2-v4-round4.md](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/reports/compare-v2-v4-round4.md) |

Label history: 2026-11-15 production ·→v1; 2026-11-15 staging ·→v2; 2026-11-15 staging v2→v1; 2026-11-16 staging v1→v2; 2026-11-16 production v1→v2

## Grounded Labelling Pipeline: policy knowledge-base Q&A

A labeller asks whether some wording breaks a rule; the answer uses only the retrieved clauses: a verdict, a short explanation, and the id and exact words of each clause it rests on. If no clause covers the question it says so. Every quote is checked with evidence-check. The pipeline's own registry holds the same asset with the same labels.

- Location: `pipeline/kb_qa.py` (grounded-labelling-pipeline)
- Model lock: claude-haiku-5-5, effort medium, top 5 clauses, max_tokens 1500 in the evaluation and 4000 in the bot

| Version | Date | Change | Score at the time | Decision | Why |
|---|---|---|---|---|---|
| **v1** | 2026-11-17 | First version.<br>`kb_qa.INSTRUCTIONS`: four verdicts (violation, allowed, depends, not in the library), only retrieved clauses may be cited, quotes copied word for word | *Replay of a question set: 80 questions (half Chinese, half English, some not answerable from the library), 2 runs each*<br>Answered right: 134/160<br>Said "not in the library" when it was not: 44/48<br>Quotes that failed the check: 1/160<br>Chinese questions: right clause in the top five (BM25): 23/28 | adopted | The plan and predictions were written before the run. Answered right 134/160; said "not in the library" when it was not 44/48; quotes that failed the check 1/160. The prediction that failed is retrieval for Chinese questions: the right clause was in the top five for only 23/28, and every "not in the library" on an answerable question came from there.<br>Source: [grounded-labelling-pipeline/reports/kb-qa.md](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/reports/kb-qa.md) |

Label history: 2026-11-17 production ·→v1

## Regression check

When a pull request changes files under `prompts/`, a GitHub Action runs promptfoo on the versions behind the production and staging labels over one frozen item set and posts each label's pass count, version, failed items and cost on the pull request. The evidence-check skill is wired in, on its development set v1 (fictional event documents, 12 drafts); the check turns red when a request gets no answer, when either label fails more than 2 drafts, or when staging passes 2 or more fewer than production, as set in [regression/report.mjs](regression/report.mjs). Configuration: [regression/](regression/).
