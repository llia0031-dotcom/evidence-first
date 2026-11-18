"""Offline tests: no model calls, no network. The last test needs the project folders next to this
repository and is skipped when they are absent (for example in CI)."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_cards as bc  # noqa: E402
import extractors as ex  # noqa: E402
import prompts as pr  # noqa: E402
from stats import bootstrap_median_ci, wilson  # noqa: E402


class FakeReader(bc.Reader):
    """Reads from a temporary folder instead of the projects."""

    def __init__(self, base: Path):
        super().__init__()
        self.base = base

    def path(self, rel: str) -> Path:
        p = self.base / rel
        self.seen[rel] = "test"
        return p


class Stats(unittest.TestCase):
    def test_wilson_known_values(self):
        lo, hi = wilson(191, 192)
        self.assertAlmostEqual(lo, 0.9711, places=3)
        self.assertAlmostEqual(hi, 0.9991, places=3)
        lo, hi = wilson(0, 8)
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 0.3244, places=3)

    def test_wilson_rejects_bad_counts(self):
        with self.assertRaises(ValueError):
            wilson(5, 4)

    def test_bootstrap_is_reproducible(self):
        vals = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        self.assertEqual(bootstrap_median_ci(vals), bootstrap_median_ci(vals))


class Prose(unittest.TestCase):
    def test_bare_numbers_are_rejected(self):
        for text in ("判对 191/192", "费用是 17%", "rate 0.5%"):
            with self.assertRaises(bc.BuildError):
                bc.lint_prose(text, "test")

    def test_placeholders_and_plain_numbers_pass(self):
        bc.lint_prose("判对 {heldout_oneshot}，32 条条款，v1.3，claude-haiku-5-5", "test")

    def test_fill(self):
        v = bc.Value(kind="proportion", k=3, n=24, ci=wilson(3, 24))
        self.assertEqual(bc.fill("从 {a} 降", {"a": v}, "zh", "t"), "从 3/24 降")
        self.assertEqual(bc.fill("{a:pct}", {"a": v}, "zh", "t"), "12%")

    def test_record_matching(self):
        v = bc.Value(kind="proportion", k=2379, n=2736, ci=wilson(2379, 2736))
        self.assertTrue(bc.matches_record(v, "87.0%"))
        self.assertTrue(bc.matches_record(v, "2379/2736"))
        self.assertFalse(bc.matches_record(v, "87.1%"))


class Extractors(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.rd = FakeReader(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write(self, name: str, text: str) -> str:
        (self.tmp / name).write_text(text, encoding="utf-8")
        return name

    def test_md_cell_sections_and_arrows(self):
        name = self.write("s.md", "\n".join([
            "# Report", "## Free answers", "| | plain | skill |", "|---|---|---|",
            "| **Answers with an invented number** | 4/32 | 0/32 |",
            "## Script", "| Rule | Correct (old → new) |", "|---|---|", "| **Total** | **0/11 → 11/11** |",
        ]))
        self.assertEqual(ex.md_cell(self.rd, name, "Answers with an invented number", "plain", section="Free"), {"k": 4, "n": 32})
        self.assertEqual(ex.md_cell(self.rd, name, "Total", "Correct (old → new)", part="before"), {"k": 0, "n": 11})
        self.assertEqual(ex.md_cell(self.rd, name, "Total", "Correct (old → new)", part="after"), {"k": 11, "n": 11})

    def test_json_counts_and_rows(self):
        name = self.write("r.json", json.dumps({
            "oneshot": {"counts": {"items": 192, "tp": 124, "tn": 67, "fp": 1}},
            "summary": [{"method": "a", "lang": "all", "hit5": 44, "n": 45, "mrr": 0.839}],
        }))
        self.assertEqual(ex.json_counts(self.rd, name, arm="oneshot", num=["tp", "tn"], den="items"), {"k": 191, "n": 192})
        self.assertEqual(ex.json_counts(self.rd, name, arm="oneshot", num="tp", den="items", minus_den=["tn", "fp"]), {"k": 124, "n": 124})
        self.assertEqual(ex.json_row(self.rd, name, "summary", {"method": "a", "lang": "all"}, "hit5", "n"), {"k": 44, "n": 45})

    def test_multiturn_keeps_last_clean_row(self):
        rows = [{"item": "a", "run": 1, "errors": ["boom"]},
                {"item": "a", "run": 1, "errors": [], "advice_raw_problems": ["x"]},
                {"item": "a", "run": 1, "errors": [], "advice_raw_problems": []},
                {"item": "b", "run": 1, "errors": [], "advice_raw_problems": ["y"]}]
        name = self.write("m.jsonl", "\n".join(json.dumps(r) for r in rows))
        self.assertEqual(ex.gr_multiturn(self.rd, name, "advice_raw_problems"), {"k": 1, "n": 2})


class Specs(unittest.TestCase):
    """Catch TOML keys that land inside the wrong table (a key after [out_of_scope] belongs to it)."""

    def test_spec_shape(self):
        required = {"id", "order", "layer", "status", "card_version", "updated", "name", "problem",
                    "primary_metric", "summary", "uses", "out_of_scope", "eval", "limitation", "version"}
        for spec in bc.load_specs():
            with self.subTest(spec=spec["_file"]):
                self.assertTrue(required <= set(spec), required - set(spec))
                for key in ("uses", "out_of_scope"):
                    self.assertEqual(set(spec[key]), {"zh", "en"})
                if "judge" in spec:
                    self.assertEqual(set(spec["judge"]), {"zh", "en"})
                self.assertIn(spec["layer"], bc.LAYERS)


class Labels(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.orig = pr.LABELS
        pr.LABELS = self.tmp / "labels.json"
        shutil.copy(self.orig, pr.LABELS)

    def tearDown(self):
        pr.LABELS = self.orig
        shutil.rmtree(self.tmp)

    def test_production_only_from_staging(self):
        self.assertEqual(pr.cmd_promote("grounded-review/advice", "v1.1", "production", "test"), 1)

    def test_not_adopted_cannot_go_live(self):
        self.assertEqual(pr.cmd_promote("grounded-review/advice", "v1.2", "staging", "test"), 0)
        self.assertEqual(pr.cmd_promote("grounded-review/advice", "v1.2", "production", "test"), 1)

    def test_rollback_moves_to_previous_production(self):
        self.assertEqual(pr.cmd_rollback("grounded-review/advice", "test"), 0)
        labels = json.loads(pr.LABELS.read_text(encoding="utf-8"))
        self.assertEqual(labels["grounded-review/advice"]["production"], "v1.1")
        self.assertEqual(labels["grounded-review/advice"]["history"][-1]["reason"], "rollback: test")

    def test_labels_point_at_registered_versions(self):
        labels = pr.load_labels()
        for a in pr.load_registry():
            ids = {v["id"] for v in a["version"]}
            self.assertIn(labels[a["asset"]]["production"], ids)
            self.assertIn(labels[a["asset"]]["staging"], ids)


PROJECT_FOLDERS = ["evidence-check-public", "cairn-public", "grounded-review-public", "sellpoint-check", "screening-audit",
                   "voice-agent-eval", "evidence-pipeline-public", "grounded-business-review-public",
                   "creator-skills-public", "policy-model-lab-public", "judge-calibration-public",
                   "labelling-agent-kit-public", "agent-trace-eval-public",
                   "launchpad-tracedesk", "aigc-scene-eval"]


@unittest.skipUnless(all((bc.PORTFOLIO / f).is_dir() for f in PROJECT_FOLDERS),
                     "needs every project folder next to this repository (two are not public)")
class AgainstProjects(unittest.TestCase):
    def test_cards_match_project_records(self):
        self.assertEqual(bc.main(["--check"]), 0)

    def test_registry_is_current(self):
        self.assertEqual(pr.cmd_build(check=True), 0)

    def test_content_drafts_build(self):
        import build_content
        with tempfile.TemporaryDirectory() as tmp:
            data_path = bc.DATA / "content.json"
            before = data_path.read_text(encoding="utf-8") if data_path.exists() else None
            try:
                self.assertEqual(build_content.main(["--out", tmp]), 0)
                claims = json.loads((Path(tmp) / "claims.json").read_text(encoding="utf-8"))["claims"]
                self.assertTrue(claims and all(c["evidence"][0]["quote"] for c in claims))
            finally:
                if before is not None:
                    data_path.write_text(before, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    unittest.main()
