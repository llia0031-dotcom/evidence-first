# 有据标注流水线：评测卡

> 卡片版本 1.3 · 数据截至 2026-11-17 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-15 – 2026-11-17 | Liang Liyuan | Python、Pandas、DuckDB（SQL）、BM25 和本机向量检索（Qwen3-Embedding-0.6B）、evidence-check、Lark 多维表格（工作流和 AI Agent 步骤）、批量接口 | [代码和报告](https://github.com/Jason-d-e/grounded-labelling-pipeline) |

**问题**：能核对的回答，怎么变成团队每天用的审核工作流：拿不准的交给人复核，提示词能灰度、能回滚。

**我做了什么**：我把有据审核做成一条四步审核工作流：模型判断，evidence-check 核对引文，核对没过或模型拿不准的进人工复核队列，复核结果回流成回归题；另加政策库检索评测、只按政策库回答的知识库问答、提示词版本、灰度和回滚规则、用 SQL 取数的每周报告和上线检查清单，并在 Lark 多维表格里搭了判断和复核两条工作流。

**结果**：

- 判错又自动生效：v1 17/332 → v2 9/332；送人工复核 6/332 → 72/332
- 第一轮按事先写好的规则，灰度放到 10% 就回滚了；规则写错两处，已复盘
- 第二轮用改好的规则，在新写的广告上放到 100%，没有回滚，回放里 v2 转为正式版本

## 概况

一条围绕有据审核搭的审核和标注工作流。每条广告先由模型判断并引原文，再用 evidence-check 核对引文，核对没过、读不出或模型拿不准的进人工复核队列，复核结果和模型不同的变成新的回归题。提示词按版本管理，新版本先做回归测试，再按事先写好的规则灰度放量，触发就回滚。另有一个只按政策库回答的知识库问答，库里没有管这件事的条款就说没有。流量是有据审核评测题的回放，不是真实用户；回放里的复核结论就是题目定好的答案。

- **在作品集里的位置**：运营层
- **和核心部件的关系**：每段引文都过 evidence-check 的核对脚本；只读地引用有据审核的代码，回放它存下的答案。
- **用到的模型**：分流和知识库问答用 claude-haiku-5-5（评测走批量接口）；Lark 工作流里的 AI Agent 步骤用平台模型 Seed 1.8，聊天机器人用 claude-haiku-5-5；中文条款检索用政策库自带的 BM25，英文用本机向量模型 Qwen3-Embedding-0.6B。

## 用途

- 平台审核团队的日常流程：模型先判、核对引文，拿不准和核对没过的进复核队列，复核结果变成新的回归题。
- 提示词上线流程：回归测试、按规则灰度、触发就回滚，每周看漏网错判、复核率和费用。

## 不适用的地方

- 评测题回放，不是真实用户。人工复核的结论用题目定好的答案代替。
- Lark 里的平台模型和 claude-haiku-5-5 不在同一套题上比谁准；这里只说明工作流能在 Lark 里跑通。
- 不替代审核员：拿不准、核对没过、读不出的广告都交给人。
- Lark 里的“AI Agent”步骤是固定流程里的一次模型调用，没有工具和记忆。
- 机器人问答和使用记录只有测试，没有真实使用量。

## 评测数据

### 回归测试：分流提示词 v1 对 v2（332 个回放请求）

有据审核的留出集、难题集和真实广告存下的答案，按请求回放；自己写的题，答案在写题时定好；真实广告的答案来自监管机构和法院的裁决。v2 的采用标准跑前预注册。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-15 |
| 题目和答案 | 332 个请求，每个版本 1 遍 |
| 跑了几次 | 每个版本 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，批量接口（半价） |
| 跑前冻结 | `docs/PREREGISTRATION.md` |

### 灰度回放：按事先写好的回滚规则（回放，不是真实用户）

同一批请求按周回放，按请求编号的哈希分给 v1（线上）和 v2（灰度）；回滚规则跑前写好：灰度组漏网比例更高、复核率高出 15 个百分点以上、判对率低 5 个百分点以上、费用比线上组高出百分之十五以上，任一条触发就回滚。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-15 |
| 题目和答案 | 四周，共 332 个请求 |
| 跑了几次 | 回放 1 遍 |
| 模型和发送方式 | 不调用模型，回放存下的答案 |
| 跑前冻结 | `docs/PREREGISTRATION.md` 和 `docs/CANARY-POSTMORTEM.md` |

### 第二轮灰度：改好的规则，新写的广告

新写 120 条文字广告（中英各 60），每条两遍，共 240 个请求；改好的回滚规则和预测跑前预注册。灰度分三步放到全量，灰度组从开始累计和线上组比。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-16 |
| 题目和答案 | 240 个请求 |
| 跑了几次 | 每条广告两遍，每个版本 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，批量接口（半价） |
| 跑前冻结 | `docs/PREREGISTRATION-ROUND2.md` |

### Lark 里的工作流：平台 AI Agent 步骤（25 条中文广告）

在 Lark 多维表格里加广告，平台自带的 AI Agent 步骤判断并写回表格，引文核对由脚本补；拿不准、核对没过的进复核队列。25 条中文文字广告，答案写题时定好；评测计划先写再跑。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-16 |
| 题目和答案 | 25 条广告，每条一遍 |
| 跑了几次 | 1 遍 |
| 模型和发送方式 | Lark 多维表格 AI Agent 步骤（Seed 1.8） |
| 跑前冻结 | `docs/LARK-AGENT-PLAN.md` |

### 政策库检索：正确条款进前三（124 条违规标注）

有据审核的 32 条政策条款，用它自带的 BM25 检索；每条违规标注一次查询，哪些条款算对写在标注里。比较用广告原文搜和用模型的答案搜。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-15 |
| 题目和答案 | 124 条违规标注 |
| 跑了几次 | 确定性检索，1 遍 |
| 模型和发送方式 | 不调用模型，用 v1 第一遍存下的答案 |

### 提示词第 3 版：新写的广告上不采用

另外新写 120 条文字广告，每条两遍，共 240 个请求；其中一部分写题时就定为“要人来定”，其余答案清楚。采用标准和预测跑前预注册；同时在第一轮的 332 个请求上做回归。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-17 |
| 题目和答案 | 240 个请求（另有回归 332 个） |
| 跑了几次 | 每条广告两遍，每个版本 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，批量接口（半价） |
| 跑前冻结 | `docs/PREREGISTRATION-ROUND3.md` |

### 提示词第 4 版：又一批新写的广告上不采用

又一批新写 120 条文字广告，每条两遍，共 240 个请求；其中一部分写题时就定为“要人来定”。采用标准和第三轮一字不改，预测跑前冻结；同时在第一轮的 332 个请求上做回归。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-17 |
| 题目和答案 | 240 个请求（另有回归 332 个） |
| 跑了几次 | 每条广告两遍，每个版本 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，批量接口（半价） |
| 跑前冻结 | `docs/PREREGISTRATION-ROUND4.md` |

### 政策知识库问答：只按检索到的条款回答（80 道题）

80 道题，中英各一半，其中一部分库里没有答案；答案写题时定好；每道题两遍，共 160 个请求。计划和预测跑前写好。答对要结论对、引了对的条款、引文核对通过；库里没有的题要说“没有”且不引条款。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-17 |
| 题目和答案 | 160 个请求 |
| 跑了几次 | 每道题 2 遍 |
| 模型和发送方式 | claude-haiku-5-5，批量接口；中文检索 BM25，英文检索 Qwen3-Embedding-0.6B，取前 5 条 |
| 跑前冻结 | `docs/KBQA-PLAN.md` |

### 英文条款检索换成本机向量模型（选方法时没用过的标注）

先在第一轮的标注上比较几种检索方式选定，再在选的时候没用过的第二轮、第三轮标注上验；用模型的答案去搜，只算英文。中文还用 BM25。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-17 |
| 题目和答案 | 第二轮 40 条、第三轮 23 条英文违规标注 |
| 跑了几次 | 确定性检索，1 遍 |
| 模型和发送方式 | Qwen3-Embedding-0.6B（量化版，fastembed），本机运行，不调用接口 |

### Lark 两条工作流：判断和复核（60 条中文广告，两遍）

第一条工作流判断、逐段核对引文、分流并写明原因；第二条把复核结论写回广告，分歧记进回归题。用第二轮的 60 条中文文字广告跑两遍：第一遍照跑之前写好的计划，第二遍是看过第一遍、改了引文核对之后再跑的，不算预注册。脚本核对和平台核对并排比。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-17 |
| 题目和答案 | 60 条广告 |
| 跑了几次 | 2 遍（第二遍改过才跑） |
| 模型和发送方式 | Lark 多维表格工作流；AI Agent 步骤用平台模型 Seed 1.8，平台免费额度 |
| 跑前冻结 | `docs/LARK-AGENT-PLAN.md` 第 8 节（第一遍） |

## 指标和结果

每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。

### 回归测试：分流提示词 v1 对 v2（332 个回放请求）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 判错又自动生效（v1） | 17/332（5.1%，95% 区间 3.2–8.0%） | 越低越好 | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions.json) |
| 判错又自动生效（v2） | 9/332（2.7%，95% 区间 1.4–5.1%） | 越低越好 | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions.json) |
| 送人工复核（v1） | 6/332（1.8%，95% 区间 0.8–3.9%） | 只作说明 | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions.json) |
| 送人工复核（v2） | 72/332（21.7%，95% 区间 17.6–26.4%） | 只作说明 | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions.json) |
| 判对（v1） | 315/332（94.9%，95% 区间 92.0–96.8%） | 越高越好 | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions.json) |
| 判对（v2） | 312/332（94.0%，95% 区间 90.9–96.1%） | 越高越好 | [`grounded-labelling-pipeline/data/versions.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions.json) |

v2 少放过判错的广告，代价是送人工多得多；四条采用标准都满足。

### 灰度回放：按事先写好的回滚规则（回放，不是真实用户）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 触发回滚时的灰度比例 | 10% | 只作说明 | [`grounded-labelling-pipeline/data/canary.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/canary.json) |
| 那一周灰度组判错又生效 | 1/10（10.0%，95% 区间 1.8–40.4%） | 越低越好 | [`grounded-labelling-pipeline/data/canary.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/canary.json) |
| 那一周线上组判错又生效 | 6/80（7.5%，95% 区间 3.5–15.4%） | 越低越好 | [`grounded-labelling-pipeline/data/canary.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/canary.json) |

