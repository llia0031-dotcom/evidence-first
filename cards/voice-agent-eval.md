# 实时语音 Agent 体验评测：评测卡

> 卡片版本 1.2 · 数据截至 2026-11-15 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-13 – 2026-11-15 | Liang Liyuan | Python、SenseVoice、本机 MCP 工具、FireRedChat pVAD、Claude Haiku 5.5 | [代码和报告](https://github.com/llia0031-dotcom/voice-agent-eval) |

**问题**：语音助手在用户停顿、插话、说“嗯”、背景有人说话时还能不能把事办对，体验用时延、打断、误停的数字来衡量。

**我做了什么**：我写了 42 段带停顿、插话、附和和噪声的对话、事先定好答案，搭了一条本机串联的语音 Agent 做基线；然后一项一项试改进，每项先写补充预注册再跑，最后把有效的合在一起。

**结果**：

- 严格通过：基线（开思考）61/84，四项改进合在一起 62/84；纯文字对照 82/84
- 背景人声时开口：20.4 秒 → 4.56 秒（只听主说话人）
- 真插话停下 16/16，停下时延 0.25 秒

## 概况

测一条串联的实时语音 Agent（静音检测 → 语音识别 → 带工具的模型 → 语音合成）在 42 段写好的中英对话里的表现：停顿、插话、附和词、噪声、工具调用。每段对话的答案在写题时定好，跑前冻结题目、音频和打分脚本。先测三种基线设置和纯文字对照，再在同一套题上一项一项试改进：附和不算打断、先暂停再确认、第一段语音切短、删除前先确认、只听主说话人，最后把有效的合在一起。

- **在作品集里的位置**：场景：交互类
- **和核心部件的关系**：借用 evidence-check 的预注册做法；离线另查了“说出口的确认和工具结果对不对得上”。
- **用到的模型**：claude-haiku-5-5（effort low，普通流式接口：调用都在实时回路里，不适用批量接口）；语音识别 SenseVoice；只听主说话人用 FireRedChat pVAD。

## 用途

- 比较实时语音 Agent 的设置：哪一种在停顿、插话、附和、噪声下更稳，代价是多少时延。
- 改一个设置之前，先在同一套题上回放，看有没有把原来对的改坏。

## 不适用的地方

- 不是端到端语音模型的评测：没有和端到端实时语音模型对比。
- 不代表真人用户：用户语音是合成的，时间是模拟的，回声消除按理想情况处理。

## 评测数据

### 主评测：三种基线设置和纯文字对照（42 段对话）

42 段对话：任务、停顿、插话、附和、粉红噪声、背景人声。答案写题时定好；题目、音频清单、打分脚本跑前冻结。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-13 |
| 题目和答案 | 42 段对话，每种设置 2 遍，共 84 段 |
| 跑了几次 | 每种设置 2 遍，合并计算；同一题两遍不独立，区间偏窄 |
| 模型和发送方式 | claude-haiku-5-5，普通流式接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md`（计划、预期、文件哈希） |

### 逐项改进（同一套 42 段对话）

题目、音频和打分脚本不变；每项改进跑前写一份补充预注册（改了什么、预期、文件哈希）。下表只列被采用的两项和合在一起的设置，其余各项的结果在项目报告第 6 节。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-14 |
| 题目和答案 | 42 段对话，每种设置 2 遍 |
| 跑了几次 | 每种设置 2 遍，合并计算 |
| 模型和发送方式 | claude-haiku-5-5，普通流式接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md` 的补充一到补充十一 |

## 指标和结果

每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。

### 主评测：三种基线设置和纯文字对照（42 段对话）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 纯文字对照：严格通过 | 82/84（97.6%，95% 区间 91.7–99.3%） | 只作说明 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 静音检测基线（关思考）：严格通过 | 59/84（70.2%，95% 区间 59.8–79.0%） | 越高越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 静音检测基线（开思考）：严格通过 | 61/84（72.6%，95% 区间 62.3–81.0%） | 越高越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 关思考：说完到开口（干净的任务题） | 2.94 秒（中位数，n=32，95% 区间 2.76–3.14） | 越低越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 开思考：说完到开口（干净的任务题） | 3.95 秒（中位数，n=32，95% 区间 3.49–4.66） | 越低越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 开思考：真插话时停下 | 16/16（100.0%，95% 区间 80.6–100.0%） | 越高越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 开思考：用户只说“嗯”“好的”时继续说 | 0/8（0.0%，95% 区间 0.0–32.4%） | 越高越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 关思考时把推理说出口 | 23/84（27.4%，95% 区间 19.0–37.7%） | 越低越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 开思考：背景人声题说完到开口 | 20.4 秒（中位数，n=8，95% 区间 19.1–22.5） | 越低越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |

### 逐项改进（同一套 42 段对话）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 只听主说话人：严格通过 | 63/84（75.0%，95% 区间 64.8–83.0%） | 越高越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 只听主说话人：背景人声题说完到开口 | 4.56 秒（中位数，n=8，95% 区间 2.97–5.69） | 越低越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 先暂停、确认是真插话再取消：严格通过（按原规则暂停也算停下，所以附和题仍记为没通过） | 59/84（70.2%，95% 区间 59.8–79.0%） | 越高越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 四项合在一起：严格通过 | 62/84（73.8%，95% 区间 63.5–82.0%） | 越高越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 四项合在一起：说完到开口（干净的任务题） | 3.83 秒（中位数，n=32，95% 区间 3.38–4.12） | 越低越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 四项合在一起：真插话时停下 | 16/16（100.0%，95% 区间 80.6–100.0%） | 越高越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 四项合在一起：插话到停下 | 0.25 秒（中位数，n=16，95% 区间 0.25–0.28） | 越低越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 附和不算打断：用户只说“嗯”“好的”时继续说 | 4/8（50.0%，95% 区间 21.5–78.5%） | 越高越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |
| 再固定识别语言：用户只说“嗯”“好的”时继续说 | 4/8（50.0%，95% 区间 21.5–78.5%） | 越高越好 | [`voice-agent-eval/eval/results/run1/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run1/scores.json)<br>[`voice-agent-eval/eval/results/run2/scores.json`](https://github.com/llia0031-dotcom/voice-agent-eval/blob/main/eval/results/run2/scores.json) |

四项合在一起是测过最好的设置；剩下的附和问题光看识别出的文字分不出来，得看声音本身。

## 评分器校准

- 没有用评分器：打分是冻结的规则脚本，脚本带 6 条答案已知的自检对话，每次运行先过自检。
- 推理有没有被说出口，用固定的规则匹配。

## 局限和失败案例

- 用户语音是合成的，时间是模拟的；42 段对话每种设置只跑两遍，相差一两段属于噪声。
  - 建议：上线前用真人录音（例如公开的对话语音数据）重跑，并在真实网络下测时延。
- “嗯嗯”这类附和仍会打断：识别器把它听成别的字，光看识别出的文字分不出附和和短插话。
  - 建议：用看声音本身的附和检测；现成的声学附和模型离线试过，没达到事先定的标准，所以没接进来。
- 没有和端到端实时语音模型比较。
  - 建议：接上一个有免费额度的端到端模型，用同一套题和同一个打分脚本比较。

## 版本

- **1.0**（2026-11-15）第一张卡，项目未公开。
- **1.1**（2026-11-15）开头加了时间、团队、技术、链接和“问题 / 我做了什么 / 结果”，照作品集案例页的写法；评测部分不变。
- **1.2**（2026-11-16）项目已公开：加上代码和报告的链接；数字的来源文件链到公开仓库里的同一份。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。
