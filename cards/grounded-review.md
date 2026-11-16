# 有据审核（广告审核 Agent）：评测卡

> 卡片版本 1.2 · 数据截至 2026-11-15 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-13 – 2026-11-16 | Liang Liyuan | Python、RapidOCR、BM25、evidence-check、Transformers（对比组）、批量接口 | [代码和报告](https://github.com/Jason-d-e/grounded-review) · [演示页](https://jason-d-e.github.io/grounded-review/) · [产品方案](https://github.com/Jason-d-e/grounded-review/blob/main/product/PRD.zh-CN.md) |

**问题**：广告审核要说得出违反哪一条、是哪几个字违反的，而不只是给“通过 / 拒绝”。

**我做了什么**：我从官方原文整理了 32 条政策条款，写了带陷阱的留出集，做了能查条款、引原文、多轮改稿和复审的 Agent，并和单个提示词、违禁词表、开源审核模型比较；改稿建议从 v1 迭代到 v1.3；最后换成监管机构和法院定答案的真实广告。

**结果**：

- 留出集判对：单个提示词 191/192，Agent 187/192
- 真实广告（英国 ASA 裁决）：49/60 和 51/60
- 改稿字段写错：6/36 → 0/36（v1.3）

## 概况

审核广告的 Agent：读文案和图片里的字，在 32 条政策条款里查依据，给出放行或拒绝；每处违规附类别、条款、违规原话和条款原文，引文先过 evidence-check 的核对脚本才算数。广告主追问时，它写修改后的版本，再复审广告主自己改的版本。评测对比两组：把材料一次交给模型的单个提示词，和带工具的 Agent。

- **在作品集里的位置**：场景：判断类
- **和核心部件的关系**：每段广告引文和条款引文都交给 evidence-check 的核对脚本；不是逐字出自原文的引文在回答给出之前就被拦下。
- **用到的模型**：两组都用 claude-haiku-5-5（effort medium），同一份输出格式。对比组：违禁词表、CLIP、SigLIP 2、SafeGuard-VL-RL（本机运行）。

## 用途

- 给审核员一个带依据的初判：违反哪一条、哪几个字，审核员对照原文就能确认。
- 给广告主解释为什么被拒、怎么改，并复审改后的版本。
- 当作“带工具的 Agent 和单个提示词谁更好”的对照评测样例。

## 不适用的地方

- 不能代替平台的完整政策：政策库是 32 条的节选，TikTok 各市场的专门规则没有收。
- 不是线上流量的测量：留出集和难题集都是自己写的题，真实广告只有公开裁决的文字描述。
- 不判断证据本身真不真：广告里“经临床验证”这类说法，要看广告主的证据，模型看不到。

## 评测数据

### 留出集 v1（96 条自己写的广告）

中英各半的图文广告，含专门写来骗模型的“陷阱”（看着像违规、其实合规）。答案在写题时定好；跑之前冻结题目、代码和打分脚本的哈希。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-13 |
| 题目和答案 | 96 条广告，每组跑两遍，共 192 次判断 |
| 跑了几次 | 每组 2 遍；比例按两遍合并算，同一题两遍不独立，区间偏窄 |
| 模型和发送方式 | claude-haiku-5-5，普通接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md`（计划、预期、文件哈希） |

### 留出集 v1 的图片广告：不用付费接口的做法

留出集里的 57 条图片广告，只给图片；对比组都在本机跑一遍。SafeGuard-VL-RL 是冻结计划之后加的，没有写预期。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-13 |
| 题目和答案 | 57 张图 |
| 跑了几次 | 每种做法 1 遍 |
| 模型和发送方式 | 本机 CPU，不花钱 |

### 难题集（24 条）

长文案、短视频三格截图、暗示性说法；在留出集结果出来之后由同一作者写成，答案写题时定好，跑前冻结。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-14 |
| 题目和答案 | 24 条，每组 2 遍 |
| 跑了几次 | 每组 2 遍 |
| 模型和发送方式 | claude-haiku-5-5，批量接口（半价） |
| 跑前冻结 | `eval/PREREGISTRATION.md` 难题集一节 |

### 真实广告（英文）：英国广告标准局 30 份公开裁决

答案由监管机构定：裁决“违规”或“不违规”。模型读的是裁决里对广告的文字描述，不是广告本身；监管规则和本项目的政策库不完全一样。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-14 |
| 题目和答案 | 30 份裁决（7 份判不违规），每组 2 遍 |
| 跑了几次 | 每组 2 遍 |
| 模型和发送方式 | claude-haiku-5-5，批量接口（半价） |
| 跑前冻结 | `eval/PREREGISTRATION.md` 真实广告一节；题目原文不公开，只公开汇总 |

### 真实广告（中文）：16 个公开案例

12 个被市场监管部门处罚的案例，4 个被监管部门或法院认定合法的个案。被处罚的只保留监管部门引用的广告原话。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-14 |
| 题目和答案 | 16 个案例，每组 2 遍 |
| 跑了几次 | 每组 2 遍 |
| 模型和发送方式 | claude-haiku-5-5，批量接口（半价） |
| 跑前冻结 | `eval/PREREGISTRATION.md` 真实广告一节 |

### 多轮改稿 mt2：v1 对 v1.1（12 条新广告）

三轮对话：审核、给建议和改后版本、复审广告主自己改的版本。题目在改提示词之后新写，跑前冻结。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-13 |
| 题目和答案 | 12 条新广告，每个版本 2 遍，共 24 段对话 |
| 跑了几次 | 每个版本 2 遍 |
| 模型和发送方式 | claude-haiku-5-5，普通接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md` v1.1 一节 |

### 多轮改稿 mt3：v1.1 对 v1.2（12 条新广告）

检查“修改后的文案”字段有没有写错位置；v1.2 的做法是填错就退回重交一次。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-13 |
| 题目和答案 | 12 条新广告，每个版本 3 遍，共 36 段对话 |
| 跑了几次 | 每个版本 3 遍 |
| 模型和发送方式 | claude-haiku-5-5，普通接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md` v1.2 一节 |

### 多轮改稿 mt4：v1.1 对 v1.3（12 条新广告）

v1.3 让模型先填修改后的文案、再写说明；题目在 v1.3 写好之后新写，跑前冻结。中途因账户余额不足中断一次，用同样的命令接着跑，文件没变。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-14 |
| 题目和答案 | 12 条新广告，每个版本 3 遍，共 36 段对话 |
| 跑了几次 | 每个版本 3 遍 |
| 模型和发送方式 | claude-haiku-5-5，普通接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md` v1.3 一节 |

### 记忆评测：给 Agent 看过去确认过的判定（24 条新广告）

24 条虚构文字广告（中英各 12），每条都对应同一广告主的一条旧判定：一半应照旧判，另一半旧判定不该套用（已经改掉、加了限定、只是历史、换了说法、出现新违规）。记忆只读、不写入，按相似度找出旧判定附在审核请求里，不多调用模型。广告、旧判定和答案一起写好，跑前预注册。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-16 |
| 题目和答案 | 24 条广告，每组 3 遍 |
| 跑了几次 | 每组 3 遍，合并计算；同一题几遍不独立，区间偏窄 |
| 模型和发送方式 | claude-haiku-5-5，批量接口（半价） |
| 跑前冻结 | `eval/PREREGISTRATION.md` 记忆一节 |

## 指标和结果

每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。

### 留出集 v1（96 条自己写的广告）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 判对（单个提示词） | 191/192（99.5%，95% 区间 97.1–99.9%） | 越高越好 | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| 判对（Agent） | 187/192（97.4%，95% 区间 94.0–98.9%） | 越高越好 | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| 违规拦下（单个提示词） | 124/124（100.0%，95% 区间 97.0–100.0%） | 越高越好 | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| 违规拦下（Agent） | 124/124（100.0%，95% 区间 97.0–100.0%） | 越高越好 | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| 陷阱正确放行（单个提示词） | 59/60（98.3%，95% 区间 91.1–99.7%） | 越高越好 | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| 陷阱正确放行（Agent） | 55/60（91.7%，95% 区间 81.9–96.4%） | 越高越好 | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| 条款引对（单个提示词） | 129/129（100.0%，95% 区间 97.1–100.0%） | 越高越好 | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| 条款引对（Agent） | 129/129（100.0%，95% 区间 97.1–100.0%） | 越高越好 | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| 条款引文通过核对（单个提示词） | 224/225（99.6%，95% 区间 97.5–99.9%） | 越高越好 | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| 条款引文通过核对（Agent） | 200/200（100.0%，95% 区间 98.1–100.0%） | 越高越好 | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| 每条广告的费用（单个提示词） | 0.0010 美元 | 越低越好 | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |
| 每条广告的费用（Agent） | 0.0023 美元 | 越低越好 | [`grounded-review/eval/results/test-2026-11-13.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.summary.json) |

两组都接近满分，说明自己写的题已经到顶；差别在 Agent 多拒了陷阱。

### 留出集 v1 的图片广告：不用付费接口的做法

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 参照线：全部拒绝也能判对 | 37/57（64.9%，95% 区间 51.9–76.0%） | 只作说明 | [`grounded-review/eval/results/test-2026-11-13.images.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.images.summary.json) |
| SafeGuard-VL-RL 判对 | 49/57（86.0%，95% 区间 74.7–92.7%） | 越高越好 | [`grounded-review/eval/results/test-2026-11-13.images.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.images.summary.json) |
| CLIP 零样本判对 | 36/57（63.2%，95% 区间 50.2–74.5%） | 越高越好 | [`grounded-review/eval/results/test-2026-11-13.images.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.images.summary.json) |
| SigLIP 2 零样本判对 | 35/57（61.4%，95% 区间 48.4–72.9%） | 越高越好 | [`grounded-review/eval/results/test-2026-11-13.images.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.images.summary.json) |
| 违禁词表判对 | 27/57（47.4%，95% 区间 35.0–60.1%） | 越高越好 | [`grounded-review/eval/results/test-2026-11-13.images.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.images.summary.json) |
| SafeGuard-VL-RL 每张图耗时（中位数，CPU） | 178.3 秒 | 越低越好 | [`grounded-review/eval/results/test-2026-11-13.images.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/test-2026-11-13.images.summary.json) |

这几种做法都不给条款和原话；只有 SafeGuard-VL-RL 比“全部拒绝”好。

### 难题集（24 条）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 判对（单个提示词） | 48/48（100.0%，95% 区间 92.6–100.0%） | 越高越好 | [`grounded-review/eval/results/hard-2026-11-14.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/hard-2026-11-14.summary.json) |
| 判对（Agent） | 48/48（100.0%，95% 区间 92.6–100.0%） | 越高越好 | [`grounded-review/eval/results/hard-2026-11-14.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/hard-2026-11-14.summary.json) |

两组都全对：这套题只说明到顶了，分不出高低。

### 真实广告（英文）：英国广告标准局 30 份公开裁决

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 判对（单个提示词） | 49/60（81.7%，95% 区间 70.1–89.4%） | 越高越好 | [`grounded-review/eval/results/real-2026-11-14.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/real-2026-11-14.summary.json) |
| 判对（Agent） | 51/60（85.0%，95% 区间 73.9–91.9%） | 越高越好 | [`grounded-review/eval/results/real-2026-11-14.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/real-2026-11-14.summary.json) |
| 违规拦下（单个提示词） | 43/46（93.5%，95% 区间 82.5–97.8%） | 越高越好 | [`grounded-review/eval/results/real-2026-11-14.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/real-2026-11-14.summary.json) |
| 违规拦下（Agent） | 46/46（100.0%，95% 区间 92.3–100.0%） | 越高越好 | [`grounded-review/eval/results/real-2026-11-14.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/real-2026-11-14.summary.json) |
| 判“不违规”的广告正确放行（单个提示词） | 6/14（42.9%，95% 区间 21.4–67.4%） | 越高越好 | [`grounded-review/eval/results/real-2026-11-14.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/real-2026-11-14.summary.json) |
| 判“不违规”的广告正确放行（Agent） | 5/14（35.7%，95% 区间 16.3–61.2%） | 越高越好 | [`grounded-review/eval/results/real-2026-11-14.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/real-2026-11-14.summary.json) |

两组不再满分但仍接近；Agent 更严：违规抓得更全，也多拒了合法的。大部分错来自监管规则和政策库不同。

### 真实广告（中文）：16 个公开案例

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 判对（单个提示词） | 27/32（84.4%，95% 区间 68.2–93.1%） | 越高越好 | [`grounded-review/eval/results/real-zh-2026-11-14.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/real-zh-2026-11-14.summary.json) |
| 判对（Agent） | 26/32（81.2%，95% 区间 64.7–91.1%） | 越高越好 | [`grounded-review/eval/results/real-zh-2026-11-14.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/real-zh-2026-11-14.summary.json) |

### 多轮改稿 mt2：v1 对 v1.1（12 条新广告）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 改后版本留了模板占位符（v1） | 3/24（12.5%，95% 区间 4.3–31.0%） | 越低越好 | [`grounded-review/eval/results/multiturn-mt2-v1.jsonl`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/multiturn-mt2-v1.jsonl) |
| 改后版本留了模板占位符（v1.1） | 0/24（0.0%，95% 区间 0.0–13.8%） | 越低越好 | [`grounded-review/eval/results/multiturn-mt2-v1.1.jsonl`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/multiturn-mt2-v1.1.jsonl) |

### 多轮改稿 mt3：v1.1 对 v1.2（12 条新广告）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 最后采用的建议里字段写错（v1.1） | 4/36（11.1%，95% 区间 4.4–25.3%） | 越低越好 | [`grounded-review/eval/results/multiturn-mt3-v1.1.jsonl`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/multiturn-mt3-v1.1.jsonl) |
| 最后采用的建议里字段写错（v1.2） | 6/36（16.7%，95% 区间 7.9–31.9%） | 越低越好 | [`grounded-review/eval/results/multiturn-mt3-v1.2.jsonl`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/multiturn-mt3-v1.2.jsonl) |

退回重交没用：模型第二次照样写错，v1.2 不采用。

### 多轮改稿 mt4：v1.1 对 v1.3（12 条新广告）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 交上来的建议字段写错（v1.1） | 6/36（16.7%，95% 区间 7.9–31.9%） | 越低越好 | [`grounded-review/eval/results/multiturn-mt4-v1.1.jsonl`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/multiturn-mt4-v1.1.jsonl) |
| 交上来的建议字段写错（v1.3） | 0/36（0.0%，95% 区间 0.0–9.6%） | 越低越好 | [`grounded-review/eval/results/multiturn-mt4-v1.3.jsonl`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/multiturn-mt4-v1.3.jsonl) |
| 改后版本保住品牌和价格（v1.1） | 34/36（94.4%，95% 区间 81.9–98.5%） | 越高越好 | [`grounded-review/eval/results/multiturn-mt4-v1.1.jsonl`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/multiturn-mt4-v1.1.jsonl) |
| 改后版本保住品牌和价格（v1.3） | 36/36（100.0%，95% 区间 90.4–100.0%） | 越高越好 | [`grounded-review/eval/results/multiturn-mt4-v1.3.jsonl`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/multiturn-mt4-v1.3.jsonl) |
| 每段三轮对话的费用（v1.1） | 0.0069 美元（n=36） | 越低越好 | [`grounded-review/eval/results/multiturn-mt4-v1.1.jsonl`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/multiturn-mt4-v1.1.jsonl) |
| 每段三轮对话的费用（v1.3） | 0.0068 美元（n=36） | 越低越好 | [`grounded-review/eval/results/multiturn-mt4-v1.3.jsonl`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/multiturn-mt4-v1.3.jsonl) |

### 记忆评测：给 Agent 看过去确认过的判定（24 条新广告）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 判对（不带记忆） | 69/72（95.8%，95% 区间 88.5–98.6%） | 越高越好 | [`grounded-review/eval/results/memory-2026-11-16.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/memory-2026-11-16.summary.json) |
| 判对（带记忆） | 72/72（100.0%，95% 区间 94.9–100.0%） | 越高越好 | [`grounded-review/eval/results/memory-2026-11-16.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/memory-2026-11-16.summary.json) |
| 旧判定不该套用时照搬了旧判定（带记忆） | 0/36（0.0%，95% 区间 0.0–9.6%） | 越低越好 | [`grounded-review/eval/results/memory-2026-11-16.report.md`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/memory-2026-11-16.report.md) |
| 带记忆的一次审核费用，是不带记忆的 | 0.89 倍 | 越低越好 | [`grounded-review/eval/results/memory-2026-11-16.summary.json`](https://github.com/Jason-d-e/grounded-review/blob/main/eval/results/memory-2026-11-16.summary.json) |

带记忆全对，不带记忆的错都出在同一条广告上，所以这是机制演示，不是比例；旧判定不该套用的广告上，没有一次照搬旧判定。

## 评分器校准

- 判对、拦截、条款是否引对都是按事先定好的答案用脚本算的，没有用评分器。
- 多轮任务里“改后的版本能不能通过”由另一次单个提示词复审来判；这个复审没有单独校准过，参考依据是同一组在留出集上的判对 191/192。

## 局限和失败案例

- 自己写的题到顶了：留出集两组都接近满分，难题集两组都全对，分不出 Agent 和单个提示词谁更好。
  - 建议：要分高低，用不是自己写的题：更多真实裁决、更长的视频，或模型没见过的规则。
- Agent 比单个提示词更容易误拒陷阱：留出集陷阱放行 55/60，单个提示词 59/60；Agent 的费用也更高。
  - 建议：合规但像违规的广告（送达保证、文化遗产名录、定价）要给 Agent 补正面例子或条款说明。
- 真实广告上的错大多来自规则不同：英国判不违规的酒类广告，按 TikTok 政策要写酒精度，两组都拒了。
  - 建议：上线时政策库要和执行规则的那一方一致；跨市场时按市场分库。
- 多轮改稿的题只有 12 条短文字广告、一个模型；相差一两段对话属于噪声。
  - 建议：下一版改稿提示词上线前，用图片广告和更长的文案再测一轮。
- 开源审核模型一张图要几分钟，不给条款和原话；SafeGuard-VL-RL 每张图约 178.3 秒。
  - 建议：开源模型适合当便宜的第一道筛子，拿不准的再交给带依据的审核。
- 记忆评测的差别只来自一条广告，题目是自己写的短文字广告，旧判定库也是一起写的。
  - 建议：上线前在真实的历史判定和更长的广告上再测；记忆保持只读，写入要经过人工确认。

## 版本

- **1.0**（2026-11-15）第一张卡，照公开仓库 grounded-review 的内容写：公开版没有 Granite Guardian 在真实广告上的结果，这里也不放。两个文字审核模型的对比只有报告里的表格、没有汇总数据文件，所以没有收进卡片。
- **1.1**（2026-11-15）开头加了时间、团队、技术、链接和“问题 / 我做了什么 / 结果”，照作品集案例页的写法；评测部分不变。
- **1.2**（2026-11-16）加了演示页和产品方案的链接，加了记忆评测。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。