第一步就触发了三条规则，回滚，线上留在 v1。复盘发现两条规则写错：复核率那一条和 v2 的目的矛盾，比例在灰度组只有 10 个请求时就比了。改好的规则是看过结果之后写的，在同一批请求上再回放能放到全量，但这证明不了什么，要在新流量上重新灰度。

### 第二轮灰度：改好的规则，新写的广告

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 没有回滚、最后放到的灰度比例 | 100% | 只作说明 | [`grounded-labelling-pipeline/data/canary-round2.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/canary-round2.json) |
| 判对（v1） | 239/240（99.6%，95% 区间 97.7–99.9%） | 越高越好 | [`grounded-labelling-pipeline/data/versions-round2.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-round2.json) |
| 判对（v2） | 240/240（100.0%，95% 区间 98.4–100.0%） | 越高越好 | [`grounded-labelling-pipeline/data/versions-round2.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-round2.json) |
| 送人工复核（v2） | 36/240（15.0%，95% 区间 11.0–20.1%） | 只作说明 | [`grounded-labelling-pipeline/data/versions-round2.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-round2.json) |
| 放到全量时，灰度组累计判错又生效 | 0/101（0.0%，95% 区间 0.0–3.7%） | 越低越好 | [`grounded-labelling-pipeline/data/canary-round2.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/canary-round2.json) |
| 放到全量时，线上组累计判错又生效 | 1/150（0.7%，95% 区间 0.1–3.7%） | 越低越好 | [`grounded-labelling-pipeline/data/canary-round2.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/canary-round2.json) |
| v2 每个请求的费用，是 v1 的（预测是不超过 1.05 倍，这一条没成立） | 1.0503 倍 | 越低越好 | [`grounded-labelling-pipeline/data/versions-round2.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-round2.json) |

三步都没触发回滚，v2 转为正式版本。两版在这批广告上都接近全对，所以这一轮只说明放量流程走通了；v2 少漏错判的证据仍来自第一轮。

### Lark 里的工作流：平台 AI Agent 步骤（25 条中文广告）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 写回表格 | 25/25（100.0%，95% 区间 86.7–100.0%） | 越高越好 | [`grounded-labelling-pipeline/data/lark-agent-eval1.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/lark-agent-eval1.json) |
| 判对 | 25/25（100.0%，95% 区间 86.7–100.0%） | 越高越好 | [`grounded-labelling-pipeline/data/lark-agent-eval1.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/lark-agent-eval1.json) |
| 引文核对没过、送了人工 | 2/25（8.0%，95% 区间 2.2–25.0%） | 只作说明 | [`grounded-labelling-pipeline/data/lark-agent-eval1.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/lark-agent-eval1.json) |
| 平台模型说“拿不准” | 0/25（0.0%，95% 区间 0.0–13.3%） | 只作说明 | [`grounded-labelling-pipeline/data/lark-agent-eval1.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/lark-agent-eval1.json) |
| 参照：分流模型存档答案里说“拿不准” | 13/50（26.0%，95% 区间 15.9–39.6%） | 只作说明 | [`grounded-labelling-pipeline/data/lark-agent-eval1.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/lark-agent-eval1.json) |

