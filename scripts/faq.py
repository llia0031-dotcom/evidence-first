"""The "ask me" questions and answers at the end of the portfolio, built from cards/faq.toml.

They are for a recruiter or interviewer who reads the portfolio before an interview: who this is,
what they are looking for, what they can do, which project to open, how to reach them.

Three kinds of entries:
- written ones in cards/faq.toml, with {project.metric} placeholders (and {_count} build counts);
- one per public project, made from its card (title, result line, page and code links);
- one per hiring direction, listing the projects that fit (from [[direction]] in the file).

No number is typed by hand: every sentence that carries a card number becomes an evidence-check claim
quoting the card row it comes from. A sentence holds card numbers or build counts, not both (counts
are computed from the specs and have no card row). Any other digit in a written entry must be one of
the literals the file allows. Entries in the "more" group (questions an interview would ask) come
last, and no other entry points to them as a related question.

Used by build_content.py, which writes data/faq.json and adds the claims to claims.json.
"""
from __future__ import annotations

import re
import tomllib

import build_cards as bc

FAQ = bc.ROOT / "cards" / "faq.toml"
GLOBAL = re.compile(r"\{([a-z0-9-]+)\.([a-z0-9_]+)(?::([a-z]+))?\}")
LOCAL = re.compile(r"\{([a-z0-9_]+)(:[a-z]+)?\}")
COUNT = re.compile(r"\{(_[a-z]+)\}")
ANY_PH = re.compile(r"\{[^{}]+\}")
DIGIT = re.compile(r"\d")
SENTENCE = {"zh": re.compile(r"(?<=[。！？])"), "en": re.compile(r"(?<=[.!?])\s+")}
CARD_URL = "https://github.com/llia0031-dotcom/evidence-first/blob/main/cards/{id}{suffix}.md"
SECTIONS = ("top", "work", "method", "screens", "log", "about")  # home page anchors
ANCHORS = ("evaluation", "iteration", "limits")  # project page anchors
SOURCE_TYPES = ("project", "card", "section", "url")
LATER = "more"  # the group of interview-style questions
LANGS = ("zh", "en")


def load() -> dict:
    with FAQ.open("rb") as f:
        return tomllib.load(f)


def _lint_digits(text: str, allowed: list[str], where: str) -> None:
    rest = ANY_PH.sub("", text)
    for lit in sorted(allowed, key=len, reverse=True):
        rest = rest.replace(lit, "")
    if DIGIT.search(rest):
        raise bc.BuildError(f"{where}: a typed number in {text!r}; use a placeholder or an allowed literal")


def _globalise(text: str, pid: str) -> str:
    """A card's own {metric} placeholders as {project.metric}."""
    return LOCAL.sub(lambda m: "{" + f"{pid}.{m.group(1)}" + (m.group(2) or "") + "}", text)


def _repo(spec: dict) -> str | None:
    return next((bc.tr(l["url"], "en") for l in spec.get("links", []) if "github.com/" in bc.tr(l["url"], "en")), None)


def _display(name: str) -> str:
    """A project name without its subtitle: "有据审核（广告审核 Agent）" -> "有据审核"."""
    return re.split(r"（| \(|：|: ", name, maxsplit=1)[0]


def _join_zh(a: str, b: str) -> str:
    """Chinese next to Latin letters or digits gets a space between them."""
    if a and b and (a[-1].isascii() and a[-1].isalnum()) != (b[0].isascii() and b[0].isalnum()):
        return f"{a} {b}"
    return a + b


def _end(text: str, lang: str) -> str:
    """Close a title as a sentence: a question keeps or gets its question mark."""
    if text.endswith(("。", "？", "！", ".", "?", "!")):
        return text
    if lang == "zh":
        return text + ("？" if text.endswith(("吗", "么", "呢")) else "。")
    return text + "."


def project_items(faq: dict, by_id: dict, shown: list[str]) -> list[dict]:
    tpl = faq["project_item"]
    out = []
    for n, pid in enumerate(shown):
        spec = by_id[pid]["spec"]
        full = {l: bc.tr(spec["name"], l) for l in LANGS}
        names = {l: _display(full[l]) for l in LANGS}
        shorts = {l: bc.tr(spec["short_name"], l) for l in LANGS}
        repo = _repo(spec)
        alias = {l: list(dict.fromkeys([names[l], full[l], shorts[l], pid] + ([repo.rstrip("/").rsplit("/", 1)[1]] if repo else [])))
                 for l in LANGS}
        answer = {l: _end(bc.tr(spec["card_title"], l), l) + ("" if l == "zh" else " ")
                  + _end(_globalise(bc.tr(spec["result_line"], l), pid), l) for l in LANGS}
        sources = [{"type": "project", "id": pid}]
        if repo:
            sources.append({"type": "url", "url": repo, "label": tpl["code_label"]})
        out.append({"id": f"project-{pid}", "group": tpl["group"], "order": tpl["order"] + n,
                    "q": {"zh": _join_zh(names["zh"], tpl["q"]["zh"]), "en": tpl["q"]["en"].format(name=names["en"])},
                    "aliases": alias, "a": answer,
                    "sources": sources, "related": tpl.get("related", [])})
    return out


