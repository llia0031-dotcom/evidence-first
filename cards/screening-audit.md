# 有据可查的简历初筛：评测卡

> 卡片版本 1.2 · 数据截至 2026-11-15 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-13 – 2026-11-14 | Liang Liyuan | Node.js、Python、evidence-check 0.2.0、批量接口 | [代码和报告](https://github.com/Jason-d-e/evidence-screening) |

**问题**：用模型初筛简历时，每个“符合 / 不符合”都要附简历原文；看它会不会更准、换名字性别学校后结论会不会变。

**我做了什么**：我写了虚构的岗位和简历、事先定好答案，比较普通打分、附原文、附原文加脚本核对几种做法；发现核对的接法会误伤正确的判断以后，改了两版接法；再用带陷阱的新简历、植入错误和第二次独立复核检验。

**结果**：

- 换名字后去留变化：普通打分 0/240，附原文 0/240
- 核对误伤正确的“符合”：70/424 → 10/424（先拆出简历事实）→ 0/424（交卷前自查）
- 独立复核挑出植入的错读：80/80

## 概况

检验一件事：让模型给每个“符合 / 不符合”附上简历原文、再用 evidence-check 的脚本核对，初筛会不会更准、在换掉名字、性别、学校、休学、婚育之后更稳。岗位和简历全部虚构，答案在写简历时定好。做了四版评测：第一版看准确和稳定，第二版改核对的接法，第三版用更乱、带陷阱的简历，另做了植入错误测试和第二次独立复核。

- **在作品集里的位置**：场景：判断类
- **和核心部件的关系**：用 evidence-check 0.2.0 脚本的冻结副本核对每条引文。
- **用到的模型**：claude-haiku-5-5；第三版之后走批量接口。

## 用途

- 给招聘团队一份带依据的逐条初判：每条“符合”能点开简历原文。
- 上线前的检查方法：换掉名字、性别、学校等，看去留会不会变。

## 不适用的地方

- 不是对任何产品的审计，只是一个小规模的对照测试；不用真人简历。
- 总分不能用来排名或卡分数线；关键词匹配不能单独做决定。
- 换到自己的岗位和简历上，上线前要重测。

## 评测数据

### 第一版：准确和稳定（228 个简历版本）

4 个岗位、24 份基础简历，每份改出换名字、性别、学校、休学、婚育、提示注入等版本，共 228 个。比较关键词匹配、普通打分、附原文、附原文加脚本核对。跑前冻结 11 个文件的哈希。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-13 |
| 题目和答案 | 228 个版本，每组 2 遍，共 1,368 次调用 |
| 跑了几次 | 每组 2 遍，合并计算 |
| 模型和发送方式 | claude-haiku-5-5，普通接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md` |

### 第二版：改核对的接法（12 份新简历）

让模型先拆出“简历事实”和引文，脚本只核对这两样；再试一组交卷前自己调用核对工具。12 份新简历、48 个版本，跑前冻结。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-13 |
| 题目和答案 | 48 个版本，4 组各 2 遍，共 384 次对话 |
| 跑了几次 | 每组 2 遍，合并计算 |
| 模型和发送方式 | claude-haiku-5-5，普通接口 |
| 跑前冻结 | `eval/v2/PREREGISTRATION.md` |

### 第三版：更乱、带陷阱的简历（24 份）

24 份更乱的新简历，埋了 40 个陷阱（例如只用过没做过、低于门槛、已经毕业），答案写简历时定好，跑前冻结。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-14 |
| 题目和答案 | 24 份简历、40 个陷阱，3 组各 2 遍 |
| 跑了几次 | 每组 2 遍，合并计算 |
| 模型和发送方式 | claude-haiku-5-5，批量接口（半价） |
| 跑前冻结 | `eval/v3/PREREGISTRATION.md` |

### 植入错误测试：脚本能拦住什么

在已有的正确回答里植入错误：改数字、加数字、删字、换成别人简历里的句子，以及“看错意思”（引文是真的，结论是错的）。不调用模型。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-14 |
| 题目和答案 | 409 条基础回答 |
| 跑了几次 | 确定性脚本，跑 1 遍 |
| 模型和发送方式 | 不调用模型，不花钱 |
| 跑前冻结 | `eval/seeded/PREREGISTRATION.md` |

### 第二次独立复核

对每条“符合”另做一次独立复核：一组看得到理由，一组只看引文。用第三版的 103 条正确答案和 40 条植入的错读检验。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-14 |
| 题目和答案 | 143 条，每组 2 遍 |
| 跑了几次 | 每组 2 遍，合并计算 |
| 模型和发送方式 | claude-haiku-5-5，批量接口（半价） |
| 跑前冻结 | `eval/verify/PREREGISTRATION.md` |

## 指标和结果

每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。

### 第一版：准确和稳定（228 个简历版本）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 逐条判对（普通打分） | 2728/2736（99.7%，95% 区间 99.4–99.9%） | 越高越好 | [`evidence-screening/eval/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/results/run-2026-11-13.summary.json) |
| 逐条判对（附原文） | 2735/2736（100.0%，95% 区间 99.8–100.0%） | 越高越好 | [`evidence-screening/eval/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/results/run-2026-11-13.summary.json) |
| 逐条判对（附原文 + 脚本核对） | 2379/2736（87.0%，95% 区间 85.6–88.2%） | 越高越好 | [`evidence-screening/eval/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/results/run-2026-11-13.summary.json) |
| 逐条判对（关键词匹配） | 2510/2736（91.7%，95% 区间 90.6–92.7%） | 越高越好 | [`evidence-screening/eval/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/results/run-2026-11-13.summary.json) |
| 换名字后去留变了（普通打分） | 0/240（0.0%，95% 区间 0.0–1.6%） | 越低越好 | [`evidence-screening/eval/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/results/run-2026-11-13.summary.json) |
| 换名字后去留变了（附原文） | 0/240（0.0%，95% 区间 0.0–1.6%） | 越低越好 | [`evidence-screening/eval/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/results/run-2026-11-13.summary.json) |
| 换学校后去留变了（附原文） | 0/48（0.0%，95% 区间 0.0–7.4%） | 越低越好 | [`evidence-screening/eval/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/results/run-2026-11-13.summary.json) |

