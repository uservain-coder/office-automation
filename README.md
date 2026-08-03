# office-automation · Python 办公自动化脚本集

> 计算机专业 / Python 办公自动化 —— 帮人把重复 8 小时的活儿，压到 1 分钟跑完。

🌐 **在线展示页**：https://uservain-coder.github.io/office-automation/（需在仓库 `Settings → Pages` 启用 `main` 分支 `/ (root)` 后生效）

我是计算机专业的，用 Python 写脚本解决日常办公里那些「重复、机械、容易出错」的活：
Excel 批量合并、PDF 转 Excel、文件批量整理、工资条生成…… **你描述需求，我写脚本，你点一下就完事。**

---

## 🛠 我能做什么

| 脚本 | 解决什么痛点 | 能力 |
|------|--------------|------|
| 📊 `excel_batch.py` | 每月把 10 个分公司报表合并、按部门拆分、去重 | 合并 / 横向拼接 / 按列拆分 / 去重 |
| 📄 `pdf_extract.py` | 发票、对账单 PDF 转成可编辑 Excel | 提取文本 / 提取表格（扫描件会提示） |
| 🗂 `file_rename.py` | 一堆乱文件要改名、按类型归类 | 前缀序号 / 日期 / 正则改名 / 自动分类（带预览防误删） |
| 💰 `payroll.py` | HR 每月手工做几十份工资条 | 从总表一键生成每人工资条（xlsx / pdf） |

---

## 📁 目录结构

```
office-automation/
├── scripts/                 # 4 个核心脚本（均带 argparse + 中文注释）
│   ├── excel_batch.py
│   ├── pdf_extract.py
│   ├── file_rename.py
│   └── payroll.py
├── examples/                # 脱敏示例数据 + 运行产物（证明脚本真的能跑）
│   ├── excel/   payroll/   pdf/
│   └── make_examples.py     # 一键生成脱敏示例
├── docs/                    # 每个脚本的详细用法文档
├── requirements.txt
├── index.html                 # GitHub Pages 在线展示页（深色科技风）
└── README.md
```

---

## ⚡ 效果对比（以「合并 10 个分公司月报」为例）

| 方式 | 耗时 | 出错率 | 心情 |
|------|------|--------|------|
| 手动 Ctrl+C/V | ~2 小时 | 高（粘贴错位、漏表） | 😫 熬夜 |
| 本脚本 | ~3 秒 | 0 | 😎 下班 |

---

## 🚀 快速开始

```bash
# 1. 装依赖（建议用虚拟环境）
python -m venv .venv && source .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. 生成脱敏示例数据
python examples/make_examples.py

# 3. 跑起来看效果
python scripts/excel_batch.py --mode merge --input "examples/excel/sales_*.xlsx" --output examples/out_merged.xlsx
python scripts/pdf_extract.py  --input examples/pdf/sample_invoice.pdf --output examples/out_pdf_tables.xlsx --mode tables
python scripts/file_rename.py  classify --input ./待整理目录        # 先预览，加 --yes 才执行
python scripts/payroll.py      --input examples/payroll/master.xlsx --output examples/out_payroll --format xlsx
```

> 每个脚本都有 `--help`，参数含义见 `docs/` 目录。

---

## 💡 技术服务说明

本仓库是**能力展示**用途。如果你有具体的办公自动化需求（Excel 报表、PDF 提取、批量处理、工资条等），
欢迎走闲鱼找我定制：**{{你的闲鱼昵称}}**（简介挂了本仓库链接作为案例背书）。

- 先聊需求再报价，不乱收费
- 交付附简单使用说明
- 支持闲鱼担保交易，放心拍

---

## ⚠️ 免责声明

1. 本仓库所有示例数据均为**脱敏的虚构数据**（张三 / 李四 / 某科技公司），不含任何真实个人信息。
2. 脚本仅用于**合法办公场景**，不承接任何违规需求（破解、外挂、刷单、抢票、爬取非公开数据等均不接）。
3. 使用本仓库代码产生的任何后果由使用者自行承担，作者不对数据准确性做担保。

---

⭐ 如果这个仓库对你有帮助，点个 Star 支持一下～
