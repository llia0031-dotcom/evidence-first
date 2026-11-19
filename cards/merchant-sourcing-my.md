# 马来西亚电子类目招商样本：评测卡

> 卡片版本 1.0 · 数据截至 2026-11-19 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-19 | Liang Liyuan | Python、DuckDB、SQL、Excel（openpyxl）、evidence-check、公开页面存档 | [代码和资料](https://github.com/llia0031-dotcom/merchant-sourcing-my) · [先联系谁](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/pool/PRIORITY.md) |

**问题**：类目团队招商的第一周：市场什么样、先联系哪些商家、凭什么，每类产品要哪些认证，入驻怎么跟进；每条理由都要拿得出公开出处。

**我做了什么**：我先查了现成的店铺排行工具：它们只排已经在平台上的商家，回答不了“还没进来或还没做起来的商家里先招谁”。于是用公开来源补这一块：存下官方、市场和品牌的公开页面，写出行业洞察和按品类的资质清单；打分规则在填写任何一行之前写好并冻结，按它给本地品牌、经销商和连锁店排出先后；再配上入驻跟进表、头 30 天的 SQL 和触达模板。每条事实和商家池的每一格都用 evidence-check 对回存档原文。

**结果**：

- 洞察、资质清单、两份 README 和商家池里带出处的说法，逐字对回存档原文：453/453
- 商家池 42 家、9 个细分品类，305 个格子各有核对过的原文；按冻结的规则分档，A 档 14 家
- 存了 183 个公开页面，被引用的 130 个

## 概况

给类目团队的招商“第一周作业”：行业洞察、本地品牌、经销商和连锁店的打分商家池、按品类的资质清单、入驻跟进表、头 30 天的 SQL 和触达模板。评的是这份材料里的每条事实：引文要在存档页面里，数字要在引文里，商家池的引文里还要有能当证据的词；对不上，构建就停下。

- **在作品集里的位置**：场景：判断类
- **和核心部件的关系**：每条事实都用 evidence-check 0.5.0 的核对脚本对回存档原文；头 30 天的 SQL 沿用有据经营分析的周指标做法。
- **用到的模型**：没有调用模型：读页面、打分、核对和出表都由脚本完成。

## 用途

- 类目团队开拓一个新市场的细分品类时：先看行业洞察定先招什么，再按商家池的先后和下一步去联系。
- 商家第一次通话后：把对应品类的资质清单发过去，用跟进表排出入驻节点，用头 30 天的 SQL 看新店起步。

## 不适用的地方

- 不评价任何商家；分数低只表示公开证据少或眼下能补的少。
- 不替代平台自己的卖家名单和后台数据；只用不登录就能读的公开页面。

## 评测数据

### 全文核对：每条带出处的说法

洞察、资质清单、中英两份 README 里每一行带出处标签的话，商家池每一行的每个字段，还有每条需求信号；对照的是存档的公开页面原文和结果文件。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-19 |
| 题目和答案 | 全部带出处的说法 |
| 跑了几次 | 每次构建都跑 |
| 模型和发送方式 | evidence-check 0.5.0 的核对脚本；不调用模型 |
| 跑前冻结 | `sources/manifests/`（每个网址、读取时间和原文的 SHA-256） |

### 商家池：按冻结的规则打分

本地品牌、经销商和连锁店，每个字段只从存档的公开页面填，带出处编号和原文；四个维度：需求信号、内容电商缺口、资质准备度、内容能力。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-19 |
| 题目和答案 | 商家池全部商家 |
| 跑了几次 | 每次构建都跑 |
| 模型和发送方式 | `pool/build.py` 照规则打分，先校验规则文件的指纹 |
| 跑前冻结 | `pool/SCORING.md` 第二版 |

### 来源：存档的公开页面

只读单个公开页面：先查 robots.txt，同一网站至少隔几秒，不登录，不读电商平台的商品页、店铺页和搜索页；资质只引监管机构。页面原文归原发布方，不公开，清单里有网址、读取时间和原文的 SHA-256。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-19 |
| 题目和答案 | 全部存档页面 |
| 跑了几次 | 读取一次，可用 `tools/refetch.py` 重新保存 |
| 模型和发送方式 | 不调用模型 |
| 跑前冻结 | `sources/manifests/` |

## 指标和结果

每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。

### 全文核对：每条带出处的说法

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 带出处的说法对回存档原文 | 453/453（100.0%，95% 区间 99.2–100.0%） | 越高越好 | [`merchant-sourcing-my/results/CLAIM_CHECK.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/CLAIM_CHECK.md) |
| 带数字却没标出处的行 | 0 | 越低越好 | [`merchant-sourcing-my/results/CLAIM_CHECK.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/CLAIM_CHECK.md) |

每条说法都对回了原文，带数字却没标出处的行一条也没有。

### 商家池：按冻结的规则打分

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 有核对过原文的格子 | 305 | 只作说明 | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| 商家池里的商家 | 42 | 只作说明 | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| 覆盖的细分品类 | 9 | 只作说明 | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| 找到马来西亚公司或具名经销商 | 23/42（54.8%，95% 区间 39.9–68.8%） | 只作说明 | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| A 档商家 | 14 | 只作说明 | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| 帮它开第一家内容电商店 | 17 | 只作说明 | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| 帮已开但还小的店做起来 | 18 | 只作说明 | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |

排在最前的是在别处已经卖得好、在内容电商上还没开店或还没做大的本地商家；一半以上找到了马来西亚公司或具名经销商。

### 来源：存档的公开页面

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 存档的公开页面 | 183 | 只作说明 | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| 被引用的页面 | 130/183（71.0%，95% 区间 64.1–77.1%） | 只作说明 | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |
| 官方页面 | 42 | 只作说明 | [`merchant-sourcing-my/results/SUMMARY.md`](https://github.com/llia0031-dotcom/merchant-sourcing-my/blob/main/results/SUMMARY.md) |

大部分存下的页面都被洞察、清单或商家池引用；资质清单只引监管机构的页面。

## 局限和失败案例

- “公开来源里没找到”不代表不存在，也不是对商家的评价；只读了不登录能看的页面。
  - 建议：第一次联系前，先查平台自己的卖家名单。
- 第三方给的销量数字是它们的估算；店铺榜只来自一个数据集，按件数排序。
  - 建议：拿到平台或商家自己的数据后，用它替换估算再排一次。
- 没有联系过任何商家，触达模板没有发出过；头 30 天的示例数据是虚构的，只用来测 SQL。
  - 建议：真正联系后，把回复率和入驻进度记进跟进表，再回头校准打分规则。

## 版本

- **1.0**（2026-11-19）第一张卡，照公开仓库 merchant-sourcing-my 的结果文件写。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。

第三方数据、模型和代码的来源与许可，见[项目仓库](https://github.com/llia0031-dotcom/merchant-sourcing-my)里的说明。
