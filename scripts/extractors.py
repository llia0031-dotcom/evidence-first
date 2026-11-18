"""One function per kind of number. Each reads a project's own result files through `rd`
(a build_cards.Reader, which fingerprints every file it opens) and returns a dict:

    {"k": int, "n": int}                         a proportion (the default kind)
    {"kind": "median", "values": [...], "unit": "s"}
    {"kind": "value", "value": x, "unit": "usd", "n": optional}

Paths are relative to the folder that holds all projects side by side.
"""
from __future__ import annotations

import re
from collections import Counter, OrderedDict

REGISTRY: dict = {}


def extractor(fn):
    REGISTRY[fn.__name__] = fn
    return fn


# --------------------------------------------------------------------------- generic helpers
def _walk(node, keys):
    for key in keys:
        node = node[key]
    return node


@extractor
def json_counts(rd, path: str, arm: str | None = None, num: list | str = "k", den: str = "n",
                block: str = "counts", minus_den: list | None = None, minus_num: list | None = None,
                at: list | None = None):
    """Sum one or more count fields of a summary JSON as the numerator, another field as the denominator.

    The node is `at` (a list of keys / list indexes) if given, else d[arm][block].
    `den` may name a field or be an int; `minus_den` / `minus_num` subtract fields.
    """
    d = rd.json(path)
    if at is not None:
        node = _walk(d, at)
    else:
        node = d[arm] if arm else d
        if block:
            node = node[block]
    nums = [num] if isinstance(num, str) else num
    k = sum(node[x] for x in nums) - sum(node[x] for x in minus_num or [])
    n = den if isinstance(den, int) else node[den]
    for x in minus_den or []:
        n -= node[x]
    return {"k": k, "n": n}


@extractor
def json_counts_sum(rd, paths: list, at: list, num: str = "correct", den: str = "n"):
    """Same node in several files (e.g. one arm across four test sets), counts added up."""
    k = n = 0
    for p in paths:
        node = _walk(rd.json(p), at)
        k += node[num]
        n += node[den]
    return {"k": k, "n": n}


@extractor
def json_value(rd, path: str, keys: list, unit: str = "", decimals: int = 2, scale: float = 1.0,
               n_keys: list | None = None):
    d = rd.json(path)
    out = {"kind": "value", "value": float(_walk(d, keys)) * scale, "unit": unit, "decimals": decimals}
    if n_keys:
        out["n"] = int(_walk(d, n_keys))
    return out


@extractor
def json_ratio(rd, path: str, num_at: list, den_at: list, unit: str = "pct", decimals: int = 0):
    """A ratio of two values in one file, e.g. one arm's cost as a share of another's."""
    d = rd.json(path)
    r = float(_walk(d, num_at)) / float(_walk(d, den_at))
    return {"kind": "value", "value": 100 * r if unit == "pct" else r, "unit": unit, "decimals": decimals}


# --------------------------------------------------------------------------- screening-audit
@extractor
def sa_script_loss(rd, path: str, arm: str, base: str):
    """Correct 'met' verdicts the quote script threw away: false_not_met(arm + script) - false_not_met(arm)."""
    acc = rd.json(path)["accuracy"]
    k = acc[arm]["false_not_met"] - acc[base]["false_not_met"]
    # Out of the correct "met" verdicts the base arm gave, which is what the check had to keep.
    return {"k": k, "n": acc[base]["gold_met"] - acc[base]["false_not_met"]}


@extractor
def sa_traps_right(rd, path: str, arm: str):
    """Trap requirements (answer: not met) judged not met."""
    a = rd.json(path)["accuracy"][arm]
    return {"k": a["gold_not_met"] - a["false_met"], "n": a["gold_not_met"]}


@extractor
def sa_verify(rd, path: str, arm: str, field: str = "caught", total: str = "misreadings"):
    """Second-judgement runs: add up the two runs of one arm."""
    runs = rd.json(path)["arms"][arm]
    return {"k": sum(r[field] for r in runs.values()), "n": sum(r[total] for r in runs.values())}


def _kept_runs(rows: list[dict]) -> list[dict]:
    """Drop rows that carry an error; keep the last row per (item, run) — the projects' own rule."""
    kept: "OrderedDict[tuple, dict]" = OrderedDict()
    for r in rows:
        if r.get("errors"):
            continue
        kept[(r.get("arm"), r["item"], r.get("run"))] = r
    return list(kept.values())


