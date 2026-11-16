# 有据可查 evidence-check：评测卡

> 卡片版本 1.1 · 数据截至 2026-11-15 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-12 – 2026-11-14 | Liang Liyuan | Python（只用标准库）、Agent Skill、promptfoo | [代码和报告](https://github.com/Jason-d-e/evidence-check) |

**问题**：AI 按资料写的回答和草稿，会悄悄改掉日期、数字，或者多出资料里没有的话；要让每句事实都附逐字原文，再用脚本核对。

**我做了什么**：我把 TraceDesk 里逐字核对引文和数字的规则抽出来，做成谁都能装的 Skill 加核对脚本；先在开发评测里找问题、改出 v0.2，再在冻结的留出题上和普通提示比较；之后按其他几个项目实际使用这个脚本时的误报和待改清单两次改规则（0.3.0、0.4.0），每次改之前先写好新题。

**结果**：

- 留出评测：埋的错误全部标出 60/60，正确事实误标 3/150
- 编造数字的回答：普通提示 4/32 → Skill v0.2 0/32
- 脚本 0.4.0：正确说法通过 0/11 → 11/11，改错的数字仍全部标出 13/13

## 概况

一个 Agent Skill 加一个核对脚本。Skill 让 Agent 给每句事实附上资料里逐字的原文；脚本核对两件事：原文真的在所引的文件里（大小写、空格、弯引号和标点不计较），以及这句话里的日期、时间、金额和数量也都出现在原文里，中英文数字互认（例如“下午2点”和 14:00）。脚本判断不了意思，所以 Skill 还要求 Agent 逐条读一遍通过的说法。两种用法：按资料回答问题；核对一篇草稿。

- **在作品集里的位置**：核心部件
- **和核心部件的关系**：就是核心部件本身：卖点体检、有据审核、简历初筛都调用它的脚本；匹配和数字规则移植自 TraceDesk。
- **用到的模型**：评测用 claude-haiku-5-5（effort medium）；脚本本身不调用模型，只要 Python 3.9 以上。

## 用途

- 按自己的资料回答问题，每句事实附原文，没通过核对的句子在给人看之前改掉或删掉。
- 核对一篇草稿：拆成一句句，逐句找原文、跑脚本，列出有问题的句子、原文和一条修改建议。
- 当作其他 Agent 的“引文核对”工具（有据审核、卖点体检都这样接）。

## 不适用的地方

- 观点、头脑风暴这类没有出处可查的内容。
- 判断意思：一句真实的原文可能被拿来支持相反的说法，脚本看不出来。
- 加总、换算、算出来的天数和比例：脚本会故意标出来，让人去核对。

## 评测数据

### 留出评测 v2（144 次对话）

虚构活动的资料，16 个问题（中英各 8）和 8 篇草稿，草稿里埋了 30 处错误（矛盾、数字、编造、过时、算出来的），另有 75 个正确事实。Skill v0.2 在写这些题之前就冻结；跑前冻结题目和打分脚本的哈希。三组：普通提示、Skill v0.1、Skill v0.2，同一个模型、同一份资料、同一种输出格式。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-12 |
| 题目和答案 | 24 道题，每组 2 遍，3 组共 144 次对话 |
| 跑了几次 | 每组 2 遍，合并计算；同一题两遍不独立，区间偏窄 |
| 模型和发送方式 | claude-haiku-5-5，普通接口 |
| 跑前冻结 | `eval/v2/PREREGISTRATION.md`（计划、预期、12 个文件的哈希） |

### 脚本 0.3.0：36 条新说法（只跑脚本）

照其他几个项目实际使用这个脚本时的误报改了 9 条规则。改之前先写好 36 条新说法：正确的应当通过，改错数字的必须标出，超出能力的故意标出。只跑脚本，不调用模型。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-13 |
| 题目和答案 | 36 条说法 |
| 跑了几次 | 确定性脚本，跑 1 遍 |
| 模型和发送方式 | 不调用模型，不花钱 |
| 跑前冻结 | `eval/v3/PREREGISTRATION.md` |

### 脚本 0.4.0：28 条新说法（只跑脚本）

加了 6 条规则（四舍五入保留两位有效数字就认、中文序数等）。改之前先写好 28 条新说法；v1 到 v3 的题也重跑，确认没有退步。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-14 |
| 题目和答案 | 28 条说法 |
| 跑了几次 | 确定性脚本，跑 1 遍 |
| 模型和发送方式 | 不调用模型，不花钱 |
| 跑前冻结 | `eval/v4/PREREGISTRATION.md` |

## 指标和结果

每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。

### 留出评测 v2（144 次对话）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 埋的错误被标出（Skill v0.2） | 60/60（100.0%，95% 区间 94.0–100.0%） | 越高越好 | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/Jason-d-e/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |
| 正确事实被误标（普通提示 + 脚本） | 12/150（8.0%，95% 区间 4.6–13.5%） | 越低越好 | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/Jason-d-e/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |
| 正确事实被误标（Skill v0.2） | 3/150（2.0%，95% 区间 0.7–5.7%） | 越低越好 | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/Jason-d-e/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |
| 回答里有编造的数字（普通提示） | 4/32（12.5%，95% 区间 5.0–28.1%） | 越低越好 | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/Jason-d-e/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |
| 回答里有编造的数字（Skill v0.1） | 2/32（6.2%，95% 区间 1.7–20.1%） | 越低越好 | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/Jason-d-e/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |
| 回答里有编造的数字（Skill v0.2） | 0/32（0.0%，95% 区间 0.0–10.7%） | 越低越好 | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/Jason-d-e/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |
| 48 次对话的费用（普通提示） | 0.0520 美元 | 越低越好 | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/Jason-d-e/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |
| 48 次对话的费用（Skill v0.2） | 0.1603 美元 | 越低越好 | [`evidence-check/eval/v2/results/run-2026-11-12.summary.md`](https://github.com/Jason-d-e/evidence-check/blob/main/eval/v2/results/run-2026-11-12.summary.md) |

三组都标出了全部埋的错误；Skill 的作用在回答问题时：不再编数字。

### 脚本 0.3.0：36 条新说法（只跑脚本）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 正确说法通过（0.2.0） | 3/16（18.8%，95% 区间 6.6–43.0%） | 越高越好 | [`evidence-check/eval/v3/results/script-only.md`](https://github.com/Jason-d-e/evidence-check/blob/main/eval/v3/results/script-only.md) |
| 正确说法通过（改后） | 16/16（100.0%，95% 区间 80.6–100.0%） | 越高越好 | [`evidence-check/eval/v3/results/script-only.md`](https://github.com/Jason-d-e/evidence-check/blob/main/eval/v3/results/script-only.md) |
| 改错的数字被标出（改后） | 17/17（100.0%，95% 区间 81.6–100.0%） | 越高越好 | [`evidence-check/eval/v3/results/script-only.md`](https://github.com/Jason-d-e/evidence-check/blob/main/eval/v3/results/script-only.md) |

### 脚本 0.4.0：28 条新说法（只跑脚本）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 正确说法通过（0.3.0） | 0/11（0.0%，95% 区间 0.0–25.9%） | 越高越好 | [`evidence-check/eval/v4/results/script-only.md`](https://github.com/Jason-d-e/evidence-check/blob/main/eval/v4/results/script-only.md) |
| 正确说法通过（0.4.0） | 11/11（100.0%，95% 区间 74.1–100.0%） | 越高越好 | [`evidence-check/eval/v4/results/script-only.md`](https://github.com/Jason-d-e/evidence-check/blob/main/eval/v4/results/script-only.md) |
| 改错的数字被标出（0.4.0） | 13/13（100.0%，95% 区间 77.2–100.0%） | 越高越好 | [`evidence-check/eval/v4/results/script-only.md`](https://github.com/Jason-d-e/evidence-check/blob/main/eval/v4/results/script-only.md) |

## 评分器校准

- 没有用评分器：所有分数按写题时定好的答案用脚本算。

## 局限和失败案例

- 题目和 Skill 出自同一作者，资料是虚构的；一个模型、两遍、一天。
  - 建议：装进别的 Agent 时，用那个场景自己的资料和错误再测一轮。
- 脚本单独用时抓不住意思上的矛盾：原文是真的、数字也对，但说法和原文相反，脚本会放行。
  - 建议：所以 Skill 要求 Agent 逐条重读通过的说法；要更稳就再加一次独立复核。
- 中文引文至少要 4 个字，少于 4 个字的完整短句会被挡下；翻译过的组名、离得远的序数还认不出。
  - 建议：这几类写进了下一版待改清单，改之前照样先写新题。

## 版本

- **1.0**（2026-11-15）第一张卡：Skill v0.2、脚本 0.4.0。
- **1.1**（2026-11-15）开头加了时间、团队、技术、链接和“问题 / 我做了什么 / 结果”，照作品集案例页的写法；评测部分不变。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。

第三方数据、模型和代码的来源与许可，见[项目仓库](https://github.com/Jason-d-e/evidence-check)里的说明。
