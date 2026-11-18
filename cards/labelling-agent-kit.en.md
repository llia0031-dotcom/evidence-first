# Labelling Agent Kit: evaluation card

> Card version 1.0 · Data as of 2026-11-18 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-18 | Liang Liyuan | Python, Message Batches API, BM25 retrieval, paired bootstrap tests, five Agent Skills (standard library only) | [Code and report](https://github.com/llia0031-dotcom/labelling-agent-kit) · [Results viewer](https://llia0031-dotcom.github.io/labelling-agent-kit/en.html) |

**Problem**: How should a labelling agent be built to label best, where and why does it fail, and does a fix still hold on new items?

**What I did**: I built one content-labelling agent that takes on a new task through a folder of rules and cases. Two tasks and five arms go through preregistered A/B comparisons, with per-label precision and recall, confusion and slices; the best arm's failures are sorted into five root causes, a second version is built from them and checked on a test set nothing was tuned on. The common analyses are packaged as five Agent Skills.

**Results**: 

- Test A micro F1, short prompt → full agent: ads 0.768 → 0.971, reviews 0.715 → 0.824
- Look-alike ads that are compliant: the short prompt labelled 12/32, the full agent 0/32
- The revision built from root causes, on unseen test B: reviews +0.018 [+0.005, +0.031], adopted; ads +0.021 [+0.000, +0.048], the interval reaches 0, not adopted

## Summary

A content-labelling agent that plugs into any labelling task through a folder of rules and cases, and the kit to tune it with evidence: preregistered A/B experiments, per-label precision and recall with intervals, confusion and slices, a root-cause table of failures, and a revision checked on items it never saw. The flow: retrieve similar cases, label with rule and case tools, and let code run a rule gate (labels given without reading their rule get the rule sent), quote repair and a self-check. Two tasks: ad-policy labels in Chinese and English (7 per language, answers fixed when each ad was written) and 18 aspects of restaurant reviews from the public ASAP dataset (the dataset's own labels). Five arms add one piece at a time, from a short prompt to rules plus retrieved cases plus a self-check; on reviews, real, synthetic and half-and-half case libraries are also compared. Plan, hypotheses and frozen files were written before the runs; each wrong decision of the best arm was classified twice, independently; the revision built from the causes was frozen before it ran on test B.

- **Place in the portfolio**: Operations
- **Link to the core component**: The ad items and rulebook come from the public data of Grounded Review and Policy Model Lab; the Grounded Labelling Pipeline runs the agent as a daily workflow, and this kit tunes it.
- **Models used**: claude-haiku-5-5 (effort low, Message Batches API), one run per item and arm.

## Uses

- Taking on a new labelling task: write the rules and cases folder, pick an arm with the same experiments, and find weak labels with slices and confusion.
- When labelling quality slips: use the root-cause table to tell rules, prompts and the gold labels apart, and check a revision on unseen items before it ships.

## Out of scope

- Does not show the flow works as well with other models or tasks; a new task needs its own comparison.
- Does not rewrite a dataset's gold labels: labels that read either way or were left out are reported to whoever sets the standard.

## Evaluation data

### Development round one: does the agent's first turn use a tool?

On the dev sets, whether each arm's first turn called a tool; the result changed the flow before the test sets were frozen.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | 40 dev reviews |
| Runs | 1 run per item and arm |
| Model and send mode | claude-haiku-5-5, effort low, Message Batches API |

### Test A: five arms

Ads: caption plus on-screen text in Chinese and English, 7 policy labels per language, answers fixed when each ad was written, 32 of them compliant look-alikes. Reviews: Chinese Dianping restaurant reviews, 18 aspects, the ASAP dataset's own labels. Five arms: short prompt, whole rulebook in the prompt, an agent that reads rules, plus retrieved cases, plus a self-check.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | 119 ads; 201 reviews |
| Runs | 1 run per item and arm |
| Model and send mode | claude-haiku-5-5, effort low, Message Batches API |
| Frozen before the run | `experiments/PREREGISTRATION.md` (fingerprints of 14 frozen files) |

### Test A: preregistered comparisons (B minus A, micro F1)

Two arms compared on the same items; "better" only when the paired-bootstrap interval lies above 0, "no measured difference" when it crosses 0.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | 119 ads; 201 reviews |
| Runs | 1 run per item and arm; intervals from 2,000 item bootstrap resamples |
| Model and send mode | claude-haiku-5-5, effort low, Message Batches API |
| Frozen before the run | `experiments/PREREGISTRATION.md`, section 5 |

### Root causes: the full agent's wrong decisions on test A

Each wrong label decision of the best arm (the full agent on both tasks) gets code-computed signals and is classified twice, independently, into five causes: prompt defect, model capability, rule conflict, sample distribution and label ambiguity (a gold label that reads either way or was left out). Disagreements are listed as split.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | Wrong decisions on 165 reviews and on 4 ads |
| Runs | 2 classifications per wrong decision |
| Model and send mode | claude-haiku-5-5, Message Batches API |
| Frozen before the run | `experiments/PREREGISTRATION.md`, section 6 |

### The revision built from root causes: unseen test B

The revision changes only what the root-cause tables point to: for reviews, the dataset's exceptions to "judged aspects only" (mall locations, deals, stated prices), the boundary between the two price labels and a self-check that keeps convention-required labels; for ads, effect percentages from tests as the data label and immediate weight-loss claims as the weight label only; for both, going through the whole label list before answering. It was frozen before it ran on test B.

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Items and answers | 118 ads; 199 reviews (test B, unused before) |
| Runs | 1 run per item and version; item bootstrap intervals |
| Model and send mode | claude-haiku-5-5, effort low, Message Batches API |
| Frozen before the run | `experiments/REVISION.md` (fingerprints of 17 frozen files) |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Development round one: does the agent's first turn use a tool?

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Rule tools only: first turn called a tool | 36/40 (90.0%, 95% CI 76.9–96.0%) | context only | [`labelling-agent-kit/results/dev1/FIRST_TURN.md`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/dev1/FIRST_TURN.md) |
| With case tools added: first turn called a tool | 0/40 (0.0%, 95% CI 0.0–8.8%) | context only | [`labelling-agent-kit/results/dev1/FIRST_TURN.md`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/dev1/FIRST_TURN.md) |

Offered the case tools alone, the agent never used them in its first turn; retrieval became a fixed step, so the agent and the case arm differ only in the cases.

### Test A: five arms

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Ads, short prompt: micro F1 | 0.768 | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Ads, whole rulebook in the prompt: micro F1 | 0.878 | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Ads, agent that reads rules: micro F1 | 0.925 | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Ads, plus retrieved cases: micro F1 | 0.965 | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Ads, plus self-check (full agent): micro F1 | 0.971 | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Reviews, short prompt: micro F1 | 0.715 | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Reviews, whole rulebook in the prompt: micro F1 | 0.782 | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Reviews, agent that reads rules: micro F1 | 0.799 | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Reviews, plus retrieved cases: micro F1 | 0.812 | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Reviews, plus self-check (full agent): micro F1 | 0.824 | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Compliant look-alike ads given a label, short prompt | 12/32 (37.5%, 95% CI 22.9–54.7%) | lower is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Compliant look-alike ads given a label, full agent | 0/32 (0.0%, 95% CI 0.0–10.7%) | lower is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Ad misses (a labelled ad given no label), short prompt | 5/67 (7.5%, 95% CI 3.2–16.3%) | lower is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Ad misses, full agent | 1/67 (1.5%, 95% CI 0.3–8.0%) | lower is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Ad false alarms (an unlabelled ad given a label), short prompt | 15/52 (28.8%, 95% CI 18.3–42.3%) | lower is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Ad false alarms, full agent | 0/52 (0.0%, 95% CI 0.0–6.9%) | lower is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Reviews, quotes that are the item's own words, short prompt | 1303/1330 (98.0%, 95% CI 97.1–98.6%) | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Reviews, quotes that are the item's own words, full agent | 1115/1115 (100.0%, 95% CI 99.7–100.0%) | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Ads, full agent: cost per 1,000 items | US$0.53 | lower is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Reviews, retrieved cases without self-check: cost per 1,000 items | US$0.91 | lower is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Reviews, full agent: cost per 1,000 items | US$1.59 | lower is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |

Each added piece helps on both tasks; on ads the gain is mostly no longer flagging compliant look-alikes. Reviews top out lower, which ties to their gold labels (see root causes).

### Test A: preregistered comparisons (B minus A, micro F1)

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Ads: rule-reading agent minus short prompt | +0.157 (95% CI [+0.106, +0.214]) | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Reviews: rule-reading agent minus short prompt | +0.083 (95% CI [+0.064, +0.102]) | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Ads: with retrieved cases minus without | +0.040 (95% CI [+0.007, +0.076]) | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Reviews: with retrieved cases minus without | +0.014 (95% CI [+0.003, +0.024]) | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Ads: with self-check minus without | +0.006 (95% CI [-0.023, +0.038]) | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Reviews: with self-check minus without | +0.012 (95% CI [+0.001, +0.023]) | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Ads: rule-reading agent minus whole rulebook in the prompt | +0.047 (95% CI [-0.004, +0.097]) | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Reviews: rule-reading agent minus whole rulebook in the prompt | +0.017 (95% CI [+0.000, +0.033]) | higher is better | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| Reviews: real case library minus synthetic | +0.010 (95% CI [-0.001, +0.022]) | context only | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |

Reading rules and retrieved cases are measured gains on both tasks; the self-check on reviews only; against the whole rulebook in the prompt, the agent shows no measured difference on ads.

### Root causes: the full agent's wrong decisions on test A

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Reviews: wrong label decisions | 406 | lower is better | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| Reviews: both classifications agree | 257/406 (63.3%, 95% CI 58.5–67.8%) | higher is better | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| Reviews: label ambiguity | 158 | context only | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| Reviews: prompt defect | 61 | context only | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| Reviews: model capability | 20 | context only | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| Reviews: rule conflict | 18 | context only | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| Reviews: classifications disagree (split) | 149 | context only | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| Reviews: decisions wrong in every arm | 194 | context only | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| Review test A: reviews with a strong cue for a label they lack (data acceptance A10: in the training split the phrase comes with the label at least 0.95 of the time; a lower bound on unlabelled mentions) | 7/201 (3.5%, 95% CI 1.7–7.0%) | context only | [`labelling-agent-kit/results/acceptance.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/acceptance.json) |
| Ads: both classifications agree | 3/4 (75.0%, 95% CI 30.1–95.4%) | higher is better | [`labelling-agent-kit/results/main/rca/ad_policy-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/ad_policy-test_a-agent-cases-check.json) |

On reviews the largest class is label ambiguity, and nearly half of the wrong decisions were wrong in every arm: that part is bounded by the gold labels and is reported, not fitted. The fixable part is rules and flow: labels the prompt never led the agent to consider, a self-check that deleted labels the dataset's conventions require, and a general rule that clashes with those conventions (prices, deals, mall locations).

### The revision built from root causes: unseen test B

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Reviews, v1: micro F1 | 0.834 | higher is better | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| Reviews, v2: micro F1 | 0.852 | higher is better | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| Reviews: v2 minus v1 | +0.018 (95% CI [+0.005, +0.031]) | higher is better | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| Ads, v1: micro F1 | 0.971 | higher is better | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| Ads, v2: micro F1 | 0.993 | higher is better | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| Ads: v2 minus v1 | +0.021 (95% CI [+0.000, +0.048]) | higher is better | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| Reviews, test A re-check: v2 minus v1 (the changes were written from test A's failures, so this row is for completeness, not evidence) | +0.017 (95% CI [+0.003, +0.031]) | context only | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| Ads, test A re-check: v2 minus v1 | +0.014 (95% CI [-0.018, +0.048]) | context only | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| All model calls in the project (batch prices) | US$3.6325 | lower is better | [`labelling-agent-kit/results/costs.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/costs.json) |

Reviews: a measured gain on unseen items, sitting on the price, deal and location labels the changes aimed at; adopted. Ads: slightly higher, but the interval's lower end is 0, so by the rule set beforehand it is not a gain and is not adopted; v1 made only four errors on test A, leaving little to measure.

## Grader calibration

- Gold labels: for ads, the answers fixed when each ad was written; for reviews, the annotations that ship with the ASAP dataset; no labels were collected for this project.
- Root causes are judgements: each wrong decision gets code-computed signals and is then classified twice, independently; agreement is reported and disagreements are listed as split.

## Limitations and failure cases

- Each arm labelled each item once; sampling variance is not in the item-bootstrap intervals, and several differences sit close to the edge (rules versus the whole rulebook on reviews, the half-and-half library, the ads revision).
  - Recommendation: Before relying on the close calls, run them several more times and confirm they hold.
- The ad items come from the same projects as the ad rulebook (Grounded Review and Policy Model Lab), with answers fixed by construction rather than by independent annotators; the full agent is near the ceiling on ads.
  - Recommendation: Before real use, build a test set from business items with settled outcomes.
- The review gold labels leave out some mentions: 7 of the 201 test A reviews contain a phrase that almost always comes with a label in the training split, yet lack that label; 158 decisions were classed as label ambiguity. Precision on reviews is bounded by this, and some of the agent's "errors" may be labels the dataset arguably should have.
  - Recommendation: Hand the ambiguous or unlabelled cases to whoever sets the standard, settle the labelling rules first, then compare arms.
- The synthetic reviews are shorter than real ones and were generated from the same rulebook the agent reads; a different generator could change the real-versus-synthetic result.
  - Recommendation: Build another library with a different generator or prompt and repeat the comparison.

## Versions

- **1.0** (2026-11-18) First card, from the result files in the public labelling-agent-kit repository.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.

Sources and licences of third-party data, models and code are listed in the [project repository](https://github.com/llia0031-dotcom/labelling-agent-kit).
