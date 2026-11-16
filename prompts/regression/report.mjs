// Turns a promptfoo output file into the pull-request comment: pass counts per release label, the
// version and SKILL.md fingerprint each label pointed at, the drafts that failed, and the cost.
// Exits 1 when the check is red. The rules were written before the first run on GitHub:
//   1. every request got an answer (no API error, nothing cut off);
//   2. neither label fails more than MAX_FAIL drafts;
//   3. staging passes no more than MAX_DROP - 1 drafts fewer than production.
//
//   node prompts/regression/report.mjs <promptfoo-output.json> <comment.md>
import fs from "node:fs";

const MAX_FAIL = 2; // skill v0.1 made 2 false alarms in 168 judgements on this set
const MAX_DROP = 2;
const LABELS = ["production", "staging"];

const [inFile, outFile] = process.argv.slice(2);
if (!inFile || !outFile) {
  console.error("usage: node report.mjs <promptfoo-output.json> <comment.md>");
  process.exit(2);
}

function load() {
  try {
    return JSON.parse(fs.readFileSync(inFile, "utf8"));
  } catch {
    return null;
  }
}

const usd = (x) => `${x.toFixed(4)}`;

function summarise(rows) {
  const by = Object.fromEntries(LABELS.map((l) => [l, { n: 0, pass: 0, errors: 0, cost: 0, failed: [], versions: new Set(), shas: new Set(), models: new Set() }]));
  for (const r of rows) {
    const label = r.provider?.label ?? r.response?.metadata?.label;
    const s = by[label];
    if (!s) continue;
    s.n += 1;
    s.cost += r.response?.cost ?? r.cost ?? 0;
    const md = r.response?.metadata ?? {};
    if (md.version) s.versions.add(md.version);
    if (md.skill_sha) s.shas.add(md.skill_sha);
    if (md.model_served) s.models.add(md.model_served);
    const draft = r.vars?.draft_id ?? r.testCase?.vars?.draft_id ?? "?";
    const err = r.response?.error ?? r.error;
    if (err) {
      s.errors += 1;
      s.failed.push({ draft, why: String(err).slice(0, 160) });
    } else if (r.success) {
      s.pass += 1;
    } else {
      const why = r.gradingResult?.componentResults?.[0]?.reason ?? r.gradingResult?.reason ?? r.failureReason ?? "";
      s.failed.push({ draft, why: String(why).slice(0, 160) });
    }
  }
  return by;
}

function verdict(by) {
  const red = [];
  const errors = LABELS.reduce((a, l) => a + by[l].errors, 0);
  if (errors) red.push({ zh: `${errors} 个请求没有拿到回答`, en: `${errors} requests got no answer` });
  for (const l of LABELS) {
    if (by[l].n === 0) red.push({ zh: `${l} 没有结果`, en: `no results for ${l}` });
    else if (by[l].n - by[l].pass > MAX_FAIL) red.push({ zh: `${l} 没通过 ${by[l].n - by[l].pass} 篇，超过 ${MAX_FAIL} 篇`, en: `${l} failed ${by[l].n - by[l].pass} drafts, more than ${MAX_FAIL}` });
  }
  if (by.production.pass - by.staging.pass >= MAX_DROP) {
    red.push({ zh: `staging 比 production 少通过 ${by.production.pass - by.staging.pass} 篇`, en: `staging passed ${by.production.pass - by.staging.pass} fewer drafts than production` });
  }
  return red;
}

const out = load();
const rows = out?.results?.results ?? [];
const by = summarise(rows);
const red = out ? verdict(by) : [{ zh: "评测没有跑完，没有结果文件", en: "the evaluation did not finish; no result file" }];
const sha = (process.env.HEAD_SHA ?? "").slice(0, 7);
const list = (s) => [...s].join(", ") || "—";

const zh = [
  "## 提示词回归评测：evidence-check/skill",
  "",
  `开发评测 v1：12 篇虚构草稿，每句的答案在写题时就定好；一篇里每句都判对才算通过。两个标签用同一个模型、同一套资料和同一个输出格式，只有 SKILL.md 不同。${sha ? `提交 ${sha}。` : ""}`,
  "",
  "| 标签 | 版本 | SKILL.md 指纹 | 通过 | 费用（美元） |",
  "|---|---|---|---|---|",
  ...LABELS.map((l) => `| ${l} | ${list(by[l].versions)} | ${list(by[l].shas)} | ${by[l].pass}/${by[l].n} | ${usd(by[l].cost)} |`),
  "",
];
const failedZh = LABELS.flatMap((l) => by[l].failed.map((f) => `- ${l} ${f.draft}：${f.why}`));
zh.push(failedZh.length ? "没通过的草稿：\n" + failedZh.join("\n") : "所有草稿都通过。", "");
zh.push(red.length ? `**结果：标红**（${red.map((r) => r.zh).join("；")}）` : "**结果：通过**", "");
zh.push(`标红规则（第一次在 GitHub 上跑之前定好）：有请求没拿到回答；任一标签没通过的超过 ${MAX_FAIL} 篇；staging 比 production 少通过 ${MAX_DROP} 篇或更多。模型：${list(new Set(LABELS.flatMap((l) => [...by[l].models])))}。`);

const en = [
  "<details><summary>English</summary>",
  "",
  `Development set v1: 12 fictional drafts with every sentence's answer fixed when the drafts were written; a draft passes only if every sentence is judged right. Both labels use the same model, documents and output format; only SKILL.md differs.${sha ? ` Commit ${sha}.` : ""}`,
  "",
  "| Label | Version | SKILL.md hash | Passed | Cost (US$) |",
  "|---|---|---|---|---|",
  ...LABELS.map((l) => `| ${l} | ${list(by[l].versions)} | ${list(by[l].shas)} | ${by[l].pass}/${by[l].n} | ${usd(by[l].cost)} |`),
  "",
  red.length ? `**Result: red** (${red.map((r) => r.en).join("; ")})` : "**Result: passed**",
  "",
  `Red when (rules fixed before the first run on GitHub): a request got no answer; either label fails more than ${MAX_FAIL} drafts; staging passes ${MAX_DROP} or more drafts fewer than production.`,
  "",
  "</details>",
];

fs.writeFileSync(outFile, [...zh, "", ...en, ""].join("\n"));
console.log(LABELS.map((l) => `${l}: ${by[l].pass}/${by[l].n}`).join("  "), red.length ? "RED" : "PASSED");
process.exit(red.length ? 1 : 0);