工作流在 Lark 里跑通：每条都写回、都判对；两条把条款里不相邻的几句拼成一句当引文，被脚本拦下送了人工。平台模型一次也没说拿不准，而分流用的模型在存档答案里常说，所以换模型后复核率要重新量。

### 政策库检索：正确条款进前三（124 条违规标注）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 用广告原文搜，正确条款进前三 | 66/124（53.2%，95% 区间 44.5–61.8%） | 越高越好 | [`grounded-labelling-pipeline/data/retrieval.csv`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/retrieval.csv) |
| 用模型的答案搜，正确条款进前三 | 110/124（88.7%，95% 区间 81.9–93.2%） | 越高越好 | [`grounded-labelling-pipeline/data/retrieval.csv`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/retrieval.csv) |

### 提示词第 3 版：新写的广告上不采用

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 答案清楚的广告送了人工（v2） | 44/176（25.0%，95% 区间 19.2–31.9%） | 越低越好 | [`grounded-labelling-pipeline/data/versions-v3-round3.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-v3-round3.json) |
| 答案清楚的广告送了人工（v3） | 4/176（2.3%，95% 区间 0.9–5.7%） | 越低越好 | [`grounded-labelling-pipeline/data/versions-v3-round3.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-v3-round3.json) |
| 要人来定的广告送了人工（v2） | 44/64（68.8%，95% 区间 56.6–78.8%） | 越高越好 | [`grounded-labelling-pipeline/data/versions-v3-round3.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-v3-round3.json) |
| 要人来定的广告送了人工（v3） | 19/64（29.7%，95% 区间 19.9–41.8%） | 越高越好 | [`grounded-labelling-pipeline/data/versions-v3-round3.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-v3-round3.json) |
| 回归（第一轮）：判错又自动生效（v2） | 9/332（2.7%，95% 区间 1.4–5.1%） | 越低越好 | [`grounded-labelling-pipeline/data/versions-v3.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-v3.json) |
| 回归（第一轮）：判错又自动生效（v3） | 9/332（2.7%，95% 区间 1.4–5.1%） | 越低越好 | [`grounded-labelling-pipeline/data/versions-v3.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-v3.json) |

