# Placement Monitoring Kit: evaluation card

> Card version 1.0 · Data as of 2026-11-26 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-22 to 2026-11-23 | Liang Liyuan | Python, XLSForm (pyxform and ODK Validate), KoboToolbox / ODK Central exports, pandas, openpyxl, reportlab, python-pptx, evidence-check | [Code and guide](https://github.com/llia0031-dotcom/placement-monitoring-kit) · [Quick start](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/guide/en/QUICK_START.md) · [Data checks](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/guide/en/CHECKS.md) |

**Problem**: A placement programme follows every intern month by month: whose form is missing, where the data is wrong, what to report this month; done by hand, it is slow and things slip.

**What I did**: I first checked what exists: paid monitoring platforms need money and accounts and have no internship templates; university placement systems do not cover offline collection or French; no public repository had a placement check-in form. So the kit joins recognised wording and indicator definitions: exit and destination questions and the employment classification follow the international labour statistics standards, and the kit's own questions are marked as such. The monthly run reads the form exports, checks the data, lists who to follow up with reminder text ready, and writes the tracker, a brief and a deck. The checks were measured first on a constructed sample: 50 consenting interns, 18 host organisations and 7 months, with planted errors and records that look wrong but are not.

**Results**: 

- Every planted data error in the constructed sample is caught: 17/17; the issue list has no extra rows, and none of the 14 records that look wrong but are not is flagged
- Tagged numbers in the brief and deck traced line by line to the data: 260/260; background brief 24/24
- Four English and French forms with 119 questions, each filled in through the form interface: 418/418 checks passed

## Summary

For teams that follow placements month by month: four English and French forms (intake, monthly check-in, host feedback, exit) for KoboToolbox or ODK Central; one double-click a month runs 15 data checks, computes 39 indicators and writes the tracker, a 2-page brief and an 8-slide deck. Two things are evaluated: whether the checks are accurate, measured with the planted errors and near misses of a constructed sample; and whether the report numbers are right, traced line by line to the data.

- **Place in the portfolio**: Operations
- **Link to the core component**: Every tagged number in the briefs, decks, background brief and READMEs is checked against its data row with the evidence-check 0.5.0 script.
- **Models used**: No model is called: form conversion, data checks, indicators and reports are all done by scripts.

## Uses

- Teams that follow internship or training placements month by month: download the form exports, double-click once, and get who to follow up, where the data needs fixing, and the month's brief and deck.
- Before data collection starts: write your settings into the forms and run the constructed sample first, to see what each check flags and how to fix it.

## Out of scope

- Not an online platform: the data stays on the team's own form server and computer, and the run happens once a month on Windows.
- Does not judge anyone's situation: safeguarding call-backs are listed with a date to call by, and people on the team make the calls.

## Evaluation data

### Data checks: a constructed sample with planted errors

A constructed cohort with no real people or organisations: planted data errors (duplicate submissions, unmatched IDs, impossible dates, contradictions and more), follow-ups not received, and records that look wrong but are not; what was planted and which check should flag it are listed in the planted file.

| Field | Value |
|---|---|
| Date | 2026-11-23 |
| Items and answers | Every planted error and near miss |
| Runs | On every run and every test |
| Model and send mode | All data checks; no model called |
| Frozen before the run | `data/sample/planted.json` (each planted problem, how it was planted, the expected result) |

### Reports: the numbers in the brief and deck

The constructed sample's English and French brief and deck for the month, and the background brief; every line with a number is tagged with the data row it comes from.

| Field | Value |
|---|---|
| Date | 2026-11-23 |
| Items and answers | Every tagged line |
| Runs | Checked on every run |
| Model and send mode | The evidence-check 0.5.0 script; no model called |
| Frozen before the run | `indicators/INDICATORS.md` (each indicator's numerator, denominator and rules) |

### Forms: filled in through the form interface

The four forms are converted with pyxform, the converter KoboToolbox and ODK Central use, and pass ODK Validate; then each is filled in through ODK Web Forms on a local computer, in English and French, at phone and desktop width, and the saved submissions are compared with the field names the monthly run reads.

| Field | Value |
|---|---|
| Date | 2026-11-23 |
| Items and answers | Every question of the four forms |
| Runs | Once per form, language and width |
| Model and send mode | A form-filling script; no model called |
| Frozen before the run | `forms/xlsform/` |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Data checks: a constructed sample with planted errors

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Planted data errors caught | 17/17 (100.0%, 95% CI 81.6–100.0%) | higher is better | [`placement-monitoring-kit/data/sample/planted.json`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/data/sample/planted.json)<br>[`placement-monitoring-kit/outputs/sample/en/2026-08/data/issues.csv`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/outputs/sample/en/2026-08/data/issues.csv) |
| Issue rows that are not planted errors | 0/18 (0.0%, 95% CI 0.0–17.6%) | lower is better | [`placement-monitoring-kit/data/sample/planted.json`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/data/sample/planted.json)<br>[`placement-monitoring-kit/outputs/sample/en/2026-08/data/issues.csv`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/outputs/sample/en/2026-08/data/issues.csv) |
| Near misses: records that look wrong but are not | 14 | context only | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| Planted follow-ups not received | 9 | context only | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| Consenting interns in the sample | 50 | context only | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| Host organisations in the sample | 18 | context only | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| Months in the sample | 7 | context only | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| Data checks | 15 | context only | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |

Every planted error is flagged by its check and the issue list has no extra rows; no near miss is flagged.

### Reports: the numbers in the brief and deck

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Brief and deck: tagged lines matched to data | 260/260 (100.0%, 95% CI 98.5–100.0%) | higher is better | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| Background brief: tagged lines matched to data | 24/24 (100.0%, 95% CI 86.2–100.0%) | higher is better | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| Indicators | 39 | context only | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| Pages in the brief | 2 | context only | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| Slides in the deck | 8 | context only | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |

Every tagged number matches its data row and the English and French versions agree; run again on the same data, the brief and deck are byte for byte the same.

### Forms: filled in through the form interface

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Form walk-through checks passed | 418/418 (100.0%, 95% CI 99.1–100.0%) | higher is better | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| Saved submissions matching the forms and fields | 32/32 (100.0%, 95% CI 89.3–100.0%) | higher is better | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| Questions in the four forms | 119 | context only | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| Automated tests | 479 | context only | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |

Every form can be completed in the form interface, and the saved submissions match the fields the monthly run reads.

## Limitations and failure cases

- The sample is constructed; the kit has not yet run in a live programme, against a live KoboToolbox or ODK Central server or in ODK Collect, and only on Windows.
  - Recommendation: Before going live, set up a test project on the team's own server and run the monthly cycle once with a few test submissions.
- The French text still needs a read by a French-speaking colleague in the country; some check-in and host-feedback questions have no recognised instrument and use the kit's own wording, marked as such.
  - Recommendation: Write the changes back into the forms' xlsx and rebuild; after a month or two, revise questions by how they are answered.

## Versions

- **1.0** (2026-11-26) First card, from the result files in the public placement-monitoring-kit repository.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.

Sources and licences of third-party data, models and code are listed in the [project repository](https://github.com/llia0031-dotcom/placement-monitoring-kit).
