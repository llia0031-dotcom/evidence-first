# Prompt 资产库

每个 Prompt 资产的每一版都写清：版本号、改了什么、当时在冻结的测试集上的真实分数、采用还是不采用、为什么。分数由 `scripts/prompts.py build` 从项目的结果文件算出，不手写。同一行里的“→”表示同一套题上新旧两版的对比；不同测试集的分数不互相比较。

## 上线标签

`production` 指项目决定采用、之后都用的版本，`staging` 指正在测的候选版本。上线就是把 production 挪到新版本，回滚就是挪回上一版（`python scripts/prompts.py rollback <资产>`）。标签从 2026-11-15 开始用，之前的记录按各项目的记录补记。这些项目都没有线上流量；灰度只用评测题回放演示，见 [rollout/](rollout/)。

| 资产 | production | staging | 说明 |
|---|---|---|---|
| `evidence-check/skill` | v0.2 | v0.2 | 公开仓库和插件里发布的是 v0.2。 |
| `grounded-review/advice` | v1.3 | v1.3 | 项目决定以后的评测和演示用 v1.3；代码里的默认值仍是 v1，演示页存的也是 v1 的对话。没有线上流量。 |
| `sellpoint-check/advice` | v5 | v5 | 项目现在采用第 5 版。没有线上流量。 |
| `tracedesk/answer` | grounded-v2.4-access | grounded-v2.4-access | 线上演示和公开仓库默认用 grounded-v2.4-access。 |
| `cairn/answer` | cairn-monash-v2 | cairn-monash-v2 | 线上演示用 cairn-monash-v2。 |
| `evidence-pipeline/triage` | v2 | v2 | 没有线上流量；灰度用评测题回放演示。 |
| `evidence-pipeline/kb-qa` | v1 | v1 | 没有真实使用量；评测是题库回放，机器人只在测试时问过几次。 |

## evidence-check：Skill 说明（SKILL.md）

装进 Agent 的 Skill 说明：每句事实附逐字原文、跑核对脚本、逐条重读通过的说法。核对脚本另有版本号（0.2.0 → 0.4.0），见评测卡。

- 代码位置：`skills/evidence-check/SKILL.md`（evidence-check）
- 模型锁定：claude-haiku-5-5，评测时 effort medium

