// promptfoo provider for the evidence-check skill regression check.
//
// Each instance stands for one release label (production or staging). It looks the label up in
// prompts/labels.json, loads that version's SKILL.md from prompts/texts/, and asks Claude Haiku 5.5 to
// check one draft against the fictional DemoClub documents. Both labels use the same model, effort,
// documents, wrapper text and JSON output format; only the skill text differs.
//
// The API key is read only from the file named by EF_ENV_FILE (a path relative to the repository root
// or absolute). It is never read from the environment of the calling shell, never logged and never
// written anywhere. No dependencies: Node's built-in fetch.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { parseEnv } from "node:util";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(here, "../../..");
const ASSET = "evidence-check/skill";
const MODEL = "claude-haiku-5-5"; // locked together with the prompt (see the release checklist)
const EFFORT = "medium";
const PRICE = { input: 0.1 / 1e6, output: 0.5 / 1e6 }; // list price per token, USD

function readKey() {
  const file = process.env.EF_ENV_FILE;
  if (!file) return "";
  const full = path.isAbsolute(file) ? file : path.resolve(REPO, file);
  if (!fs.existsSync(full)) return "";
  return (parseEnv(fs.readFileSync(full, "utf8")).ANTHROPIC_API_KEY ?? "").trim();
}
const apiKey = readKey();

const cases = JSON.parse(fs.readFileSync(path.join(here, "cases.json"), "utf8"));
const sourcesText = Object.values(cases.sources)
  .map((f) => `=== ${f} ===\n${fs.readFileSync(path.join(here, "sources", f), "utf8").trim()}`)
  .join("\n\n");

function skillFor(label) {
  const labels = JSON.parse(fs.readFileSync(path.join(REPO, "prompts/labels.json"), "utf8"));
  const version = labels[ASSET]?.[label];
  if (!version) throw new Error(`no ${label} label for ${ASSET}`);
  const file = path.join(REPO, "prompts/texts/evidence-check/skill", `${version}.md`);
  const text = fs.readFileSync(file, "utf8");
  return {
    version,
    sha: crypto.createHash("sha256").update(text).digest("hex").slice(0, 12),
    body: text.replace(/^---[\s\S]*?\n---\n/, "").trim(),
  };
}

function system(skillBody) {
  return [
    "You have the following skill loaded. Follow it.",
    "",
    '<skill name="evidence-check">',
    skillBody,
    "</skill>",
    "",
    'In this run you cannot execute the script yourself. Work in Mode B and return one entry per numbered line in the required JSON format: verdict "supported" only when you found a quote that states the claim; otherwise "unsupported" with an empty evidence list or the closest quote.',
  ].join("\n");
}

const SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["claims"],
  properties: {
    claims: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["id", "verdict", "evidence"],
        properties: {
          id: { type: "string" },
          verdict: { type: "string", enum: ["supported", "unsupported"] },
          evidence: {
            type: "array",
            items: {
              type: "object",
              additionalProperties: false,
              required: ["source", "quote"],
              properties: { source: { type: "string" }, quote: { type: "string" } },
            },
          },
        },
      },
    },
  },
};

function userMessage(draft) {
  const lines = draft.sentences.map((s, i) => `${i + 1}. ${s.text}`).join("\n");
  return `Source documents:\n\n${sourcesText}\n\nDraft to check (${draft.kind}; one claim per numbered line):\n${lines}`;
}

export default class SkillLabelProvider {
  constructor(options = {}) {
    this.label = options.config?.label;
  }

  id() {
    return `evidence-check-skill:${this.label}`;
  }

  async callApi(_prompt, context) {
    if (!apiKey) return { error: "NOT RUN: set EF_ENV_FILE to a file containing ANTHROPIC_API_KEY" };
    const draft = cases.drafts.find((d) => d.id === context?.vars?.draft_id);
    if (!draft) return { error: `unknown draft ${context?.vars?.draft_id}` };
    let skill;
    try {
      skill = skillFor(this.label);
    } catch (err) {
      return { error: err.message };
    }
    const started = Date.now();
    const res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "x-api-key": apiKey, "anthropic-version": "2023-06-01", "content-type": "application/json" },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: 16000,
        output_config: { effort: EFFORT, format: { type: "json_schema", schema: SCHEMA } },
        system: system(skill.body),
        messages: [{ role: "user", content: userMessage(draft) }],
      }),
    });
    if (!res.ok) return { error: `API error ${res.status}` };
    const body = await res.json();
    if (body.stop_reason === "refusal") return { error: "refused" };
    if (body.stop_reason === "max_tokens") return { error: "cut off at max_tokens" };
    const text = (body.content ?? []).filter((b) => b.type === "text").map((b) => b.text).join("");
    const { input_tokens = 0, output_tokens = 0 } = body.usage ?? {};
    return {
      output: text,
      tokenUsage: { prompt: input_tokens, completion: output_tokens, total: input_tokens + output_tokens },
      cost: input_tokens * PRICE.input + output_tokens * PRICE.output,
      metadata: {
        label: this.label, version: skill.version, skill_sha: skill.sha,
        model_served: body.model, effort: EFFORT, latency_ms: Date.now() - started,
      },
    };
  }
}
