# 创作者 Skill 合集：评测卡

> 卡片版本 1.0 · 数据截至 2026-11-17 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-17 | Liang Liyuan | Agent Skills（SKILL.md 加 Python 脚本，只用标准库）、Claude Code 插件、批量接口 | [代码和报告](https://github.com/llia0031-dotcom/creator-skills) |

**问题**：创作者每周都要对字幕、排分镜、追热点；交给 AI 助手做时，字幕会不会被改错、分镜里的口播念不念得完、热点选题卡上的事实站不站得住。

**我做了什么**：我做了三个给短视频创作者用的 Agent Skill：字幕对稿、分镜核对、热点选题。每个都带一个核对脚本，结果交出去之前先查一遍。每个都和不装 Skill 的同一个模型在事先定好答案的题上比较，计划和预测跑前冻结。

**结果**：

- 改好的字幕文件完全正确：装 Skill 20/20，不装 2/20
- 请求里不写语速时，分镜四项全过：装 Skill 20/20，不装 0/20；写明语速时不装也有 19/20
- 有伤亡的热点事件不出营销选题卡：装 Skill 4/4，不装 0/4

## 概况

三个给短视频创作者用的 Agent Skill，各带一个只用 Python 标准库的核对脚本：字幕对稿把自动字幕逐条和口播稿比、按阅读速度和时间轴标准查；分镜核对查每个镜头的口播念不念得完、稿子一句不少、总时长对得上；热点选题查每张选题卡上的事实，链接打得开、标题对得上、引文在页面里、数字在引文里、文章够新。每个都和不装 Skill 的同一个模型比较，题目和答案在写题时定好，都是虚构的创作场景。

- **在作品集里的位置**：场景：生成类
- **和核心部件的关系**：热点选题的引文匹配复制自 evidence-check 的核对脚本，规则相同：引文要逐字出自页面，数字要在引文里。
- **用到的模型**：两组都用 claude-haiku-5-5（effort medium），同一条用户消息；评测走批量接口。

## 用途

- 创作者发布前的核对：字幕对回口播稿、分镜时长念得完、热点选题的事实有出处。
- 装进 Claude Code、Codex、DeerFlow 等支持 Agent Skills 的工具直接用。

## 不适用的地方

- 题目是虚构的创作场景，不代表真实创作者的使用情况。
- 不评选题的创意、画面能不能拍、节奏适不适合某个主播。

## 评测数据

### 字幕对稿：自动字幕对回口播稿

10 段口播稿（中文 6、英文 4）切成自动字幕，埋了听错的字、临时改说的话、漏念的句子和时间轴错误；答案写题时定好。请求里写明“字幕要和我实际说的一致、不要改时间轴”。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-17 |
| 题目和答案 | 10 段字幕，每组 20 次 |
| 跑了几次 | 每段每组 2 遍 |
| 模型和发送方式 | claude-haiku-5-5，effort medium，批量接口 |
| 跑前冻结 | `eval/subtitle-check/PREREGISTRATION.md` |

### 分镜核对第一轮：请求里写明语速

10 段稿子，按目标时长写分镜表；请求里写明语速、阅读速度和计数方法。四项检查：稿子逐字按顺序都在、每个镜头的口播念得完、总时长在允许范围内、画面文字读得完。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-17 |
| 题目和答案 | 10 段稿子，每组 20 次 |
| 跑了几次 | 每段每组 2 遍 |
| 模型和发送方式 | claude-haiku-5-5，effort medium，批量接口 |
| 跑前冻结 | `eval/shotlist-check/PREREGISTRATION.md` |

### 分镜核对第二轮：请求里不写语速（新写的题）

另写 10 段稿子，第一轮一段都没用；请求照创作者平时的写法，只说大概多少秒、用我的稿子当口播，不写语速和计数方法。Skill 和脚本是第一轮的同一份冻结副本。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-17 |
| 题目和答案 | 10 段稿子，每组 20 次 |
| 跑了几次 | 每段每组 2 遍 |
| 模型和发送方式 | claude-haiku-5-5，effort medium，批量接口；按默认语速核对 |
| 跑前冻结 | `eval/shotlist-check/v2/PREREGISTRATION.md` |

### 热点选题：每张选题卡上的事实带出处

10 个虚构热点（中文 6、英文 4），每个配账号设定、固定日期和几张抓下来的网页；埋了过时页面、打不开的链接、后来被更正的数字、和官方说法不一致的传言数字、和页面标题不同的引子，以及 2 个有伤亡的事件。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-17 |
| 题目和答案 | 10 个热点，每组 20 次 |
| 跑了几次 | 每个每组 2 遍 |
| 模型和发送方式 | claude-haiku-5-5，effort medium，批量接口 |
| 跑前冻结 | `eval/trend-topic-check/PREREGISTRATION.md` |

## 指标和结果

每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。

### 字幕对稿：自动字幕对回口播稿

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 改好的字幕文件完全正确（不装 Skill） | 2/20（10.0%，95% 区间 2.8–30.1%） | 越高越好 | [`creator-skills/eval/subtitle-check/results/run-2026-11-17.summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/subtitle-check/results/run-2026-11-17.summary.md) |
| 改好的字幕文件完全正确（装 Skill） | 20/20（100.0%，95% 区间 83.9–100.0%） | 越高越好 | [`creator-skills/eval/subtitle-check/results/run-2026-11-17.summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/subtitle-check/results/run-2026-11-17.summary.md) |
| 时间轴没被改动（不装 Skill） | 12/20（60.0%，95% 区间 38.7–78.1%） | 越高越好 | [`creator-skills/eval/subtitle-check/results/run-2026-11-17.summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/subtitle-check/results/run-2026-11-17.summary.md) |
| 时间轴没被改动（装 Skill） | 20/20（100.0%，95% 区间 83.9–100.0%） | 越高越好 | [`creator-skills/eval/subtitle-check/results/run-2026-11-17.summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/subtitle-check/results/run-2026-11-17.summary.md) |
| 临时改说的话照实保留（不装 Skill） | 9/38（23.7%，95% 区间 13.0–39.2%） | 越高越好 | [`creator-skills/eval/subtitle-check/results/run-2026-11-17.summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/subtitle-check/results/run-2026-11-17.summary.md) |
| 临时改说的话照实保留（装 Skill） | 38/38（100.0%，95% 区间 90.8–100.0%） | 越高越好 | [`creator-skills/eval/subtitle-check/results/run-2026-11-17.summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/subtitle-check/results/run-2026-11-17.summary.md) |

两组都能改对听错的字；不装 Skill 时常动时间轴、把临时改说的话改回原稿，所以改好的文件很少完全正确。

### 分镜核对第一轮：请求里写明语速

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 四项全过（不装 Skill） | 19/20（95.0%，95% 区间 76.4–99.1%） | 越高越好 | [`creator-skills/eval/shotlist-check/results/summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/shotlist-check/results/summary.md) |
| 四项全过（装 Skill） | 20/20（100.0%，95% 区间 83.9–100.0%） | 越高越好 | [`creator-skills/eval/shotlist-check/results/summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/shotlist-check/results/summary.md) |

请求把语速和计数方法都写清时，不装 Skill 也几乎全过，题目到顶；预测的“最多一半”没成立。

### 分镜核对第二轮：请求里不写语速（新写的题）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 四项全过（不装 Skill，默认语速） | 0/20（0.0%，95% 区间 0.0–16.1%） | 越高越好 | [`creator-skills/eval/shotlist-check/v2/results/summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/shotlist-check/v2/results/summary.md) |
| 四项全过（装 Skill，默认语速） | 20/20（100.0%，95% 区间 83.9–100.0%） | 越高越好 | [`creator-skills/eval/shotlist-check/v2/results/summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/shotlist-check/v2/results/summary.md) |
| 口播念不完的镜头（不装 Skill） | 90/182（49.5%，95% 区间 42.3–56.7%） | 越低越好 | [`creator-skills/eval/shotlist-check/v2/results/summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/shotlist-check/v2/results/summary.md) |
| 口播念不完的镜头（装 Skill） | 0/230（0.0%，95% 区间 0.0–1.6%） | 越低越好 | [`creator-skills/eval/shotlist-check/v2/results/summary.md`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/shotlist-check/v2/results/summary.md) |

不写语速时，不装 Skill 的分镜大量镜头念不完，一张都没全过；装了 Skill，脚本先查出念不完的镜头，全部通过。

### 热点选题：每张选题卡上的事实带出处

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 有伤亡的事件处理得当（不装 Skill） | 0/4（0.0%，95% 区间 0.0–49.0%） | 越高越好 | [`creator-skills/eval/trend-topic-check/results/scores.json`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/trend-topic-check/results/scores.json) |
| 有伤亡的事件处理得当（装 Skill） | 4/4（100.0%，95% 区间 51.0–100.0%） | 越高越好 | [`creator-skills/eval/trend-topic-check/results/scores.json`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/trend-topic-check/results/scores.json) |
| 数字不在引文里的事实（不装 Skill） | 6/125（4.8%，95% 区间 2.2–10.1%） | 越低越好 | [`creator-skills/eval/trend-topic-check/results/scores.json`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/trend-topic-check/results/scores.json) |
| 数字不在引文里的事实（装 Skill） | 0/128（0.0%，95% 区间 0.0–2.9%） | 越低越好 | [`creator-skills/eval/trend-topic-check/results/scores.json`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/trend-topic-check/results/scores.json) |
| 装 Skill 的费用是不装的 | 2.9 倍 | 越低越好 | [`creator-skills/eval/trend-topic-check/results/scores.json`](https://github.com/llia0031-dotcom/creator-skills/blob/main/eval/trend-topic-check/results/scores.json) |

两组的出处大多核对得上；差别在有伤亡的事件和数字：不装 Skill 时给伤亡事件出了营销卡，也有数字不在引文里。

## 评分器校准

- 没有用评分器：每一项都按写题时定好的答案用脚本算；选题的创意和是否适合账号没有打分。

## 局限和失败案例

- 题目都是合成的，写题时就想着 Skill 能查出来的问题；真实音频、口音、背景音乐和多人说话都没覆盖。
  - 建议：上线前拿真实视频的自动字幕和真实热点再测一批。
- 一个模型，每题每组两遍，差一两题算噪声。
  - 建议：换模型或改 effort 时重新跑同一套题。
- 分镜的差别只在请求不写语速时出现：写明语速时不装 Skill 也有 19/20。
  - 建议：看用户平时怎么提需求，决定这个 Skill 值不值得默认装上。
- 热点选题只查事实的出处和伤亡事件，不评选题的创意和是否适合账号。
  - 建议：创意和账号是否合适另定评分规则再测。

## 版本

- **1.0**（2026-11-17）第一张卡，照公开仓库 creator-skills 的结果文件写。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。

第三方数据、模型和代码的来源与许可，见[项目仓库](https://github.com/llia0031-dotcom/creator-skills)里的说明。
