# 灰度回放演示

> **这是用评测题回放的演示，不是真实用户。** 这些项目没有线上流量。

做法：项目在冻结的对比评测里已经让新旧两版各回答了同一批题。回放把每段对话当成一个请求，按“题号#第几遍”的哈希分到 0–99 的桶里；桶号小于灰度比例的请求由 staging 版本的存档回答“接待”，其余由 production 版本接待。灰度按 10% → 50% → 100% 放量，每一步都检查下面的回滚条件（回放前写好），触发就停下、production 不动。

回滚条件：

- 灰度组的字段写错比例高于线上组
- 灰度组改后版本丢品牌或价格的比例高于线上组
- 灰度组每段对话的平均费用比线上组高 10% 以上

样本很小（每步只有几段到几十段对话），所以这里演示的是机制，不是统计结论。

## `grounded-review/advice`：v1.1 → v1.3

回放的请求：36（mt4：12 条新广告，每版 3 遍）

| 灰度比例 | staging 接待 | 字段写错 | 丢品牌或价格 | 平均费用 | 触发的回滚条件 |
|---|---|---|---|---|---|
| 10% | 1 | staging 0/1 · production 6/35 | staging 0/1 · production 2/35 | staging 0.0057 · production 0.0069 | 无 |
| 50% | 17 | staging 0/17 · production 3/19 | staging 0/17 · production 1/19 | staging 0.0065 · production 0.0072 | 无 |
| 100% | 36 | staging 0/36 · production 6/36 | staging 0/36 · production 2/36 | staging 0.0068 · production 0.0069 | 无 |

**结果：全量。** 每一步都没有触发回滚条件，production 挪到 v1.3。

费用单位是美元。100% 那一步没有 production 接待的请求，所以用 production 版本在全部请求上的存档做对照。

来源文件：`grounded-review-public/eval/results/multiturn-mt4-v1.1.jsonl`（bb262b3d8268）、`grounded-review-public/eval/results/multiturn-mt4-v1.3.jsonl`（ff1db0e0ca09）

## `grounded-review/advice`：v1.1 → v1.2

回放的请求：36（mt3：12 条新广告，每版 3 遍）

| 灰度比例 | staging 接待 | 字段写错 | 丢品牌或价格 | 平均费用 | 触发的回滚条件 |
|---|---|---|---|---|---|
| 10% | 3 | staging 0/3 · production 4/33 | staging 0/3 · production 3/33 | staging 0.0076 · production 0.0069 | 无 |
| 50% | 15 | staging 3/15 · production 3/21 | staging 1/15 · production 3/21 | staging 0.0080 · production 0.0066 | 灰度组的字段写错比例高于线上组、灰度组每段对话的平均费用比线上组高 10% 以上 |

**结果：回滚。** production 留在 v1.1，v1.2 退回。

费用单位是美元。

来源文件：`grounded-review-public/eval/results/multiturn-mt3-v1.1.jsonl`（903512b60ade）、`grounded-review-public/eval/results/multiturn-mt3-v1.2.jsonl`（547256bcdcb8）
