# 模型裁判校准：评测卡

> 卡片版本 1.2 · 数据截至 2026-11-18 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-18 | Liang Liyuan | Python、批量接口、Cohen's kappa 和自助区间、质检 Agent（两个工具） | [代码和报告](https://github.com/llia0031-dotcom/judge-calibration) |

**问题**：用模型当裁判打分省事，可它能信到什么程度；哪些检查可以交给它，哪些该用脚本，哪些必须留给人。

**我做了什么**：我把一个模型裁判分别和三种标准比：出题时定好的答案、监管和法院的结论、公开数据集自带的人工评分；再定出哪些检查交给脚本、哪些交给裁判、哪些留给人，并做了一个带验收标准的质检 Agent。方案、冻结的文件和预测跑前写好。

**结果**：

- 和出题时定好的答案一致 702/711，植入的错误抓到 385/390
- 监管和法院结论：从广告本身能看出的 33/35，要靠外部证据的只有 6/11
- 先用规则、再交裁判、拿不准的送人：漏掉的错误 2/390，只用裁判时 7/390；送人工 49/711

## 概况

检验一个模型裁判能信到什么程度。三种标准分开比：出题时定好答案的判断题（审核意见、简历判断、修改建议）、监管机构和法院对真实广告的结论、公开数据集自带的人工评分（Judge's Verdict、SummEval、WMT MQM 中译英）。再按结果把检查分成三类：能用脚本查的、能交给裁判的、必须留给人的，比较“只用裁判”和“先规则、再裁判、拿不准的送人工”两种接法；最后做了一个用两个工具的质检 Agent，并按模拟批次给它定验收标准。没有为这个项目另做人工评分。

- **在作品集里的位置**：运营层
- **和核心部件的关系**：判断题来自有据审核、简历初筛和卖点体检的存档答案；能用规则查的部分照 evidence-check 的做法交给脚本。
- **用到的模型**：裁判用 claude-haiku-5-5（effort medium，批量接口）；在 120 道题上用 claude-sonnet-5-5 做第二裁判对照。

## 用途

- 评测团队决定哪些检查交给模型裁判：先在定好答案的题上校准，再看在外部标准上能信到哪里。
- 上线质检：规则先查、裁判再判、拿不准的送人工，按批次验收。

## 不适用的地方

- 不评裁判以外的模型，也不证明某个裁判在别的任务上可靠；换任务要重新校准。
- 公开数据集的人工评分有自己的口径和噪声，裁判和它们一致不等于裁判对。

## 评测数据

### 裁判提示词 v1 到 v4（开发集）

开发集上比较四版裁判提示词，按三类判断题的平均平衡准确率选一版，选定后冻结，再在测试集上跑。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 开发集 |
| 跑了几次 | 每版每题 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，effort medium，批量接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md` |

### 定好答案的判断题（测试集，三次判断取多数）

审核意见、简历判断、修改建议三类判断题，取自有据审核、简历初筛和卖点体检的存档答案，并植入引文、条款、格式、结论等类型的错误；答案在出题时定好。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 711 道 |
| 跑了几次 | 每题判三次，取多数 |
| 模型和发送方式 | claude-haiku-5-5，effort medium，批量接口；提示词 v2 |
| 跑前冻结 | `eval/PREREGISTRATION.md` |

### 监管和法院的结论（46 条真实广告）

英国广告标准局的 30 份裁决和中文的 16 个监管或法院案例；按结论能不能从广告本身看出来分成两组。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 46 条广告 |
| 跑了几次 | 每条判三次，取多数 |
| 模型和发送方式 | claude-haiku-5-5，effort medium，批量接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md` |

### 公开数据集自带的人工评分

