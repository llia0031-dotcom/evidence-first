# 实习安置监测包：评测卡

> 卡片版本 1.0 · 数据截至 2026-11-26 · 已公开
>
> 数字由 `scripts/build_cards.py` 从项目的结果文件算出；比例附 Wilson 95% 区间。

| 时间 | 团队 | 技术 | 链接 |
|---|---|---|---|
| 2026-11-22 至 2026-11-23 | Liang Liyuan | Python、XLSForm（pyxform 和 ODK Validate）、KoboToolbox / ODK Central 导出、pandas、openpyxl、reportlab、python-pptx、evidence-check | [代码和说明](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/README.zh-CN.md) · [快速上手](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/guide/en/QUICK_START.md) · [数据检查说明](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/guide/en/CHECKS.md) |

**问题**：把实习生安置到接收单位的项目，要按月跟进每个人：谁的表还没交、数据哪里有错、本月该向管理层报什么；靠人工翻表，又慢又容易漏。

**我做了什么**：我先查了现成的：付费的监测平台要钱要账号，也没有实习就业的模板；大学的实习管理系统不面向离线收集和法语；公开仓库里没找到实习回访的表单。于是把公认的问法和指标定义接起来：结束去向的问法和就业分类照劳动统计的国际标准，自己写的题在表里注明。每月的程序读表单导出，做数据检查，列出谁该跟进并配好提醒话术，再出跟进表、简报和演示稿。检查先在构造的样例上量过：50 名同意参加的实习生、18 家接收单位、7 个月，里面埋好了错误，也放了看着像错、其实没错的记录。

**结果**：

- 构造样例里埋好的数据错误全部查出：17/17；问题表里没有多出的行，14 处看着像错、其实没错的记录一处没报
- 简报和演示稿里带出处的数字逐行对回数据：260/260；背景简报 24/24
- 四张英法双语表单共 119 道题，在填表界面里逐张填过：418/418 项检查通过

## 概况

给按月跟进实习安置的团队用：四张英法双语表单（入组、每月回访、接收单位反馈、结束去向），可在 KoboToolbox 或 ODK Central 里用；每月双击一次，程序做 15 项数据检查、算 39 个指标，写出跟进表、2 页简报和 8 页演示稿。评的是两件事：检查查得准不准，用构造样例里埋好的错误和像错其实没错的记录来量；报告里的数字对不对，逐行对回数据。

- **在作品集里的位置**：运营层
- **和核心部件的关系**：简报、演示稿、背景简报和 README 里每个带出处的数字，都用 evidence-check 0.5.0 的核对脚本对回它来自的那一行数据。
- **用到的模型**：没有调用模型：表单转换、数据检查、指标和报告都由脚本完成。

## 用途

- 按月跟进实习或培训安置的团队：每月下载表单导出，双击一次，拿到谁该跟进、数据哪里有问题、本月的简报和演示稿。
- 开始收数据之前：把自己的设置写进表单，先拿构造样例跑一遍，看清每项检查会报什么、怎么改。

## 不适用的地方

- 不是在线平台：数据留在团队自己的表单服务器和电脑上，每月在 Windows 上跑一次。
- 不替人判断个人情况：安全方面的回访只列出该打的电话和最晚日期，由团队的人来打。

## 评测数据

### 数据检查：埋好错误的构造样例

构造的样例队列，没有真实的人和单位：埋了数据错误（重复提交、编号对不上、日期不合理、前后矛盾等）、没收到的跟进，以及看着像错、其实没错的记录；每处埋了什么、该由哪项检查报出，都写在埋错清单里。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-23 |
| 题目和答案 | 全部埋错和像错其实没错的记录 |
| 跑了几次 | 每次运行和每次测试都跑 |
| 模型和发送方式 | 全部数据检查；不调用模型 |
| 跑前冻结 | `data/sample/planted.json`（每处埋错、怎么埋的、应有的结果） |

### 报告：简报和演示稿里的数字

构造样例当月的英文和法文简报、演示稿，以及背景简报；每一行带数字的话都标了它来自哪一行数据。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-23 |
| 题目和答案 | 全部带标签的行 |
| 跑了几次 | 每次运行都核对 |
| 模型和发送方式 | evidence-check 0.5.0 的核对脚本；不调用模型 |
| 跑前冻结 | `indicators/INDICATORS.md`（每个指标的分子、分母和规则） |

