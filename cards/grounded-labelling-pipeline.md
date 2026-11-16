# 有据标注流水线：评测卡

> 卡片版本 1.0 · 数据截至 2026-11-16 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-15 – 2026-11-16 | Liang Liyuan | Python、Pandas、BM25、evidence-check、Lark 多维表格、批量接口 | [代码和报告](https://github.com/Jason-d-e/grounded-labelling-pipeline) |

**问题**：能核对的回答，怎么变成团队每天用的审核工作流：拿不准的交给人复核，提示词能灰度、能回滚。

**我做了什么**：我把有据审核做成一条四步审核工作流：模型判断，evidence-check 核对引文，核对没过或模型拿不准的进人工复核队列，复核结果回流成回归题；另加政策库检索评测、提示词版本、灰度和回滚规则、每周报告和上线检查清单，复核队列可以同步到 Lark 多维表格。

**结果**：

- 判错又自动生效：v1 17/332 → v2 9/332；送人工复核 6/332 → 72/332
- 按事先写好的回滚规则，灰度放到 10% 就回滚了；规则写错两处，已复盘

## 概况

一条围绕有据审核搭的审核和标注工作流。每条广告先由模型判断并引原文，再用 evidence-check 核对引文，核对没过、读不出或模型拿不准的进人工复核队列，复核结果和模型不同的变成新的回归题。提示词按版本管理，新版本先做回归测试，再按事先写好的规则灰度放量，触发就回滚。流量是有据审核评测题的回放，不是真实用户；回放里的复核结论就是题目定好的答案。

- **在作品集里的位置**：运营层
- **和核心部件的关系**：每段引文都过 evidence-check 的核对脚本；只读地引用有据审核的代码，回放它存下的答案。
- **用到的模型**：claude-haiku-5-5，批量接口；检索用政策库自带的 BM25。

## 用途

- 平台审核团队的日常流程：模型先判、核对引文，拿不准和核对没过的进复核队列，复核结果变成新的回归题。
- 提示词上线流程：回归测试、按规则灰度、触发就回滚，每周看漏网错判、复核率和费用。

## 不适用的地方

- 不是线上流量：请求是有据审核评测题的回放，复核结论是题目定好的答案。
- 不替代审核员：拿不准、核对没过、读不出的广告都交给人。

## 评测数据

### 回归测试：分流提示词 v1 对 v2（332 个回放请求）

有据审核的留出集、难题集和真实广告存下的答案，按请求回放；每个请求的答案在写题时定好。v2 的采用标准跑前预注册。

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

### 政策库检索：正确条款进前三（124 条违规标注）

有据审核的 32 条政策条款，用它自带的 BM25 检索；每条违规标注一次查询，哪些条款算对写在标注里。比较用广告原文搜和用模型的答案搜。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-15 |
| 题目和答案 | 124 条违规标注 |
| 跑了几次 | 确定性检索，1 遍 |
| 模型和发送方式 | 不调用模型，用 v1 第一遍存下的答案 |

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

### 政策库检索：正确条款进前三（124 条违规标注）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 用广告原文搜，正确条款进前三 | 66/124（53.2%，95% 区间 44.5–61.8%） | 越高越好 | [`grounded-labelling-pipeline/data/retrieval.csv`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/retrieval.csv) |
| 用模型的答案搜，正确条款进前三 | 110/124（88.7%，95% 区间 81.9–93.2%） | 越高越好 | [`grounded-labelling-pipeline/data/retrieval.csv`](https://github.com/Jason-d-e/grounded-labelling-pipeline/blob/main/data/retrieval.csv) |

## 评分器校准

- 没有用评分器：判对按题目定好的答案算；回放里的复核结论就是题目的答案。

## 局限和失败案例

- 流量是评测题的回放，不是真实用户；复核结论用的是题目定好的答案，没有真的审核员。
  - 建议：上线后按版本统计真实请求的漏网错判和复核量，抽检结果回流成回归题。
- v2 少放过判错，但送人工从 6/332 涨到 72/332，很多是清楚的广告也说“拿不准”。
  - 建议：下一版试着减少清楚广告上的“拿不准”，同样先过回归测试再灰度。
- 回滚规则写错两处，改好的规则是看过结果之后写的，在同一批请求上回放放到全量不算证据。
  - 建议：回滚条件要和改动目的、采用标准对齐；样本小的一步只查硬条件；用改好的规则在新写的题上重新灰度。

## 版本

- **1.0**（2026-11-16）第一张卡，照公开仓库 grounded-labelling-pipeline 的结果文件写。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。
