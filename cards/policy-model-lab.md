# 审核模型实验：评测卡

> 卡片版本 1.0 · 数据截至 2026-11-18 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-17 – 2026-11-18 | Liang Liyuan | Python、PyTorch、LoRA 微调（Qwen3）、本机视觉语言模型（Qwen3.5、Qwen3-VL）、SigLIP 2、mmBERT、OCR、批量接口 | [代码和报告](https://github.com/llia0031-dotcom/policy-model-lab) |

**问题**：按广告政策审核短视频广告，模型要看到什么才够；用合成广告训练的小模型能不能胜任。

**我做了什么**：我在一台笔记本显卡上按预注册的方案做了三组实验：一条短视频广告要让模型看到什么（文案、封面、抽帧、整段视频、帧上识别的文字）才审得准；用合成广告微调的小模型能不能比得上大模型；再拿 300 条另一平台的真实短视频核对。最后对照近一年的研究写了一份调研报告。

**结果**：

- 视频广告：claude-haiku-5-5 看 16 帧判对 86/96，违规全抓到（64/64）；只给文案时违规只抓到 25/64
- 本机 Qwen3.5-4B 只看 16 帧上识别出的文字判对 80/96，和看整段视频（80/96）一样，每条只要 2.4 秒，看视频要 19.2 秒
- 用合成广告微调的 Qwen3-1.7B 在有据审核的测试题上判对 133/168，和 claude-haiku-5-5（138/168）分不出高下（配对差 -3.0 个百分点）

## 概况

按广告政策审核短视频广告的三组实验，都在一台笔记本显卡上跑，方案和预测跑前预注册。第一组比较同一段广告给模型看文案、封面、抽帧、整段视频或帧上识别出的文字时审得准不准；第二组用合成广告微调小模型，在有据审核的测试题、视频文字和真实案例上和大模型比；第三组拿另一平台 300 条真实短视频核对“违不违规”。真实视频和真实案例只公开汇总数字。

- **在作品集里的位置**：场景：判断类
- **和核心部件的关系**：第二组用有据审核的测试题和政策类别做测试集；结论接到有据标注流水线的分流环节上。
- **用到的模型**：大模型用 claude-haiku-5-5（批量接口）；本机跑 Qwen3.5-4B、Qwen3-VL-2B、SigLIP 2、mmBERT 和 LoRA 微调的 Qwen3-0.6B、Qwen3-1.7B。

## 用途

- 审核团队选输入和模型：视频广告先读帧上的字，再决定要不要送更贵的模型看画面。
- 上线前的检查方法：同一套题上比较给模型看的东西、比较大小模型，按事先写好的预测逐条对照。

## 不适用的地方

- 视频广告是合成的，答案写题时定好；真实视频来自另一个平台，标准和本项目的政策库不同。
- 真实视频和真实案例只公开汇总数字，不放原文和画面。
- Qwen3-VL-2B 跑的时候显卡上还有别的程序，它的用时不拿来比较。

## 评测数据

### 视频广告：给模型看什么（96 段）

96 段合成视频广告（中英各一半），64 段违规、32 段合规（其中一部分是看起来像违规的陷阱）；答案写题时定好。同一段广告分别给文案、封面、抽 8 帧或 16 帧、整段视频、帧上识别出的文字。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-17 |
| 题目和答案 | 96 段视频 |
| 跑了几次 | 每种看法 1 遍 |
| 模型和发送方式 | claude-haiku-5-5 走批量接口；本机模型在一台笔记本显卡上跑 |
| 跑前冻结 | `eval/PREREGISTRATION.md` |

### 合成广告微调小模型

用合成广告训练，测试集没训练过：有据审核的测试题（168 个判断）、视频广告的文字、46 个真实案例（只公开汇总）和合成验证集。和不微调的同一模型、claude-haiku-5-5、mmBERT 比较；配对差按 4,000 次自助重抽样给区间。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-17 |
| 题目和答案 | 有据审核的测试题 168 个判断；真实案例 46 个 |
| 跑了几次 | 每个模型 1 遍 |
| 模型和发送方式 | Qwen3-1.7B 加 LoRA，在一台笔记本显卡上训练；claude-haiku-5-5 走批量接口 |
| 跑前冻结 | `eval/PREREGISTRATION.md` |

### 另一平台的真实短视频：违不违规（300 条，只公开汇总）

KuaiMod 测试集 1,000 条里按固定种子抽 300 条（173 条正常、127 条违规），问“这条视频违不违反平台的社区规范”。本机模型看的是缩小的帧，claude-haiku-5-5 收到的是原图。不放画面、标题和原文。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-17 |
| 题目和答案 | 300 条视频 |
| 跑了几次 | 每个模型 1 遍 |
| 模型和发送方式 | claude-haiku-5-5 走批量接口；Qwen3.5-4B 在本机 |
| 跑前冻结 | `eval/PREREGISTRATION.md` |

## 指标和结果

每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。

### 视频广告：给模型看什么（96 段）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 只给文案：违规抓到（claude-haiku-5-5） | 25/64（39.1%，95% 区间 28.1–51.3%） | 越高越好 | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| 看 16 帧：判对（claude-haiku-5-5） | 86/96（89.6%，95% 区间 81.9–94.2%） | 越高越好 | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| 看 16 帧：违规抓到（claude-haiku-5-5） | 64/64（100.0%，95% 区间 94.3–100.0%） | 越高越好 | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| 看整段视频：判对（Qwen3.5-4B，本机） | 80/96（83.3%，95% 区间 74.6–89.5%） | 越高越好 | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| 只读 16 帧上的文字：判对（Qwen3.5-4B，本机） | 80/96（83.3%，95% 区间 74.6–89.5%） | 越高越好 | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| 看整段视频：每条用时中位数（Qwen3.5-4B） | 19.2 秒 | 越低越好 | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| 只读帧上的文字：每条用时中位数（Qwen3.5-4B） | 2.4 秒 | 越低越好 | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| 看 8 帧：合规广告被错拒（Qwen3-VL-2B） | 28/32（87.5%，95% 区间 71.9–95.0%） | 越低越好 | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |
| 看 16 帧：判对（SigLIP 2） | 62/96（64.6%，95% 区间 54.6–73.4%） | 越高越好 | [`policy-model-lab/results/video_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/video_summary.md) |

只给文案时违规大多漏掉；看的帧越多抓得越全。本机的 Qwen3.5-4B 只读帧上识别出的文字，和看整段视频一样准，快得多，显存也少。

### 合成广告微调小模型

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 有据审核的测试题：判对（Qwen3-1.7B + LoRA） | 133/168（79.2%，95% 区间 72.4–84.6%） | 越高越好 | [`policy-model-lab/results/text_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_summary.md) |
| 有据审核的测试题：判对（claude-haiku-5-5） | 138/168（82.1%，95% 区间 75.7–87.2%） | 越高越好 | [`policy-model-lab/results/text_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_summary.md) |
| 配对差：1.7B + LoRA 减 claude-haiku-5-5（百分点） | -3.0 | 只作说明 | [`policy-model-lab/results/text_paired.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_paired.md) |
| 配对差：微调减不微调（百分点） | 11.3 | 越高越好 | [`policy-model-lab/results/text_paired.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_paired.md) |
| 真实案例：判对（Qwen3-1.7B + LoRA） | 38/46（82.6%，95% 区间 69.3–90.9%） | 越高越好 | [`policy-model-lab/results/text_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_summary.md) |
| 真实案例：判对（claude-haiku-5-5） | 33/46（71.7%，95% 区间 57.5–82.7%） | 越高越好 | [`policy-model-lab/results/text_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_summary.md) |
| 合成验证集：判对（mmBERT） | 173/191（90.6%，95% 区间 85.6–94.0%） | 越高越好 | [`policy-model-lab/results/text_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_summary.md) |
| 真实案例：判对（mmBERT） | 25/46（54.3%，95% 区间 40.2–67.8%） | 越高越好 | [`policy-model-lab/results/text_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/text_summary.md) |
| 训练用时（分钟，Qwen3-1.7B + LoRA） | 46.2 | 只作说明 | [`policy-model-lab/results/train/qwen3-1.7b-lora.json`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/train/qwen3-1.7b-lora.json) |

微调后的 1.7B 在有据审核的测试题上和 claude-haiku-5-5 分不出高下，比不微调高一截；离合成数据越远掉得越多，mmBERT 在真实案例上只剩一半左右。

### 另一平台的真实短视频：违不违规（300 条，只公开汇总）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 看画面加文字：判对（Qwen3.5-4B，本机） | 225/300（75.0%，95% 区间 69.8–79.6%） | 越高越好 | [`policy-model-lab/results/kuaimod_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/kuaimod_summary.md) |
| 看画面加文字：判对（claude-haiku-5-5） | 214/300（71.3%，95% 区间 66.0–76.2%） | 越高越好 | [`policy-model-lab/results/kuaimod_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/kuaimod_summary.md) |
| 正常视频被标成违规（Qwen3.5-4B） | 45/173（26.0%，95% 区间 20.0–33.0%） | 越低越好 | [`policy-model-lab/results/kuaimod_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/kuaimod_summary.md) |
| 正常视频被标成违规（claude-haiku-5-5） | 70/173（40.5%，95% 区间 33.4–47.9%） | 越低越好 | [`policy-model-lab/results/kuaimod_summary.md`](https://github.com/llia0031-dotcom/policy-model-lab/blob/main/results/kuaimod_summary.md) |

看画面加文字时，本机 Qwen3.5-4B 判对稍多，claude-haiku-5-5 把更多正常视频标成违规；两者收到的画面大小不同，标准也来自另一个平台，只作参考。

## 评分器校准

- 没有用评分器：判对按写题时定好的答案（真实视频和真实案例按原来的标注）用脚本算。

## 局限和失败案例

- 视频广告和训练数据都是合成的；离合成数据越远，微调模型掉得越多（mmBERT 在真实案例上 25/46）。
  - 建议：上线前用平台自己的历史审核结果做一批题再测，按需要补真实数据再训练。
- 真实短视频来自另一个平台，标准和本项目的政策库不同；两组模型收到的画面大小也不同。
  - 建议：换到目标平台的数据和标准上，用同样大小的输入重测。
- 每个模型每题只跑一遍；有些差别落在区间里，分不出高下。
  - 建议：差别小的那几组加题、多跑几遍再定。

## 版本

- **1.0**（2026-11-18）第一张卡，照公开仓库 policy-model-lab 的结果文件写。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。

第三方数据、模型和代码的来源与许可，见[项目仓库](https://github.com/llia0031-dotcom/policy-model-lab)里的说明。
