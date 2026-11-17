# Creator skills: evaluation card

> Card version 1.0 · Data as of 2026-11-17 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-17 | Liang Liyuan | Agent Skills (SKILL.md plus standard-library Python scripts), Claude Code plugin, Message Batches API | [Code and report](https://github.com/llia0031-dotcom/creator-skills) |

**Problem**: Creators fix subtitles, plan shot lists and chase trends weekly. When an assistant does it, do subtitles stay right, can every shot be spoken in time, and do trend facts hold?

**What I did**: I built three Agent Skills for short-video creators: subtitle checking, shot-list checking and trend topics. Each carries a checking script that runs before anything is handed back. Each was compared with the same model without the skill on items whose answers were fixed in advance, with plans and predictions frozen before the runs.

**Results**: 

- Corrected subtitle files fully right: with the skill 20/20, without 2/20
- Shot lists passing all four checks when the request gives no rates: with the skill 20/20, without 0/20; with the rates stated, even without it 19/20
- Trends involving casualties get no marketing cards: with the skill 4/4, without 0/4

## Summary

Three Agent Skills for short-video creators, each with a checking script that uses only the Python standard library. Subtitle checking compares every auto-caption with the script and checks reading speed and timing; shot-list checking checks that each shot's voiceover can be spoken in time, that no line of the script is lost and that the total length fits; trend topics checks every fact on a topic card: the link opens, the title matches, the quote is on the page, the numbers are in the quote and the page is recent. Each is compared with the same model without the skill, on fictional creator scenarios whose answers were fixed when they were written.

- **Place in the portfolio**: Scenario: generation
- **Link to the core component**: Trend topics copies its quote matching from the evidence-check script, with the same rules: a quote must come word for word from the page, and the numbers must be in the quote.
- **Models used**: Both arms use claude-haiku-5-5 (effort medium) with the same user message; evaluations go through the Message Batches API.

## Uses

- A creator's pre-publishing check: subtitles against the script, shot lengths that can be spoken, and sourced facts on trend cards.
- Install into Claude Code, Codex, DeerFlow or another tool that supports Agent Skills.

## Out of scope

- The items are fictional creator scenarios and do not represent real creators' use.
- Ideas, whether visuals can be filmed and whether the pace suits a given speaker are not judged.

## Evaluation data

### Subtitle checking: auto-captions against the script

10 voiceover scripts (6 Chinese, 4 English) cut into auto-captions, with misheard words, ad-libs, skipped sentences and timing errors planted; answers fixed when the cases were built. The request says the subtitles must match what was said and the timings must not change.

| Field | Value |
|---|---|
| Date | 2026-11-17 |
| Items and answers | 10 subtitle files, 20 runs per arm |
| Runs | 2 runs per case per arm |
| Model and send mode | claude-haiku-5-5, effort medium, Message Batches API |
| Frozen before the run | `eval/subtitle-check/PREREGISTRATION.md` |

### Shot lists, round one: the request states the rates

10 scripts turned into shot lists for a target length; the request states the speaking rate, reading rate and how to count. Four checks: the script is covered word for word in order, each shot's voiceover fits, the total is within range, and on-screen text can be read.

| Field | Value |
|---|---|
| Date | 2026-11-17 |
| Items and answers | 10 scripts, 20 runs per arm |
| Runs | 2 runs per case per arm |
| Model and send mode | claude-haiku-5-5, effort medium, Message Batches API |
| Frozen before the run | `eval/shotlist-check/PREREGISTRATION.md` |

### Shot lists, round two: no rates in the request (new items)

10 new scripts, none from round one; the request is written as a creator would write it, giving only an approximate length and asking for the script as voiceover, with no rates or counting rule. The skill and script are the same frozen copies as in round one.

| Field | Value |
|---|---|
| Date | 2026-11-17 |
| Items and answers | 10 scripts, 20 runs per arm |
| Runs | 2 runs per case per arm |
| Model and send mode | claude-haiku-5-5, effort medium, Message Batches API; checked at the default rates |
| Frozen before the run | `eval/shotlist-check/v2/PREREGISTRATION.md` |

### Trend topics: every fact on a card carries its source

10 fictional trends (6 Chinese, 4 English), each with an account profile, a fixed date and several fetched pages; planted stale pages, dead links, figures later corrected, rumour figures that disagree with an official page, teaser lines that differ from the page title, and 2 events with casualties.

| Field | Value |
|---|---|
| Date | 2026-11-17 |
| Items and answers | 10 trends, 20 runs per arm |
| Runs | 2 runs per case per arm |
| Model and send mode | claude-haiku-5-5, effort medium, Message Batches API |
| Frozen before the run | `eval/trend-topic-check/PREREGISTRATION.md` |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Subtitle checking: auto-captions against the script

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Corrected files fully right (without the skill) | 2/20 (10.0%, 95% CI 2.8–30.1%) | higher is better | [`creator-skills/eval/subtitle-check/results/run-2026-11-17.summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/subtitle-check/results/run-2026-11-17.summary.md) |
| Corrected files fully right (with the skill) | 20/20 (100.0%, 95% CI 83.9–100.0%) | higher is better | [`creator-skills/eval/subtitle-check/results/run-2026-11-17.summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/subtitle-check/results/run-2026-11-17.summary.md) |
| Timings kept (without the skill) | 12/20 (60.0%, 95% CI 38.7–78.1%) | higher is better | [`creator-skills/eval/subtitle-check/results/run-2026-11-17.summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/subtitle-check/results/run-2026-11-17.summary.md) |
| Timings kept (with the skill) | 20/20 (100.0%, 95% CI 83.9–100.0%) | higher is better | [`creator-skills/eval/subtitle-check/results/run-2026-11-17.summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/subtitle-check/results/run-2026-11-17.summary.md) |
| Ad-libs kept as said (without the skill) | 9/38 (23.7%, 95% CI 13.0–39.2%) | higher is better | [`creator-skills/eval/subtitle-check/results/run-2026-11-17.summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/subtitle-check/results/run-2026-11-17.summary.md) |
| Ad-libs kept as said (with the skill) | 38/38 (100.0%, 95% CI 90.8–100.0%) | higher is better | [`creator-skills/eval/subtitle-check/results/run-2026-11-17.summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/subtitle-check/results/run-2026-11-17.summary.md) |

Both arms fix the misheard words; without the skill the model often moves timings and turns ad-libs back into the script, so few corrected files are fully right.

### Shot lists, round one: the request states the rates

| Metric | Result | Direction | Source file |
|---|---|---|---|
| All four checks pass (without the skill) | 19/20 (95.0%, 95% CI 76.4–99.1%) | higher is better | [`creator-skills/eval/shotlist-check/results/summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/shotlist-check/results/summary.md) |
| All four checks pass (with the skill) | 20/20 (100.0%, 95% CI 83.9–100.0%) | higher is better | [`creator-skills/eval/shotlist-check/results/summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/shotlist-check/results/summary.md) |

When the request spells out the rates and the counting, the model passes almost every time without the skill, a ceiling; the predicted "at most half" did not hold.

### Shot lists, round two: no rates in the request (new items)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| All four checks pass (without the skill, default rates) | 0/20 (0.0%, 95% CI 0.0–16.1%) | higher is better | [`creator-skills/eval/shotlist-check/v2/results/summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/shotlist-check/v2/results/summary.md) |
| All four checks pass (with the skill, default rates) | 20/20 (100.0%, 95% CI 83.9–100.0%) | higher is better | [`creator-skills/eval/shotlist-check/v2/results/summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/shotlist-check/v2/results/summary.md) |
| Shots whose voiceover overflows (without the skill) | 90/182 (49.5%, 95% CI 42.3–56.7%) | lower is better | [`creator-skills/eval/shotlist-check/v2/results/summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/shotlist-check/v2/results/summary.md) |
| Shots whose voiceover overflows (with the skill) | 0/230 (0.0%, 95% CI 0.0–1.6%) | lower is better | [`creator-skills/eval/shotlist-check/v2/results/summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/shotlist-check/v2/results/summary.md) |

With no rates given, shot lists without the skill had many shots whose voiceover cannot be spoken in time, and none passed; with the skill, the script caught them first and all passed.

### Trend topics: every fact on a card carries its source

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Casualty events handled correctly (without the skill) | 0/4 (0.0%, 95% CI 0.0–49.0%) | higher is better | [`creator-skills/eval/trend-topic-check/results/scores.json`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/trend-topic-check/results/scores.json) |
| Casualty events handled correctly (with the skill) | 4/4 (100.0%, 95% CI 51.0–100.0%) | higher is better | [`creator-skills/eval/trend-topic-check/results/scores.json`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/trend-topic-check/results/scores.json) |
| Facts with a number not in the quote (without the skill) | 6/125 (4.8%, 95% CI 2.2–10.1%) | lower is better | [`creator-skills/eval/trend-topic-check/results/scores.json`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/trend-topic-check/results/scores.json) |
| Facts with a number not in the quote (with the skill) | 0/128 (0.0%, 95% CI 0.0–2.9%) | lower is better | [`creator-skills/eval/trend-topic-check/results/scores.json`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/trend-topic-check/results/scores.json) |
| Cost with the skill relative to without | 2.9× | lower is better | [`creator-skills/eval/trend-topic-check/results/scores.json`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/trend-topic-check/results/scores.json) |

Most sources check out in both arms; the difference is in casualty events and numbers: without the skill the model made marketing cards for casualty events, and some numbers were not in their quotes.

## Grader calibration

- No grader is used: every measure is computed by script against answers fixed when the items were written; the ideas and their fit to the account are not scored.

## Limitations and failure cases

- All items are synthetic and written with the skills' checks in mind; real audio, accents, music and several speakers are not covered.
  - Recommendation: Before release, test again on real auto-captions and real trends.
- One model and two runs per item per arm; a difference of one or two items is noise.
  - Recommendation: Run the same items again after a model or effort change.
- The shot-list gap appears only when the request gives no rates: with the rates stated, even without the skill 19/20 passed.
  - Recommendation: Look at how users actually ask before deciding whether to install this skill by default.
- Trend topics checks only the sources of facts and casualty events, not the quality of the ideas or their fit to the account.
  - Recommendation: Write separate scoring rules for ideas and account fit, then test.

## Versions

- **1.0** (2026-11-17) First card, from the result files in the public creator-skills repository.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.

Sources and licences of third-party data, models and code are listed in the [project repository](https://github.com/llia0031-dotcom/creator-skills).
