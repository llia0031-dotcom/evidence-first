"""Prompt registry: version tables, production / staging labels, promote and rollback.

    python scripts/prompts.py build                       # prompts/README*.md and data/prompts.json
    python scripts/prompts.py status                      # where every label points
    python scripts/prompts.py promote <asset> <version> --to staging --reason "..."
    python scripts/prompts.py promote <asset> <version> --to production --reason "..."
    python scripts/prompts.py rollback <asset> --reason "..."

Scores are never typed in: a registry entry either refers to a number on an evaluation card
(`refs = ["project.metric"]`) or names an extractor that reads the project's result file.
Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import build_cards as bc  # noqa: E402

REGISTRY = ROOT / "prompts" / "registry"
LABELS = ROOT / "prompts" / "labels.json"
DECISION = {
    "adopted": ("采用", "adopted"),
    "not_adopted": ("不采用", "not adopted"),
    "superseded": ("已被替换", "superseded"),
    "retired": ("停用", "retired"),
}


def load_registry() -> list[dict]:
    assets = []
    for p in sorted(REGISTRY.glob("*.toml")):
        with p.open("rb") as f:
            a = tomllib.load(f)
        a["_file"] = p.name
        assets.append(a)
    assets.sort(key=lambda a: a.get("order", 99))
    return assets


def load_labels() -> dict:
    return json.loads(LABELS.read_text(encoding="utf-8"))


def save_labels(labels: dict) -> None:
    LABELS.write_text(json.dumps(labels, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def card_values() -> dict[str, bc.Value]:
    problems: list[str] = []
    out: dict[str, bc.Value] = {}
    for spec in bc.load_specs():
        proj = bc.build_project(spec, problems)
        for mid, v in proj["values"].items():
            out[f"{spec['id']}.{mid}"] = v
    if problems:
        raise bc.BuildError("; ".join(problems))
    return out


def resolve_scores(asset: dict, values: dict[str, bc.Value]) -> None:
    """Attach computed values to every score entry, in place."""
    for ver in asset.get("version", []):
        for s in ver.get("scores", []):
            if "refs" in s:
                missing = [r for r in s["refs"] if r not in values]
                if missing:
                    raise bc.BuildError(f"{asset['asset']} {ver['id']}: unknown card metric {missing}")
                s["_values"] = [values[r] for r in s["refs"]]
            elif "pair" in s:
                s["_values"] = [bc.compute(m, asset["asset"]) for m in s["pair"]]
            else:
                s["_values"] = [bc.compute(s, asset["asset"])]


def fill(text: str, values: dict[str, bc.Value], lang: str, where: str) -> str:
    """Placeholders here are {project.metric}; reuse the card filler with dotted keys."""
    flat = {k.replace(".", "__").replace("-", "_"): v for k, v in values.items()}
    import re
    text = re.sub(r"\{([a-z0-9-]+)\.([a-z0-9_]+)\}", lambda m: "{" + (m.group(1) + "__" + m.group(2)).replace("-", "_") + "}", text)
    return bc.fill(text, flat, lang, where)


def score_text(s: dict, lang: str) -> str:
    vals = s["_values"]
    return " → ".join(v.short(lang) for v in vals)


def render(assets: list[dict], labels: dict, values: dict, lang: str) -> str:
    zh = lang == "zh"
    L = (lambda a, b: a if zh else b)  # noqa: E731
    out = [L("# Prompt 资产库", "# Prompt registry"), ""]
    out.append(L(
        "每个 Prompt 资产的每一版都写清：版本号、改了什么、当时在冻结的测试集上的真实分数、采用还是不采用、为什么。分数由 `scripts/prompts.py build` 从项目的结果文件算出，不手写。同一行里的“→”表示同一套题上新旧两版的对比；不同测试集的分数不互相比较。",
        "Every version of every prompt asset records its id, what changed, its real score on a frozen test set at the time, whether it was adopted, and why. Scores are computed by `scripts/prompts.py build` from the projects' result files, never typed in. An arrow compares old and new versions on the same items; scores from different test sets are not compared."))
    out.append("")
    out.append(L("## 上线标签", "## Release labels"))
    out.append("")
    out.append(L(
        "`production` 指项目决定采用、之后都用的版本，`staging` 指正在测的候选版本。上线就是把 production 挪到新版本，回滚就是挪回上一版（`python scripts/prompts.py rollback <资产>`）。标签从 2026-11-15 开始用，之前的记录按各项目的记录补记。这些项目都没有线上流量；灰度只用评测题回放演示，见 [rollout/](rollout/)。",
        "`production` is the version a project has adopted and uses from then on; `staging` is the candidate under test. A release moves production to the new version; a rollback moves it back (`python scripts/prompts.py rollback <asset>`). Labels start on 2026-11-15; earlier entries are back-filled from each project's records. None of these projects has live traffic; rollout is shown only by replaying test items, see [rollout/](rollout/)."))
    out.append("")
    out.append(f"| {L('资产', 'Asset')} | production | staging | {L('说明', 'Note')} |")
    out.append("|---|---|---|---|")
    for a in assets:
        lab = labels.get(a["asset"], {})
        out.append(f"| `{a['asset']}` | {lab.get('production', '—')} | {lab.get('staging', '—')} | {bc.tr(a['production_note'], lang)} |")
    out.append("")
    for a in assets:
        out.append(f"## {bc.tr(a['name'], lang)}")
        out.append("")
        out.append(bc.tr(a["what"], lang))
        out.append("")
        out.append(f"- {L('代码位置', 'Location')}{L('：', ': ')}`{a['where']}`（{a['project']}）" if zh
                   else f"- Location: `{a['where']}` ({a['project']})")
        out.append(f"- {L('模型锁定', 'Model lock')}{L('：', ': ')}{a['model_lock']}")
        out.append("")
        out.append(f"| {L('版本', 'Version')} | {L('日期', 'Date')} | {L('改了什么', 'Change')} | {L('当时的分数', 'Score at the time')} | {L('决定', 'Decision')} | {L('为什么', 'Why')} |")
        out.append("|---|---|---|---|---|---|")
        for ver in a["version"]:
            where = f"{a['asset']}.{ver['id']}"
            scores = []
            if ver.get("scores"):
                if "compare_set" in ver:
                    scores.append(f"*{bc.tr(ver['compare_set'], lang)}*")
                for s in ver["scores"]:
                    scores.append(f"{bc.tr(s['label'], lang)}{L('：', ': ')}{score_text(s, lang)}")
            score_cell = "<br>".join(scores) if scores else L("没有存成结果文件的评测", "no stored evaluation")
            dec = DECISION[ver["decision"]][0 if zh else 1]
            if ver.get("superseded_by"):
                dec += L(f"（后被 {ver['superseded_by']} 替换）", f" (later replaced by {ver['superseded_by']})")
            change = bc.tr(ver["change"], lang) + "<br>" + bc.tr(ver["text"], lang)
            why = fill(bc.tr(ver["why"], lang), values, lang, where)
            if ver.get("source"):
                src = ver["source"]
                text = src.split("github.com/Jason-d-e/")[-1].replace("/blob/main/", "/") if src.startswith("http") else src
                why += f"<br>{L('出处', 'Source')}{L('：', ': ')}" + (f"[{text}]({src})" if src.startswith("http") else src)
            out.append(f"| **{ver['id']}** | {ver['date']} | {change} | {score_cell} | {dec} | {why} |")
        out.append("")
        hist = labels.get(a["asset"], {}).get("history", [])
        if hist:
            out.append(f"{L('标签记录', 'Label history')}{L('：', ': ')}" + "；".join(
                f"{h['date']} {h['label']} {h.get('from', '·')}→{h['to']}" for h in hist) if zh else
                "Label history: " + "; ".join(f"{h['date']} {h['label']} {h.get('from', '·')}→{h['to']}" for h in hist))
            out.append("")
    out.append(L("## 回归评测", "## Regression check"))
    out.append("")
    out.append(L(
        "改 `prompts/` 下的文件并开 PR 时，GitHub Action 用 promptfoo 把 production 和 staging 两个标签指向的版本放在同一套冻结的题上跑，把两版的通过数贴到 PR 里。现在接上的是 evidence-check 的 Skill，题目是它的开发评测 v1（虚构活动资料、12 篇草稿）。配置在 [regression/](regression/)。",
        "When a pull request changes files under `prompts/`, a GitHub Action runs promptfoo on the versions behind the production and staging labels over one frozen item set and posts both pass counts on the pull request. The evidence-check skill is wired in, on its development set v1 (fictional event documents, 12 drafts). Configuration: [regression/](regression/)."))
    out.append("")
    return "\n".join(out)


def assets_json(assets: list[dict], labels: dict, values: dict) -> list[dict]:
    out = []
    for a in assets:
        item = {"asset": a["asset"], "project": a["project"], "name": a["name"], "what": a["what"],
                "where": a["where"], "model_lock": a["model_lock"], "labels": labels.get(a["asset"], {}),
                "versions": []}
        for ver in a["version"]:
            v = {k: ver[k] for k in ("id", "date", "decision", "change", "text", "source") if ver.get(k) != "" and k in ver}
            v["why"] = {lang: fill(bc.tr(ver["why"], lang), values, lang, ver["id"]) for lang in ("zh", "en")}
            v["scores"] = [{"label": s["label"], "values": [x.as_json() for x in s["_values"]],
                            "direction": s.get("direction", "higher")} for s in ver.get("scores", [])]
            if "compare_set" in ver:
                v["compare_set"] = ver["compare_set"]
            item["versions"].append(v)
        out.append(item)
    return out


def cmd_build(check: bool = False) -> int:
    assets, labels = load_registry(), load_labels()
    values = card_values()
    for a in assets:
        resolve_scores(a, values)
        ids = {v["id"] for v in a["version"]}
        lab = labels.get(a["asset"])
        if not lab:
            raise bc.BuildError(f"no labels for {a['asset']}")
        for key in ("production", "staging"):
            if lab[key] not in ids:
                raise bc.BuildError(f"{a['asset']}: {key} points at unknown version {lab[key]}")
    outputs = {
        ROOT / "prompts" / "README.md": render(assets, labels, values, "zh"),
        ROOT / "prompts" / "README.en.md": render(assets, labels, values, "en"),
        ROOT / "data" / "prompts.json": json.dumps(assets_json(assets, labels, values), ensure_ascii=False, indent=2) + "\n",
    }
    if check:
        stale = [str(p.relative_to(ROOT)) for p, t in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
        if stale:
            print("Out of date:", ", ".join(stale))
            return 1
        print(f"OK: {len(assets)} prompt assets.")
        return 0
    for p, t in outputs.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(t, encoding="utf-8", newline="\n")
    print(f"Built registry: {len(assets)} assets, {sum(len(a['version']) for a in assets)} versions.")
    return 0


def cmd_status() -> int:
    labels = load_labels()
    for a in load_registry():
        lab = labels.get(a["asset"], {})
        print(f"{a['asset']:28} production={lab.get('production')}  staging={lab.get('staging')}")
    return 0


def _record(labels: dict, asset: str, label: str, to: str, reason: str) -> None:
    entry = labels[asset]
    labels[asset]["history"].append({"date": dt.date.today().isoformat(), "label": label,
                                     "from": entry[label], "to": to, "reason": reason})
    entry[label] = to


def cmd_promote(asset: str, version: str, to: str, reason: str) -> int:
    labels = load_labels()
    reg = {a["asset"]: a for a in load_registry()}
    if asset not in reg:
        print(f"unknown asset {asset}")
        return 2
    vers = {v["id"]: v for v in reg[asset]["version"]}
    if version not in vers:
        print(f"unknown version {version}")
        return 2
    if to == "production":
        if labels[asset]["staging"] != version:
            print("A version reaches production only from staging: promote it to staging first.")
            return 1
        if vers[version]["decision"] != "adopted":
            print(f"{version} is recorded as '{vers[version]['decision']}': record the regression result and decision first.")
            return 1
    _record(labels, asset, to, version, reason)
    save_labels(labels)
    print(f"{asset}: {to} → {version}")
    return 0


def cmd_rollback(asset: str, reason: str) -> int:
    labels = load_labels()
    entry = labels.get(asset)
    if not entry:
        print(f"unknown asset {asset}")
        return 2
    moves = [h for h in entry["history"] if h["label"] == "production" and h.get("from") and h["to"] == entry["production"]]
    if not moves:
        print("No earlier production version to go back to.")
        return 1
    _record(labels, asset, "production", moves[-1]["from"], f"rollback: {reason}")
    save_labels(labels)
    print(f"{asset}: production → {entry['production']} (rollback)")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--check", action="store_true")
    sub.add_parser("status")
    p = sub.add_parser("promote")
    p.add_argument("asset")
    p.add_argument("version")
    p.add_argument("--to", choices=["staging", "production"], required=True)
    p.add_argument("--reason", required=True)
    r = sub.add_parser("rollback")
    r.add_argument("asset")
    r.add_argument("--reason", required=True)
    args = ap.parse_args(argv)
    try:
        if args.cmd == "build":
            return cmd_build(args.check)
        if args.cmd == "status":
            return cmd_status()
        if args.cmd == "promote":
            return cmd_promote(args.asset, args.version, args.to, args.reason)
        return cmd_rollback(args.asset, args.reason)
    except bc.BuildError as e:
        print("PROBLEM:", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
