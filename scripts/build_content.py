"""Portfolio content drafts: one per project, the same case template, ready to paste into a site template.

Sections: one line, facts, problem, what I did, evaluation, iteration, result, limitations, then the
numbers (each with its source) and the images, listed separately. Every number comes from the
evaluation cards; the numbers list is also written as an evidence-check claims file, with each claim
quoting the card line it comes from, so the checker can confirm the drafts match the cards.

    python scripts/build_content.py                 # writes build/content/ and data/content.json
    python scripts/build_content.py --out <folder>  # somewhere else
Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import build_cards as bc  # noqa: E402

DEFAULT_OUT = ROOT / "build" / "content"
MEDIA = ROOT / "cards" / "media.toml"
PH = re.compile(r"\{([a-z0-9_]+)(?::[a-z]+)?\}")
FIELDS_WITH_NUMBERS = ("headline", "iteration", "limitation")


def used_metrics(spec: dict) -> list[str]:
    """Metric ids referenced by the parts of the spec that the draft shows, in order of first use."""
    seen: list[str] = []
    texts: list[str] = []
    for h in spec.get("headline", []):
        texts += [h["zh"], h["en"]]
    texts += spec.get("iteration", {}).get("zh", []) + spec.get("iteration", {}).get("en", [])
    for key in ("result_line", "assumed", "showed"):
        if key in spec:
            texts += [spec[key]["zh"], spec[key]["en"]]
    for k in spec.get("key_numbers", []):
        texts += [k["label"]["zh"], k["label"]["en"]]
    for lim in spec.get("limitation", []):
        texts += [lim["text"]["zh"], lim["text"]["en"], lim.get("advice", {}).get("zh", ""), lim.get("advice", {}).get("en", "")]
    for t in texts:
        for m in PH.finditer(t):
            if m.group(1) not in seen:
                seen.append(m.group(1))
    extra = [k["metric"] for k in spec.get("key_numbers", [])]
    for t in spec.get("timeline", []):
        extra += [t[x] for x in ("before", "after") if x in t]
    for mid in extra:
        if mid not in seen:
            seen.append(mid)
    return seen


LIMITS = {"short_name": (8, 22), "card_title": (24, 60), "key_label": (20, 70), "result_line": (40, 110),
          "assumed": (40, 120), "showed": (40, 120), "timeline_text": (30, 60)}


def check_len(kind: str, text: str, lang: str, where: str, problems: list[str]) -> None:
    limit = LIMITS[kind][0 if lang == "zh" else 1]
    # In Chinese a Han character or full-width mark counts as one; Latin letters, digits and spaces as half.
    size = sum(1 if ord(c) >= 0x2E80 else 0.5 for c in text) if lang == "zh" else len(text)
    if size > limit:
        problems.append(f"{where} {kind} ({lang}) is {size:g} characters, limit {limit}: {text}")


def page_fields(s: dict, vals: dict, lang: str, nid: dict[str, str], problems: list[str]) -> dict:
    """Short fields the portfolio pages use: names, a card title, three key numbers, a turn, a timeline."""
    pid = s["id"]
    tr = lambda x: bc.tr(x, lang)  # noqa: E731
    out = {"short_name": tr(s["short_name"]), "card_title": tr(s["card_title"]),
           "assumed": bc.fill(tr(s["assumed"]), vals, lang, f"{pid}.assumed") if "assumed" in s else "",
           "showed": bc.fill(tr(s["showed"]), vals, lang, f"{pid}.showed") if "showed" in s else ""}
    check_len("short_name", out["short_name"], lang, pid, problems)
    check_len("card_title", out["card_title"], lang, pid, problems)
    if re.search(r"\d", out["card_title"]):
        problems.append(f"{pid} card_title ({lang}) contains a digit: {out['card_title']}")
    for kind in ("assumed", "showed"):
        if out[kind]:
            check_len(kind, out[kind], lang, pid, problems)
    out["result_line"] = bc.fill(tr(s["result_line"]), vals, lang, f"{pid}.result_line") if "result_line" in s else ""
    if out["result_line"]:
        check_len("result_line", out["result_line"], lang, pid, problems)
    out["key_numbers"] = []
    for k in s.get("key_numbers", []):
        label = bc.fill(tr(k["label"]), vals, lang, f"{pid}.key_numbers")
        check_len("key_label", label, lang, pid, problems)
        out["key_numbers"].append({"id": nid[k["metric"]], "label": label})
    out["timeline"] = []
    for t in s.get("timeline", []):
        item = {"date": t["date"], "label": tr(t["label"]), "text": tr(t["text"])}
        check_len("timeline_text", item["text"], lang, pid, problems)
        bc.lint_prose(item["text"], f"{pid}.timeline")
        for x in ("before", "after"):
            if x in t:
                item[x] = vals[t[x]].short(lang)
                item[f"{x}_id"] = nid[t[x]]
        if "adopted" in t:
            item["adopted"] = t["adopted"]
        out["timeline"].append(item)
    return out


def metric_index(spec: dict) -> dict[str, tuple[dict, dict]]:
    return {m["id"]: (ev, m) for ev in spec["eval"] for m in ev["metric"]}


def card_line(card_text: str, v: bc.Value, lang: str, label: str) -> str:
    """The row of the card's results table that shows this label and value; used as the claim's quote."""
    full = v.full(lang)
    for line in card_text.splitlines():
        if line.startswith(f"| {label} | {full} |"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            return f"{cells[0]} | {cells[1]}"
    raise bc.BuildError(f"value {full} not found in the card")


def eval_line(ev: dict, f, lang: str) -> str:
    """One line per evaluation: name, items, runs (only when the items text does not already say), setup."""
    zh = lang == "zh"
    items = f(bc.tr(ev["items"], lang), "items")
    parts = [items]
    if not ("遍" in items or "run" in items.lower()):
        parts.append(f(bc.tr(ev["runs"], lang), "runs"))
    parts.append(bc.tr(ev["setup"], lang))
    sep = "；" if zh else "; "
    return f"**{bc.tr(ev['name'], lang)}**{'：' if zh else ': '}{sep.join(parts)}"


def render(proj: dict, media: list[dict], lang: str, card_text: str) -> tuple[str, list[dict], dict]:
    s, vals = proj["spec"], proj["values"]
    pid = s["id"]
    zh = lang == "zh"
    L = (lambda a, b: a if zh else b)  # noqa: E731
    f = lambda t, w: bc.fill(t, vals, lang, f"{pid}.{w}")  # noqa: E731
    idx = metric_index(s)
    nums = used_metrics(s)
    out: list[str] = []
    data: dict = {"id": pid, "lang": lang, "order": s["order"], "name": bc.tr(s["name"], lang),
                  "status": s["status"], "layer": bc.LAYERS[s["layer"]][0 if zh else 1],
                  "period": s["period"], "team": s["team"], "stack": bc.tr(s["stack"], lang)}

    out.append(f"# {bc.tr(s['name'], lang)}")
    out.append("")
    out.append(L("> 内容稿：作品集模板直接用。数字由 `evidence-first/scripts/build_content.py` 从评测卡数据生成，不要手改；要改文字，改 `evidence-first/cards/specs/` 再重新生成。",
                 "> Content draft for the portfolio template. Numbers are generated from the evaluation card data by `evidence-first/scripts/build_content.py`; do not edit by hand, change `evidence-first/cards/specs/` and rebuild."))
    out.append("")
    summary = f(bc.tr(s["summary"], lang), "summary")
    one_line = summary.split("。")[0] + "。" if zh else summary.split(". ")[0].rstrip(".") + "."
    problem = f(bc.tr(s["problem"], lang), "problem")
    if not problem.endswith(("。", ".", "？", "?")):
        problem += "。" if zh else "."
    data["one_line"] = one_line
    out.append(L("## 一句话", "## One line"))
    out.append("")
    out.append(one_line)
    out.append("")

    status = L("已公开", "Public") if s["status"] == "public" else L("未公开", "Not public")
    links = [{"label": bc.tr(l["label"], lang), "url": bc.tr(l["url"], lang)} for l in s.get("links", [])] if s["status"] == "public" else []
    card_rel = f"evidence-first/cards/{pid}{'' if zh else '.en'}.md"
    facts = [(L("时间", "When"), s["period"]), (L("团队", "Team"), s["team"]),
             (L("技术", "Stack"), bc.tr(s["stack"], lang)),
             (L("在作品集里的位置", "Place in the portfolio"), bc.LAYERS[s["layer"]][0 if zh else 1]),
             (L("状态", "Status"), status)]
    out.append(L("## 信息栏", "## Facts"))
    out.append("")
    out.append(f"| {L('栏', 'Field')} | {L('内容', 'Value')} |")
    out.append("|---|---|")
    for a, b in facts:
        out.append(f"| {a} | {b} |")
    for l in links:
        out.append(f"| {L('链接', 'Link')} | [{l['label']}]({l['url']}) |")
    out.append(f"| {L('评测卡', 'Evaluation card')} | `{card_rel}` |")
    out.append("")
    data["facts"] = [{"label": a, "value": b} for a, b in facts]
    data["links"] = links

    sections = [
        ("problem", L("问题", "Problem"), [problem]),
        ("did", L("我做了什么", "What I did"), [f(bc.tr(s["did"], lang), "did")]),
        ("evaluation", L("评测", "Evaluation"), [
            eval_line(ev, f, lang) for ev in s["eval"]]),
        ("iteration", L("迭代", "Iteration"), [f(t, "iteration") for t in bc.tr(s.get("iteration", {}), lang) or []]),
        ("result", L("结果", "Result"), [f(bc.tr(s["conclusion"], lang), "conclusion")]),
        ("limitations", L("局限", "Limitations"), [
            f(bc.tr(lim["text"], lang), "limitation") + (f"{L('建议：', ' Recommendation: ')}{f(bc.tr(lim['advice'], lang), 'advice')}" if "advice" in lim else "")
            for lim in s["limitation"]]),
    ]
    for key, title, items in sections:
        out.append(f"## {title}")
        out.append("")
        if key in ("problem", "did", "result"):
            out += [items[0], ""]
        else:
            out += [f"- {x}" for x in items] + [""]
        data[key] = items

    # Numbers, listed apart from the text.
    out.append(L("## 关键数字", "## Key numbers"))
    out.append("")
    out.append(L("“结果”下面的几条可以直接做成数字卡片；全部数字和 95% 区间见评测卡。",
                 "The headline lines can become number cards as they are; every number with its 95% interval is on the evaluation card."))
    out.append("")
    headline = [f(bc.tr(h, lang), "headline") for h in s.get("headline", [])]
    for h in headline:
        out.append(f"- {h}")
    out.append("")
    out.append(f"| # | {L('数字', 'Number')} | {L('意思', 'Meaning')} | {L('评测', 'Evaluation')} | {L('出处', 'Source')} |")
    out.append("|---|---|---|---|---|")
    claims = []
    numbers = []
    for i, mid in enumerate(nums, 1):
        ev, m = idx[mid]
        v = vals[mid]
        label = bc.fill(bc.tr(m["label"], lang), vals, lang, mid)
        if "note" in m:
            label += L("（", " (") + bc.fill(bc.tr(m["note"], lang), vals, lang, mid) + L("）", ")")
        src = "<br>".join(f"`{p}`" for p in v.sources)
        out.append(f"| N{i} | {v.full(lang)} | {label} | {bc.tr(ev['name'], lang)} | {L('评测卡', 'card')} + {src} |")
        numbers.append({"id": f"N{i}", "metric": mid, "label": label, "value": v.short(lang), "full": v.full(lang),
                        "evaluation": bc.tr(ev["name"], lang), "sources": v.sources,
                        "source_urls": [bc.public_source(x)[1] for x in v.sources], **v.as_json(),
                        "display": v.short(lang)})  # as shown on the card, with the card's precision and unit
        claims.append({"id": f"{pid}-{lang}-N{i}", "text": f"{label}{L('，结果 ', ', result ')}{v.short(lang)}",
                       "evidence": [{"source": f"{pid}{'' if zh else '.en'}.md", "quote": card_line(card_text, v, lang, label)}]})
    out.append("")
    data["headline"] = headline
    data["numbers"] = numbers
    nid = {n["metric"]: n["id"] for n in numbers}
    page_problems: list[str] = []
    data.update(page_fields(s, vals, lang, nid, page_problems))
    if page_problems:
        raise bc.BuildError("; ".join(page_problems))
    source = f"{pid}{'' if zh else '.en'}.md"
    by_id = {n["id"]: n for n in numbers}

    def quotes(mids: list[str]) -> list[dict]:
        return [{"source": source, "quote": card_line(card_text, vals[m], lang, by_id[nid[m]]["label"])} for m in mids]

    for key in ("result_line", "showed", "assumed"):
        if data.get(key):
            refs = [m.group(1) for m in PH.finditer(bc.tr(s[key], lang))]
            if refs:
                claims.append({"id": f"{pid}-{lang}-{key}", "text": data[key], "evidence": quotes(refs)})
    for i, (k, shown) in enumerate(zip(s.get("key_numbers", []), data["key_numbers"]), 1):
        refs = [k["metric"]] + [m.group(1) for m in PH.finditer(bc.tr(k["label"], lang))]
        text = f"{shown['label']}{L('，', ', ')}{vals[k['metric']].short(lang)}"
        claims.append({"id": f"{pid}-{lang}-key{i}", "text": text, "evidence": quotes(refs)})

    out.append(L("## 配图", "## Images"))
    out.append("")
    mine = [m for m in media if m["project"] == pid]
    if mine:
        out.append(f"| {L('文件', 'File')} | {L('说明', 'Caption')} | {L('已公开', 'Public')} |")
        out.append("|---|---|---|")
        for m in mine:
            out.append(f"| `{m['path']}` | {bc.tr(m['caption'], lang)} | {L('是', 'yes') if m['public'] else L('否', 'no')} |")
        out.append("")
        out.append(L("说明按文件名和项目记录写，挑图时请看一眼原图。", "Captions follow file names and project records; check each image when choosing."))
    else:
        out.append(L("暂无。", "None yet."))
    out.append("")
    data["images"] = [{"path": m["path"], "caption": bc.tr(m["caption"], lang), "public": m["public"]} for m in mine]
    return "\n".join(out), claims, data


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args(argv)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    with MEDIA.open("rb") as fh:
        media = tomllib.load(fh)["media"]
    missing = [m["path"] for m in media if not (bc.PORTFOLIO / m["path"]).is_file()]
    if missing:
        print("Missing media files:", missing)
        return 1
    problems: list[str] = []
    projects = [bc.build_project(spec, problems) for spec in bc.load_specs()]
    if problems:
        print("PROBLEMS:", problems)
        return 1
    all_claims, all_data, index = [], [], []
    for p in projects:
        pid = p["spec"]["id"]
        if pid in bc.WITHHOLD:
            for lang in ("zh", "en"):
                sp = p["spec"]
                all_data.append({"id": pid, "lang": lang, "order": sp["order"], "status": "private", "withheld": True,
                                 "name": bc.tr(sp["name"], lang), "short_name": bc.tr(sp["short_name"], lang),
                                 "card_title": bc.tr(sp["card_title"], lang),
                                 "layer": bc.LAYERS[sp["layer"]][0 if lang == "zh" else 1]})
            index.append((sp["order"], pid, bc.tr(sp["name"], "zh"), "private"))
            continue
        for lang, suffix in (("zh", ""), ("en", ".en")):
            card_text = (bc.CARDS / f"{pid}{suffix}.md").read_text(encoding="utf-8")
            text, claims, data = render(p, media, lang, card_text)
            (out_dir / f"{p['spec']['order']:02d}_{pid}{suffix}.md").write_text(text + "\n", encoding="utf-8", newline="\n")
            all_claims += claims
            all_data.append(data)
        index.append((p["spec"]["order"], pid, bc.tr(p["spec"]["name"], "zh"), p["spec"]["status"]))
    lines = ["# 内容稿（阶段 2）", "",
             "每个项目一份，中英各一。模板：一句话 → 信息栏 → 问题 → 我做了什么 → 评测 → 迭代 → 结果 → 局限，后面单独列关键数字（带出处）和配图。",
             "由 `evidence-first/scripts/build_content.py` 生成，数字来自评测卡数据；`核对记录.md` 是用 evidence-check 把每个数字对回评测卡的结果。", "",
             "| 顺序 | 项目 | 中文 | 英文 | 状态 |", "|---|---|---|---|---|"]
    for order, pid, name, status in index:
        lines.append(f"| {order} | {name} | [{order:02d}_{pid}.md]({order:02d}_{pid}.md) | [{order:02d}_{pid}.en.md]({order:02d}_{pid}.en.md) | {'已公开' if status == 'public' else '未公开'} |")
    (out_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    (out_dir / "claims.json").write_text(json.dumps({"claims": all_claims}, ensure_ascii=False, indent=2) + "\n",
                                         encoding="utf-8", newline="\n")
    (bc.DATA / "content.json").write_text(json.dumps(all_data, ensure_ascii=False, indent=2) + "\n",
                                          encoding="utf-8", newline="\n")
    print(f"Wrote {len(all_data)} drafts and {len(all_claims)} claims to {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
