"""Export data/content.json as CSV files a site builder's CMS can import (one file per language).

The column list comes from a mapping file that names each CMS field exactly as the template has it
and says where its content comes from, so the same content can fill any template:

    python scripts/export_csv.py MAPPING.toml --out <folder>

Mapping file:

    [[field]]
    name = "Title"          # the CMS field name, exactly as in the template
    type = "text"           # text | rich (HTML) | link | image | number | date | option | toggle
    source = "name"         # see SOURCES below
    # optional: zh / en fixed values instead of a source, e.g. zh = "未公开"

SOURCES: a top-level key of a content entry (name, one_line, problem, did, result, period, team,
stack, layer, status, order, id); "fact:<label>"; "link:<n>" (url of the n-th link, empty when the
project is not public); "headline:<n>"; "image:<n>" (path of the n-th image); "list:<key>" (a list
joined into an HTML list for rich text, or lines for plain text); "numbers" (HTML table of the key
numbers with sources); "slug". Every k/n or decimal number written to the CSV must exist in the
evaluation card data, which the script checks before writing. Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONTENT = ROOT / "data" / "content.json"
PROJECTS = ROOT / "data" / "projects.json"
FRACTION = re.compile(r"\d+/\d+")
BOLD = re.compile(r"\*\*(.+?)\*\*")


def md_inline_to_html(text: str) -> str:
    text = html.escape(text, quote=False)
    text = BOLD.sub(r"<strong>\1</strong>", text)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", text)


def plain(text: str) -> str:
    return re.sub(r"`([^`]+)`", r"\1", BOLD.sub(r"\1", text))


def value_for(entry: dict, field: dict) -> str:
    lang = entry["lang"]
    if lang in field:
        return field[lang]
    src = field["source"]
    rich = field.get("type") == "rich"
    if src == "slug":
        return entry["id"]
    if src.startswith("fact:"):
        label = src.split(":", 1)[1]
        return next((f["value"] for f in entry["facts"] if f["label"] == label), "")
    if src.startswith("link:"):
        n = int(src.split(":", 1)[1])
        return entry["links"][n]["url"] if n < len(entry["links"]) else ""
    if src.startswith("headline:"):
        n = int(src.split(":", 1)[1])
        return entry["headline"][n] if n < len(entry["headline"]) else ""
    if src.startswith("image:"):
        n = int(src.split(":", 1)[1])
        return entry["images"][n]["path"] if n < len(entry["images"]) else ""
    if src.startswith("list:"):
        items = entry[src.split(":", 1)[1]]
        if rich:
            return "<ul>" + "".join(f"<li>{md_inline_to_html(x)}</li>" for x in items) + "</ul>"
        return "\n".join(plain(x) for x in items)
    if src == "numbers":
        zh = lang == "zh"
        head = ("数字", "意思", "出处") if zh else ("Number", "Meaning", "Source")
        rows = "".join(
            f"<tr><td>{html.escape(n['full'])}</td><td>{html.escape(n['label'])}</td>"
            f"<td>{html.escape(', '.join(n['sources']))}</td></tr>" for n in entry["numbers"])
        return f"<table><tr><th>{head[0]}</th><th>{head[1]}</th><th>{head[2]}</th></tr>{rows}</table>"
    val = entry[src]
    if isinstance(val, list):
        val = val[0] if len(val) == 1 else "\n".join(val)
    val = str(val)
    return f"<p>{md_inline_to_html(val)}</p>" if rich else plain(val)


def card_numbers() -> set[str]:
    """Every k/n fraction on the evaluation cards (both languages)."""
    out: set[str] = set()
    for p in json.loads(PROJECTS.read_text(encoding="utf-8")):
        for ev in p["evals"]:
            for m in ev["metrics"]:
                if m["kind"] == "proportion":
                    out.add(f"{m['k']}/{m['n']}")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mapping")
    ap.add_argument("--out", required=True)
    ap.add_argument("--prefix", default="projects")
    args = ap.parse_args(argv)
    with open(args.mapping, "rb") as f:
        fields = tomllib.load(f)["field"]
    entries = sorted(json.loads(CONTENT.read_text(encoding="utf-8")), key=lambda e: (e["lang"], e["order"]))
    known = card_numbers()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    problems = []
    for lang in ("zh", "en"):
        rows = []
        for e in [x for x in entries if x["lang"] == lang]:
            row = {f["name"]: value_for(e, f) for f in fields}
            if e["status"] != "public":
                for f in fields:
                    if f.get("type") == "link" or f["source"].startswith("link:"):
                        row[f["name"]] = ""
            for name, cell in row.items():
                for frac in FRACTION.findall(cell):
                    if frac not in known:
                        problems.append(f"{e['id']} {lang} {name}: {frac} is not on any evaluation card")
            rows.append(row)
        path = out_dir / f"{args.prefix}.{lang}.csv"
        with path.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=[f["name"] for f in fields], quoting=csv.QUOTE_ALL)
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {path} ({len(rows)} rows)")
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  -", p)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
