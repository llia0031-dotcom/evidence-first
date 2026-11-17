# 卖点体检：评测卡

> 卡片版本 1.2 · 数据截至 2026-11-15 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-12 – 2026-11-14 | Liang Liyuan | Node.js、DuckDB、Orama、evidence-check、批量接口 | [代码](https://github.com/llia0031-dotcom/sellpoint-check) · [设计案例](https://llia0031-dotcom.github.io/sellpoint-check/design/case/) · [可点击原型](https://llia0031-dotcom.github.io/sellpoint-check/design/prototype/product.html) |

**问题**：商品页的卖点有没有被买家评价证实：买家只看到被证实的卖点和原话，其余卖点私下交给商家，附修改建议。

**我做了什么**：我把卖点核对设计成平台和商家一起用的功能：买家只看被证实的卖点，其余私下交给商家；比较三种找证据的做法的准确率和费用；给商家的修改建议迭代了六版，每版先在新写的冻结题上测，再决定用不用。

**结果**：

- 答案已知的 60 条卖点：采用的做法 60/60，逐条判断 58/60，先检索 52/60
- 真实数据：调用次数是逐条判断的 2.8%，费用是 17%
- 修改建议第 5 版，真实数据两次独立评分：142/151、143/151

## 概况

把商品页的卖点拆开，在买家评价里找支持或反驳的原话，每段原话用 evidence-check 的脚本逐字核对，再给每条卖点贴上“证实、反驳、有争议、没提到”。买家页只展示被证实的卖点和原话；没被证实的进商家后台的“卖点体检”，附原话和修改建议，只有商家本人看得到。评测比较三种找证据的做法：先检索再判断（A）、逐条评价判断再汇总（B，照 PRAISE 论文的做法）、全部评价一次交给模型（C，采用）。

- **在作品集里的位置**：场景：判断类
- **和核心部件的关系**：直接调用 evidence-check 的核对脚本：引文没通过就丢掉，不算证据。
- **用到的模型**：claude-haiku-5-5（effort medium）；先检索的做法用本机的检索模型和 Orama 混合检索（来自 Cairn）。

## 用途

- 平台在商品页和门店页只展示被买家评价证实的卖点，配原话。
- 商家后台私下看到哪些卖点没被证实、买家原话是什么、怎么改写。

## 不适用的地方

- 不对外公布“被反驳”“有争议”的标签，不用来判违规、不触发处罚。
- 不判断买家看不到的卖点，例如成分含量、实验室检测结果。
- 评价太少的商品不判；第一版不碰推荐排序。
- 研究用的真实评价数据没有商用许可，评价原文不转载。

## 评测数据

### 构造测试集 v1（60 条卖点，答案已知）

12 个虚构商品、433 条评价，答案在写题时定好，其中有专门的陷阱评价（看着像证据、其实不是）。题目在真实数据跑完之后由同一作者写成；跑前冻结。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-12 |
| 题目和答案 | 60 条卖点 |
| 跑了几次 | 每种做法 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，普通接口 |
| 跑前冻结 | `testset/PREREGISTRATION.md`（题目指纹、预期） |

### 真实数据（30 个商品，没有标准答案）

公开研究数据集 Amazon Reviews 2023（美妆类）里的 30 个美妆商品、538 条评价、210 条卖点。没有标准答案，所以比较费用、调用次数，并对每条证据做第二次独立判断。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-12 |
| 题目和答案 | 30 个商品、210 条卖点 |
| 跑了几次 | 每种做法 1 遍；A 和 C 另各重跑 1 遍看一致率 |
| 模型和发送方式 | claude-haiku-5-5，普通接口 |

### 中文测试集（50 条卖点，网络用语和反话）

10 个虚构商品、312 条中文评价，含网络用语、反话和陷阱，答案写题时定好，跑前冻结。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-14 |
| 题目和答案 | 50 条卖点 |
| 跑了几次 | 每种做法 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，普通接口 |
| 跑前冻结 | `testset/zh/PREREGISTRATION.md` |

### 英文测试集 v2（50 条卖点，长评价、错别字、反话）

10 个虚构商品、490 条评价，比 v1 更难，答案写题时定好，跑前冻结。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-14 |
| 题目和答案 | 50 条卖点 |
| 跑了几次 | 每种做法 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，批量接口（半价） |
| 跑前冻结 | `testset/v2/PREREGISTRATION.md` |

### 检索改进 A2：A 没跑过的 180 条卖点

A2 换用 Orama 混合检索和句子窗口。在四套新写的测试集（混合、混合二、口语、口语二）上和 A、C 比较；计划和判断标准跑前写好。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-14 |
| 题目和答案 | 四套共 180 条卖点 |
| 跑了几次 | 每种做法 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，大部分走批量接口 |
| 跑前冻结 | `testset/ARM_A2_PLAN.md` |

### 修改建议（商家后台）：第 1 版和现在采用的第 5 版

答案已知的 40 条卖点和真实数据的 151 条没被证实的卖点。每条建议按评分表独立打两次分（能不能直接照着改）。第 2 到第 6 版各在为它新写的测试集上测过，逐版记录见 Prompt 资产库；这里只列第 1 版和第 5 版在同一批真实数据上的结果。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-14 |
| 题目和答案 | 测试集 40 条；真实数据 151 条 |
| 跑了几次 | 每版生成 1 遍，评分 2 遍 |
| 模型和发送方式 | claude-haiku-5-5；第 1 到 3 版普通接口，第 4 到 6 版批量接口 |
| 跑前冻结 | `testset/SUGGEST_PLAN.md` 和各测试集的 PREREGISTRATION |

## 指标和结果

每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。

### 构造测试集 v1（60 条卖点，答案已知）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 判对：全部评价一次给（C，采用） | 60/60（100.0%，95% 区间 94.0–100.0%） | 越高越好 | [`sellpoint-check/results/score-testset.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset.json) |
| 判对：逐条判断再汇总（B） | 58/60（96.7%，95% 区间 88.6–99.1%） | 越高越好 | [`sellpoint-check/results/score-testset.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset.json) |
| 判对：先检索再判断（A） | 52/60（86.7%，95% 区间 75.8–93.1%） | 越高越好 | [`sellpoint-check/results/score-testset.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset.json) |
| 陷阱评价被当成证据（C） | 0/11（0.0%，95% 区间 0.0–25.9%） | 越低越好 | [`sellpoint-check/results/score-testset.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset.json) |

### 真实数据（30 个商品，没有标准答案）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 调用次数：C 占 B 的比例 | 2.8% | 越低越好 | [`sellpoint-check/results/compare-run.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/compare-run.json) |
| 费用：C 占 B 的比例 | 17% | 越低越好 | [`sellpoint-check/results/compare-run.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/compare-run.json) |
| 第二次独立判断同意：C 的支持证据 | 184/208（88.5%，95% 区间 83.4–92.1%） | 越高越好 | [`sellpoint-check/results/audit-run.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/audit-run.json) |
| 第二次独立判断同意：C 的反驳证据 | 86/94（91.5%，95% 区间 84.1–95.6%） | 越高越好 | [`sellpoint-check/results/audit-run.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/audit-run.json) |
| 第二次独立判断同意：A 的支持证据 | 143/173（82.7%，95% 区间 76.3–87.6%） | 越高越好 | [`sellpoint-check/results/audit-run.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/audit-run.json) |
| C 跑两遍标签一致 | 92.9%（n=210） | 越高越好 | [`sellpoint-check/results/repeat-run.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/repeat-run.json) |
| 参照：第二次判断在答案已知的题上和答案一致 | 95.8%（n=72） | 越高越好 | [`sellpoint-check/results/audit-testset.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/audit-testset.json) |

### 中文测试集（50 条卖点，网络用语和反话）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 判对（C） | 50/50（100.0%，95% 区间 92.9–100.0%） | 越高越好 | [`sellpoint-check/results/score-testset-zh.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-zh.json) |
| 判对（B） | 47/50（94.0%，95% 区间 83.8–97.9%） | 越高越好 | [`sellpoint-check/results/score-testset-zh.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-zh.json) |
| 判对（A） | 44/50（88.0%，95% 区间 76.2–94.4%） | 越高越好 | [`sellpoint-check/results/score-testset-zh.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-zh.json) |

### 英文测试集 v2（50 条卖点，长评价、错别字、反话）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 判对（C） | 50/50（100.0%，95% 区间 92.9–100.0%） | 越高越好 | [`sellpoint-check/results/score-testset-v2.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-v2.json) |
| 判对（B） | 48/50（96.0%，95% 区间 86.5–98.9%） | 越高越好 | [`sellpoint-check/results/score-testset-v2.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-v2.json) |
| 判对（A） | 46/50（92.0%，95% 区间 81.2–96.8%） | 越高越好 | [`sellpoint-check/results/score-testset-v2.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-v2.json) |

### 检索改进 A2：A 没跑过的 180 条卖点

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 判对（A） | 167/180（92.8%，95% 区间 88.0–95.7%） | 越高越好 | [`sellpoint-check/results/score-testset-mixed.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-mixed.json)<br>[`sellpoint-check/results/score-testset-mixed2.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-mixed2.json)<br>[`sellpoint-check/results/score-testset-voice.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-voice.json)<br>[`sellpoint-check/results/score-testset-voice2.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-voice2.json) |
| 判对（A2） | 173/180（96.1%，95% 区间 92.2–98.1%） | 越高越好 | [`sellpoint-check/results/score-testset-mixed.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-mixed.json)<br>[`sellpoint-check/results/score-testset-mixed2.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-mixed2.json)<br>[`sellpoint-check/results/score-testset-voice.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-voice.json)<br>[`sellpoint-check/results/score-testset-voice2.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-voice2.json) |
| 判对（C） | 177/180（98.3%，95% 区间 95.2–99.4%） | 越高越好 | [`sellpoint-check/results/score-testset-mixed.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-mixed.json)<br>[`sellpoint-check/results/score-testset-mixed2.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-mixed2.json)<br>[`sellpoint-check/results/score-testset-voice.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-voice.json)<br>[`sellpoint-check/results/score-testset-voice2.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/score-testset-voice2.json) |

A2 比 A 好，但采用的仍是 C；A2 留作评价太多、一次放不下时的备选。

### 修改建议（商家后台）：第 1 版和现在采用的第 5 版

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 第 1 版，测试集，第一次评分可以直接照着改 | 35/40（87.5%，95% 区间 73.9–94.5%） | 越高越好 | [`sellpoint-check/results/suggest-testset.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset.json) |
| 第 1 版，测试集，第二次评分 | 32/40（80.0%，95% 区间 65.2–89.5%） | 越高越好 | [`sellpoint-check/results/suggest-testset.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset.json) |
| 第 1 版，真实数据，第一次评分 | 140/151（92.7%，95% 区间 87.4–95.9%） | 越高越好 | [`sellpoint-check/results/suggest-run.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-run.json) |
| 第 5 版，真实数据，第一次评分 | 142/151（94.0%，95% 区间 89.1–96.8%） | 越高越好 | [`sellpoint-check/results/suggest-run-v5.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-run-v5.json) |
| 第 5 版，真实数据，第二次评分 | 143/151（94.7%，95% 区间 89.9–97.3%） | 越高越好 | [`sellpoint-check/results/suggest-run-v5.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-run-v5.json) |
| 第 3 版：新文案里没有“买家说”这类写法 | 140/151（92.7%，95% 区间 87.4–95.9%） | 越高越好 | [`sellpoint-check/results/suggest-run-v3.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-run-v3.json) |
| 第 5 版：新文案里没有“买家说”这类写法 | 151/151（100.0%，95% 区间 97.5–100.0%） | 越高越好 | [`sellpoint-check/results/suggest-run-v5.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-run-v5.json) |
| 评分器校准：第一次判对已知好坏的建议 | 31/32（96.9%，95% 区间 84.3–99.4%） | 越高越好 | [`sellpoint-check/results/suggest-testset.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset.json) |
| 评分器校准：第二次 | 30/32（93.8%，95% 区间 79.9–98.3%） | 越高越好 | [`sellpoint-check/results/suggest-testset.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset.json) |
| 中文测试集（第 2 版的对比）：第 1 版可以直接照着改 | 30/34（88.2%，95% 区间 73.4–95.3%） | 越高越好 | [`sellpoint-check/results/suggest-testset-zh.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset-zh.json) |
| 中文测试集（第 2 版的对比）：第 2 版可以直接照着改 | 32/34（94.1%，95% 区间 80.9–98.4%） | 越高越好 | [`sellpoint-check/results/suggest-testset-zh-v2.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset-zh-v2.json) |
| 混合测试集（第 3 版的对比）：第 2 版用对语言 | 20/40（50.0%，95% 区间 35.2–64.8%） | 越高越好 | [`sellpoint-check/results/suggest-testset-mixed-v2.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset-mixed-v2.json) |
| 混合测试集（第 3 版的对比）：第 3 版用对语言 | 40/40（100.0%，95% 区间 91.2–100.0%） | 越高越好 | [`sellpoint-check/results/suggest-testset-mixed-v3.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset-mixed-v3.json) |
| 混合测试集二（第 4 版的对比）：第 3 版可以直接照着改 | 38/39（97.4%，95% 区间 86.8–99.5%） | 越高越好 | [`sellpoint-check/results/suggest-testset-mixed2-v3.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset-mixed2-v3.json) |
| 混合测试集二（第 4 版的对比）：第 4 版可以直接照着改 | 36/39（92.3%，95% 区间 79.7–97.3%） | 越高越好 | [`sellpoint-check/results/suggest-testset-mixed2-v4.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset-mixed2-v4.json) |
| 口语测试集二（第 6 版的对比）：第 5 版可以直接照着改 | 29/32（90.6%，95% 区间 75.8–96.8%） | 越高越好 | [`sellpoint-check/results/suggest-testset-voice2-v5.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset-voice2-v5.json) |
| 口语测试集二（第 6 版的对比）：第 6 版可以直接照着改 | 26/32（81.2%，95% 区间 64.7–91.1%） | 越高越好 | [`sellpoint-check/results/suggest-testset-voice2-v6.json`](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset-voice2-v6.json) |

## 评分器校准

- 卖点判对按写题时定好的答案用脚本算，没有用评分器。
- 真实数据没有标准答案，所以每条证据另做一次独立判断：先在答案已知的题上检验这个判断，和答案一致 95.8%。
- 修改建议由评分器按评分表独立评两次。评分器先在事先写好、已知好坏的建议上校准：两次分别判对 31/32、30/32。评分器和生成建议用的是同一个模型（claude-haiku-5-5），这是局限。

## 局限和失败案例

- 测试集的评价比真实评价短、干净；测试题在真实数据跑完之后由同一作者写成。
  - 建议：上线前用平台自己的、有许可的评价数据重做一遍真实数据的评测。
- 真实数据没有标准答案：第二次独立判断和第一次的一致率（C 的支持证据 88%、反驳证据 91%）只说明两次判断接近，不等于判对。
  - 建议：上线时抽一部分请人工复核，复核结果回流成新的评测题。
- 修改建议的评分器和生成建议用的是同一个模型；两次评分之间的一致性中等。
  - 建议：换一个不同厂家的模型当第二评分方，或抽样人工评分。
- evidence-check 对中文引文要求至少 4 个字，两条完整的 3 个字的标题评价被挡下。
  - 建议：核对脚本对“整条评价就是这几个字”的情况放行。

## 版本

- **1.0**（2026-11-15）第一张卡，项目未公开。
- **1.1**（2026-11-15）开头加了时间、团队、技术、链接和“问题 / 我做了什么 / 结果”，照作品集案例页的写法；评测部分不变。
- **1.2**（2026-11-16）项目已公开：加上代码、设计案例和可点击原型的链接。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。

第三方数据、模型和代码的来源与许可，见[项目仓库](https://github.com/llia0031-dotcom/sellpoint-check)里的说明。
