"""The "ask me" questions and answers at the end of the portfolio, built from cards/faq.toml.

Answers are written once with {project.metric} placeholders (and {_count} build counts); the build
fills them from the evaluation cards, so no number is typed by hand. Every sentence that carries a
card number becomes an evidence-check claim quoting the card row it comes from. Sentences may hold
build counts or card numbers, not both: counts are computed from the specs and have no card row.
Any other digit must be one of the literals the file allows (a model name, a year the person gave).

Used by build_content.py, which writes data/faq.json and adds the claims to claims.json.
"""
from __future__ import annotations

import re
import tomllib

import build_cards as bc

FAQ = bc.ROOT / "cards" / "faq.toml"
GLOBAL = re.compile(r"\{([a-z0-9-]+)\.([a-z0-9_]+)(?::([a-z]+))?\}")
COUNT = re.compile(r"\{(_[a-z]+)\}")
ANY_PH = re.compile(r"\{[^{}]+\}")
DIGIT = re.compile(r"\d")
SENTENCE = {"zh": re.compile(r"(?<=[。！？])"), "en": re.compile(r"(?<=[.!?])\s+")}
CARD_URL = "https://github.com/llia0031-dotcom/evidence-first/blob/main/cards/{id}{suffix}.md"
SECTIONS = ("top", "work", "method", "screens", "log", "about")  # home page anchors
ANCHORS = ("evaluation", "iteration", "limits")  # project page anchors
SOURCE_TYPES = ("project", "card", "section", "url")


def load() -> dict:
    with FAQ.open("rb") as f:
        return tomllib.load(f)


def _lint_digits(text: str, allowed: list[str], where: str) -> None:
    rest = ANY_PH.sub("", text)
    for lit in sorted(allowed, key=len, reverse=True):
        rest = rest.replace(lit, "")
    if DIGIT.search(rest):
        raise bc.BuildError(f"{where}: a typed number in {text!r}; use a placeholder or an allowed literal")


def build(projects: list[dict], card_texts: dict[tuple[str, str], str]) -> tuple[dict, list[dict]]:
    faq = load()
    allowed = faq.get("allowed_literals", [])
    flat = bc.global_values(projects)
    by_id = {p["spec"]["id"]: p for p in projects}
    shown = {pid for pid, p in by_id.items() if p["spec"]["status"] == "public" and pid not in bc.WITHHOLD}
    groups = {g["id"] for g in faq["group"]}
    ids = [it["id"] for it in faq["item"]]
    if len(ids) != len(set(ids)):
        raise bc.BuildError("faq: duplicate item id")
    items, claims = [], []
    for it in sorted(faq["item"], key=lambda x: x["order"]):
        iid = it["id"]
        if it["group"] not in groups:
            raise bc.BuildError(f"faq.{iid}: unknown group {it['group']}")
        for rel in it.get("related", []):
            if rel not in ids:
                raise bc.BuildError(f"faq.{iid}: unknown related item {rel}")
        answer = {}
        for lang in ("zh", "en"):
            raw = it["a"][lang]
            for text in [raw, it["q"][lang], *it["aliases"][lang]]:
                _lint_digits(text, allowed, f"faq.{iid}.{lang}")
            for m in GLOBAL.finditer(raw):
                if m.group(1) not in shown:
                    raise bc.BuildError(f"faq.{iid}: {m.group(1)} is not a public project")
            answer[lang] = bc.fill_global(raw, flat, lang, f"faq.{iid}")
            claims += _claims(iid, raw, lang, flat, by_id, card_texts)
        items.append({"id": iid, "group": it["group"], "order": it["order"], "chip": it.get("chip", False),
                      "q": it["q"], "aliases": it["aliases"], "a": answer,
                      "sources": [_source(s, by_id, shown, iid) for s in it.get("sources", [])],
                      "related": it.get("related", [])})
    data = {"groups": faq["group"], "items": items, "fallback": faq["fallback"]}
    return data, claims


def _claims(iid: str, raw: str, lang: str, flat: dict, by_id: dict, card_texts: dict) -> list[dict]:
    out = []
    for n, sent in enumerate(s for s in SENTENCE[lang].split(raw) if s.strip()):
        refs = [(m.group(1), m.group(2)) for m in GLOBAL.finditer(sent)]
        if not refs:
            continue
        if COUNT.search(sent):
            raise bc.BuildError(f"faq.{iid}.{lang}: a sentence mixes build counts and card numbers: {sent}")
        evidence = []
        for pid, mid in dict.fromkeys(refs):
            p = by_id[pid]
            ev_m = {m["id"]: m for ev in p["spec"]["eval"] for m in ev["metric"]}
            if mid not in ev_m:
                raise bc.BuildError(f"faq.{iid}: {pid} has no metric {mid}")
            m, v = ev_m[mid], p["values"][mid]
            label = bc.fill(bc.tr(m["label"], lang), p["values"], lang, mid)
            if "note" in m:
                note = bc.fill(bc.tr(m["note"], lang), p["values"], lang, mid)
                label += ("（" + note + "）") if lang == "zh" else (" (" + note + ")")
            source = f"{pid}{'' if lang == 'zh' else '.en'}.md"
            evidence.append({"source": source, "quote": _row(card_texts[(pid, lang)], v, lang, label)})
        out.append({"id": f"faq-{iid}-{lang}-{n + 1}", "text": bc.fill_global(sent.strip(), flat, lang, f"faq.{iid}"),
                    "evidence": evidence})
    return out


def _row(card_text: str, v: bc.Value, lang: str, label: str) -> str:
    full = v.full(lang)
    for line in card_text.splitlines():
        if line.startswith(f"| {label} | {full} |"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            return f"{cells[0]} | {cells[1]}"
    raise bc.BuildError(f"faq: {label} = {full} not found in the card")


def _source(s: dict, by_id: dict, shown: set, iid: str) -> dict:
    kind = s["type"]
    if kind not in SOURCE_TYPES:
        raise bc.BuildError(f"faq.{iid}: unknown source type {kind}")
    if kind in ("project", "card"):
        if s["id"] not in shown:
            raise bc.BuildError(f"faq.{iid}: {s['id']} is not a public project")
        spec = by_id[s["id"]]["spec"]
        name = {l: bc.tr(spec["name"], l) for l in ("zh", "en")}
        if kind == "project":
            if s.get("anchor") not in (None, *ANCHORS):
                raise bc.BuildError(f"faq.{iid}: unknown project anchor {s['anchor']}")
            repo = next((l["url"] for l in spec.get("links", []) if "github.com/" in bc.tr(l["url"], "en")), None)
            return {"type": kind, "id": s["id"], "label": s.get("label", name),
                    **({"anchor": s["anchor"]} if "anchor" in s else {}),
                    **({"url": {l: bc.tr(repo, l) for l in ("zh", "en")}} if repo else {})}
        return {"type": kind, "id": s["id"],
                "label": s.get("label", {"zh": f"评测卡：{name['zh']}", "en": f"Evaluation card: {name['en']}"}),
                "url": {"zh": CARD_URL.format(id=s["id"], suffix=""), "en": CARD_URL.format(id=s["id"], suffix=".en")}}
    if kind == "section":
        if s["id"] not in SECTIONS:
            raise bc.BuildError(f"faq.{iid}: unknown section {s['id']}")
        return {"type": kind, "id": s["id"], "label": s["label"]}
    url = s["url"]
    return {"type": kind, "label": s["label"], "url": url if isinstance(url, dict) else {"zh": url, "en": url}}