def direction_items(faq: dict, by_id: dict, shown: list[str]) -> list[dict]:
    tpl = faq["direction_item"]
    out = []
    for n, d in enumerate(faq.get("direction", [])):
        for pid in d["projects"]:
            if pid not in shown:
                raise bc.BuildError(f"faq direction {d['id']}: {pid} is not a public project")
        parts = {l: [f"{_display(bc.tr(by_id[p]['spec']['name'], l))}{'（' if l == 'zh' else ' ('}"
                     f"{bc.tr(by_id[p]['spec']['card_title'], l).rstrip('?')}{'）' if l == 'zh' else ')'}"
                     for p in d["projects"]] for l in LANGS}
        answer = {"zh": "；".join(parts["zh"]) + "。", "en": "; ".join(parts["en"]) + "."}
        out.append({"id": f"direction-{d['id']}", "group": tpl["group"], "order": tpl["order"] + n,
                    "q": d["q"], "aliases": d["aliases"], "a": answer,
                    "sources": [{"type": "project", "id": p} for p in d["projects"]],
                    "related": tpl.get("related", [])})
    return out


def build(projects: list[dict], card_texts: dict[tuple[str, str], str]) -> tuple[dict, list[dict]]:
    faq = load()
    allowed = faq.get("allowed_literals", [])
    flat = bc.global_values(projects)
    by_id = {p["spec"]["id"]: p for p in projects}
    shown = [p["spec"]["id"] for p in sorted(projects, key=lambda p: p["spec"]["order"])
             if p["spec"]["status"] == "public" and p["spec"]["id"] not in bc.WITHHOLD]
    groups = {g["id"] for g in faq["group"]}
    written = faq["item"]
    for it in written:
        for lang in LANGS:
            for text in [it["a"][lang], it["q"][lang], *it["aliases"][lang]]:
                _lint_digits(text, allowed, f"faq.{it['id']}.{lang}")
    every = written + direction_items(faq, by_id, shown) + project_items(faq, by_id, shown)
    group_of = {it["id"]: it["group"] for it in every}
    if len(group_of) != len(every):
        raise bc.BuildError("faq: duplicate item id")
    ordered = sorted(every, key=lambda x: x["order"])
    if any(it["group"] == LATER for it in ordered[:len(ordered) - sum(1 for x in every if x["group"] == LATER)]):
        raise bc.BuildError("faq: interview-style questions must come last")
    items, claims = [], []
    for it in ordered:
        iid = it["id"]
        if it["group"] not in groups:
            raise bc.BuildError(f"faq.{iid}: unknown group {it['group']}")
        if it.get("chip") and it["group"] == LATER:
            raise bc.BuildError(f"faq.{iid}: an interview-style question cannot be a chip")
        for rel in it.get("related", []):
            if rel not in group_of:
                raise bc.BuildError(f"faq.{iid}: unknown related item {rel}")
            if group_of[rel] == LATER and it["group"] != LATER:
                raise bc.BuildError(f"faq.{iid}: points to {rel}, an interview-style question")
        answer = {}
        for lang in LANGS:
            raw = it["a"][lang]
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


def _source(s: dict, by_id: dict, shown: list, iid: str) -> dict:
    kind = s["type"]
    if kind not in SOURCE_TYPES:
        raise bc.BuildError(f"faq.{iid}: unknown source type {kind}")
    if kind in ("project", "card"):
        if s["id"] not in shown:
            raise bc.BuildError(f"faq.{iid}: {s['id']} is not a public project")
        spec = by_id[s["id"]]["spec"]
        name = {l: bc.tr(spec["name"], l) for l in LANGS}
        if kind == "project":
            if s.get("anchor") not in (None, *ANCHORS):
                raise bc.BuildError(f"faq.{iid}: unknown project anchor {s['anchor']}")
            repo = _repo(spec)
            return {"type": kind, "id": s["id"], "label": s.get("label", name),
                    **({"anchor": s["anchor"]} if "anchor" in s else {}),
                    **({"url": {l: repo for l in LANGS}} if repo else {})}
        return {"type": kind, "id": s["id"],
                "label": s.get("label", {"zh": f"评测卡：{name['zh']}", "en": f"Evaluation card: {name['en']}"}),
                "url": {"zh": CARD_URL.format(id=s["id"], suffix=""), "en": CARD_URL.format(id=s["id"], suffix=".en")}}
    if kind == "section":
        if s["id"] not in SECTIONS:
            raise bc.BuildError(f"faq.{iid}: unknown section {s['id']}")
        return {"type": kind, "id": s["id"], "label": s["label"]}
    url = s["url"]
    return {"type": kind, "label": s["label"], "url": url if isinstance(url, dict) else {"zh": url, "en": url}}
