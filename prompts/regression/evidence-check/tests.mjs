// One test per draft. Only the draft id reaches the provider; labels never reach the model.
// Each test passes only if every sentence gets the verdict fixed when the draft was written:
// every planted error marked unsupported and no correct sentence marked unsupported.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const { drafts } = JSON.parse(fs.readFileSync(path.join(here, "cases.json"), "utf8"));

function grade(output, draftId) {
  const draft = drafts.find((d) => d.id === draftId);
  let parsed;
  try {
    parsed = JSON.parse(output);
  } catch {
    return { pass: false, score: 0, reason: "output is not JSON" };
  }
  const byId = new Map((parsed.claims ?? []).map((c) => [String(c.id), c.verdict]));
  let right = 0;
  const wrong = [];
  draft.sentences.forEach((s, i) => {
    const got = byId.get(String(i + 1));
    if (got === s.label) right += 1;
    else wrong.push(`${i + 1}:${s.type}→${got ?? "missing"}`);
  });
  const n = draft.sentences.length;
  return {
    pass: wrong.length === 0,
    score: right / n,
    reason: wrong.length ? `${right}/${n} right; wrong: ${wrong.join(", ")}` : `${n}/${n} right`,
  };
}

export default drafts.map((d) => ({
  description: `${d.id} (${d.lang}, ${d.kind})`,
  vars: { draft_id: d.id },
  assert: [{ type: "javascript", value: (output) => grade(output, d.id) }],
}));