答案清楚的广告少了多余的复核，但写题时定为“要人来定”的广告送人工也少了，降幅超过事先写好的十个百分点上限，不采用，production 留在 v2。假如照样放量，灰度的回滚规则一条也不会触发：拦下它的是题目里那批要人来定的广告和事先写好的采用标准。

### 提示词第 4 版：又一批新写的广告上不采用

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 答案清楚的广告送了人工（v2） | 43/176（24.4%，95% 区间 18.7–31.3%） | 越低越好 | [`grounded-labelling-pipeline/data/versions-v4-round4.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-v4-round4.json) |
| 答案清楚的广告送了人工（v4） | 11/176（6.2%，95% 区间 3.5–10.8%） | 越低越好 | [`grounded-labelling-pipeline/data/versions-v4-round4.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-v4-round4.json) |
| 要人来定的广告送了人工（v2） | 42/64（65.6%，95% 区间 53.4–76.1%） | 越高越好 | [`grounded-labelling-pipeline/data/versions-v4-round4.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-v4-round4.json) |
| 要人来定的广告送了人工（v4） | 47/64（73.4%，95% 区间 61.5–82.7%） | 越高越好 | [`grounded-labelling-pipeline/data/versions-v4-round4.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-v4-round4.json) |
| 答案清楚的广告判错又自动生效（v2） | 0/176（0.0%，95% 区间 0.0–2.1%） | 越低越好 | [`grounded-labelling-pipeline/data/versions-v4-round4.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-v4-round4.json) |
| 答案清楚的广告判错又自动生效（v4）（同一条陷阱题的两遍） | 2/176（1.1%，95% 区间 0.3–4.0%） | 越低越好 | [`grounded-labelling-pipeline/data/versions-v4-round4.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-v4-round4.json) |
| 回归（第一轮）：判错又自动生效（v2） | 9/332（2.7%，95% 区间 1.4–5.1%） | 越低越好 | [`grounded-labelling-pipeline/data/versions-v4.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-v4.json) |
| 回归（第一轮）：判错又自动生效（v4） | 13/332（3.9%，95% 区间 2.3–6.6%） | 越低越好 | [`grounded-labelling-pipeline/data/versions-v4.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/versions-v4.json) |