Judge's Verdict（200 道，三位标注员）、SummEval（30 篇新闻各 4 条摘要，四个维度各 120 条，三位专家）、WMT MQM 中译英（240 句）。人工评分都是数据集自带的。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | Judge's Verdict 200 道；SummEval 每个维度 120 条摘要；WMT MQM 240 句 |
| 跑了几次 | 每题判三次 |
| 模型和发送方式 | claude-haiku-5-5，effort medium，批量接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md` |

### 规则、裁判和复核队列怎么分工（711 道）

同一批定好答案的判断题，比较只用裁判（A）和先用规则、再判一次、拿不准的送人工（B）。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 711 道，其中 390 道含错误 |
| 跑了几次 | 每种接法 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，effort medium，批量接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md` |

### 加废话、加保证语会不会骗过裁判（368 道）

同一批题，答案里加上不相干的长段落，或加上“保证没错”这类话，看裁判的判断变不变；同时量重复判一次本来就会变多少。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 368 道 |
| 跑了几次 | 每种改法 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，effort medium，批量接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md` |

### 质检 Agent 和验收标准

239 条审核记录（119 条有错、120 条正确），比较只用脚本和用两个工具的质检 Agent；验收标准在每批 100 条、不同错误率的模拟批次上检验。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 239 条记录；模拟批次 |
| 跑了几次 | 每条 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，effort medium，批量接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md` |

## 指标和结果

每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。

### 裁判提示词 v1 到 v4（开发集）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 平均平衡准确率（v1） | 0.860 | 越高越好 | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| 平均平衡准确率（v2） | 0.976 | 越高越好 | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |

v2 最好，采用；v3 和 v2 打平但更贵，v4 更严、把对的也判错了一些，都不采用。

### 定好答案的判断题（测试集，三次判断取多数）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 和定好的答案一致 | 702/711（98.7%，95% 区间 97.6–99.3%） | 越高越好 | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| 植入的错误抓到 | 385/390（98.7%，95% 区间 97.0–99.5%） | 越高越好 | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| Cohen's kappa | 0.974 | 越高越好 | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |

答案清楚的判断题上，裁判几乎全对，植入的错误大多抓到。剩下的 9 处不一致都是裁判判错；原来 12 处里，3 处是题目当初少给了商品页，2 处是出题时漏标了必须写的提示语，两处都已更正重跑（更正 1、2）。

### 监管和法院的结论（46 条真实广告）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 和监管、法院结论一致 | 39/46（84.8%，95% 区间 71.8–92.4%） | 越高越好 | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| 从广告本身能看出的 | 33/35（94.3%，95% 区间 81.4–98.4%） | 越高越好 | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| 要靠外部证据的 | 6/11（54.5%，95% 区间 28.0–78.7%） | 越高越好 | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |

能从广告本身看出结论的，裁判大多判对；要靠外部证据（检测报告、资质、实际效果）才能定的，只对一半左右。

### 公开数据集自带的人工评分

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| Judge's Verdict：裁判和每位标注员完全一致（平均） | 67.3% | 越高越好 | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| Judge's Verdict：标注员彼此完全一致（平均） | 64.3% | 只作说明 | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| SummEval 流畅度：和专家的 Spearman 相关 | 0.408 | 越高越好 | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| SummEval 事实一致：和专家的 Spearman 相关 | 0.682 | 越高越好 | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| WMT MQM 中译英：加权 kappa | 0.290 | 越高越好 | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |

答对答错这类题，裁判和标注员的一致程度与标注员彼此之间差不多；主观质量（流畅度、连贯性）和翻译错误的严重程度，裁判和人差得多。

### 规则、裁判和复核队列怎么分工（711 道）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 只用裁判：漏掉的错误 | 7/390（1.8%，95% 区间 0.9–3.7%） | 越低越好 | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| 规则、裁判、复核队列：漏掉的错误 | 2/390（0.5%，95% 区间 0.1–1.9%） | 越低越好 | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| 规则、裁判、复核队列：送人工 | 49/711（6.9%，95% 区间 5.3–9.0%） | 越低越好 | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| 只用裁判：每 1,000 道的费用 | 0.304 美元 | 越低越好 | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| 规则、裁判、复核队列：每 1,000 道的费用 | 0.244 美元 | 越低越好 | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| 第一次判断说“确定”的错误率 | 3/662（0.5%，95% 区间 0.2–1.3%） | 越低越好 | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| 第一次判断说“拿不准”的错误率 | 10/49（20.4%，95% 区间 11.5–33.6%） | 只作说明 | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |

