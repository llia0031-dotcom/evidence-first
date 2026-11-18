# Agent 评测台：评测卡

> 卡片版本 1.0 · 数据截至 2026-11-18 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-18 | Liang Liyuan | Python、批量接口、过程记录和逐步规则检查、evidence-check、agentevals、Inspect AI 日志 | [代码和报告](https://github.com/llia0031-dotcom/agent-trace-eval) |

**问题**：会调工具的 Agent 只看最后答案对不对不够：它每一步做了什么，上线前的检查能拦住哪些错，失败从哪一步开始，改了以后会不会把别处弄坏。

**我做了什么**：我给三个已有的、会调工具的 Agent 新写了 46 道题，每题跑三次，把每一步记下来；评分按理解、规划、工具调用、知识引用、结果五个阶段写成规则，再加上线前的自动关卡和失败归因表。看完基线后，跑之前先写下两个修复的预测，再在整组题上做回归重测。

**结果**：

- 基线任务成功：广告审核 53/60、经营分析 47/54、创作流程 21/24；三次都成功 80%、72%、88%
- 关卡管得住格式，管不住判断：基线失败 17 次，关卡拦下 1 次、放过 16 次
- 装 Skill 和不装：创作流程成功 21/24 对 8/24（符号检验 p = 0.031）
- 预注册的修复：审核轮误调建议工具 36/60 → 0/60；门店下线定位到商家 3/6 → 6/6，回归重测查出另一道题变差

## 概况

评一个会调工具的 Agent 每一步做了什么，不只看最后的答案。三个已有的 Agent 照原样运行（有据审核、有据经营分析、创作者 Skill），46 道新题：广告审核 20、经营分析 18、创作流程 8，从一步就能答的题到多轮对话、要拿捏分寸的题分成三档，每题三次。题目和答案在出题时定好，题目、答案、评分代码和配置跑前记下指纹。评分是对过程记录的规则检查，分五个阶段；任务成功只看结果检查，过程检查用来说明它怎么走到这一步。另有上线前的自动关卡（引文核对、数字核对、Skill 自带的检查脚本），关卡拦下的要人确认；失败归因记下每个失败从哪一步开始、为什么、怎么改。

- **在作品集里的位置**：运营层
- **和核心部件的关系**：引文和数字用 evidence-check 的脚本核对；评的是有据审核、有据经营分析和创作者 Skill 三个项目的 Agent，不改它们的代码，补的是它们各自评测没量的过程和关卡。
- **用到的模型**：三个 Agent 和判官都用 claude-haiku-5-5（effort medium）；基线第一次试验走普通接口量时延，第二、三次和修复、对照都走批量接口。

## 用途

- 给一个会调工具的 Agent 做上线前评测：按步骤看它在哪一步出错，哪些错关卡拦得住、哪些要靠人。
- 改提示词或规则之前：先写下预测，再在整组题上回归重测，确认修好的地方没有把别处弄坏。

## 不适用的地方

- 不证明这三个 Agent 在真实业务里的表现；题目是为这套评测新写的合成或虚构题。
- 修复只在写它的那组题上验证过，能不能推广到新题还要新题来测。

## 评测数据

### 基线：三个 Agent 照原样运行

广告审核（中英文广告，含三轮对话：审核、给修改建议、再审新版本）、经营分析（合成的本地生活平台数据，埋好的原因、平静的周、节假日、只问一件事的请求）、创作流程（同一段对话里热点选题、拆分镜、对字幕）。答案在出题时定好，用各 Agent 项目自己的校验和打分代码。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 46 道题：广告审核 20、经营分析 18、创作流程 8 |
| 跑了几次 | 每题 3 次 |
| 模型和发送方式 | claude-haiku-5-5，effort medium；第一次走普通接口，第二、三次走批量接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md`、`eval/frozen.json` |

### 上线前的自动关卡和失败归因（基线）

关卡是上线前会跑的检查：引文核对、数字核对、Skill 自带的检查脚本，拦下的要人确认。每个失败的试验，最早没过的那条检查定阶段；原因来自每条检查的规则，或读完过程记录后写下的说明。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 基线 138 次试验里失败的那些 |
| 跑了几次 | 每题 3 次 |
| 模型和发送方式 | claude-haiku-5-5，effort medium |
| 跑前冻结 | `eval/PREREGISTRATION.md` |

### 装 Skill 和不装（创作流程）

同样的 8 道创作流程题，一组装上三个创作者 Skill 和它们的检查工具，一组不装；按题配对，用精确符号检验。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 8 道题 |
| 跑了几次 | 每题 3 次 |
| 模型和发送方式 | claude-haiku-5-5，effort medium，批量接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md` |

### 预注册的两个修复和回归重测

看完基线后，两个修复各在 Agent 的说明里加两条规则，跑之前写下预测和采用规则。广告审核：一句话只记一处违规、归到最具体的类别；每个请求只用它要的那个收尾工具。经营分析：门店下线的原因定位到商家；只把监控报警的切片当原因。各在整组题上重跑三次，这就是回归测试。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 广告审核 20 道；经营分析 18 道 |
| 跑了几次 | 每题 3 次 |
| 模型和发送方式 | claude-haiku-5-5，effort medium，批量接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md`（变更记录，2026-11-18 20:48）、`eval/frozen-changes.json` |

### 判官校准和总花费

规则查不了的 7 条标准，按写好的指南每个答案判两遍；先在 12 条写好结论的校准答案上检验，再判基线的答案。判断项不影响任务成功。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 校准答案 12 条；基线答案 88 条 |
| 跑了几次 | 每个答案判 2 遍 |
| 模型和发送方式 | claude-haiku-5-5，effort medium |
| 跑前冻结 | `eval/PREREGISTRATION.md` |

## 指标和结果

每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。

### 基线：三个 Agent 照原样运行

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 广告审核：任务成功 | 53/60（88.3%，95% 区间 77.8–94.2%） | 越高越好 | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| 经营分析：任务成功 | 47/54（87.0%，95% 区间 75.6–93.6%） | 越高越好 | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| 创作流程：任务成功 | 21/24（87.5%，95% 区间 69.0–95.7%） | 越高越好 | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| 广告审核：三次都成功（pass^3） | 80% | 越高越好 | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| 经营分析：三次都成功（pass^3） | 72% | 越高越好 | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| 创作流程：三次都成功（pass^3） | 88% | 越高越好 | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| 广告审核：工具调用正确 | 351/387（90.7%，95% 区间 87.4–93.2%） | 越高越好 | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| 广告审核：审核那一轮还调了建议工具（被运行框架拒掉，没有影响任务成功） | 36/60（60.0%，95% 区间 47.4–71.4%） | 越低越好 | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| 经营分析：被数字核对拦下、要人确认 | 9/54（16.7%，95% 区间 9.0–28.7%） | 只作说明 | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |

三类任务的成功率接近，失败大多出在结果这一步：同一句话贴了两个类别、门店下线定位得太粗、把普通产品参数判成违规。过程上的毛病在答对的试验里也常见：广告审核多数试验在审核那一轮还顺手调了建议工具。

### 上线前的自动关卡和失败归因（基线）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 基线失败的试验 | 17 | 越低越好 | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| 失败里被关卡拦下的 | 1/17（5.9%，95% 区间 1.0–27.0%） | 越高越好 | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| 失败里关卡放过去的 | 16/17（94.1%，95% 区间 73.0–99.0%） | 越低越好 | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| 失败里属于题目或答案本身的问题 | 5/17（29.4%，95% 区间 13.3–53.1%） | 只作说明 | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |

关卡几乎什么也没拦下：广告审核每次失败引的原话和条款都是真的，错在结论；经营分析的数字核对拦下的多是对的报告，反而加了复核量。失败里有一部分是题目或答案本身的问题，照实留在分数里并写明原因。

### 装 Skill 和不装（创作流程）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 不装 Skill：任务成功 | 8/24（33.3%，95% 区间 18.0–53.3%） | 越高越好 | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| 按题配对的精确符号检验 p 值 | 0.031 | 只作说明 | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| 装 Skill 每次试验的费用（按标准价）是不装的几倍 | 2.8 倍 | 只作说明 | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |

不装 Skill 时，分镜凭感觉定时长、字幕把临时改说的话改回稿子，还给致死火灾出了营销选题，而且引的都是真实、最新的网页，来源核对照样放过：这类政策上的错，形式检查拦不住。

### 预注册的两个修复和回归重测

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 修复后：审核那一轮还调了建议工具 | 0/60（0.0%，95% 区间 0.0–6.0%） | 越低越好 | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| 修复后：每次试验的输出 token 变化 | -15% | 越低越好 | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| 广告审核修复后：任务成功 | 54/60（90.0%，95% 区间 79.9–95.3%） | 越高越好 | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| 广告审核修复后：工具调用正确 | 345/345（100.0%，95% 区间 98.9–100.0%） | 越高越好 | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| 修复前：门店下线定位到商家 | 3/6（50.0%，95% 区间 18.8–81.2%） | 越高越好 | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| 修复后：门店下线定位到商家 | 6/6（100.0%，95% 区间 61.0–100.0%） | 越高越好 | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| 经营分析修复后：任务成功 | 48/54（88.9%，95% 区间 77.8–94.8%） | 越高越好 | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| 经营分析修复后：三次都成功（pass^3） | 83% | 越高越好 | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |
| 经营分析修复后：按题看变差的题数 | 2 | 越低越好 | [`agent-trace-eval/eval/results/summary.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/summary.md) |

