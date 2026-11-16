# 评测卡模板

每个项目一张评测卡，章节相同。章节照 [Hugging Face 模型卡模板](https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/templates/modelcard_template.md)（Apache-2.0）来定，按“AI 能力的评测”改了名字。卡片由 `scripts/build_cards.py` 从 `cards/specs/<项目>.toml` 生成，不要手改生成的 `.md`。

| 章节 | 写什么 | 对应 HF 模型卡 |
|---|---|---|
| 概况 | 一段话：这个能力做什么；在作品集里属于哪一层；和核心部件 evidence-check 的关系；用到的模型 | Model Details |
| 用途 | 设计时就打算用在哪里 | Uses → Direct Use |
| 不适用的地方 | 明确不该拿它做的事 | Out-of-Scope Use |
| 评测数据 | 每个评测版本一节：题目从哪来、答案什么时候定、几条、跑了几次、模型和发送方式、跑前冻结了什么 | Evaluation → Testing Data |
| 指标和结果 | 每个评测版本一张表：指标、结果（比例附 95% 区间）、越高越好还是越低越好、来源文件 | Evaluation → Metrics, Results |
| 评分器校准 | 用评分器的地方：先拿事先定好答案的样本检验评分器，写一致率 | （新增，照 openai/evals 的建议） |
| 局限和失败案例 | 写成数字；每条配一条建议 | Bias, Risks, and Limitations → Recommendations |
| 版本 | 卡片和评测的版本、日期、改了什么 | （新增，照 inspect_evals 的版本规则） |
| 出处 | 每个数字的来源文件和指纹 | Citation |

## 写数字的规矩

1. **数字不手抄。** spec 里只写“从哪个文件、按什么规则算”（`extractor`），数字由 `scripts/extractors.py` 读结果文件算出来。文字里提到数字，只能写占位符，例如 `{heldout_oneshot}`；写裸的分数或百分比，生成脚本会报错。
2. **对照项目记录。** 每个数字可以附项目报告里的原话（`record`）和出处（`record_src`），算出来对不上就报错。
3. **比例加区间。** 比例一律附 Wilson 95% 区间；写明跑了几次。同一题跑两遍合并算的，区间偏窄，要写出来。
4. **按版本分开。** 题目或评分规则改过就是新的评测版本，单独一张表，不拿新旧分数相减。
5. **方向和日期。** 每个指标写越高越好还是越低越好；卡片写数据截至哪天。

## spec 的字段

```toml
id = "项目编号"            # 也是生成文件名
order = 1                  # 在总表里的顺序
layer = "judgement"        # core / retrieval / judgement / generation / interaction / operations
status = "public"          # public / private（private 在总表里写“未公开”）
card_version = "1.0"
updated = "2026-11-15"     # 数据截至
name = { zh = "…", en = "…" }
problem = { zh = "…", en = "…" }          # 总表“解决什么问题”
primary_metric = { zh = "…", en = "…" }   # 总表“主要指标”
headline = [ { zh = "…{占位符}…", en = "…" } ]  # 总表“关键数字”
summary = { zh = "…", en = "…" }
links = [ { label = { zh = "代码", en = "Code" }, url = "https://…" } ]
uses = { zh = ["…"], en = ["…"] }
out_of_scope = { zh = ["…"], en = ["…"] }
judge = { zh = ["…"], en = ["…"] }        # 可选

[[eval]]
id = "评测版本编号"
name = { zh = "…", en = "…" }
date = "2026-11-13"
data = { zh = "…", en = "…" }
items = { zh = "…", en = "…" }
runs = { zh = "…", en = "…" }
setup = { zh = "claude-haiku-5-5，普通接口", en = "…" }
frozen = { zh = "…", en = "…" }           # 可选

  [[eval.metric]]
  id = "指标编号"
  label = { zh = "…", en = "…" }
  extractor = "函数名"
  args = { }                               # 可选
  direction = "higher"                     # higher / lower / none
  record = "191/192"                       # 可选：项目报告里的原话，用来对照
  record_src = "项目的评测报告"

[[limitation]]
text = { zh = "…", en = "…" }
advice = { zh = "…", en = "…" }

[[version]]
id = "1.0"
date = "2026-11-15"
text = { zh = "…", en = "…" }
```