先用规则、再交裁判、拿不准的送人工，漏掉的错误更少，费用也更低；裁判自己说“拿不准”的那部分错得多，正好拿来决定送人工。

### 加废话、加保证语会不会骗过裁判（368 道）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 加废话后判断变了 | 0/368（0.0%，95% 区间 0.0–1.0%） | 越低越好 | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| 加保证语后判断变了 | 2/368（0.5%，95% 区间 0.1–2.0%） | 越低越好 | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |

加废话一道没变；加保证语变了 2/368，都是边界上的好建议，没有让错的被放过；事先预测的“会被骗”没成立。

### 质检 Agent 和验收标准

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 质检 Agent：错误记录查出 | 119/119（100.0%，95% 区间 96.9–100.0%） | 越高越好 | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| 质检 Agent：正确记录被误报 | 7/120（5.8%，95% 区间 2.9–11.6%） | 越低越好 | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| 错误率百分之二的批次被放行（目标是至少九成） | 86.6% | 越高越好 | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| 错误率百分之十的批次被放行（目标是不超过一成） | 9.4% | 越低越好 | [`judge-calibration/eval/results/RESULTS.md`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/RESULTS.md) |
| 事先写好的预测成立 | 8/12（66.7%，95% 区间 39.1–86.2%） | 只作说明 | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |
| 整个项目的接口费用（批量价） | 2.63 美元 | 越低越好 | [`judge-calibration/eval/results/summary.json`](https://github.com/llia0031-dotcom/judge-calibration/blob/main/eval/results/summary.json) |

质检 Agent 查出全部错误记录，误报少；但查漏标不行：答案补标之前，有六条“正确”记录其实缺了必须写的提示语，它只标出一条，它的说明里也没要求查是否标全。验收标准只达到一个目标：错误率百分之二的批次放行得不够（目标至少九成），错误率百分之十的批次达标（目标至多一成）；多一条误报就能让结果翻过来，离两个目标都很近。

## 评分器校准

- 被检验的就是裁判本身：和每种标准的一致率都用脚本算；“人工评分”只指公开数据集自带的评分，没有为这个项目另做人工评分。

## 局限和失败案例

- 判断题来自同一组项目的存档答案，错误是植入的；“论证成错误结论”这类错误样本由 `eval/gen_flips.py` 生成，生成时用的是同一个模型，裁判认得自己写法的偏差没有排除。
  - 建议：上线前用真实业务里已经有结论的记录再校准一次，错误样本换不同来源。
- 监管和法院的结论只有 46 条，要靠外部证据的只有 11 条；区间很宽。
  - 建议：这类结论直接留给人，或者先补齐外部证据再交裁判。
- 验收标准在错误率百分之二的批次上只放行了 86.6%，没达到事先定的至少九成；百分之十的批次放行 9.4%，达标。质检 Agent 的误报让标记率变模糊，事后看，单靠调标记率门槛两个目标同时达不到。
  - 建议：只把复核确认过的标记算进放行门槛（还没测过），再在模拟批次上重测。

## 版本

- **1.0**（2026-11-18）第一张卡，照公开仓库 judge-calibration 的结果文件写。
- **1.1**（2026-11-18）跟随项目的更正 1：修改建议题当初少给了商品页，补上后整组重跑；卡上相关的数字按更正后的结果文件重新算出，不一致的说法照实改。提示词版本的选择不变。
- **1.2**（2026-11-18）跟随项目的更正 2：出题时有几条答案漏标了必须写的提示语，补标后重算；质检 Agent 的误报、验收标准两档批次的放行比例和总费用按新的结果文件重新算出，不一致的说法和验收标准的结论照实改。和定好的答案一致的比例不变。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。

第三方数据、模型和代码的来源与许可，见[项目仓库](https://github.com/llia0031-dotcom/judge-calibration)里的说明。
