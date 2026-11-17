# Cairn: evaluation card

> Card version 1.1 · Data as of 2026-11-15 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-09 – 2026-11-11 (LaunchPad Hacks) | Liang Liyuan, ZIzi821 | Node.js, React, local embedding and reranking, Claude Haiku 5.5 | [Code](https://github.com/llia0031-dotcom/cairn) · [Live demo](https://llia0031-dotcom.github.io/cairn/) · [Demo video](https://youtu.be/0OJ8MqxsqYE) |

**Problem**: Answer questions from an organisation's own published rules with word-for-word quotes, which first needs the right page to be found.

**What I did**: We built a desk that answers from published rules with word-for-word quotes: pick a campus, ask, then retrieval, generation and quote checking in code; seven retrieval methods were compared on 45 questions with known right pages, and real student questions were scored separately.

**Results**: 

- 45 questions, 7 retrieval methods: the method in use has the right page in the top five for 44/45, MRR 0.839
- Questions from students in their own words: top five 14/15, MRR 0.724

## Summary

A desk that answers questions from an organisation's published rules and quotes them word for word. The public instance uses 58 public Monash student pages. Retrieval translates the question into English, then runs vector search and reranking; quotes in the answer are shown only after they pass the check, and paraphrases that do not match word for word are withheld. The evaluation compares seven retrieval methods.

- **Place in the portfolio**: Scenario: grounded Q&A
- **Link to the core component**: The grounded Q&A scenario where the thread starts: every answer carries its source. Sellpoint Check's retrieval arms reuse its embedding models and Orama hybrid search.
- **Models used**: claude-haiku-5-5 for answers and for translating Chinese questions; local embedding and reranking models for retrieval.

## Uses

- Answer student-administration questions from published rules, with every sentence linked to its source.
- Compare retrieval methods on one question set to see which finds the right page first.

## Out of scope

- Covers only the 58 public pages collected: no unit guides and nothing behind a login.
- A prototype, not advice; it does not answer personal, legal or medical questions.
- The evaluation measures retrieval, not the quality of the written answers.

## Evaluation data

### Retrieval evaluation: 45 questions, 7 methods

45 questions (25 English, 20 Chinese), each with its right page fixed at writing. Seven methods compared: keyword, vector, two hybrid searches, with reranking, and translate-then-retrieve. No hashes were frozen before the run.

| Field | Value |
|---|---|
| Date | 2026-11-10 |
| Items and answers | 45 questions |
| Runs | 1 run per method |
| Model and send mode | Retrieval runs locally; Chinese questions are translated with claude-haiku-5-5, standard API |

### Real questions from students (scored separately)

20 questions from students in their own words (10 Chinese, 9 English, 1 Malay), copied as written with names and medical details removed and published with consent. 15 have an answer in the 58 pages and only those are scored. Scored as their own set, apart from the set above.

| Field | Value |
|---|---|
| Date | 2026-11-11 |
| Items and answers | 15 answerable questions |
| Runs | 1 run |
| Model and send mode | Method in use, as above |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Retrieval evaluation: 45 questions, 7 methods

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Right page first (method in use) | 34/45 (75.6%, 95% CI 61.3–85.8%) | higher is better | [`cairn/app/eval/results/retrieval-2026-11-10.json`](https://github.com/llia0031-dotcom/cairn/blob/main/app/eval/results/retrieval-2026-11-10.json) |
| Right page in the top five (method in use) | 44/45 (97.8%, 95% CI 88.4–99.6%) | higher is better | [`cairn/app/eval/results/retrieval-2026-11-10.json`](https://github.com/llia0031-dotcom/cairn/blob/main/app/eval/results/retrieval-2026-11-10.json) |
| MRR@10 (method in use) | 0.839 (n=45) | higher is better | [`cairn/app/eval/results/retrieval-2026-11-10.json`](https://github.com/llia0031-dotcom/cairn/blob/main/app/eval/results/retrieval-2026-11-10.json) |
| MRR@10 (vector only) | 0.709 (n=45) | higher is better | [`cairn/app/eval/results/retrieval-2026-11-10.json`](https://github.com/llia0031-dotcom/cairn/blob/main/app/eval/results/retrieval-2026-11-10.json) |
| MRR@10 (keyword only) | 0.375 (n=45) | higher is better | [`cairn/app/eval/results/retrieval-2026-11-10.json`](https://github.com/llia0031-dotcom/cairn/blob/main/app/eval/results/retrieval-2026-11-10.json) |
| Chinese questions in the top five: no translation | 18/20 (90.0%, 95% CI 69.9–97.2%) | higher is better | [`cairn/app/eval/results/retrieval-2026-11-10.json`](https://github.com/llia0031-dotcom/cairn/blob/main/app/eval/results/retrieval-2026-11-10.json) |
| Chinese questions in the top five: translated first | 19/20 (95.0%, 95% CI 76.4–99.1%) | higher is better | [`cairn/app/eval/results/retrieval-2026-11-10.json`](https://github.com/llia0031-dotcom/cairn/blob/main/app/eval/results/retrieval-2026-11-10.json) |

### Real questions from students (scored separately)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Right page in the top five | 14/15 (93.3%, 95% CI 70.2–98.8%) | higher is better | [`cairn/app/eval/results/student-retrieval-2026-11-11.json`](https://github.com/llia0031-dotcom/cairn/blob/main/app/eval/results/student-retrieval-2026-11-11.json) |
| MRR@10 | 0.724 (n=15) | higher is better | [`cairn/app/eval/results/student-retrieval-2026-11-11.json`](https://github.com/llia0031-dotcom/cairn/blob/main/app/eval/results/student-retrieval-2026-11-11.json) |

## Grader calibration

- No grader is used: each question's right page was fixed when it was written, and hits and MRR are computed by script.

## Limitations and failure cases

- Real wording is harder: MRR 0.724 on students' questions against 0.839 on the written set; the misses were an online exam that lost connection and the Malay question.
  - Recommendation: After launch, score real user questions the same way as a separate set and keep watching the gap.
- Answer quality itself is not evaluated; in a smoke test one Malaysia-campus question was answered from Australian rules.
  - Recommendation: Add campus-specific items and check that the cited page matches the asker's campus.

## Versions

- **1.0** (2026-11-15) First card; the live prompt is cairn-monash-v2.
- **1.1** (2026-11-15) Added when, team, stack, links and "problem / what I did / results" at the top, the way portfolio case studies open; the evaluation sections are unchanged.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.