| 版本 | 日期 | 改了什么 | 当时的分数 | 决定 | 为什么 |
|---|---|---|---|---|---|
| **v0.1** | 2026-11-12 | 第一版 Skill。<br>`eval/v2/skill-versions/SKILL-v0.1.md`（指纹 9aec983a7522） | *留出评测 v2：16 个问题、8 篇草稿，每组 2 遍*<br>回答里有编造的数字：2/32<br>正确事实被误标：2/150 | 已被替换 | 开发评测 v1 暴露三个问题：两次误报都是把英文原文正确译成中文却被判错；唯一漏掉的错句是算错的时长；费用接近普通提示的两倍。<br>出处：[evidence-check/eval/EVALUATION.md](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/EVALUATION.md) |
| **v0.2** | 2026-11-12 | 意思相同的改写、总结、翻译算有依据；只写资料给出的数字；整体缩短约三成。在写留出题之前冻结。<br>`skills/evidence-check/SKILL.md`（指纹 8dcadfc8cd45，现行） | *留出评测 v2：16 个问题、8 篇草稿，每组 2 遍*<br>回答里有编造的数字（v0.1 → v0.2）：2/32 → 0/32<br>正确事实被误标（v0.2）：3/150<br>48 次对话的费用（v0.2）：0.1603 美元 | 采用 | 留出评测里不再编数字，费用略低；误标多一条，属于噪声。<br>出处：[evidence-check/eval/EVALUATION.md](https://github.com/llia0031-dotcom/evidence-check/blob/main/eval/EVALUATION.md) |

标签记录：2026-11-12 production ·→v0.1；2026-11-12 staging ·→v0.2；2026-11-12 production v0.1→v0.2

## 有据审核：改稿建议

广告主问“哪里违规、怎么改”时，Agent 给出解释和修改后版本的那一段提示词、规则和输出格式。审核本身的提示词在各版之间没有变。

- 代码位置：`agent/review_agent.py`（grounded-review）
- 模型锁定：claude-haiku-5-5, effort medium

| 版本 | 日期 | 改了什么 | 当时的分数 | 决定 | 为什么 |
|---|---|---|---|---|---|
| **v1** | 2026-11-13 | 第一版：审核、给建议和改后版本、复审广告主的版本。<br>`SYSTEM`、`ADVICE_SCHEMA` 和改稿提问（`agent/review_agent.py`） | 没有存成结果文件的评测 | 已被替换 | 多轮任务里，改后版本偶尔留下要人填的模板占位符。<br>出处：[grounded-review/eval/EVALUATION.md](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/EVALUATION.md) |
| **v1.1** | 2026-11-13 | 改后版本要能直接上线、不留空格子；缺的信息写进回答让广告主补；加一个检查改后版本的工具。<br>v1 加 `ADVICE_RULES_V11` 和 `check_revision` 工具 | *mt2：12 条新广告，每版 2 遍*<br>改后版本留了占位符（v1 → v1.1）：3/24 → 0/24 | 已被替换 | 在为它新写的 12 条广告上，占位符从 3/24 降到 0/24；之后发现“修改后的文案”有时写错位置。<br>出处：[grounded-review/eval/EVALUATION.md](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/EVALUATION.md) |
| **v1.2** | 2026-11-13 | 检查建议的各个字段，填错了退回给模型重交一次。<br>v1.1 加“字段填错就退回重交一次” | *mt3：12 条新广告，每版 3 遍*<br>最后采用的建议里字段写错（v1.1 → v1.2）：4/36 → 6/36 | 不采用 | 退回重交没用：模型第二次照样写错；字段写错 v1.1 4/36，v1.2 6/36，费用还更高。<br>出处：[grounded-review/eval/EVALUATION.md](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/EVALUATION.md) |
| **v1.3** | 2026-11-14 | 输出格式里先填修改后的文案、再写说明；混进来的格式标签在代码里清掉，不多调用模型。<br>`ADVICE_SCHEMA_V13`（先填修改后的文案，再写说明）和 `common.clean_advice` | *mt4：12 条新广告，每版 3 遍*<br>交上来的建议字段写错（v1.1 → v1.3）：6/36 → 0/36<br>品牌和价格保住（v1.1 → v1.3）：34/36 → 36/36<br>每段三轮对话的费用（v1.1 → v1.3）：0.0069 美元 → 0.0068 美元 | 采用 | 在又一组新写的 12 条广告上，交上来的建议字段写错从 6/36 降到 0/36；品牌和价格保住 36/36；费用没变。<br>出处：[grounded-review/eval/EVALUATION.md](https://github.com/llia0031-dotcom/grounded-review/blob/main/eval/EVALUATION.md) |

标签记录：2026-11-13 production ·→v1；2026-11-13 staging ·→v1.1；2026-11-13 production v1→v1.1；2026-11-13 staging v1.1→v1.2；2026-11-13 staging v1.2→v1.3；2026-11-14 production v1.1→v1.3

## 卖点体检：给商家的修改建议

没被评价证实的卖点，在商家后台给出的修改建议和改写后的文案。每一版都先在为它新写、跑前冻结的测试集上和上一版比较，再看同一批真实数据。

- 代码位置：`pipeline/lib/suggest_prompts.mjs, suggest_v2.mjs … suggest_v6.mjs`（sellpoint-check）
- 模型锁定：claude-haiku-5-5, effort medium

| 版本 | 日期 | 改了什么 | 当时的分数 | 决定 | 为什么 |
|---|---|---|---|---|---|
| **v1** | 2026-11-13 | 第一版：对每条没被证实的卖点给出原因、买家原话和可以直接照着改的文案。<br>`pipeline/lib/suggest_prompts.mjs`（指纹 b5b2a58fdbde） | *答案已知的 40 条；真实数据 151 条*<br>测试集可以直接照着改（两次评分）：35/40、32/40<br>真实数据：没有残留被反驳的说法：136/151 | 已被替换 | 真实数据里有一部分改写还留着被评价反驳的说法。<br>出处：[sellpoint-check/results/suggest-run.md](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-run.md) |
| **v2** | 2026-11-14 | 加三条规则，并在代码里检查：改写里还留着被反驳的说法就退回重写。<br>`pipeline/lib/suggest_v2.mjs`（指纹 279e9280f000） | *中文测试集 34 条（v1 对 v2）；真实数据 151 条*<br>中文测试集可以直接照着改，第一次评分（v1 → v2）：30/34 → 32/34<br>真实数据：没有残留被反驳的说法（v1 → v2）：136/151 → 151/151<br>中文商品的建议用中文（v2）：10/34 | 采用（后被 v3 替换） | 残留问题清零，在新写的中文题上更好；但中文商品的建议大多还是英文。<br>出处：[sellpoint-check/results/suggest-testset-zh-v2.md](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset-zh-v2.md) |
| **v3** | 2026-11-14 | 有争议的卖点保留每个被证实的部分和它的条件；商品的语言在代码里定好；退回重写的范围放宽。<br>`pipeline/lib/suggest_v3.mjs`（指纹 c346201974cd） | *混合测试集 40 条（v2 对 v3）；真实数据 151 条*<br>用对语言（v2 → v3）：20/40 → 40/40<br>可以直接照着改，第一次评分（v2 → v3）：37/40 → 37/40<br>真实数据可以直接照着改，第一次评分（v3）：143/151 | 采用（后被 v5 替换） | 中文商家必须收到中文的建议：在新写的混合测试集上，用对语言的从 v2 的一半变成全部，可以直接照着改的条数基本持平。<br>出处：[sellpoint-check/results/suggest-testset-mixed-v3.md](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset-mixed-v3.md) |
| **v4** | 2026-11-14 | 新加“被反驳的词”字段和四条规则，更多情况退回重写。<br>`pipeline/lib/suggest_v4.mjs`（指纹 7b0d5b8debfe） | *混合测试集二 39 条（v3 对 v4）；真实数据 151 条*<br>可以直接照着改，第一次评分（v3 → v4）：38/39 → 36/39<br>真实数据可以直接照着改，第一次评分（v4）：136/151 | 不采用 | 让模型先列出被反驳的词，它就倾向于把这些词整个删掉，删得太多，总分下降。<br>出处：[sellpoint-check/results/suggest-testset-mixed2-v4.md](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset-mixed2-v4.md) |
| **v5** | 2026-11-14 | 第 3 版的提示词不变，加一条代码检查：新文案里出现“买家说”这类写法就退回重写。<br>`pipeline/lib/suggest_v5.mjs`（指纹 4f50d20090bd） | *口语测试集 31 条（v3 对 v5）；真实数据 151 条*<br>可以直接照着改，第一次评分（v3 → v5）：31/31 → 29/31<br>真实数据：新文案里没有“买家说”（v3 → v5）：140/151 → 151/151<br>真实数据可以直接照着改，第一次评分（v5）：142/151 | 采用 | 真实数据上没有“买家说”写法的从 140/151 升到 151/151，可以直接照着改的条数持平。<br>出处：[sellpoint-check/results/suggest-testset-voice-v5.md](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset-voice-v5.md) |
| **v6** | 2026-11-14 | 放宽“买家说”的同义词表，退回重写时加一句“限定条件留着”。<br>`pipeline/lib/suggest_v6.mjs`（指纹 ce17fbc23ce9） | *口语测试集二 32 条（v5 对 v6）；真实数据 151 条*<br>可以直接照着改，第一次评分（v5 → v6）：29/32 → 26/32<br>真实数据可以直接照着改，第一次评分（v6）：139/151 | 不采用 | “限定条件留着”让模型把已被反驳的具体说法也当成限定条件留下了，总分下降；修改建议先停在第 5 版。<br>出处：[sellpoint-check/results/suggest-testset-voice2-v6.md](https://github.com/llia0031-dotcom/sellpoint-check/blob/main/results/suggest-testset-voice2-v6.md) |

标签记录：2026-11-13 production ·→v1；2026-11-14 production v1→v2；2026-11-14 production v2→v3；2026-11-14 staging v3→v4；2026-11-14 staging v4→v5；2026-11-14 production v3→v5；2026-11-14 staging v5→v6；2026-11-14 staging v6→v5

## TraceDesk：带出处的回答

常见问题助手回答时用的系统提示词：只按资料回答、先说结论、每条附逐字原文、截止时间要有出处。对照组是同一个模型的普通提示（baseline-v2）。

- 代码位置：`app/lib/prompts.js`（tracedesk）
- 模型锁定：claude-haiku-5-5, effort medium

| 版本 | 日期 | 改了什么 | 当时的分数 | 决定 | 为什么 |
|---|---|---|---|---|---|
| **grounded-v2-access** | 2026-11-09 | 输出格式升级为 v2：加一句话结论和行动清单。<br>原文没有存档 | 没有存成结果文件的评测 | 已被替换 | 只做过冒烟测试，没有存成评测结果。<br>出处：[tracedesk-lite/app/lib/prompts.js](https://github.com/llia0031-dotcom/tracedesk-lite/blob/main/app/lib/prompts.js) |
| **grounded-v2.1-access** | 2026-11-09 | 日期按读者的语言写。<br>原文没有存档 | 没有存成结果文件的评测 | 已被替换 | 没有单独评测。<br>出处：[tracedesk-lite/app/lib/prompts.js](https://github.com/llia0031-dotcom/tracedesk-lite/blob/main/app/lib/prompts.js) |
| **grounded-v2.2-access** | 2026-11-09 | 加入改编自 i-have-adhd 的写作风格规则。<br>公开仓库提交 d78874c 的 `app/lib/prompts.js` | *开发组 20 道题（普通提示对 v2.2）*<br>自动检查全部通过（普通提示 → v2.2）：17/20 → 19/20 | 已被替换 | 开发组上通过自动检查的比普通提示多；之后发现截止时间有时没挂在对应的步骤上。<br>出处：[tracedesk-lite/app/lib/prompts.js](https://github.com/llia0031-dotcom/tracedesk-lite/blob/main/app/lib/prompts.js) |
| **grounded-v2.3-access** | 2026-11-09 | 每个步骤的截止时间必须挂在这个步骤上，引文里要写着这个时间。<br>公开仓库提交 8064b58 的 `app/lib/prompts.js` | *检查组 20 道题，第一轮*<br>自动检查全部通过（普通提示 → v2.3）：15/20 → 19/20 | 已被替换 | 检查组第一轮通过自动检查的比普通提示多；中文问题的截止时间还会按英文写。<br>出处：[tracedesk-lite/EVALUATION.md](https://github.com/llia0031-dotcom/tracedesk-lite/blob/main/EVALUATION.md) |
| **grounded-v2.4-access** | 2026-11-09 | 截止时间也按读者的语言写。<br>公开仓库提交 2951bef 的 `app/lib/prompts.js`（现行默认） | *检查组 20 道题，第二轮*<br>自动检查全部通过（普通提示 → v2.4）：17/20 → 20/20<br>20 道题的费用（普通提示 → v2.4）：0.0093 美元 → 0.0134 美元 | 采用 | 检查组第二轮自动检查全部通过；但这一轮是在看过第一轮之后、用同一组题跑的，不算干净的留出结果。<br>出处：[tracedesk-lite/EVALUATION.md](https://github.com/llia0031-dotcom/tracedesk-lite/blob/main/EVALUATION.md) |

标签记录：2026-11-09 production ·→grounded-v2-access；2026-11-09 production grounded-v2-access→grounded-v2.1-access；2026-11-09 production grounded-v2.1-access→grounded-v2.2-access；2026-11-09 production grounded-v2.2-access→grounded-v2.3-access；2026-11-09 production grounded-v2.3-access→grounded-v2.4-access

## Cairn：按规定回答

Cairn 回答问题时用的系统提示词：先结论，写截止时间和下一步，标明校区，不编日期、费用和联系方式。

- 代码位置：`app/lib/prompt.js`（cairn）
- 模型锁定：claude-haiku-5-5

| 版本 | 日期 | 改了什么 | 当时的分数 | 决定 | 为什么 |
|---|---|---|---|---|---|
| **cairn-v1** | 2026-11-09 | 最早的版本，资料是无障碍规范（WCAG）。<br>公开仓库提交 f63aafa 的 `app/lib/prompt.js` | 没有存成结果文件的评测 | 停用 | 资料换成学生事务页面后停用。 |
| **cairn-monash-v1** | 2026-11-10 | 先结论、写截止时间和下一步、标明校区、不编日期费用联系方式。<br>公开仓库提交 921e557 的 `app/lib/prompt.js` | 没有存成结果文件的评测 | 已被替换 | 最后一轮可读性检查之后改出 v2。 |
| **cairn-monash-v2** | 2026-11-10 | 对读者只说“页面”、不说“段落”；规定各校区一样时不提校区；回答了的问题不再补充页面没写什么；校区直接告诉模型，不让它反问。<br>公开仓库提交 45f0b13 的 `app/lib/prompt.js`（现行） | 没有存成结果文件的评测 | 采用 | 来自可读性检查。两版都只做了冒烟测试，结果只打印在控制台、没有存成结果文件，所以这里不列分数；检索评测和提示词无关。<br>出处：[cairn/app/lib/prompt.js](https://github.com/llia0031-dotcom/cairn/blob/main/app/lib/prompt.js) |

标签记录：2026-11-09 production ·→cairn-v1；2026-11-10 production cairn-v1→cairn-monash-v1；2026-11-10 production cairn-monash-v1→cairn-monash-v2

## 有据标注流水线：第一道判断

广告进入流水线后的第一道判断：通过还是拒绝、违反哪一条、广告里是哪句话。v2 起还要说自己确定还是拿不准，拿不准的送人工复核。流水线自己的资产库里是同一个资产、同样的标签。

- 代码位置：`pipeline/triage.py`（grounded-labelling-pipeline）
- 模型锁定：claude-haiku-5-5, effort medium, max_tokens 8000

| 版本 | 日期 | 改了什么 | 当时的分数 | 决定 | 为什么 |
|---|---|---|---|---|---|
| **v1** | 2026-11-15 | 第一版：整套政策库、图、文案和图上文字放进一次请求，按审核格式回答。<br>有据审核 Agent 的单次提示词，原样（`agent/oneshot.py`） | *有据审核的 166 条题各回放 2 遍*<br>判错又自动生效：17/332<br>判对：315/332 | 已被替换 | 回放请求里判错的全部自动生效（17/332）；引文核对只拦下判对了但引文有毛病的答案。<br>出处：[grounded-labelling-pipeline/reports/compare-v1-v2.md](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/reports/compare-v1-v2.md) |
| **v2** | 2026-11-15 | 模型说自己确定还是拿不准；拿不准的送人工复核。<br>v1 加一条“拿不准”规则（`triage.CERTAINTY_RULE`），输出格式加 `certainty`、`unsure_reason` | *第一轮：有据审核的 166 条题各回放 2 遍；第二轮：新写 120 条文字广告各 2 遍*<br>判错又自动生效（v1 → v2）：17/332 → 9/332<br>送人工复核（v1 → v2）：6/332 → 72/332<br>判对（v1 → v2）：315/332 → 312/332<br>每个请求的费用（v1 → v2）：0.00062 美元 → 0.00063 美元<br>第二轮新广告：判对（v1 → v2）：239/240 → 240/240 | 采用 | 回归测试按预注册的四条采用标准全部通过，判错又自动生效 17/332 → 9/332。但按跑之前写好的回滚规则，灰度在 10% 时就回滚了；复盘发现两条规则写错。改好的规则在新写的广告上重新灰度，三步都没触发回滚，采用，production 挪到 v2。第二轮两版都接近全对，只说明放量流程走通了；v2 少漏错判的证据来自第一轮。<br>出处：[grounded-labelling-pipeline/docs/CANARY-POSTMORTEM.md](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/docs/CANARY-POSTMORTEM.md) |
| **v3** | 2026-11-17 | 想让答案清楚的广告少送人工：文字广告没配图、写明出处的事实核实不了、广告主的资质和定向、指导条款明明允许的用语，都不再算“拿不准”。<br>v2 的“拿不准”规则重写（`triage.CERTAINTY_RULE_V3`）：写明几种情况算拿不准、几种不算；输出格式不变 | *第三轮：另外新写 120 条文字广告各 2 遍；回归：第一轮 166 条题各回放 2 遍*<br>答案清楚的广告送了人工（v2 → v3）：44/176 → 4/176<br>要人来定的广告送了人工（v2 → v3）：44/64 → 19/64<br>回归：判错又自动生效（v2 → v3）：9/332 → 9/332<br>回归：送人工复核（v2 → v3）：72/332 → 30/332 | 不采用 | 在另外新写的广告上（采用标准和预测跑前预注册），答案清楚的广告送人工从 44/176 降到 4/176；但写题时定为“要人来定”的广告，送人工也从 44/64 降到 19/64，超过事先写好的上限，不采用，production 留在 v2。第一轮回归里判错又自动生效 9/332 对 9/332。假如照样放量，灰度的回滚规则一条也不会触发，是采用标准拦下的。<br>出处：[grounded-labelling-pipeline/reports/compare-v2-v3-round3.md](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/reports/compare-v2-v3-round3.md) |
| **v4** | 2026-11-17 | 想两头都过：答案清楚的广告少送人工，该交人工的不少送。写明几类常见边界，并加一句自查：另一种读法也说得通就答拿不准。<br>v3 的“拿不准”规则加一类：结论取决于把一句话放进还是放出某条规则、而这句话正好在边界上（`triage.CERTAINTY_RULE_V4`）；输出格式不变 | *第四轮：又一批新写的 120 条文字广告各 2 遍；回归：第一轮 166 条题各回放 2 遍*<br>答案清楚的广告送了人工（v2 → v4）：43/176 → 11/176<br>要人来定的广告送了人工（v2 → v4）：42/64 → 47/64<br>答案清楚的广告判错又自动生效（v2 → v4）：0/176 → 2/176<br>回归：判错又自动生效（v2 → v4）：9/332 → 13/332 | 不采用 | 在又一批新写的广告上（采用标准和第三轮一字不改，预测跑前冻结），两头都比 v2 好：答案清楚的广告送人工 43/176 → 11/176，要人来定的送人工 42/64 → 47/64。但它判错时更常说“确定”：答案清楚的广告判错又自动生效 0/176 → 2/176（同一条陷阱题两遍，答案有争议，按预注册没改），第一轮回归漏网 9/332 → 13/332。不采用，production 留在 v2；假如照样放量，灰度的回滚规则一条也不会触发。<br>出处：[grounded-labelling-pipeline/reports/compare-v2-v4-round4.md](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/reports/compare-v2-v4-round4.md) |

标签记录：2026-11-15 production ·→v1；2026-11-15 staging ·→v2；2026-11-15 staging v2→v1；2026-11-16 staging v1→v2；2026-11-16 production v1→v2

## 有据标注流水线：政策知识库问答

标注员问“这样写算不算违规”，只按检索到的条款回答：结论、说明、每条依据的编号和原文；库里没有管这件事的条款就说“没有”。每段引文都用 evidence-check 核对。流水线自己的资产库里是同一个资产、同样的标签。

- 代码位置：`pipeline/kb_qa.py`（grounded-labelling-pipeline）
- 模型锁定：claude-haiku-5-5，effort medium，取前 5 条条款，max_tokens 评测时 1500、机器人里 4000

| 版本 | 日期 | 改了什么 | 当时的分数 | 决定 | 为什么 |
|---|---|---|---|---|---|
| **v1** | 2026-11-17 | 第一版。<br>`kb_qa.INSTRUCTIONS`：四种结论（违规、可以、要看条件、库里没有），只能引检索到的条款，引文逐字抄 | *题库回放：80 道题（中英各一半，一部分库里没有答案），每道 2 遍*<br>答对：134/160<br>库里没有的题说了“没有”：44/48<br>没核对上的引文：1/160<br>中文问题：算对的条款进前 5（BM25）：23/28 | 采用 | 计划和预测跑前写好。答对 134/160；库里没有的题说了“没有” 44/48；没核对上的引文 1/160。没成立的预测是中文问题的检索：算对的条款进前 5 只有 23/28，库里有答案却说“没有”的都出在这里。<br>出处：[grounded-labelling-pipeline/reports/kb-qa.md](https://github.com/llia0031-dotcom/grounded-labelling-pipeline/blob/main/reports/kb-qa.md) |

标签记录：2026-11-17 production ·→v1

## 回归评测

改 `prompts/` 下的文件并开 PR 时，GitHub Action 用 promptfoo 把 production 和 staging 两个标签指向的版本放在同一套冻结的题上跑，把两版的通过数、版本、没通过的题和费用贴到 PR 里。现在接上的是 evidence-check 的 Skill，题目是它的开发评测 v1（虚构活动资料、12 篇草稿）；有请求没拿到回答、任一标签没通过的超过 2 篇，或 staging 比 production 少通过 2 篇以上时标红，规则在 [regression/report.mjs](regression/report.mjs)。配置在 [regression/](regression/)。