# --------------------------------------------------------------------------- grounded-review (ad review)
@extractor
def gr_multiturn(rd, path: str, field: str, test: str = "nonempty"):
    """Multi-turn files: count kept conversations where `field` is non-empty (a fault) or empty (clean)."""
    rows = _kept_runs(rd.jsonl(path))
    def value(r):
        node = r
        for part in field.split("."):
            node = node.get(part) if isinstance(node, dict) else None
        return node
    if test == "nonempty":
        k = sum(1 for r in rows if value(r))
    elif test == "empty":
        k = sum(1 for r in rows if not value(r))
    elif test == "true":
        k = sum(1 for r in rows if value(r) is True)
    else:
        raise ValueError(test)
    return {"k": k, "n": len(rows)}


@extractor
def gr_multiturn_cost(rd, path: str):
    rows = _kept_runs(rd.jsonl(path))
    total = sum(r["agent_usage"]["cost_usd"] for r in rows)
    return {"kind": "value", "value": total / len(rows), "unit": "usd", "decimals": 4, "n": len(rows)}


@extractor
def json_mean_ci(rd, path: str, at: list, unit: str = "", decimals: int = 2, n_at: list | None = None):
    """A mean with its interval as stored by the project (e.g. a bootstrap done in the project's own script)."""
    d = rd.json(path)
    node = _walk(d, at)
    out = {"kind": "mean", "value": node["mean"], "ci": node["ci"], "unit": unit, "decimals": decimals}
    if n_at:
        out["n"] = int(_walk(d, n_at))
    return out


# --------------------------------------------------------------------------- voice-agent-eval
VOICE_RUNS = ["voice-agent-eval/eval/results/run1/scores.json", "voice-agent-eval/eval/results/run2/scores.json"]


def _voice_items(rd, arm: str, runs: list | None = None):
    for p in runs or VOICE_RUNS:
        d = rd.json(p)
        yield d, d["items"][arm]


@extractor
def vo_strict(rd, arm: str, runs: list | None = None):
    """Strict pass (task done and interaction right), both runs pooled."""
    k = n = 0
    for d, _ in _voice_items(rd, arm, runs):
        k += d["summary"][arm]["strict_pass"]
        n += d["summary"][arm]["n"]
    return {"k": k, "n": n}


@extractor
def vo_first_audio(rd, arm: str, cat: str = "task", noise: str | None = "none"):
    """Seconds from end of user speech to first audio, request turns only, both runs pooled (tables.py rule)."""
    vals = []
    for _, items in _voice_items(rd, arm):
        for it in items:
            if it["cat"] != cat or (noise is not None and it.get("noise", "none") != noise):
                continue
            for lat in it.get("latency", []):
                if lat.get("role") == "request" and lat.get("first_audio") is not None:
                    vals.append(lat["first_audio"])
    return {"kind": "median", "values": vals, "unit": "s", "decimals": 2}


@extractor
def vo_interaction(rd, arm: str, cat: str, field: str, want: bool = True):
    """Items of one category whose interaction field has the wanted value, both runs pooled."""
    k = n = 0
    for _, items in _voice_items(rd, arm):
        for it in items:
            ia = it.get("interaction") or {}
            if it["cat"] == cat and field in ia:
                n += 1
                k += ia[field] is want
    return {"k": k, "n": n}


@extractor
def vo_stop_latency(rd, arm: str):
    vals = []
    for _, items in _voice_items(rd, arm):
        vals += [it["stop_latency"] for it in items if it["cat"] == "interrupt" and "stop_latency" in it]
    return {"kind": "median", "values": vals, "unit": "s", "decimals": 2}


@extractor
def vo_leaks(rd, arm: str):
    k = n = 0
    for _, items in _voice_items(rd, arm):
        n += len(items)
        k += sum(1 for it in items if it.get("leak"))
    return {"k": k, "n": n}


# --------------------------------------------------------------------------- markdown summaries
FRACTION = re.compile(r"(\d+)\s*/\s*(\d+)")


def _md_tables(text: str, section: str | None):
    """Yield (header_cells, row_cells) for every table row, optionally only under a heading that starts with `section`."""
    active = section is None
    header = None
    for line in text.splitlines():
        if line.startswith("#"):
            if section is not None:
                active = line.lstrip("#").strip().startswith(section)
            header = None
            continue
        if not active or not line.strip().startswith("|"):
            header = None if not line.strip().startswith("|") else header
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        if header is None:
            header = cells
            continue
        yield header, cells