### 表单：在填表界面里逐张填写

四张表单用 KoboToolbox 和 ODK Central 用的转换器 pyxform 转换，并过 ODK Validate；再在本机的 ODK Web Forms 里，用英文和法文、按手机和电脑宽度逐张填写，存下的提交和每月程序读的字段名逐项比对。

| 项目 | 内容 |
|---|---|
| 日期 | 2026-11-23 |
| 题目和答案 | 四张表单的全部题目 |
| 跑了几次 | 每张表、每种语言和宽度各一遍 |
| 模型和发送方式 | 填表脚本；不调用模型 |
| 跑前冻结 | `forms/xlsform/` |

## 指标和结果

每个评测版本单独列表。题目或评分规则改过的版本之间不直接比较分数。

### 数据检查：埋好错误的构造样例

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 埋好的数据错误查出 | 17/17（100.0%，95% 区间 81.6–100.0%） | 越高越好 | [`placement-monitoring-kit/data/sample/planted.json`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/data/sample/planted.json)<br>[`placement-monitoring-kit/outputs/sample/en/2026-08/data/issues.csv`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/outputs/sample/en/2026-08/data/issues.csv) |
| 问题表里不是埋错的行 | 0/18（0.0%，95% 区间 0.0–17.6%） | 越低越好 | [`placement-monitoring-kit/data/sample/planted.json`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/data/sample/planted.json)<br>[`placement-monitoring-kit/outputs/sample/en/2026-08/data/issues.csv`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/outputs/sample/en/2026-08/data/issues.csv) |
| 看着像错、其实没错的记录 | 14 | 只作说明 | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| 埋好的没收到的跟进 | 9 | 只作说明 | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| 样例里同意参加的实习生 | 50 | 只作说明 | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| 样例里的接收单位 | 18 | 只作说明 | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| 样例的月数 | 7 | 只作说明 | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| 数据检查项 | 15 | 只作说明 | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |

每处埋错都被对应的检查报出，问题表里没有多出的行；像错其实没错的记录一处没报。

### 报告：简报和演示稿里的数字

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 简报和演示稿：带标签的行对回数据 | 260/260（100.0%，95% 区间 98.5–100.0%） | 越高越好 | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| 背景简报：带标签的行对回数据 | 24/24（100.0%，95% 区间 86.2–100.0%） | 越高越好 | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| 指标 | 39 | 只作说明 | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| 简报页数 | 2 | 只作说明 | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| 演示稿页数 | 8 | 只作说明 | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |

每个带出处的数字都对回了数据行，英法两版的数字一致；同样的数据再跑一次，简报和演示稿逐字节相同。

### 表单：在填表界面里逐张填写

| 指标 | 结果 | 方向 | 来源文件 |
|---|---|---|---|
| 填表检查通过 | 418/418（100.0%，95% 区间 99.1–100.0%） | 越高越好 | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| 存下的提交和表单、字段对得上 | 32/32（100.0%，95% 区间 89.3–100.0%） | 越高越好 | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| 四张表单的题目 | 119 | 只作说明 | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |
| 自动测试 | 479 | 只作说明 | [`placement-monitoring-kit/results/SUMMARY.md`](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/results/SUMMARY.md) |

每张表都能在填表界面里填完，存下的提交和每月程序读的字段对得上。

## 局限和失败案例

- 样例是构造的；还没在真实的项目、真实的 KoboToolbox 或 ODK Central 服务器和 ODK Collect 手机端上用过，只在 Windows 上跑过。
  - 建议：上线前在团队自己的服务器上建一个测试项目，用几份测试提交把每月流程跑通一次。
- 法文文字还要请当地讲法语的同事通读一遍；每月回访和接收单位反馈的部分题目没有公认的现成问卷，是这套工具自己的写法，在表里注明了。
  - 建议：通读后把改动写回表单的 xlsx 再生成；用过一两个月后，照回答情况改题。

## 版本

- **1.0**（2026-11-26）第一张卡，照公开仓库 placement-monitoring-kit 的结果文件写。

## 出处

模板照 Hugging Face 模型卡（Apache-2.0）的章节；每个数字的来源文件和指纹见 `cards/sources.lock.json`。

第三方数据、模型和代码的来源与许可，见[项目仓库](https://github.com/llia0031-dotcom/placement-monitoring-kit/blob/main/README.zh-CN.md)里的说明。
