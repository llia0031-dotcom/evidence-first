# Text on Product: Chinese copy on AI product images: evaluation card

> Card version 1.2 · Data as of 2026-11-15 · public
>
> Numbers are computed by `scripts/build_cards.py` from the project's result files; proportions carry a Wilson 95% interval.

| When | Team | Stack | Links |
|---|---|---|---|
| 2026-11-12 – 2026-11-14 | Liang Liyuan | Seedream and Seedance through the BytePlus API, RapidOCR, in-browser OCR | [Guide](https://jason-d-e.github.io/text-on-product/) · [Pre-listing checker](https://jason-d-e.github.io/text-on-product/check/) · [Code](https://github.com/Jason-d-e/text-on-product) |

**Problem**: When Seedream makes Chinese product images, does the selling-point text come out exactly; how to write and lay it out so the text holds; how to check before listing.

**What I did**: I fixed 20 tasks and froze the rubric before generation, checked the text in every image character by character with OCR and rated each work three times against the rubric; turned the findings into a guide for merchants and built an in-browser pre-listing checker that never uploads the image.

**Results**: 

- Images with exactly right text: Seedream 4.5 16/16, 4.0 15/16, 5.0 lite 16/16
- Image-to-video clips with exactly right text: 1/4

## Summary

Twenty fixed tasks (16 images, 4 videos) test how reliably Seedream 4.0, 4.5 and 5.0 lite and Seedance 1.0 pro render Chinese selling-point text. Text in every image is checked character by character with OCR, with doubtful cases compared against the image; every work is rated three times, independently, against a rubric. The results became a guide for merchants plus an in-browser pre-listing checker: drop in a product image and the required text, and it lists line by line what differs or was added, without uploading the image.

- **Place in the portfolio**: Scenario: generation
- **Link to the core component**: The generation scenario: the same word-for-word idea applied to text inside images. It has its own OCR check and does not call the evidence-check script.
- **Models used**: Generation with Seedream 4.0, 4.5, 5.0 lite and Seedance 1.0 pro through the BytePlus API (free quota); OCR with RapidOCR (PP-OCRv6).

## Uses

- Guide merchants writing prompts for Chinese product images: which wording keeps text stable and what to recheck after generation.
- Check before listing that the text in the image matches the required copy exactly.

## Out of scope

- Only three Seedream versions were tested, not other vendors' models, and through the API rather than the web app.
- One generation per task; only Chinese characters, letters and digits are compared, not symbols; misses on artistic fonts were not measured.
- Simplified Chinese only; no buyer research.

## Evaluation data

### Main evaluation: 16 image tasks and 4 video tasks

Tasks in four tiers of text difficulty (short title, title with numbers, several lines of selling points, mixed scripts with vertical text and small packaging print); tasks and rubric frozen before generation. One generation per version per task.

| Field | Value |
|---|---|
| Date | 2026-11-12 |
| Items and answers | 16 images per image version, 4 videos |
| Runs | 1 generation per task; 3 ratings |
| Model and send mode | BytePlus API, free quota |
| Frozen before the run | `data/freeze.json` (task and rubric hashes) |

## Metrics and results

Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ.

### Main evaluation: 16 image tasks and 4 video tasks

| Metric | Result | Direction | Source file |
|---|---|---|---|
| Images with exactly right text (Seedream 4.5) | 16/16 (100.0%, 95% CI 80.6–100.0%) | higher is better | `aigc-scene-eval/report/results.json` |
| Images with exactly right text (Seedream 4.0) | 15/16 (93.8%, 95% CI 71.7–98.9%) | higher is better | `aigc-scene-eval/report/results.json` |
| Images with exactly right text (Seedream 5.0 lite) | 16/16 (100.0%, 95% CI 80.6–100.0%) | higher is better | `aigc-scene-eval/report/results.json` |
| Videos with exactly right text (Seedance 1.0 pro) | 1/4 (25.0%, 95% CI 4.6–69.9%) | higher is better | `aigc-scene-eval/report/results.json` |
| Overall rating (Seedream 4.5, out of 5) | 4.29 (mean, n=48, 95% CI 4.03–4.56) | higher is better | `aigc-scene-eval/report/results.json` |
| Overall rating (Seedream 4.0) | 4.21 (mean, n=48, 95% CI 3.93–4.46) | higher is better | `aigc-scene-eval/report/results.json` |
| Overall rating (Seedream 5.0 lite) | 3.76 (mean, n=48, 95% CI 3.50–4.02) | higher is better | `aigc-scene-eval/report/results.json` |
| Rated usable as is (Seedream 4.5) | 30/48 (62.5%, 95% CI 48.4–74.8%) | higher is better | `aigc-scene-eval/report/results.json` |
| Rated usable as is (Seedream 5.0 lite) | 21/48 (43.8%, 95% CI 30.7–57.7%) | higher is better | `aigc-scene-eval/report/results.json` |
| OCR self-check: characters misread in known text | 2/1332 (0.2%, 95% CI 0.0–0.5%) | lower is better | `aigc-scene-eval/report/results.json` |
| Planted text errors caught by OCR | 80/80 (100.0%, 95% CI 95.4–100.0%) | higher is better | `aigc-scene-eval/report/results.json` |

Image text is almost always right, with one wrong digit from 4.0; video text does not hold. In appearance 4.5 and 4.0 are close and 5.0 lite is clearly lower.

## Grader calibration

- Text correctness is not rated: OCR compares character by character. OCR was first self-checked on known text (2/1332 characters wrong) and then on images with planted errors (80/80 caught).
- Appearance is rated three times, independently, against a rubric, with works shuffled and versions hidden; agreement between the three is in the project report. There is no comparison with blind ratings by buyers, which is a limit.

## Limitations and failure cases

- Small sample: 16 image and 4 video tasks, one generation each; only 1/4 videos have exactly right text.
  - Recommendation: Add text to videos in editing rather than relying on generation.
- Ratings were not compared with blind ratings by buyers; all three come from the same rating method.
  - Recommendation: Before launch, have a few real buyers blind-rate a small set and compare with the rubric.
- The prompt mini-experiment has only a few images: stating the text colour worked, asking for a large title with top margin did not reliably help.
  - Recommendation: After generation, check whether the title was clipped and regenerate if so.

## Versions

- **1.0** (2026-11-15) First card. Only the site is public; the report and data are internal.
- **1.1** (2026-11-15) Added when, team, stack, links and "problem / what I did / results" at the top, the way portfolio case studies open; the evaluation sections are unchanged.
- **1.2** (2026-11-17) Corrected: the tasks have four difficulty tiers, not three; the limit now says ratings were not compared with blind ratings by buyers. Numbers unchanged.

## Provenance

Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`.

Sources and licences of third-party data, models and code are listed in the [project repository](https://github.com/Jason-d-e/text-on-product).