NUMBER = re.compile(r"[-+]?\d+(?:\.\d+)?")


def _first_number(cell: str) -> float:
    m = NUMBER.search(cell.replace(",", ""))
    if not m:
        raise ValueError(f"no number in {cell!r}")
    return float(m.group(0))


@extractor
def text_fraction(rd, path: str, label: str):
    """The k/n that follows a fixed label in running text, e.g. "marked unsure: 11/49"."""
    text = rd.text(path)
    i = text.find(label)
    if i < 0 or text.find(label, i + 1) >= 0:
        raise ValueError(f"{path}: label {label!r} must appear exactly once")
    m = FRACTION.search(text, i + len(label))
    return {"k": int(m.group(1)), "n": int(m.group(2))}


@extractor
def json_count_true(rd, path: str, at: list, field: str):
    """How many entries of a dict or list have `field` true, out of all entries."""
    node = _walk(rd.json(path), at)
    rows = list(node.values()) if isinstance(node, dict) else list(node)
    return {"k": sum(1 for r in rows if r.get(field) is True), "n": len(rows)}


@extractor
def json_sum(rd, path: str, at: list, field: str, unit: str = "", decimals: int = 2):
    """The sum of one field over the entries of a dict, e.g. the cost of every stage."""
    node = _walk(rd.json(path), at)
    rows = list(node.values()) if isinstance(node, dict) else list(node)
    return {"kind": "value", "value": sum(float(r[field]) for r in rows if isinstance(r, dict) and field in r), "unit": unit, "decimals": decimals}


def _clean(cell: str) -> str:
    return cell.replace("**", "").strip()


@extractor
def md_cell(rd, path: str, row: str, col: str, section: str | None = None, part: str = "only"):
    """A k/n cell in a markdown table produced by the project's own scoring script.

    `row` matches the first cell (bold and spacing ignored); `col` matches a header cell.
    For cells like "0/11 → 11/11", `part` picks "before" or "after".
    """
    for header, cells in _md_tables(rd.text(path), section):
        if _clean(cells[0]) != row:
            continue
        idx = [_clean(h) for h in header].index(col)
        cell = _clean(cells[idx])
        if "→" in cell:
            before, after = cell.split("→")
            cell = before if part == "before" else after
        m = FRACTION.search(cell)
        return {"k": int(m.group(1)), "n": int(m.group(2))}
    raise KeyError(f"{path}: row {row!r} not found")


@extractor
def md_match_cell(rd, path: str, match: dict, col: str):
    """A k/n cell from the one markdown table row whose named columns hold the given values."""
    hits = []
    for header, cells in _md_tables(rd.text(path), None):
        names = [_clean(h) for h in header]
        if col not in names or not all(k in names for k in match):
            continue
        for row in cells if isinstance(cells[0], list) else [cells]:
            if all(_clean(row[names.index(k)]) == v for k, v in match.items()):
                hits.append(_clean(row[names.index(col)]))
    if len(hits) != 1:
        raise ValueError(f"{path}: {len(hits)} rows match {match}")
    m = FRACTION.search(hits[0])
    return {"k": int(m.group(1)), "n": int(m.group(2))}


@extractor
def md_match_value(rd, path: str, match: dict, col: str, unit: str = "", decimals: int = 2):
    """A plain number from the one markdown table row whose named columns hold the given values."""
    hits = []
    for header, cells in _md_tables(rd.text(path), None):
        names = [_clean(h) for h in header]
        if col not in names or not all(k in names for k in match):
            continue
        if all(_clean(cells[names.index(k)]) == v for k, v in match.items()):
            hits.append(_clean(cells[names.index(col)]))
    if len(hits) != 1:
        raise ValueError(f"{path}: {len(hits)} rows match {match}")
    return {"kind": "value", "value": _first_number(hits[0]), "unit": unit, "decimals": decimals}


@extractor
def md_value(rd, path: str, row: str, col: str, section: str | None = None, unit: str = "", decimals: int = 2):
    for header, cells in _md_tables(rd.text(path), section):
        if _clean(cells[0]) == row:
            idx = [_clean(h) for h in header].index(col)
            return {"kind": "value", "value": _first_number(_clean(cells[idx])), "unit": unit, "decimals": decimals}
    raise KeyError(f"{path}: row {row!r} not found")


