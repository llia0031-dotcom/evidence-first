# Malaysia Electronics Merchant Sourcing Pack: evaluation card

> Card version 1.1 · Data as of 2026-11-20 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-19 | Liang Liyuan | Python, DuckDB, SQL, Excel (openpyxl), evidence-check, saved public pages | [Code and materials](https://github.com/llia0031-dotcom/merchant-sourcing-my) · [Who to contact first](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/pool/PRIORITY.md) · [Charging deep dive](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/insight/DEEP_DIVE_CHARGING.md) · [Inside the team: data and calibration](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/pool/INSIDE_THE_TEAM.md) |

**Problem**: A category team's first week of merchant recruiting: what the market looks like, which merchants to contact first and why, which approvals each product needs, how onboarding is tracked; every reason backed by a public source.

**What I did**: I first checked the existing shop-ranking tools: they rank merchants already on a platform and cannot answer "which merchants not yet there, or not yet large, to recruit first". This pack fills that gap from public sources: saved official, market and brand pages, an industry insight and a per-category approvals checklist; scoring rules written and frozen before any row was filled, ranking local brands, distributors and retailers; then an onboarding tracker, first-30-days SQL and outreach templates; a one-page deep dive on chargers, power banks and cables; and a guide to which public fields to replace with team data first and how to test the scoring weights against results, with a calibration script. Every fact and every cell of the pool is checked against its saved page with evidence-check.

**Results**: 

- Sourced claims in the insight, the checklist, both READMEs and the pool, matched word for word against the saved pages: 493/493
- A pool of 42 merchants across 9 sub-categories, 303 cells each with a checked quote; tiered by the frozen rules, 14 in tier A
- 183 public pages saved, 131 of them quoted

## Summary

A first-week recruiting pack for a category team: industry insight, a scored pool of local brands, distributors and retailers, a per-category approvals checklist, an onboarding tracker, first-30-days SQL and outreach templates. What is evaluated is every fact in the pack: the quote must be in the saved page, the number in the quote, and a pool quote must contain a word that counts as evidence; if not, the build stops.

- **Place in the portfolio**: Scenario: judgement
- **Link to the core component**: Every fact is checked against its saved page with the evidence-check 0.5.0 script; the first-30-days SQL follows Grounded Business Review's weekly metrics.
- **Models used**: No model is called: reading pages, scoring, checking and building the tables are all done by scripts.

## Uses

- When a category team opens sub-categories in a new market: the insight decides what to recruit first, the pool's order and next steps decide whom to call.
- After a merchant's first call: send the approvals checklist for its category, plan onboarding dates in the tracker, and follow the new shop with the first-30-days SQL.
- Once the first batch has results: replace public fields with the team's own data, check with the calibration script whether each dimension tracks results, then set the next version of the rules.

## Out of scope

- Does not judge any merchant; a low score means less public evidence or less to gain right now.
- Does not replace a platform's own seller lists or back-office data; only pages readable without signing in are used.

## Evaluation data

### Full check: every sourced claim

Every tagged line of the insight, the checklist and both READMEs, every field of every pool row and every demand signal, against the saved public pages and the result files.

| Field | Value |
|---|---|
| Date | 2026-11-19 |
| Items and answers | All sourced claims |
| Runs | Run on every build |
| Model and send mode | The evidence-check 0.5.0 script; no model called |
| Frozen before the run | `sources/manifests/` (each URL, fetch time and the SHA-256 of the text) |

### Merchant pool: scored by frozen rules

Local brands, distributors and retailers; every field filled only from saved public pages, with a source id and a verbatim quote; four dimensions: demand signal, content-commerce gap, qualification readiness and content capability.

| Field | Value |
|---|---|
| Date | 2026-11-19 |
| Items and answers | Every merchant in the pool |
| Runs | Run on every build |
| Model and send mode | `pool/build.py` scores by the rules after checking the rules file's fingerprint |
| Frozen before the run | `pool/SCORING.md` version two |

### Sources: saved public pages

Single public pages only: robots.txt first, a pause between requests to the same site, no sign-in, no platform product, shop or search pages; approvals quote regulators only. Page texts belong to their publishers and are not redistributed; the manifests list each URL, fetch time and text SHA-256.

| Field | Value |
|---|---|
| Date | 2026-11-19 |
| Items and answers | Every saved page |
| Runs | Fetched once; `tools/refetch.py` saves them again |
| Model and send mode | No model called |
| Frozen before the run | `sources/manifests/` |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Full check: every sourced claim

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Sourced claims matched to saved pages | 493/493 (100.0%, 95% CI 99.2–100.0%) | higher is better | [`merchant-sourcing-my/results/CLAIM_CHECK.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/CLAIM_CHECK.md) |
| Lines with a number but no source tag | 0 | lower is better | [`merchant-sourcing-my/results/CLAIM_CHECK.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/CLAIM_CHECK.md) |

Every claim matches its source, and no line carries a number without a source tag.

### Merchant pool: scored by frozen rules

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Cells with a checked quote | 303 | context only | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| Merchants in the pool | 42 | context only | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| Sub-categories covered | 9 | context only | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| Malaysian company or named distributor found | 23/42 (54.8%, 95% CI 39.9–68.8%) | context only | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| Tier A merchants | 14 | context only | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| To open a first content-commerce shop | 17 | context only | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| To grow a shop that is open but small | 18 | context only | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |

The top of the list is local merchants that already sell well elsewhere but have no content-commerce shop yet, or a small one; more than half have a Malaysian company or named distributor.

### Sources: saved public pages

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Public pages saved | 183 | context only | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| Pages quoted | 131/183 (71.6%, 95% CI 64.7–77.6%) | context only | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| Official pages | 42 | context only | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |

Most saved pages are quoted by the insight, the checklist or the pool; the approvals checklist quotes regulators only.

## Limitations and failure cases

- "Not found in public sources" does not mean it does not exist, and is no judgement of the merchant; only pages readable without signing in were read.
  - Recommendation: Check the platform's own seller list before the first call.
- Third-party sales figures are their estimates; the shop ranking comes from one dataset, ordered by units.
  - Recommendation: Re-rank with the platform's or the merchant's own data once available.
- No merchant has been contacted and the outreach templates have not been sent; the first-30-days example data is fictional and only tests the SQL.
  - Recommendation: Once outreach starts, record onboarding and week-4 sales, then test the weights with pool/calibrate.py as pool/INSIDE_THE_TEAM.md describes.

## Versions

- **1.0** (2026-11-19) First card, from the result files in the public merchant-sourcing-my repository.
- **1.1** (2026-11-20) Follows the project's a29f0c8: claim and quoted-page counts from the new result files; adds the charging deep dive and the team-data and calibration guide.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.

Sources and licences of third-party data, models and code are listed in the [project repository](https://github.com/llia0031-dotcom/merchant-sourcing-my).