两个修复都按事先的规则采用。广告审核的预测全部成立，提升在过程上，任务成功没测出差别。经营分析门店定位全对，但“只认报警切片”那条没管住，还让一道退款题被定位到某一家连锁、比实际更细：照失败写的规则会带出副作用，下一步把两条规则从提示词搬进代码。

### 判官校准和总花费

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 校准答案：和写好的结论一致（更正后） | 53/56（94.6%，95% 区间 85.4–98.2%） | 越高越好 | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| 校准答案：和写好的结论一致（原样） | 51/56（91.1%，95% 区间 80.7–96.1%） | 只作说明 | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| 基线答案：两遍判断一致 | 182/194（93.8%，95% 区间 89.5–96.4%） | 越高越好 | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |
| 全部花费（所有运行、判官和试跑） | 1.48 美元 | 越低越好 | [`agent-trace-eval/eval/results/facts.md`](https://github.com/llia0031-dotcom/agent-trace-eval/blob/main/eval/results/facts.md) |

两遍判断大多一致。判断项补出了规则看不见的两件事：改好的广告新加了需要证明的卖点词，规则检查却通过了；平静的周里“继续观察”被判不合格，是指南本身没写到这种情况，不是 Agent 的问题。

## 评分器校准

- 规则查不了的 7 条标准（建议是否讲清、建议是否从原因出发、选题是否贴合账号等）按写好的指南判两遍；判官用 claude-haiku-5-5，和被测的三个 Agent 是同一个模型。
- 校准：12 条写好结论的答案上一致 53/56（原样 51/56，其中一条写好的结论本身错了，已更正）；基线上两遍判断一致 182/194。判断项不影响任务成功；没有另做人工评分。

## 局限和失败案例

- 每题只跑三次，题目是为这套评测新写的，区间很宽：经营分析任务成功 47/54（87.0%，95% 区间 75.6–93.6%）；按题比较只靠三次试验。
  - 建议：重要的结论多跑几次、加新题再确认。
- 题目是合成或虚构的，出自运行它的同一个项目；有两道题的题目或答案本身有问题，照实留在分数里。
  - 建议：给那两道题改名或重建后重跑，并用真实业务里已有结论的样本另建一组题。
- 判官和被测的 Agent 是同一个模型，指南在平静的周上有漏洞；判断项不影响任务成功，也没有另做人工评分。
  - 建议：补上指南的漏洞，换一个不同的模型做第二判官对照。
- 两个修复只在写它们的那组题上验证过；时延只来自基线第一次走普通接口的试验，每题一次。
  - 建议：用新题检验修复能不能推广，再把规则搬进代码后重测退款类的题。

## 版本

- **1.0**（2026-11-18）第一张卡，照公开仓库 agent-trace-eval 的结果文件写。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。

第三方数据、模型和代码的来源与许可，见[项目仓库](https://github.com/llia0031-dotcom/agent-trace-eval)里的说明。