附原文本身不降准确率；但把脚本核对直接接在“符合”上会误伤：模型的“符合”里常复述岗位门槛的数字，简历原文里没有，被判没依据。

### 第二版：改核对的接法（12 份新简历）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 正确的“符合”被核对误伤（附原文 + 脚本） | 70/424（16.5%，95% 区间 13.3–20.3%） | 越低越好 | [`evidence-screening/eval/v2/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/v2/results/run-2026-11-13.summary.json) |
| 正确的“符合”被核对误伤（先拆简历事实 + 脚本） | 10/424（2.4%，95% 区间 1.3–4.3%） | 越低越好 | [`evidence-screening/eval/v2/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/v2/results/run-2026-11-13.summary.json) |
| 正确的“符合”被核对误伤（交卷前自查 + 脚本） | 0/424（0.0%，95% 区间 0.0–0.9%） | 越低越好 | [`evidence-screening/eval/v2/results/run-2026-11-13.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/v2/results/run-2026-11-13.summary.json) |

### 第三版：更乱、带陷阱的简历（24 份）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 陷阱判成“不符合”（交卷前自查） | 80/80（100.0%，95% 区间 95.4–100.0%） | 越高越好 | [`evidence-screening/eval/v3/results/run-2026-11-14.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/v3/results/run-2026-11-14.summary.json) |
| 陷阱判成“不符合”（普通打分） | 80/80（100.0%，95% 区间 95.4–100.0%） | 越高越好 | [`evidence-screening/eval/v3/results/run-2026-11-14.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/v3/results/run-2026-11-14.summary.json) |
| 逐条判对（交卷前自查 + 脚本） | 286/288（99.3%，95% 区间 97.5–99.8%） | 越高越好 | [`evidence-screening/eval/v3/results/run-2026-11-14.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/v3/results/run-2026-11-14.summary.json) |

### 植入错误测试：脚本能拦住什么

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 加进去的数字被拦下 | 409/409（100.0%，95% 区间 99.1–100.0%） | 越高越好 | [`evidence-screening/eval/seeded/results/seeded-2026-11-14.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/seeded/results/seeded-2026-11-14.json) |
| 别人简历里的句子被拦下 | 409/409（100.0%，95% 区间 99.1–100.0%） | 越高越好 | [`evidence-screening/eval/seeded/results/seeded-2026-11-14.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/seeded/results/seeded-2026-11-14.json) |
| 看错意思被拦下 | 0/40（0.0%，95% 区间 0.0–8.8%） | 越高越好 | [`evidence-screening/eval/seeded/results/seeded-2026-11-14.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/seeded/results/seeded-2026-11-14.json) |

引文核对防编造，不防看错意思；所以还要第二次独立复核。

### 第二次独立复核

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 挑出植入的错读（看得到理由） | 80/80（100.0%，95% 区间 95.4–100.0%） | 越高越好 | [`evidence-screening/eval/verify/results/run-2026-11-14.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/verify/results/run-2026-11-14.summary.json) |
| 挑出植入的错读（只看引文） | 79/80（98.8%，95% 区间 93.3–99.8%） | 越高越好 | [`evidence-screening/eval/verify/results/run-2026-11-14.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/verify/results/run-2026-11-14.summary.json) |
| 正确答案被误报（看得到理由） | 0/206（0.0%，95% 区间 0.0–1.8%） | 越低越好 | [`evidence-screening/eval/verify/results/run-2026-11-14.summary.json`](https://github.com/Jason-d-e/evidence-screening/blob/main/eval/verify/results/run-2026-11-14.summary.json) |

## 评分器校准

- 逐条要求按写简历时定好的答案用脚本算，没有用评分器。
- 第二次独立复核先在答案已知的样本上检验：植入的错读挑出 80/80，正确答案误报 0/206。

## 局限和失败案例

- 简历是虚构的、短的，和答案出自同一作者；一个模型、一个设置。
  - 建议：上线前用脱敏的真实简历和招聘团队自己的岗位重测。
- 植入的错读是写进去的，复核和初筛用的是同一个模型。
  - 建议：复核换一个不同厂家的模型，或抽样人工复核。
- 答案里有一格有争议（第三版唯一的错格就出在这里）。
  - 建议：有争议的答案标出来，单独统计，不计入主指标。

## 版本

- **1.0**（2026-11-15）第一张卡，项目未公开。正在跑的低 effort 一轮还没打分，不收。
- **1.1**（2026-11-15）开头加了时间、团队、技术、链接和“问题 / 我做了什么 / 结果”，照作品集案例页的写法；评测部分不变。
- **1.2**（2026-11-16）项目已公开：加上代码和报告的链接；演示页还没上线。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。

第三方数据、模型和代码的来源与许可，见[项目仓库](https://github.com/Jason-d-e/evidence-screening)里的说明。