两头都比 v2 好：答案清楚的广告少了多余的复核，要人来定的广告送人工也多了。但它判错时更常说“确定”：新题上一条陷阱题两遍都判错又自动生效（v2 判得一样，但说了拿不准、送了人工），第一轮回归里漏网的错判也变多，按事先写好的标准不采用，production 留在 v2。那条陷阱题的答案有争议，按预注册没有改。

### 政策知识库问答：只按检索到的条款回答（80 道题）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 答对 | 134/160（83.8%，95% 区间 77.3–88.7%） | 越高越好 | [`grounded-labelling-pipeline/data/kbqa-eval.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/kbqa-eval.json) |
| 库里没有的题说了“没有” | 44/48（91.7%，95% 区间 80.4–96.7%） | 越高越好 | [`grounded-labelling-pipeline/data/kbqa-eval.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/kbqa-eval.json) |
| 没核对上的引文 | 1/160（0.6%，95% 区间 0.1–3.5%） | 越低越好 | [`grounded-labelling-pipeline/data/kbqa-eval.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/kbqa-eval.json) |
| 中文问题：算对的条款进前 5（BM25）（预测是百分之九十以上，这一条没成立；按题数算，每道题两遍的检索结果相同） | 23/28（82.1%，95% 区间 64.4–92.1%） | 越高越好 | [`grounded-labelling-pipeline/data/retrieval-methods.csv`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/retrieval-methods.csv) |

多数题答对，库里没有的题大多说了“没有”，引文几乎全部核对通过。事先写好的预测里只有中文检索那一条没成立；库里有答案却说“没有”的，都是检索没找到条款，不是模型编造。

### 英文条款检索换成本机向量模型（选方法时没用过的标注）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 第二轮英文：正确条款进前三（BM25） | 38/40（95.0%，95% 区间 83.5–98.6%） | 越高越好 | [`grounded-labelling-pipeline/data/retrieval-methods.csv`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/retrieval-methods.csv) |
| 第二轮英文：正确条款进前三（向量） | 39/40（97.5%，95% 区间 87.1–99.6%） | 越高越好 | [`grounded-labelling-pipeline/data/retrieval-methods.csv`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/retrieval-methods.csv) |
| 第三轮英文：正确条款进前三（BM25） | 21/23（91.3%，95% 区间 73.2–97.6%） | 越高越好 | [`grounded-labelling-pipeline/data/retrieval-methods.csv`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/retrieval-methods.csv) |
| 第三轮英文：正确条款进前三（向量） | 23/23（100.0%，95% 区间 85.7–100.0%） | 越高越好 | [`grounded-labelling-pipeline/data/retrieval-methods.csv`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/retrieval-methods.csv) |

