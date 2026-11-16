# Cairn：评测卡

> 卡片版本 1.1 · 数据截至 2026-11-15 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-09 – 2026-11-11（LaunchPad Hacks） | Liang Liyuan、ZIzi821 | Node.js、React、本机向量检索和重排、Claude Haiku 5.5 | [代码](https://github.com/Jason-d-e/cairn) · [在线演示](https://jason-d-e.github.io/cairn/) |

**问题**：按一个机构自己公开的规定回答问题，每句话逐字引原文；先要把对的那一页找出来。

**我做了什么**：我们做了按公开规定回答、逐字引原文的问答台：先选校区再提问，检索、生成、在代码里核对引文；用 45 道写好正确页面的题比较 7 种检索做法，再用学生的真实提问单独测。

**结果**：

- 45 道题、7 种检索做法：采用的做法正确页面进前 5 名 44/45，MRR 0.839
- 学生用自己的话提的问题：前 5 名 14/15，MRR 0.724

## 概况

一个按机构公开规定回答问题的问答台，每句话都逐字引原文。公开的这一版用 Monash 学生事务的 58 个公开页面。检索先把问题翻译成英文，再做向量检索和重排；回答里的引文先核对通过才显示，不能逐字对上的改写会被拦下。评测比较了 7 种检索做法。

- **在作品集里的位置**：场景：检索问答
- **和核心部件的关系**：检索问答场景，主线的起点：回答必须附原文。卖点体检的“先检索”做法用的就是这里的检索模型和 Orama 混合检索。
- **用到的模型**：回答和中文问题翻译用 claude-haiku-5-5；检索用本机的向量模型和重排模型。

## 用途

- 按公开规定回答学生事务这类问题，每句都能点开原文。
- 比较检索做法：同一套题上看哪种做法最先找到对的页面。

## 不适用的地方

- 只覆盖收录的 58 个公开页面，没有课程手册，也没有要登录才能看的内容。
- 是原型，不是正式建议；不回答个人、法律、医疗方面的问题。
- 评测测的是检索，不是写出来的回答好不好。

## 评测数据

### 检索评测：45 道题、7 种做法

45 道题（英文 25、中文 20），每题的正确页面写题时定好。比较关键词、向量、两种混合检索、加重排、先翻译再检索等 7 种做法。没有跑前冻结的哈希。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-10 |
| 题目和答案 | 45 道题 |
| 跑了几次 | 每种做法 1 遍 |
| 模型和发送方式 | 检索在本机跑；中文问题的翻译用 claude-haiku-5-5，普通接口 |

### 学生提的真实问题（另算一套）

学生用自己的话提的 20 个问题（中文 10、英文 9、马来文 1），照原样收录，去掉了名字和医疗细节，经同意公开。其中 15 个在 58 个页面里有答案，只算这 15 个。单独算，不和上面那套题混在一起。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-11 |
| 题目和答案 | 15 个有答案的问题 |
| 跑了几次 | 1 遍 |
| 模型和发送方式 | 采用的做法，同上 |

## 指标和结果

每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。

### 检索评测：45 道题、7 种做法

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 正确页面排第 1（采用的做法） | 34/45（75.6%，95% 区间 61.3–85.8%） | 越高越好 | [`cairn/app/eval/results/retrieval-2026-11-10.json`](https://github.com/Jason-d-e/cairn/blob/main/app/eval/results/retrieval-2026-11-10.json) |
| 正确页面进前 5（采用的做法） | 44/45（97.8%，95% 区间 88.4–99.6%） | 越高越好 | [`cairn/app/eval/results/retrieval-2026-11-10.json`](https://github.com/Jason-d-e/cairn/blob/main/app/eval/results/retrieval-2026-11-10.json) |
| MRR@10（采用的做法） | 0.839（n=45） | 越高越好 | [`cairn/app/eval/results/retrieval-2026-11-10.json`](https://github.com/Jason-d-e/cairn/blob/main/app/eval/results/retrieval-2026-11-10.json) |
| MRR@10（只用向量检索） | 0.709（n=45） | 越高越好 | [`cairn/app/eval/results/retrieval-2026-11-10.json`](https://github.com/Jason-d-e/cairn/blob/main/app/eval/results/retrieval-2026-11-10.json) |
| MRR@10（只用关键词） | 0.375（n=45） | 越高越好 | [`cairn/app/eval/results/retrieval-2026-11-10.json`](https://github.com/Jason-d-e/cairn/blob/main/app/eval/results/retrieval-2026-11-10.json) |
| 中文题进前 5：不翻译 | 18/20（90.0%，95% 区间 69.9–97.2%） | 越高越好 | [`cairn/app/eval/results/retrieval-2026-11-10.json`](https://github.com/Jason-d-e/cairn/blob/main/app/eval/results/retrieval-2026-11-10.json) |
| 中文题进前 5：先翻译 | 19/20（95.0%，95% 区间 76.4–99.1%） | 越高越好 | [`cairn/app/eval/results/retrieval-2026-11-10.json`](https://github.com/Jason-d-e/cairn/blob/main/app/eval/results/retrieval-2026-11-10.json) |

### 学生提的真实问题（另算一套）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 正确页面进前 5 | 14/15（93.3%，95% 区间 70.2–98.8%） | 越高越好 | [`cairn/app/eval/results/student-retrieval-2026-11-11.json`](https://github.com/Jason-d-e/cairn/blob/main/app/eval/results/student-retrieval-2026-11-11.json) |
| MRR@10 | 0.724（n=15） | 越高越好 | [`cairn/app/eval/results/student-retrieval-2026-11-11.json`](https://github.com/Jason-d-e/cairn/blob/main/app/eval/results/student-retrieval-2026-11-11.json) |

## 评分器校准

- 没有用评分器：每道题的正确页面在写题时定好，命中和 MRR 用脚本算。

## 局限和失败案例

- 真实提问比自己写的题难：学生问题的 MRR 0.724，自己写的题 0.839；漏掉的是断网的线上考试和马来文的问题。
  - 建议：上线后把用户的真实问题按同样的方法单独打分，持续盯住这个差距。
- 没有评测回答本身写得好不好；冒烟测试里有一次把马来西亚校区的问题按澳大利亚的规定回答了。
  - 建议：加一套带校区的题，检查答案引用的页面和提问者的校区一致。

## 版本

- **1.0**（2026-11-15）第一张卡；线上用的提示词是 cairn-monash-v2。
- **1.1**（2026-11-15）开头加了时间、团队、技术、链接和“问题 / 我做了什么 / 结果”，照作品集案例页的写法；评测部分不变。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。
