# 有据经营分析：评测卡

> 卡片版本 1.0 · 数据截至 2026-11-17 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-16 – 2026-11-17 | Liang Liyuan | Python、DuckDB（SQL）、Pandas、evidence-check 0.4.0、批量接口、Excel、Dify | [代码和报告](https://github.com/llia0031-dotcom/grounded-business-review) |

**问题**：每周看经营数据的人要知道哪些指标异动、原因在哪；让模型找原因、写周报，原因找得准不准，周报里的数字能不能都对回查询结果（在合成数据上测）。

**我做了什么**：我在合成的到店团购数据上搭了指标字典、一条 SQL 的周监控、贡献度和率效应拆解、带数字核对的经营周报，比较固定脚本、一次提示词和 Agent 三种找原因的做法；埋好答案的测试题和评测计划在跑之前冻结；另把同一条流程搭成 Dify 工作流。

**结果**：

- 埋好的原因全找对：脚本 31/36，一次提示词 28/36，Agent 34/36
- 按题配对，Agent 比一次提示词多对 6 题、少对 0 题（p = 0.031）；和脚本比分不出高下（p = 0.45）
- 改一次以内放行：一次提示词 35/36，Agent 33/36；没放行的都卡在中文数字上，没有一个错数

## 概况

在一份合成的到店团购数据上，把“每周监控 → 按维度拆解 → 写经营周报 → 数字核对”做成一条可以重跑的线，并比较三种找原因的做法：固定规则的脚本、把固定查询结果交给模型的一次提示词、让模型自己用工具查数的 Agent。周报里每段带数字的话都要引用查询结果的行，用 evidence-check 逐段核对，对不上就退回改一次，再不过就不放行。数据由脚本按随机种子生成，不是任何平台的真实经营数据。

- **在作品集里的位置**：场景：判断类
- **和核心部件的关系**：周报的数字核对直接调用 evidence-check 0.4.0 的脚本，项目自己另加三条结构规则。
- **用到的模型**：评测里两种模型做法都用 claude-haiku-5-5（effort medium，批量接口）；脚本不调用模型。Dify 版的模型节点默认用平台额度里的 gpt-5-mini，只用来确认流程在平台上能跑通，不在评测里。

## 用途

- 给经营分析团队一份每周的异动周报：发现、原因、建议，每个数字都能点回查询结果。
- 上线前的检查方法：在埋好答案的数据上比较几种找原因的做法，看谁找得准、花多少钱。

## 不适用的地方

- 数据是合成的，不是任何平台的真实经营数据；指标口径是为这份数据拟的。
- 建议没有打分。
- Dify 版只确认流程能跑通，没有评测。

## 评测数据

### 测试集：埋好答案的题（脚本、一次提示词、Agent）

合成到店团购数据上 36 道题，每道题是一个由自己的随机种子生成的“世界”，在分析周里埋一个或两个事件，答案出题时写进题目文件：单原因单维度 20 道、单原因两个维度交叉 6 道、两个原因 4 道、对照 6 道。开发集 16 道用来写规则和提示词，和测试集不共用种子。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-17 |
| 题目和答案 | 36 道题 |
| 跑了几次 | 每种做法每题 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，effort medium，批量接口；脚本不调用模型 |
| 跑前冻结 | `eval/PREREGISTRATION.md`；跑前冻结的文件指纹在 `eval/frozen.json`，跑完核对都没变 |

### 开发集：用来写规则和提示词（第 4 版）

16 道题，种子和测试集不重复；规则和提示词都在这上面改，改完才冻结。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-17 |
| 题目和答案 | 16 道题 |
| 跑了几次 | 每种做法每题 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，effort medium，批量接口 |

## 指标和结果

每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。

### 测试集：埋好答案的题（脚本、一次提示词、Agent）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 埋好的原因全找对（脚本） | 31/36（86.1%，95% 区间 71.3–93.9%） | 越高越好 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| 埋好的原因全找对（一次提示词） | 28/36（77.8%，95% 区间 61.9–88.3%） | 越高越好 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| 埋好的原因全找对（Agent） | 34/36（94.4%，95% 区间 81.9–98.5%） | 越高越好 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| 两个维度交叉的原因找对（脚本） | 6/6（100.0%，95% 区间 61.0–100.0%） | 越高越好 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| 两个维度交叉的原因找对（一次提示词） | 0/6（0.0%，95% 区间 0.0–39.0%） | 越高越好 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| 两个维度交叉的原因找对（Agent） | 4/6（66.7%，95% 区间 30.0–90.3%） | 越高越好 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| 按题配对：只有 Agent 对、一次提示词错的题 | 6 | 只作说明 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| 按题配对：只有一次提示词对、Agent 错的题 | 0 | 只作说明 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| Agent 对一次提示词：精确检验的 p 值 | 0.031 | 只作说明 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| Agent 对脚本：精确检验的 p 值 | 0.45 | 只作说明 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| 周报放行（脚本） | 36/36（100.0%，95% 区间 90.4–100.0%） | 越高越好 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| 改一次以内放行（一次提示词） | 35/36（97.2%，95% 区间 85.8–99.5%） | 越高越好 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| 改一次以内放行（Agent） | 33/36（91.7%，95% 区间 78.2–97.1%） | 越高越好 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| 第一次交卷就放行（一次提示词）（预测在七成到八成五之间，这一条没成立） | 19/36（52.8%，95% 区间 37.0–68.0%） | 越高越好 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| 第一次交卷就放行（Agent） | 12/36（33.3%，95% 区间 20.2–49.7%） | 越高越好 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| Agent 第一稿：引了不在引用行里的数的段落（改一次以后是零） | 19 | 越低越好 | [`grounded-business-review/eval/EVALUATION.md`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/EVALUATION.md) |
| 每题费用（一次提示词，批量价） | 0.0032 美元 | 越低越好 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| 每题费用（Agent，批量价） | 0.0057 美元 | 越低越好 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |
| Agent 每题费用是一次提示词的 | 1.8 倍 | 越低越好 | [`grounded-business-review/eval/results/summary-test.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-test.json) |

Agent 原因找得最准，按题配对明显好过一次提示词；和脚本只差几题，分不出高下。一次提示词拿到的固定材料只按单个维度拆，两个维度交叉的原因一道也没对。改一次以内，三种做法的周报大多放行；第一次交卷就放行的比例比预测低。

### 开发集：用来写规则和提示词（第 4 版）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 开发集：原因全找对（脚本） | 12/16（75.0%，95% 区间 50.5–89.8%） | 越高越好 | [`grounded-business-review/eval/results/summary-dev.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-dev.json) |
| 开发集：原因全找对（一次提示词） | 13/16（81.2%，95% 区间 57.0–93.4%） | 越高越好 | [`grounded-business-review/eval/results/summary-dev.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-dev.json) |
| 开发集：原因全找对（Agent） | 16/16（100.0%，95% 区间 80.6–100.0%） | 越高越好 | [`grounded-business-review/eval/results/summary-dev.json`](https://github.com/llia0031-dotcom/grounded-business-review/blob/main/eval/results/summary-dev.json) |

开发集是改规则和提示词用的，数字偏乐观，不拿来和测试集比。

## 评分器校准

- 没有用评分器：原因对不对按出题时埋好的答案用规则算，周报能不能放行用 evidence-check 0.4.0 的脚本加三条结构规则判。

## 局限和失败案例

- 数据、埋的事件、监控和三种做法都出自同一个项目；埋的事件干净，都落在现有维度里，真实的原因常常不是这样。
  - 建议：换到真实数据前，先拿历史上已经查清原因的周做一批题再测。
- Agent 和脚本只差几题（p = 0.45），这批题分不出高下。
  - 建议：要分出高下得加题，尤其是两个原因和两个维度交叉的题。
- 数字核对对中文数字太严：最后没放行的周报里没有一个错数，没过的段落都卡在“这两项”“前一天”这类词上。
  - 建议：把计数词和数量分开处理，或给计数词单独的规则；严到什么程度是产品上的取舍，要和使用的人一起定。
- Agent 第一稿引了不在引用行里的数的段落有 19 段，靠退回改一次才全部改好；没有核对就会发出去。
  - 建议：核对放在发出之前，不能省。
- 建议没有打分。
  - 建议：给建议定评分规则，再在同一批题上测。

## 版本

- **1.0**（2026-11-17）第一张卡，照公开仓库 grounded-business-review 的结果文件写。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。

第三方数据、模型和代码的来源与许可，见[项目仓库](https://github.com/llia0031-dotcom/grounded-business-review)里的说明。