# --------------------------------------------------------------------------- rows selected by field values
@extractor
def json_row(rd, path: str, list_key: str, match: dict, num: str, den: str | None = None,
             value: bool = False, unit: str = "", decimals: int = 3):
    """Pick the one row of a list whose fields equal `match`; return num/den or a single value."""
    rows = [r for r in rd.json(path)[list_key] if all(r.get(k) == v for k, v in match.items())]
    if len(rows) != 1:
        raise KeyError(f"{path}: {len(rows)} rows match {match}")
    r = rows[0]
    if value:
        return {"kind": "value", "value": float(r[num]), "unit": unit, "decimals": decimals, "n": r.get("n")}
    return {"k": r[num], "n": r[den]}


# --------------------------------------------------------------------------- aigc-scene-eval (text on product)
@extractor
def ai_tool(rd, path: str, section: str, tool: str, what: str):
    """One tool's entry in report/results.json: text exact, overall rating (mean, CI), usable, best pick."""
    rows = [r for r in rd.json(path)[section]["summary"] if r["tool"] == tool]
    if len(rows) != 1:
        raise KeyError(f"{path}: tool {tool} not found")
    r = rows[0]
    if what == "text_exact":
        return {"k": r["text"]["exact"], "n": r["text"]["transcribed"]}
    if what == "overall":
        return {"kind": "mean", "value": r["overall"]["mean"], "ci": r["overall"]["ci"], "decimals": 2,
                "n": r["n_judgments"]}
    if what == "usable":
        return {"k": r["usable"]["能直接用"], "n": r["n_judgments"]}
    if what == "best":
        return {"k": r["best"]["won"], "n": r["best"]["chances"]}
    raise ValueError(what)


# --------------------------------------------------------------------------- grounded-labelling-pipeline
@extractor
def pl_version(rd, path: str, version: str, field: str):
    """Regression replay stats per prompt version: escaped / queued / decision_right out of requests."""
    st = rd.json(path)["stats"][version]
    return {"k": st[field], "n": st["requests"]}


@extractor
def pl_canary_rollback_share(rd, path: str):
    """Canary share (percent of requests) at the first step where a rollback rule fired."""
    d = rd.json(path)
    fired = [s for s in d["steps"] if s["fired"]]
    if not fired:
        raise ValueError(f"{path}: no rollback")
    return {"kind": "value", "value": fired[0]["share"], "unit": "pct", "decimals": 0}


@extractor
def pl_canary_step(rd, path: str, share: int, arm: str, field: str):
    """One arm at one canary step: a count field out of the arm's requests."""
    step = next(s for s in rd.json(path)["steps"] if s["share"] == share and s[arm]["n"])
    return {"k": step[arm][field], "n": step[arm]["n"]}


@extractor
def pl_retrieval(rd, path: str, query: str, col: str = "hit@3"):
    """Policy retrieval: share of labelled violations whose right clause is in the top results."""
    import csv
    import io
    rows = [r for r in csv.DictReader(io.StringIO(rd.text(path))) if r["query"] == query]
    return {"k": sum(1 for r in rows if r[col] == "True"), "n": len(rows)}


@extractor
def pl_retrieval_method(rd, path: str, set: str, query: str, lang: str, method: str, model: str = "", col: str = "hit@3"):
    """One row of the retrieval comparison table: a hit rate over n labels, turned back into a count."""
    import csv
    import io
    rows = [r for r in csv.DictReader(io.StringIO(rd.text(path)))
            if (r["set"], r["query"], r["lang"], r["method"], r["model"]) == (set, query, lang, method, model)]
    if len(rows) != 1:
        raise ValueError(f"{path}: {len(rows)} rows for {set}/{query}/{lang}/{method}/{model}")
    n = int(rows[0]["n"])
    k = round(float(rows[0][col]) * n)
    if abs(k / n - float(rows[0][col])) > 0.0001:
        raise ValueError(f"{path}: {col} {rows[0][col]} is not a whole count of {n}")
    return {"k": k, "n": n}


@extractor
def pl_canary_final_share(rd, path: str):
    """Canary share at the last step of a replay that finished without a rollback."""
    d = rd.json(path)
    if d.get("result") != "full":
        raise ValueError(f"{path}: replay did not reach full release")
    return {"kind": "value", "value": d["steps"][-1]["share"], "unit": "pct", "decimals": 0}
