"""Canary rollout, demonstrated by replaying stored test conversations. Not real users.

Each stored conversation (one test item, one run) is treated as a request. Both prompt versions
have already answered every request in the project's frozen comparison, so a replay only decides
which version's stored answer "serves" it: requests whose hash bucket is below the canary share go
to staging, the rest to production. At each step the rollback rules (written in ROLLOUTS below,
before the replay) are checked; if one fires, the replay stops and production stays put.

    python scripts/replay_canary.py          # writes prompts/rollout/canary-replay*.md and data/canary_replay.json
Standard library only. No model calls.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import build_cards as bc  # noqa: E402
from extractors import _kept_runs  # noqa: E402

STEPS = [10, 50, 100]
RESULTS = "grounded-review-public/eval/results/"

# Written before replaying. fault_field: the per-conversation failure the change is meant to fix.
ROLLOUTS = [
    {
        "id": "grounded-review-advice-v1.3",
        "asset": "grounded-review/advice",
        "production": "v1.1", "staging": "v1.3",
        "production_file": RESULTS + "multiturn-mt4-v1.1.jsonl",
        "staging_file": RESULTS + "multiturn-mt4-v1.3.jsonl",
        "fault_field": "advice_raw_problems",
        "set": {"zh": "mt4：12 条新广告，每版 3 遍", "en": "mt4: 12 new ads, 3 runs per version"},
    },
    {
        "id": "grounded-review-advice-v1.2",
        "asset": "grounded-review/advice",
        "production": "v1.1", "staging": "v1.2",
        "production_file": RESULTS + "multiturn-mt3-v1.1.jsonl",
        "staging_file": RESULTS + "multiturn-mt3-v1.2.jsonl",
        "fault_field": "fix_field_problems",
        "set": {"zh": "mt3：12 条新广告，每版 3 遍", "en": "mt3: 12 new ads, 3 runs per version"},
    },
]
RULES = {
    "fault": {"zh": "灰度组的字段写错比例高于线上组", "en": "staging's share of malformed advice is above production's"},
    "facts": {"zh": "灰度组改后版本丢品牌或价格的比例高于线上组", "en": "staging loses brand or price more often than production"},
    "cost": {"zh": "灰度组每段对话的平均费用比线上组高 10% 以上", "en": "staging's mean cost per conversation is more than 10% above production's"},
}


def bucket(item: str, run) -> int:
    return int(hashlib.sha256(f"{item}#{run}".encode()).hexdigest(), 16) % 100


def arm_stats(rows: list[dict], fault_field: str) -> dict:
    n = len(rows)
    if n == 0:
        return {"n": 0}
    return {
        "n": n,
        "faults": sum(1 for r in rows if r.get(fault_field)),
        "facts_lost": sum(1 for r in rows if r.get("fix_facts_kept") is not True),
        "cost": sum(r["agent_usage"]["cost_usd"] for r in rows) / n,
    }


def replay(cfg: dict, rd: bc.Reader) -> dict:
    prod = {(r["item"], r["run"]): r for r in _kept_runs(rd.jsonl(cfg["production_file"]))}
    stag = {(r["item"], r["run"]): r for r in _kept_runs(rd.jsonl(cfg["staging_file"]))}
    keys = sorted(set(prod) & set(stag))
    steps = []
    decision = "full"
    for share in STEPS:
        to_staging = [k for k in keys if bucket(*k) < share]
        to_prod = [k for k in keys if bucket(*k) >= share]
        s = arm_stats([stag[k] for k in to_staging], cfg["fault_field"])
        p = arm_stats([prod[k] for k in to_prod], cfg["fault_field"]) if to_prod else arm_stats([prod[k] for k in keys], cfg["fault_field"])
        fired = []
        if s["n"]:
            if s["faults"] / s["n"] > p["faults"] / p["n"]:
                fired.append("fault")
            if s["facts_lost"] / s["n"] > p["facts_lost"] / p["n"]:
                fired.append("facts")
            if s["cost"] > 1.10 * p["cost"]:
                fired.append("cost")
        steps.append({"share": share, "staging": s, "production": p,
                      "production_baseline": "served" if to_prod else "all requests (100% step)",
                      "fired": fired})
        if fired:
            decision = "rollback"
            break
    return {"id": cfg["id"], "asset": cfg["asset"], "production": cfg["production"], "staging": cfg["staging"],
            "requests": len(keys), "set": cfg["set"], "steps": steps, "decision": decision,
            "sources": sorted(rd.seen), "fingerprints": {k: v[:12] for k, v in rd.seen.items()}}


def pct(a: int, n: int) -> str:
    return f"{a}/{n}" if n else "—"


def render(results: list[dict], lang: str) -> str:
    zh = lang == "zh"
    L = (lambda a, b: a if zh else b)  # noqa: E731
    out = [L("# 灰度回放演示", "# Canary rollout replay"), ""]
    out.append(L("> **这是用评测题回放的演示，不是真实用户。** 这些项目没有线上流量。",
                 "> **This is a replay of test conversations, not real users.** None of these projects has live traffic."))
    out.append("")
    out.append(L(
        "做法：项目在冻结的对比评测里已经让新旧两版各回答了同一批题。回放把每段对话当成一个请求，按“题号#第几遍”的哈希分到 0–99 的桶里；桶号小于灰度比例的请求由 staging 版本的存档回答“接待”，其余由 production 版本接待。灰度按 "
        + " → ".join(f"{s}%" for s in STEPS) + " 放量，每一步都检查下面的回滚条件（回放前写好），触发就停下、production 不动。",
        "Method: in the project's frozen comparison both versions already answered the same items. The replay treats each stored conversation as a request and hashes \"item#run\" into buckets 0–99; requests below the canary share are served by the staging version's stored answer, the rest by production. The share goes "
        + " → ".join(f"{s}%" for s in STEPS) + "; at each step the rollback rules below (written before the replay) are checked, and if one fires the replay stops and production stays."))
    out.append("")
    out.append(L("回滚条件：", "Rollback rules:"))
    out.append("")
    for k, v in RULES.items():
        out.append(f"- {v[lang]}")
    out.append("")
    out.append(L("样本很小（每步只有几段到几十段对话），所以这里演示的是机制，不是统计结论。",
                 "The samples are tiny (a few to a few dozen conversations per step), so this shows the mechanism, not a statistical result."))
    out.append("")
    for r in results:
        out.append(f"## `{r['asset']}`：{r['production']} → {r['staging']}" if zh else f"## `{r['asset']}`: {r['production']} → {r['staging']}")
        out.append("")
        out.append(f"{L('回放的请求', 'Requests replayed')}{L('：', ': ')}{r['requests']}（{r['set'][lang]}）" if zh
                   else f"Requests replayed: {r['requests']} ({r['set'][lang]})")
        out.append("")
        out.append(f"| {L('灰度比例', 'Canary share')} | {L('staging 接待', 'Served by staging')} | {L('字段写错', 'Malformed advice')} | {L('丢品牌或价格', 'Brand or price lost')} | {L('平均费用', 'Mean cost')} | {L('触发的回滚条件', 'Rules fired')} |")
        out.append("|---|---|---|---|---|---|")
        for st in r["steps"]:
            s, p = st["staging"], st["production"]
            fired = "、".join(RULES[f][lang] for f in st["fired"]) if zh else "; ".join(RULES[f][lang] for f in st["fired"])
            out.append(
                f"| {st['share']}% | {s['n']} | staging {pct(s.get('faults', 0), s['n'])} · production {pct(p['faults'], p['n'])} | "
                f"staging {pct(s.get('facts_lost', 0), s['n'])} · production {pct(p['facts_lost'], p['n'])} | "
                f"staging {s.get('cost', 0):.4f} · production {p['cost']:.4f} | {fired or L('无', 'none')} |")
        out.append("")
        if r["decision"] == "rollback":
            out.append(L(f"**结果：回滚。** production 留在 {r['production']}，{r['staging']} 退回。",
                         f"**Result: rollback.** Production stays at {r['production']}; {r['staging']} is withdrawn."))
        else:
            out.append(L(f"**结果：全量。** 每一步都没有触发回滚条件，production 挪到 {r['staging']}。",
                         f"**Result: full release.** No rule fired at any step; production moves to {r['staging']}."))
        out.append("")
        if r["steps"][-1]["share"] == 100:
            out.append(L("费用单位是美元。100% 那一步没有 production 接待的请求，所以用 production 版本在全部请求上的存档做对照。",
                         "Cost is in US dollars. At the 100% step no request is served by production, so production's stored answers to all requests are the reference."))
        else:
            out.append(L("费用单位是美元。", "Cost is in US dollars."))
        out.append("")
        out.append(L("来源文件：", "Source files: ") + "、".join(f"`{p}`（{r['fingerprints'][p]}）" for p in r["sources"]) if zh
                   else "Source files: " + ", ".join(f"`{p}` ({r['fingerprints'][p]})" for p in r["sources"]))
        out.append("")
    return "\n".join(out)


def main() -> int:
    results = []
    for cfg in ROLLOUTS:
        results.append(replay(cfg, bc.Reader()))
    out_dir = ROOT / "prompts" / "rollout"
    (out_dir / "canary-replay.md").write_text(render(results, "zh"), encoding="utf-8", newline="\n")
    (out_dir / "canary-replay.en.md").write_text(render(results, "en"), encoding="utf-8", newline="\n")
    data = {"note": {"zh": "用评测题回放的演示，不是真实用户", "en": "Replay of test conversations, not real users"},
            "steps": STEPS, "rules": RULES, "rollouts": results}
    (ROOT / "data" / "canary_replay.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                                                       encoding="utf-8", newline="\n")
    for r in results:
        print(f"{r['id']}: {r['decision']} after {len(r['steps'])} step(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
