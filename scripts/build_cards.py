"""Build one evaluation card per project, the README project table and the JSON data files.

Every number on a card is computed here from the project's own result files; the specs in
cards/specs/*.toml only say which file and which rule to use. Prose in a spec may refer to a
number only through a placeholder such as {heldout_oneshot}; a bare fraction or percentage in
prose is an error.

Usage (from evidence-first/):
    python scripts/build_cards.py          # build cards/*.md, data/*.json, README.md, README.en.md
    python scripts/build_cards.py --check  # build in memory only; fail on any mismatch or changed source
Standard library only (Python 3.11+).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # evidence-first/
PORTFOLIO = ROOT.parent                 # folder that holds every project side by side
sys.path.insert(0, str(HERE))

import extractors  # noqa: E402
from stats import bootstrap_median_ci, wilson  # noqa: E402

SPECS = ROOT / "cards" / "specs"
CARDS = ROOT / "cards"
DATA = ROOT / "data"
LOCK = ROOT / "cards" / "sources.lock.json"

LAYERS = {
    "core": ("核心部件", "Core component"),
    "retrieval": ("场景：检索问答", "Scenario: grounded Q&A"),
    "judgement": ("场景：判断类", "Scenario: judgement"),
    "generation": ("场景：生成类", "Scenario: generation"),
    "interaction": ("场景：交互类", "Scenario: interaction"),
    "operations": ("运营层", "Operations"),
}
DIRECTION = {
    "higher": ("越高越好", "higher is better"),
    "lower": ("越低越好", "lower is better"),
    "none": ("只作说明", "context only"),
}
BARE_NUMBER = re.compile(r"(?<![\w.{])\d+(?:\.\d+)?\s*/\s*\d+(?![\w}])|(?<![\w.{])\d+(?:\.\d+)?\s*%")
PLACEHOLDER = re.compile(r"\{([a-z0-9_]+)(?::([a-z]+))?\}")


class BuildError(Exception):
    pass


# --------------------------------------------------------------------------- values
@dataclass
class Value:
    kind: str                     # proportion | median | mean | value
    k: int | None = None
    n: int | None = None
    value: float | None = None
    unit: str = ""                # for value / median: "s", "usd", "" ...
    decimals: int = 1
    ci: tuple[float, float] | None = None
    sources: list[str] = field(default_factory=list)

    @property
    def pct(self) -> float:
        return 100.0 * self.k / self.n

    def short(self, lang: str) -> str:
        if self.kind == "proportion":
            return f"{self.k}/{self.n}"
        return fmt_unit(self.value, self.unit, self.decimals, lang)

    def full(self, lang: str) -> str:
        if self.kind == "proportion":
            lo, hi = self.ci
            ci = f"{100*lo:.1f}–{100*hi:.1f}%"
            if lang == "zh":
                return f"{self.k}/{self.n}（{self.pct:.1f}%，95% 区间 {ci}）"
            return f"{self.k}/{self.n} ({self.pct:.1f}%, 95% CI {ci})"
        if self.kind == "median":
            lo, hi = self.ci
            v = fmt_unit(self.value, self.unit, self.decimals, lang)
            rng = f"{lo:.{self.decimals}f}–{hi:.{self.decimals}f}"
            if lang == "zh":
                return f"{v}（中位数，n={self.n}，95% 区间 {rng}）"
            return f"{v} (median, n={self.n}, 95% CI {rng})"
        v = fmt_unit(self.value, self.unit, self.decimals, lang)
        if self.kind == "mean":
            lo, hi = self.ci
            rng = f"{lo:.{self.decimals}f}–{hi:.{self.decimals}f}"
            n = f"，n={self.n}" if self.n else ""
            n_en = f", n={self.n}" if self.n else ""
            return f"{v}（均值{n}，95% 区间 {rng}）" if lang == "zh" else f"{v} (mean{n_en}, 95% CI {rng})"
        if self.n:
            return f"{v}（n={self.n}）" if lang == "zh" else f"{v} (n={self.n})"
        return v

    def as_json(self) -> dict:
        d = {"kind": self.kind, "sources": shown_sources(self.sources)}
        if self.kind == "proportion":
            d.update(k=self.k, n=self.n, rate=round(self.k / self.n, 4),
                     ci95=[round(self.ci[0], 4), round(self.ci[1], 4)])
        else:
            d.update(value=self.value, unit=self.unit, n=self.n)
            if self.ci:
                d["ci95"] = [round(self.ci[0], 4), round(self.ci[1], 4)]
        return d


def fmt_unit(v: float, unit: str, decimals: int, lang: str) -> str:
    num = f"{v:.{decimals}f}"
    if unit == "s":
        return f"{num} 秒" if lang == "zh" else f"{num} s"
    if unit == "usd":
        return f"{num} 美元" if lang == "zh" else f"US${num}"
    if unit == "x":
        return f"{num} 倍" if lang == "zh" else f"{num}×"
    if unit == "pct":
        return f"{num}%"
    return num


class Reader:
    """Reads project files and remembers each file's fingerprint."""

    def __init__(self) -> None:
        self.seen: dict[str, str] = {}

    def path(self, rel: str) -> Path:
        p = (PORTFOLIO / rel).resolve()
        if not p.is_file():
            raise BuildError(f"missing source file: {rel}")
        self.seen[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
        return p

    def text(self, rel: str) -> str:
        return self.path(rel).read_text(encoding="utf-8")

    def json(self, rel: str):
        return json.loads(self.text(rel))

    def jsonl(self, rel: str) -> list[dict]:
        return [json.loads(line) for line in self.text(rel).splitlines() if line.strip()]


def compute(metric: dict, project: str) -> Value:
    name = metric["extractor"]
    fn = extractors.REGISTRY.get(name)
    if fn is None:
        raise BuildError(f"{project}.{metric['id']}: unknown extractor {name}")
    rd = Reader()
    raw = fn(rd, **metric.get("args", {}))
    kind = raw.get("kind", "proportion")
    v = Value(kind=kind, sources=sorted(rd.seen), decimals=metric.get("decimals", raw.get("decimals", 1)))
    v._hashes = rd.seen  # type: ignore[attr-defined]
    if kind == "proportion":
        v.k, v.n = int(raw["k"]), int(raw["n"])
        v.ci = wilson(v.k, v.n)
    elif kind == "median":
        vals = [float(x) for x in raw["values"]]
        v.n = len(vals)
        import statistics
        v.value = statistics.median(vals)
        v.ci = bootstrap_median_ci(vals)
        v.unit = raw.get("unit", "")
    else:
        v.value = float(raw["value"])
        v.unit = raw.get("unit", "")
        v.n = raw.get("n")
        if kind == "mean":
            v.ci = tuple(raw["ci"])
    return v


def matches_record(v: Value, record: str) -> bool:
    record = record.strip()
    if "/" in record:
        k, n = (int(x) for x in record.split("/"))
        return v.kind == "proportion" and (v.k, v.n) == (k, n)
    if record.endswith("%"):
        num = record[:-1]
        dec = len(num.split(".")[1]) if "." in num else 0
        val = v.pct if v.kind == "proportion" else v.value
        return f"{val:.{dec}f}" == num
    dec = len(record.split(".")[1]) if "." in record else 0
    val = v.value if v.kind != "proportion" else v.k / v.n
    return f"{val:.{dec}f}" == record


# --------------------------------------------------------------------------- prose
def lint_prose(text: str, where: str) -> None:
    for m in BARE_NUMBER.finditer(PLACEHOLDER.sub("", text)):
        raise BuildError(f"{where}: bare number '{m.group(0)}' in prose; use a placeholder")


def fill(text: str, values: dict[str, Value], lang: str, where: str) -> str:
    lint_prose(text, where)

    def sub(m: re.Match) -> str:
        key, mode = m.group(1), m.group(2) or "short"
        if key not in values:
            raise BuildError(f"{where}: unknown placeholder {{{key}}}")
        v = values[key]
        if mode == "short":
            return v.short(lang)
        if mode == "full":
            return v.full(lang)
        if mode == "pct":
            return f"{v.pct:.0f}%"
        if mode == "pct1":
            return f"{v.pct:.1f}%"
        if mode == "k":
            return str(v.k)
        if mode == "n":
            return str(v.n)
        raise BuildError(f"{where}: unknown placeholder mode {mode}")

    return PLACEHOLDER.sub(sub, text)


def tr(obj, lang: str):
    """Pick the language variant of a spec field ({zh=..., en=...} or a plain string)."""
    if isinstance(obj, dict) and ("zh" in obj or "en" in obj):
        return obj.get(lang) or obj.get("zh")
    return obj


# --------------------------------------------------------------------------- build
def load_specs() -> list[dict]:
    specs = []
    for p in sorted(SPECS.glob("*.toml")):
        with p.open("rb") as f:
            s = tomllib.load(f)
        s["_file"] = p.name
        specs.append(s)
    specs.sort(key=lambda s: s.get("order", 99))
    return specs


def build_project(spec: dict, problems: list[str]) -> dict:
    pid = spec["id"]
    values: dict[str, Value] = {}
    hashes: dict[str, str] = {}
    for ev in spec.get("eval", []):
        for m in ev.get("metric", []):
            mid = m["id"]
            if mid in values:
                raise BuildError(f"{pid}: duplicate metric id {mid}")
            v = compute(m, pid)
            values[mid] = v
            hashes.update(v._hashes)  # type: ignore[attr-defined]
            if "record" in m and not matches_record(v, m["record"]):
                problems.append(f"{pid}.{mid}: computed {v.short('zh')} but the project record says "
                                f"{m['record']} ({m.get('record_src', 'no source given')})")
    return {"spec": spec, "values": values, "hashes": hashes}


def render_card(proj: dict, lang: str) -> str:
    s, vals = proj["spec"], proj["values"]
    pid = s["id"]
    zh = lang == "zh"
    L = (lambda a, b: a if zh else b)  # noqa: E731
    out: list[str] = []
    name = tr(s["name"], lang)
    out.append(f"# {name}：{L('评测卡', 'evaluation card')}" if zh else f"# {name}: evaluation card")
    out.append("")
    status = L("已公开", "public") if s["status"] == "public" else L("未公开", "not public")
    links = " · ".join(f"[{tr(l['label'], lang)}]({tr(l['url'], lang)})" for l in s.get("links", [])) or status
    meta = [f"{L('卡片版本', 'Card version')} {s['card_version']}",
            f"{L('数据截至', 'Data as of')} {s['updated']}", status]
    out.append("> " + " · ".join(meta))
    out.append(">")
    out.append("> " + L("数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。",
                         "Numbers are computed by `scripts/build_cards.py` from the project's result files; "
                         "proportions carry a Wilson 95% interval."))
    out.append("")
    # Case header, the way portfolio case studies open: a metadata row, then problem / what I did / result.
    out.append(f"| {L('时间', 'When')} | {L('团队', 'Team')} | {L('技术', 'Stack')} | {L('链接', 'Links')} |")
    out.append("|---|---|---|---|")
    out.append(f"| {tr(s['period'], lang)} | {tr(s['team'], lang)} | {tr(s['stack'], lang)} | {links} |")
    out.append("")
    sep = "：" if zh else ": "
    problem = fill(tr(s['problem'], lang), vals, lang, f'{pid}.problem')
    if not problem.endswith(("。", "？", ".", "?")):
        problem += "。" if zh else "."
    out.append(f"**{L('问题', 'Problem')}**{sep}{problem}")
    out.append("")
    out.append(f"**{L('我做了什么', 'What I did')}**{sep}{fill(tr(s['did'], lang), vals, lang, f'{pid}.did')}")
    out.append("")
    out.append(f"**{L('结果', 'Results')}**{sep}")
    out.append("")
    for h in s.get("headline", []):
        out.append(f"- {fill(tr(h, lang), vals, lang, f'{pid}.headline')}")
    out.append("")
    out.append(L("## 概况", "## Summary"))
    out.append("")
    out.append(fill(tr(s["summary"], lang), vals, lang, f"{pid}.summary"))
    out.append("")
    out.append(f"- **在作品集里的位置**：{LAYERS[s['layer']][0]}" if zh
               else f"- **Place in the portfolio**: {LAYERS[s['layer']][1]}")
    for key, label in (("core_link", L("和核心部件的关系", "Link to the core component")),
                       ("models", L("用到的模型", "Models used"))):
        if key in s:
            sep = "：" if zh else ": "
            out.append(f"- **{label}**{sep}{fill(tr(s[key], lang), vals, lang, f'{pid}.{key}')}")
    out.append("")
    for key, title in (("uses", L("## 用途", "## Uses")),
                       ("out_of_scope", L("## 不适用的地方", "## Out of scope"))):
        out.append(title)
        out.append("")
        for item in tr(s[key], lang):
            out.append(f"- {fill(item, vals, lang, f'{pid}.{key}')}")
        out.append("")

    out.append(L("## 评测数据", "## Evaluation data"))
    out.append("")
    for ev in s["eval"]:
        out.append(f"### {tr(ev['name'], lang)}")
        out.append("")
        out.append(fill(tr(ev["data"], lang), vals, lang, f"{pid}.{ev['id']}.data"))
        out.append("")
        rows = [(L("日期", "Date"), ev["date"]),
                (L("题目和答案", "Items and answers"), fill(tr(ev["items"], lang), vals, lang, f"{pid}.{ev['id']}.items")),
                (L("跑了几次", "Runs"), fill(tr(ev["runs"], lang), vals, lang, f"{pid}.{ev['id']}.runs")),
                (L("模型和发送方式", "Model and send mode"), tr(ev["setup"], lang))]
        if "frozen" in ev:
            rows.append((L("跑前冻结", "Frozen before the run"), tr(ev["frozen"], lang)))
        out.append(f"| {L('项目', 'Field')} | {L('内容', 'Value')} |")
        out.append("|---|---|")
        for a, b in rows:
            out.append(f"| {a} | {b} |")
        out.append("")

    out.append(L("## 指标和结果", "## Metrics and results"))
    out.append("")
    out.append(L("每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。",
                 "Each evaluation version has its own table. Scores are not compared across versions whose items or scoring rules differ."))
    out.append("")
    for ev in s["eval"]:
        out.append(f"### {tr(ev['name'], lang)}")
        out.append("")
        out.append(f"| {L('指标', 'Metric')} | {L('结果', 'Result')} | {L('方向', 'Direction')} | {L('来源文件', 'Source file')} |")
        out.append("|---|---|---|---|")
        for m in ev["metric"]:
            v = vals[m["id"]]
            label = fill(tr(m["label"], lang), vals, lang, f"{pid}.{m['id']}.label")
            if "note" in m:
                label += L("（", " (") + fill(tr(m["note"], lang), vals, lang, f"{pid}.{m['id']}.note") + L("）", ")")
            src = "<br>".join(source_md(p) for p in v.sources)
            out.append(f"| {label} | {v.full(lang)} | {DIRECTION[m.get('direction', 'higher')][0 if zh else 1]} | {src} |")
        out.append("")
        if "takeaway" in ev:
            out.append(fill(tr(ev["takeaway"], lang), vals, lang, f"{pid}.{ev['id']}.takeaway"))
            out.append("")

    if "judge" in s:
        out.append(L("## 评分器校准", "## Grader calibration"))
        out.append("")
        for item in tr(s["judge"], lang):
            out.append(f"- {fill(item, vals, lang, f'{pid}.judge')}")
        out.append("")

    out.append(L("## 局限和失败案例", "## Limitations and failure cases"))
    out.append("")
    for lim in s["limitation"]:
        text = fill(tr(lim["text"], lang), vals, lang, f"{pid}.limitation")
        out.append(f"- {text}")
        if "advice" in lim:
            adv = fill(tr(lim["advice"], lang), vals, lang, f"{pid}.limitation.advice")
            out.append(f"  - {L('建议', 'Recommendation')}{L('：', ': ')}{adv}")
    out.append("")

    out.append(L("## 版本", "## Versions"))
    out.append("")
    for ver in s["version"]:
        out.append(f"- **{ver['id']}**（{ver['date']}）{fill(tr(ver['text'], lang), vals, lang, f'{pid}.version')}" if zh
                   else f"- **{ver['id']}** ({ver['date']}) {fill(tr(ver['text'], lang), vals, lang, f'{pid}.version')}")
    out.append("")
    out.append(L("## 出处", "## Provenance"))
    out.append("")
    out.append(L("模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。",
                 "Sections follow the Hugging Face model card template (Apache-2.0); the source file and fingerprint of every number are in `cards/sources.lock.json`."))
    repo = next((tr(l["url"], lang) for l in s.get("links", []) if "github.com/" in tr(l["url"], lang)), None)
    if s["status"] == "public" and repo:
        out.append("")
        out.append(L(f"第三方数据、模型和代码的来源与许可，见[项目仓库]({repo})里的说明。",
                     f"Sources and licences of third-party data, models and code are listed in the [project repository]({repo})."))
    out.append("")
    return "\n".join(out)


def short_src(rel: str) -> str:
    return rel.replace("\\", "/")


def _load_toml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("rb") as f:
        return tomllib.load(f)


PUBLIC_MAP = _load_toml(ROOT / "cards" / "public_sources.toml").get("map", [])
# The public copy is built without the export script; there, data files name public repositories
# instead of local folder names and leave out images that are not published.
PUBLIC_BUILD = not (HERE / "export_public.py").exists()
WITHHOLD = set(_load_toml(ROOT / "cards" / "hold.toml").get("withhold", []))


def public_source(rel: str) -> tuple[str, str | None]:
    """(text to show, public URL or None) for a source file path."""
    rel = short_src(rel)
    for m in PUBLIC_MAP:
        if rel.startswith(m["prefix"]):
            rest = rel[len(m["prefix"]):]
            return f"{m['repo']}/{rest}", m["url"] + rest
    return rel, None


def shown_sources(rels: list[str]) -> list[str]:
    """Source paths as written into data files: public repository paths in the public build."""
    return [public_source(r)[0] for r in rels] if PUBLIC_BUILD else list(rels)


def source_md(rel: str) -> str:
    text, url = public_source(rel)
    return f"[`{text}`]({url})" if url else f"`{text}`"


def project_json(proj: dict) -> dict:
    s, vals = proj["spec"], proj["values"]
    if s["id"] in WITHHOLD:
        return {"id": s["id"], "order": s.get("order"), "layer": s["layer"], "status": "private", "withheld": True,
                "name": {l: tr(s["name"], l) for l in ("zh", "en")},
                "problem": {l: tr(s["problem"], l) for l in ("zh", "en")}}
    out = {"id": s["id"], "order": s.get("order"), "layer": s["layer"], "status": s["status"],
           "updated": s["updated"], "card_version": s["card_version"],
           "card": {"zh": f"cards/{s['id']}.md", "en": f"cards/{s['id']}.en.md"},
           "links": s.get("links", []), "period": {l: tr(s["period"], l) for l in ("zh", "en")},
           "team": {l: tr(s["team"], l) for l in ("zh", "en")}, "stack": s["stack"], "evals": []}
    for key in ("name", "problem", "primary_metric", "summary", "did"):
        out[key] = {lang: fill(tr(s[key], lang), vals, lang, f"{s['id']}.{key}") for lang in ("zh", "en")}
    out["headline"] = []
    for h in s.get("headline", []):
        out["headline"].append({lang: fill(tr(h, lang), vals, lang, f"{s['id']}.headline") for lang in ("zh", "en")})
    for ev in s["eval"]:
        e = {"id": ev["id"], "name": {l: tr(ev["name"], l) for l in ("zh", "en")}, "date": ev["date"], "metrics": []}
        for m in ev["metric"]:
            d = {"id": m["id"], "label": {l: fill(tr(m["label"], l), vals, l, m["id"]) for l in ("zh", "en")},
                 "direction": m.get("direction", "higher")}
            d.update(vals[m["id"]].as_json())
            d["source_urls"] = [public_source(x)[1] for x in vals[m["id"]].sources]
            e["metrics"].append(d)
        out["evals"].append(e)
    return out


def render_readme(projects: list[dict], lang: str) -> str:
    tpl = (HERE / "templates" / f"README.{lang}.md").read_text(encoding="utf-8")
    zh = lang == "zh"
    rows = []
    head = ("| 项目 | 层 | 解决什么问题 | 主要指标 | 关键数字 | 链接 |" if zh else
            "| Project | Layer | Problem | Main metric | Key numbers | Links |")
    rows.append(head)
    rows.append("|---|---|---|---|---|---|")
    for p in projects:
        s, vals = p["spec"], p["values"]
        name = tr(s["name"], lang)
        layer = LAYERS[s["layer"]][0 if zh else 1]
        problem = fill(tr(s["problem"], lang), vals, lang, f"{s['id']}.problem")
        metric = fill(tr(s["primary_metric"], lang), vals, lang, f"{s['id']}.primary_metric")
        if s["id"] in WITHHOLD:
            rows.append(f"| **{name}**<br>{tr(s['period'], lang)} | {layer} | {fill(tr(s['problem'], lang), vals, lang, 'p')} | — | — | "
                        f"{'未公开' if zh else 'not public'} |")
            continue
        nums = "<br>".join(fill(tr(h, lang), vals, lang, f"{s['id']}.headline") for h in s.get("headline", []))
        if s["status"] == "public":
            links = " · ".join(f"[{tr(l['label'], lang)}]({tr(l['url'], lang)})" for l in s.get("links", []))
        else:
            links = "未公开" if zh else "not public"
        card = f"[{'评测卡' if zh else 'Card'}](cards/{s['id']}{'' if zh else '.en'}.md)"
        links = f"{links}<br>{card}"
        rows.append(f"| **{name}**<br>{tr(s['period'], lang)} | {layer} | {problem} | {metric} | {nums} | {links} |")
    story = load_story()
    flat = global_values(projects)
    intro = fill_global(tr(story["intro"], lang), flat, lang, "story.intro")
    intro += "\n\n" + " · ".join(f"[{tr(l['label'], lang)}]({tr(l['url'], lang)})" for l in story.get("links", []))
    return (tpl.replace("{{INTRO}}", intro)
               .replace("{{SCENES}}", render_scenes(story, projects, flat, lang))
               .replace("{{PROJECT_TABLE}}", "\n".join(rows)))


# --------------------------------------------------------------------------- storyline
STORY = ROOT / "cards" / "story.toml"
SCENE_NO = ["一", "二", "三", "四", "五", "六", "七", "八"]


def load_story() -> dict:
    with STORY.open("rb") as f:
        return tomllib.load(f)


def global_values(projects: list[dict]) -> dict[str, Value]:
    """Every card number as project__metric, plus counts of this build."""
    flat: dict[str, Value] = {}
    for p in projects:
        for mid, v in p["values"].items():
            flat[f"{p['spec']['id']}__{mid}".replace("-", "_")] = v
    n_records = sum(1 for p in projects for ev in p["spec"]["eval"] for m in ev["metric"] if "record" in m)
    for key, val in (("_cards", len(projects)), ("_numbers", sum(len(p["values"]) for p in projects)),
                     ("_records", n_records)):
        flat[key] = Value(kind="value", value=val, decimals=0)
    return flat


def fill_global(text: str, flat: dict[str, Value], lang: str, where: str) -> str:
    """Placeholders written as {project.metric} (or {_count}) across all cards."""
    text = re.sub(r"\{([a-z0-9-]+)\.([a-z0-9_]+)\}",
                  lambda m: "{" + f"{m.group(1)}__{m.group(2)}".replace("-", "_") + "}", text)
    return fill(text, flat, lang, where)


def render_scenes(story: dict, projects: list[dict], flat: dict[str, Value], lang: str) -> str:
    zh = lang == "zh"
    by_id = {p["spec"]["id"]: p["spec"] for p in projects}
    sep = "：" if zh else ": "
    out: list[str] = []
    for i, sc in enumerate(story["scene"]):
        title = tr(sc["title"], lang)
        out.append(f"### 第{SCENE_NO[i]}幕：{title}" if zh else f"### Scene {i + 1}: {title}")
        out.append("")
        if sc["projects"]:
            names = []
            if sc.get("self"):
                names.append("**本仓库**（[评测卡](cards/) · [Prompt 资产库](prompts/README.md)）" if zh
                             else "**This repository** ([cards](cards/) · [prompt registry](prompts/README.en.md))")
            for pid in sc["projects"]:
                spec = by_id[pid]
                if pid in WITHHOLD:
                    names.append(f"**{tr(spec['name'], lang)}**（未公开）" if zh else f"**{tr(spec['name'], lang)}** (not public)")
                    continue
                bits = [f"[{'评测卡' if zh else 'card'}](cards/{pid}{'' if zh else '.en'}.md)"]
                if spec["status"] == "public":
                    bits += [f"[{tr(l['label'], lang)}]({tr(l['url'], lang)})" for l in spec.get("links", [])]
                else:
                    bits.append("未公开" if zh else "not public")
                names.append(f"**{tr(spec['name'], lang)}**（{' · '.join(bits)}）" if zh
                             else f"**{tr(spec['name'], lang)}** ({' · '.join(bits)})")
            out.append("；".join(names) if zh else "; ".join(names))
        else:
            extra = "".join(f"；**{tr(l['label'], lang)}**（[代码]({tr(l['url'], lang)})）" if zh
                            else f"; **{tr(l['label'], lang)}** ([code]({tr(l['url'], lang)}))" for l in sc.get("links", []))
            out.append(("**本仓库**（[评测卡](cards/) · [Prompt 资产库](prompts/README.md)）" if zh
                        else "**This repository** ([cards](cards/) · [prompt registry](prompts/README.en.md))") + extra)
        out.append("")
        out.append(f"- **{'问题' if zh else 'Problem'}**{sep}{fill_global(tr(sc['purpose'], lang), flat, lang, 'story')}")
        out.append(f"- **{'我做了什么' if zh else 'What I did'}**{sep}{fill_global(tr(sc['did'], lang), flat, lang, 'story')}")
        out.append(f"- **{'结果' if zh else 'Results'}**{sep}" + ("；" if zh else "; ").join(
            fill_global(tr(r, lang), flat, lang, "story") for r in shown_results(sc)))
        out.append(f"- **{'和其他项目的连接' if zh else 'Connections'}**{sep}{fill_global(tr(sc['reuse'], lang), flat, lang, 'story')}")
        out.append("")
    return "\n".join(out).rstrip()


def shown_results(scene: dict) -> list:
    """Result lines, minus any that quote a withheld project's numbers."""
    return [r for r in scene["result"]
            if not any(f"{{{pid}." in r["zh"] or f"{{{pid}." in r["en"] for pid in WITHHOLD)]


def story_json(projects: list[dict]) -> dict:
    story = load_story()
    flat = global_values(projects)
    out = {"intro": {l: fill_global(tr(story["intro"], l), flat, l, "story") for l in ("zh", "en")},
           **({"about": {l: fill_global(tr(story["about"], l), flat, l, "story.about") for l in ("zh", "en")}}
              if "about" in story else {}),
           "links": story.get("links", []), "scenes": []}
    for sc in story["scene"]:
        out["scenes"].append({
            "title": sc["title"], "projects": sc["projects"], "links": sc.get("links", []),
            **{k: {l: fill_global(tr(sc[k], l), flat, l, "story") for l in ("zh", "en")} for k in ("purpose", "did", "reuse")},
            "result": [{l: fill_global(tr(r, l), flat, l, "story") for l in ("zh", "en")} for r in shown_results(sc)],
        })
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="build in memory, fail on mismatches or changed sources")
    args = ap.parse_args(argv)
    problems: list[str] = []
    projects = []
    for spec in load_specs():
        try:
            projects.append(build_project(spec, problems))
        except BuildError as e:
            problems.append(str(e))
    lock = {p["spec"]["id"]: dict(sorted(p["hashes"].items())) for p in projects}
    if LOCK.exists() and args.check:
        old = json.loads(LOCK.read_text(encoding="utf-8"))
        for pid, files in lock.items():
            for rel, h in files.items():
                if old.get(pid, {}).get(rel) not in (None, h):
                    problems.append(f"{pid}: source changed since the cards were built: {rel}")
    outputs: dict[Path, str] = {}
    try:
        for p in projects:
            pid = p["spec"]["id"]
            if pid in WITHHOLD:
                continue
            outputs[CARDS / f"{pid}.md"] = render_card(p, "zh")
            outputs[CARDS / f"{pid}.en.md"] = render_card(p, "en")
        outputs[ROOT / "README.md"] = render_readme(projects, "zh")
        outputs[ROOT / "README.en.md"] = render_readme(projects, "en")
        data = [project_json(p) for p in projects]
        outputs[DATA / "story.json"] = json.dumps(story_json(projects), ensure_ascii=False, indent=2) + "\n"
    except BuildError as e:
        problems.append(str(e))
        data = []
    if problems:
        print("PROBLEMS:")
        for x in problems:
            print("  -", x)
        return 1
    if args.check:
        stale = [str(p.relative_to(ROOT)) for p, text in outputs.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != text]
        if stale:
            print("Out of date (run without --check):", ", ".join(stale))
            return 1
        n_rec = sum(1 for p in projects for ev in p["spec"]["eval"] for m in ev["metric"] if "record" in m)
        extra = f", {n_rec} numbers match the project reports" if n_rec else ""
        print(f"OK: {len(projects)} cards up to date, source files unchanged{extra}.")
        return 0
    for p, text in outputs.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="\n")
    DATA.mkdir(exist_ok=True)
    (DATA / "projects.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    LOCK.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Built {len(projects)} cards ({sum(len(p['values']) for p in projects)} numbers).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