两批没用过的标注上，英文正确条款进前三都提高了；第一轮是选方法用的，数字偏乐观，不拿来报告。

### Lark 两条工作流：判断和复核（60 条中文广告，两遍）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 第一遍：两种引文核对一致 | 49/60（81.7%，95% 区间 70.1–89.4%） | 越高越好 | [`grounded-labelling-pipeline/data/lark-agent-eval2.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/lark-agent-eval2.json) |
| 第一遍：判错又没送人工 | 0/60（0.0%，95% 区间 0.0–6.0%） | 越低越好 | [`grounded-labelling-pipeline/data/lark-agent-eval2.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/lark-agent-eval2.json) |
| 第二遍：两种引文核对一致 | 60/60（100.0%，95% 区间 94.0–100.0%） | 越高越好 | [`grounded-labelling-pipeline/data/lark-agent-eval3.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/lark-agent-eval3.json) |
| 第二遍：平台的去向和规则一致 | 60/60（100.0%，95% 区间 94.0–100.0%） | 越高越好 | [`grounded-labelling-pipeline/data/lark-agent-eval3.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/lark-agent-eval3.json) |
| 第二遍：复核结论写回广告 | 8/8（100.0%，95% 区间 67.6–100.0%） | 越高越好 | [`grounded-labelling-pipeline/data/lark-agent-eval3.json`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/lark-agent-eval3.json) |

第一遍平台的逐字查找被条款里的换行挡住，两种核对有不一致的，不一致的都是多送了人工，没有漏送；把换行处理好以后，第二遍两种核对和去向全部一致，复核结论都写回了。第二遍是看过第一遍才改的，只说明改法有效，不算事先的预测。

## 评分器校准

- 没有用评分器：判对按题目定好的答案算；回放里的复核结论就是题目的答案。

## 局限和失败案例

- 流量是评测题的回放，不是真实用户；复核结论用的是题目定好的答案，没有真的审核员。
  - 建议：上线后按版本统计真实请求的漏网错判和复核量，抽检结果回流成回归题。
- v2 少放过判错，但送人工从 6/332 涨到 72/332，很多是清楚的广告也说“拿不准”。
  - 建议：第 3 版放宽“拿不准”，要人来定的也少送了；第 4 版两头都好了，判错时却更常说“确定”。下一版要同时守住三头：清楚的少送、要人定的不少送、判错的不放过，同样先过回归和新题再灰度。
- 第二轮在新流量上放到全量，但两版在这批广告上都接近全对，没有再证明 v2 能少漏错判；v2 的好处仍来自第一轮。
  - 建议：再找 v1 会漏判的新广告（例如更长、更含糊的），在同样的规则下比一次。
- Lark 里的平台模型一次也没说拿不准（0/25），分流模型的存档答案里却有 13/50 说了；机器人问答只有测试，没有真实使用量。
  - 建议：换模型后先重新量复核率，再调“拿不准”的门槛；机器人先用一批问题测，再看真实的使用记录。
- 中文问题的检索偏弱：算对的条款进前 5 只有 23/28，库里有答案却说“没有”的都出在检索没找到。
  - 建议：中文检索也试本机向量或混合检索，先在选方法时没用过的问题上验。

## 版本

- **1.0**（2026-11-16）第一张卡，照公开仓库 grounded-labelling-pipeline 的结果文件写。
- **1.1**（2026-11-16）加第二轮灰度（新流量，v2 转为正式版本）、Lark 里的工作流评测和截图。
- **1.2**（2026-11-17）加提示词第 3 版（不采用）、知识库问答、英文检索换本机向量模型、Lark 两条工作流；Lark 截图换成新版。
- **1.3**（2026-11-17）加提示词第 4 版（第四轮新写的广告，不采用）；Lark 看板截图线上换了新图。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。

第三方数据、模型和代码的来源与许可，见[项目仓库](https://github.com/Jason-d-e/grounded-labelling-pipeline)里的说明。
