# 标注 Agent 工具箱：评测卡

> 卡片版本 1.0 · 数据截至 2026-11-18 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-18 | Liang Liyuan | Python、批量接口、BM25 检索、配对自助检验、五个 Agent Skill（只用标准库） | [代码和报告](https://github.com/llia0031-dotcom/labelling-agent-kit) · [结果查看页](https://llia0031-dotcom.github.io/labelling-agent-kit/) |

**问题**：标注 Agent 怎么设计标得最好，错在哪些标签、哪类样本上，为什么错，改了以后在新样本上还成不成立。

**我做了什么**：我做了一个通用的内容标注 Agent：换一个放规则和案例的文件夹就能接新任务。用两个任务、五种做法做预注册的 A/B 对照，算每个标签的精确率和召回率、混淆和切片；把最好的做法的失败样本归到五类根因，按根因改出第二版，再在没用过的测试集上检验。常用的分析做成了五个 Agent Skill。

**结果**：

- 测试集 A 微平均 F1，短提示词 → 完整 Agent：广告 0.768 → 0.971，点评 0.715 → 0.824
- 形似违规其实合规的广告：短提示词打了标签 12/32，完整 Agent 0/32
- 按根因改的第二版，在没用过的测试集 B 上：点评 +0.018 [+0.005, +0.031]，采用；广告 +0.021 [+0.000, +0.048]，区间碰到 0，不采用

## 概况

一个换一套规则和案例就能接新任务的内容标注 Agent，配一整套用证据调它的工具：预注册的 A/B 对照、每个标签的精确率和召回率（带区间）、混淆和切片、失败样本根因表，以及按根因改版后在没用过的样本上验证。流程是：先检索相似案例，再用规则和案例工具标注，代码负责规则门（没读规则就给的标签，补发规则）、原话修正和自查。两个任务：中英文广告政策标签（每种语言 7 类，答案在写广告时定好），和公开数据集 ASAP 的餐厅点评 18 个方面（标签是数据集自带的）。五种做法从短提示词到“查规则 + 检索案例 + 自查”逐步加，点评另比较真实、合成和一半一半三种案例库。方案、假设和冻结文件跑前写好；最好的做法的失败样本，每个错误判断独立归因两次；按根因改出第二版，冻结后才在测试集 B 上跑。

- **在作品集里的位置**：运营层
- **和核心部件的关系**：广告任务的题目和规则来自有据审核和审核模型实验公开的数据；有据标注流水线负责把 Agent 跑成每天的流程，这个工具箱负责把它调准。
- **用到的模型**：claude-haiku-5-5（effort low，批量接口），每条样本每种做法跑一次。

## 用途

- 接一个新的标注任务：写好规则和案例文件夹，用同一套对照实验选做法，用切片和混淆找出弱的标签。
- 标注质量出问题时：按根因表分清是规则、提示词还是标准标签本身的问题，改版后先在没用过的样本上验证再上线。

## 不适用的地方

- 不证明这套流程在别的模型、别的任务上同样有效；换任务要重新跑对照。
- 不替数据集改标准标签：可两读或漏标的标签照实报告，交给定标准的一方。

## 评测数据

### 开发集第一轮：Agent 第一步用不用工具

开发集上记下每种做法第一步有没有调用工具；结果用来改流程，测试集冻结前完成。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 点评开发集 40 条 |
| 跑了几次 | 每条每种做法 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，effort low，批量接口 |

### 测试集 A：五种做法

广告：中英文广告文案加画面上的字，每种语言 7 类政策标签，答案在写广告时定好，其中 32 条形似违规其实合规。点评：大众点评的中文餐厅点评，18 个方面，标签是 ASAP 数据集自带的。五种做法：短提示词、整本规则放进提示词、会查规则的 Agent、再加检索相似案例、再加自查。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 广告 119 条；点评 201 条 |
| 跑了几次 | 每条每种做法 1 遍 |
| 模型和发送方式 | claude-haiku-5-5，effort low，批量接口 |
| 跑前冻结 | `experiments/PREREGISTRATION.md`（14 个冻结文件的指纹） |

### 测试集 A：预注册的对照（后一种减前一种，微平均 F1）

同一批题上两种做法配对比较；配对自助区间整个在 0 以上才算“更好”，跨过 0 算“没测出差别”。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 广告 119 条；点评 201 条 |
| 跑了几次 | 每条每种做法 1 遍；区间按题目自助重抽样 2,000 次 |
| 模型和发送方式 | claude-haiku-5-5，effort low，批量接口 |
| 跑前冻结 | `experiments/PREREGISTRATION.md` 第五节 |

### 根因：完整 Agent 在测试集 A 上的错误判断

最好的做法（两个任务都是完整 Agent）的每个错误标签判断，先由代码算出线索，再独立归类两次，归到五类：提示词缺陷、模型能力、规则冲突、样本分布、标签歧义（数据集的标签可两读或漏标）。两次不一致的单列为“分歧”。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 点评 165 条里的错误判断；广告 4 条里的错误判断 |
| 跑了几次 | 每个错误判断归类 2 次 |
| 模型和发送方式 | claude-haiku-5-5，批量接口 |
| 跑前冻结 | `experiments/PREREGISTRATION.md` 第六节 |

### 按根因改的第二版：没用过的测试集 B

第二版只改根因表指出的地方：点评补上数据集对“只标有评价的方面”的例外（商场位置、优惠、标价）、两个价格标签的分界和自查保留惯例要求的标签；广告把检测得出的效果百分比归到数据类、把“立刻减重”只归到减重类；两个任务都让 Agent 答前过一遍全部标签。冻结后才在测试集 B 上跑。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-18 |
| 题目和答案 | 广告 118 条；点评 199 条（测试集 B，之前没用过） |
| 跑了几次 | 每条每个版本 1 遍；区间按题目自助重抽样 |
| 模型和发送方式 | claude-haiku-5-5，effort low，批量接口 |
| 跑前冻结 | `experiments/REVISION.md`（17 个冻结文件的指纹） |

## 指标和结果

每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。

### 开发集第一轮：Agent 第一步用不用工具

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 只给规则工具：第一步调用了工具 | 36/40（90.0%，95% 区间 76.9–96.0%） | 只作说明 | [`labelling-agent-kit/results/dev1/FIRST_TURN.md`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/dev1/FIRST_TURN.md) |
| 再给检索案例的工具：第一步调用了工具 | 0/40（0.0%，95% 区间 0.0–8.8%） | 只作说明 | [`labelling-agent-kit/results/dev1/FIRST_TURN.md`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/dev1/FIRST_TURN.md) |

只给检索案例的工具，Agent 第一步一次也不用；检索改成流程里固定的一步，Agent 和加案例的做法之间只差案例本身。

### 测试集 A：五种做法

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 广告，短提示词：微平均 F1 | 0.768 | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 广告，整本规则放进提示词：微平均 F1 | 0.878 | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 广告，会查规则的 Agent：微平均 F1 | 0.925 | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 广告，再加检索相似案例：微平均 F1 | 0.965 | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 广告，再加自查（完整 Agent）：微平均 F1 | 0.971 | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 点评，短提示词：微平均 F1 | 0.715 | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 点评，整本规则放进提示词：微平均 F1 | 0.782 | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 点评，会查规则的 Agent：微平均 F1 | 0.799 | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 点评，再加检索相似案例：微平均 F1 | 0.812 | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 点评，再加自查（完整 Agent）：微平均 F1 | 0.824 | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 形似违规其实合规的广告被打了标签，短提示词 | 12/32（37.5%，95% 区间 22.9–54.7%） | 越低越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 形似违规其实合规的广告被打了标签，完整 Agent | 0/32（0.0%，95% 区间 0.0–10.7%） | 越低越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 广告漏判（该有标签却一个没给），短提示词 | 5/67（7.5%，95% 区间 3.2–16.3%） | 越低越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 广告漏判，完整 Agent | 1/67（1.5%，95% 区间 0.3–8.0%） | 越低越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 广告误判（不该有标签却给了），短提示词 | 15/52（28.8%，95% 区间 18.3–42.3%） | 越低越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 广告误判，完整 Agent | 0/52（0.0%，95% 区间 0.0–6.9%） | 越低越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 点评，引的原话一字不差，短提示词 | 1303/1330（98.0%，95% 区间 97.1–98.6%） | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 点评，引的原话一字不差，完整 Agent | 1115/1115（100.0%，95% 区间 99.7–100.0%） | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 广告，完整 Agent：每 1,000 条的费用 | 0.53 美元 | 越低越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 点评，加检索案例、不自查：每 1,000 条的费用 | 0.91 美元 | 越低越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 点评，完整 Agent：每 1,000 条的费用 | 1.59 美元 | 越低越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |

每加一步，两个任务上都更好；广告上提升主要来自不再误判形似违规的合规广告。点评的天花板更低，和它的标准标签有关（见根因）。

### 测试集 A：预注册的对照（后一种减前一种，微平均 F1）

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 广告：查规则的 Agent 减短提示词 | +0.157（95% 区间 [+0.106, +0.214]） | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 点评：查规则的 Agent 减短提示词 | +0.083（95% 区间 [+0.064, +0.102]） | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 广告：加检索案例减不加 | +0.040（95% 区间 [+0.007, +0.076]） | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 点评：加检索案例减不加 | +0.014（95% 区间 [+0.003, +0.024]） | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 广告：加自查减不加 | +0.006（95% 区间 [-0.023, +0.038]） | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 点评：加自查减不加 | +0.012（95% 区间 [+0.001, +0.023]） | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 广告：查规则的 Agent 减整本规则放进提示词 | +0.047（95% 区间 [-0.004, +0.097]） | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 点评：查规则的 Agent 减整本规则放进提示词 | +0.017（95% 区间 [+0.000, +0.033]） | 越高越好 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |
| 点评：真实案例库减合成案例库 | +0.010（95% 区间 [-0.001, +0.022]） | 只作说明 | [`labelling-agent-kit/results/main/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/analysis.json) |

查规则、检索案例在两个任务上都测出提升；自查只在点评上；整本规则放进提示词和 Agent 比，广告上没测出差别。

### 根因：完整 Agent 在测试集 A 上的错误判断

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 点评：错误标签判断 | 406 | 越低越好 | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| 点评：两次独立归类一致 | 257/406（63.3%，95% 区间 58.5–67.8%） | 越高越好 | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| 点评：标签歧义 | 158 | 只作说明 | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| 点评：提示词缺陷 | 61 | 只作说明 | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| 点评：模型能力 | 20 | 只作说明 | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| 点评：规则冲突 | 18 | 只作说明 | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| 点评：两次归类不一致（分歧） | 149 | 只作说明 | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| 点评：在所有做法里都错的判断 | 194 | 只作说明 | [`labelling-agent-kit/results/main/rca/asap-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/asap-test_a-agent-cases-check.json) |
| 点评测试集 A：含有强线索词却没有对应标签的点评（数据验收 A10：训练集里这个词出现时有这个标签的比例不低于 0.95；这是漏标的下限） | 7/201（3.5%，95% 区间 1.7–7.0%） | 只作说明 | [`labelling-agent-kit/results/acceptance.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/acceptance.json) |
| 广告：两次独立归类一致 | 3/4（75.0%，95% 区间 30.1–95.4%） | 越高越好 | [`labelling-agent-kit/results/main/rca/ad_policy-test_a-agent-cases-check.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/main/rca/ad_policy-test_a-agent-cases-check.json) |

点评最多的一类是标签歧义，近一半错误判断在所有做法里都错：这部分受标准标签本身限制，照实报告，不去拟合。能改的是规则和流程：提示词没让 Agent 想到的标签、自查删掉了数据集惯例要的标签、通用规则和数据集惯例冲突（价格、优惠、商场位置）。

### 按根因改的第二版：没用过的测试集 B

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 点评，第一版：微平均 F1 | 0.834 | 越高越好 | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| 点评，第二版：微平均 F1 | 0.852 | 越高越好 | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| 点评：第二版减第一版 | +0.018（95% 区间 [+0.005, +0.031]） | 越高越好 | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| 广告，第一版：微平均 F1 | 0.971 | 越高越好 | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| 广告，第二版：微平均 F1 | 0.993 | 越高越好 | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| 广告：第二版减第一版 | +0.021（95% 区间 [+0.000, +0.048]） | 越高越好 | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| 点评，测试集 A 上复看：第二版减第一版（改动是照测试集 A 的失败写的，这一行只作完整记录，不当证据） | +0.017（95% 区间 [+0.003, +0.031]） | 只作说明 | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| 广告，测试集 A 上复看：第二版减第一版 | +0.014（95% 区间 [-0.018, +0.048]） | 只作说明 | [`labelling-agent-kit/results/revision/analysis.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/revision/analysis.json) |
| 整个项目的模型调用费用（批量价） | 3.6325 美元 | 越低越好 | [`labelling-agent-kit/results/costs.json`](https://github.com/llia0031-dotcom/labelling-agent-kit/blob/main/results/costs.json) |

点评：第二版在没用过的题上测出提升，收益落在改动瞄准的价格、优惠和位置标签上，采用。广告：也高一点，但区间下端是 0，按事先定的规则不算提升，不采用；第一版在测试集 A 上只错了四条，能测的空间本来就小。

## 评分器校准

- 标准标签：广告是写广告时定好的答案，点评是 ASAP 数据集自带的标注；这个项目没有另做标注。
- 根因归类是判断：每个错误判断先由代码算出线索，再独立归类两次，两次一致的比例照实列出，不一致的单列为“分歧”。

## 局限和失败案例

- 每种做法每条只跑了一次；模型采样带来的波动不在按题目重抽样的区间里，几处差别离边界很近（点评上查规则对整本规则、一半一半案例库、广告的第二版）。
  - 建议：上线前对离边界近的几组多跑几次，确认结论不变。
- 广告的题目和广告规则出自同一组项目（有据审核、审核模型实验），答案在写广告时定好，不是独立标注员定的；完整 Agent 在广告上已接近满分。
  - 建议：接真实业务前，用业务里已有结论的样本另建测试集。
- 点评的标准标签漏掉了一些提及：测试集 A 的 201 条点评里，有 7 条含有在训练集里几乎总伴随某个标签的词，却没有那个标签；根因里还有 158 个判断归为标签歧义。点评上的精确率受这个限制，Agent 的一部分“错误”可能是数据集该有的标签。
  - 建议：把可两读或漏标的样本整理给定标准的一方，先统一标注口径，再比较做法。
- 合成点评比真实点评短，而且是照 Agent 读的同一本规则生成的；换一种生成方式，真实对合成的结论可能不同。
  - 建议：用不同的生成提示或模型再造一个案例库，重做这组对照。

## 版本

- **1.0**（2026-11-18）第一张卡，照公开仓库 labelling-agent-kit 的结果文件写。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。

第三方数据、模型和代码的来源与许可，见[项目仓库](https://github.com/llia0031-dotcom/labelling-agent-kit)里的说明。
