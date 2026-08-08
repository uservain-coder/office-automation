# office-automation · Python 办公自动化脚本集

> 计算机专业 / Python 办公自动化 —— 帮人把重复 8 小时的活儿，压到 1 分钟跑完。

🌐 **在线展示页**：[https://uservain-coder.github.io/office-automation/](https://uservain-coder.github.io/office-automation/)（需在仓库 `Settings → Pages` 启用 `main` 分支 `/ (root)` 后生效）

我是计算机专业的，用 Python 写脚本解决日常办公里那些「重复、机械、容易出错」的活：
Excel 批量合并、PDF 转 Excel、文件批量整理、工资条生成…… **你描述需求，我写脚本，你点一下就完事。**

---

## 一、项目整体架构

本仓库是一个**纯脚本型作品集**，无服务端、无构建步骤，靠 `argparse` 命令行驱动。整体分三层：

```
需求方（闲鱼客户 / 自己）
        │  描述需求
        ▼
   scripts/ 核心脚本（A~D + 公共字体模块）
        │  读入 xlsx / pdf / 目录
        ▼
   examples/ 脱敏示例 + 运行产物（能力证明）
   docs/     每个脚本的详细用法文档
```

- **输入**：Excel（`.xlsx`）、PDF、本地目录。
- **输出**：合并/拆分后的 Excel、PDF 提取出的 Excel、改名/分类后的文件、工资条（xlsx 或 pdf）。
- **公共依赖**：`cn_font.py` 统一解决「中文 PDF 在网页阅读器（腾讯文档/浏览器）不显示」的跨脚本问题。



### 技术栈


| 用途              | 库                                 |
| --------------- | --------------------------------- |
| 数据处理 / Excel 读写 | pandas、openpyxl                   |
| PDF 文本与表格提取     | pdfplumber                        |
| PDF 生成 + 中文嵌入字体 | reportlab                         |
| 命令行进度条          | tqdm                              |
| 文件改名/分类         | Python 标准库（pathlib / re / shutil） |


---



## 二、变更摘要（最近一次梳理）

> 本次对 README 做全面重写，并同步修正了一处会导致「永久修复」失效的隐患。

**✅ 已落地的重要修改**

1. **新增** `scripts/cn_font.py`**（统一中文嵌入字体模块）**：注册并嵌入本机黑体（SimHei）子集，字形数据直接打进 PDF。所有生成 PDF 的脚本都从这里取字体，保证「生成的 PDF 处处可显示」。
2. `scripts/payroll.py` **的** `to_pdf()` **修复中文显示**：原先写死 `Helvetica`（不含中文字形），中文在桌面阅读器也是方块、腾讯文档直接空白；已改为调用 `cn_font` 嵌入字体，`examples/out_payroll.pdf` 已重新生成并验证可显示。
3. `examples/pdf/sample_invoice.pdf` **修复**：原先中文用 `STSong-Light`（非嵌入 CID 字体），网页阅读器无此字体→整页空白；现由 `generate_sample_invoice.py` 用嵌入子集重新生成（10 页、每页表格+文本）。
4. `examples/make_examples.py` **同步改为复用** `cn_font`：原来它生成 PDF 时也用 `STSong-Light`，重跑会把它覆盖回「坏版本」。现已修正，避免回归。

**⚠️ 已知不一致 / 待办（已如实标注，未改动以免扩大范围）**

- `docs/file_rename.md` 引用的 `examples/file_rename/input/`（9 个脱敏演示文件）**当前仓库中不存在**，文档与代码暂未对齐。
- `requirements.txt` 中的 `python-docx` **当前任何脚本均未使用**（闲置声明）。
- `examples/make_examples.py` 内含一行无用的 `from PIL import Image`，导致它隐性依赖 **Pillow**，但 Pillow **未写入** `requirements.txt`（运行该脚本需本机已装 Pillow，否则启动即报错）。
- `docs/` 早先提及的 `闲鱼文案.md`、`待填清单.md` 现已不在仓库，本 README 仅记录现存文件。

**💡 常见疑问（来自此前讨论）**

- `payroll.py` **没有 "split 模式"**：它只有 `--format xlsx|pdf`。其 xlsx 模式是「逐人生成一份工资条」（1 行→1 文件），与 `excel_batch.py` 的 `split`（按某列不同取值分组，可能多行→1 文件）机制不同，不要混淆。

---



## 三、目录结构（当前真实状态）

```
office-automation/
├── scripts/                  # 核心脚本（均带 argparse + 中文注释）
│   ├── cn_font.py            # 【新增】统一中文嵌入字体模块（所有 PDF 生成脚本共用）
│   ├── excel_batch.py        # 脚本A：Excel 合并/拼接/拆分/去重
│   ├── pdf_extract.py        # 脚本B：PDF 文本/表格 → Excel
│   ├── file_rename.py        # 脚本C：文件批量改名 + 自动分类
│   └── payroll.py            # 脚本D：工资条/对账单生成（xlsx / pdf）
├── examples/                 # 脱敏示例数据 + 运行产物（能力证明）
│   ├── make_examples.py      # 一键生成全部脱敏示例
│   ├── debug.log             # make_examples.py 的运行调试日志（开发产物）
│   ├── excel/
│   │   ├── sales_01~03.xlsx  # 分公司销售表（合并演示）
│   │   ├── by_dept.xlsx      # 含重复行的部门总表（拆分/去重演示）
│   │   ├── out_merged.xlsx   # merge 产物
│   │   ├── out_concated.xlsx # concat 产物
│   │   ├── out_dedup.xlsx    # dedup 产物
│   │   ├── out_split/        # 按「部门」拆分 → 技术部.xlsx / 市场部.xlsx
│   │   └── out_split_name/   # 按「姓名」拆分 → 张三/李四/王五.xlsx
│   ├── out_pdf_tables.xlsx   # pdf_extract tables 产物
│   ├── out_pdf_text.xlsx     # pdf_extract text 产物
│   ├── out_payroll.pdf       # payroll --format pdf 产物（3 页，已嵌入字体）
│   ├── out_payroll/          # payroll --format xlsx 产物（每人一份）
│   ├── payroll/master.xlsx   # 工资条总表（每人一行）
│   └── pdf/
│       ├── generate_sample_invoice.py  # 专用 PDF 生成器（嵌入字体，内容稳定）
│       └── sample_invoice.pdf           # 10 页演示 PDF（已嵌入字体）
├── docs/                     # 每个脚本的详细用法文档
│   ├── excel_batch.md
│   ├── pdf_extract.md
│   ├── file_rename.md        # 详版（引用了暂不存在的 examples/file_rename/input）
│   ├── payroll.md
│   └── COMPLIANCE.md         # 脱敏与合规自检（发布前）
├── index.html                # GitHub Pages 在线展示页（深色科技风，纯静态）
├── requirements.txt
├── .gitignore
└── README.md
```

---



## 四、逐文件说明



### 4.1 核心脚本 `scripts/`



#### `scripts/cn_font.py`　【新增 · 公共基础设施】

- **职责**：统一注册并嵌入中文字体，供所有生成 PDF 的脚本复用，彻底解决「中文 PDF 在腾讯文档/浏览器（PDF.js）不显示」。
- **关键接口**：
  - `register_cn_font() -> str`：注册并嵌入字体，返回字体名 `CN_FONT`（值 `"SimHei"`）；重复调用安全（只注册一次）。
  - 模块常量 `CN_FONT`：PDF 内部引用名。
- **字体候选**（按优先级，首个存在即用）：`C:\Windows\Fonts\simhei.ttf` → `simsun.ttc` → `msyh.ttc`（后两者为 TTC，自动带 `subfontIndex=0` 回退）。
- **依赖**：reportlab。
- **近期修改**：2026-08-08 新建。把原先分散在各脚本里的「非嵌入字体」统一改为「嵌入 TrueType 子集」。
- **被谁依赖**：`payroll.py`、`examples/pdf/generate_sample_invoice.py`、`examples/make_examples.py`。



#### `scripts/excel_batch.py`　（脚本 A）

- **职责**：Excel 批量处理，四种模式。
  - `merge`：多文件纵向合并成一张总表
  - `concat`：多文件按行号横向拼接（列名加 `__表N` 后缀避免冲突）
  - `split`：按 `--key` 列的不同取值拆成多个文件
  - `dedup`：按 `--key` 列去重（`keep="first"`）
- **关键函数**：`collect_files()`（收集目录/通配符，排除 `~$` 锁文件）、`load_all()`（读取+空值统计+进度条）、`do_merge/do_concat/do_split/do_dedup`。
- **命令行参数**：`--mode`(必填) · `--input`(必填,目录或通配符) · `--output`(必填,split 为目录) · `--key`(split/dedup 必填) · `--sheet`(可选)。
- **依赖**：pandas、openpyxl、tqdm。
- **近期修改**：无逻辑改动；与 `payroll.py` 的「逐人生成」区别见第二节常见疑问。



#### `scripts/pdf_extract.py`　（脚本 B）

- **职责**：PDF → Excel。
  - `tables`（默认）：`pdfplumber` 提取每页表格 → 每页一个 sheet（`P1`…`P10`）。
  - `text`：提取每页文本 → 单 sheet 或每页一个 sheet（`--per-page`）。
- **关键函数**：`extract_tables()`、`extract_text()`、`clean_text()`（清理 openpyxl 不允许的控制字符）、`parse_pages()`（解析 `"1,3,5-7"` 页码表达式）。
- **命令行参数**：`--input` · `--output` · `--mode`(texttables,默认 tables) · `--pages`(如 `1,3,5-7`,默认全部) · `--per-page`(text 模式每页一 sheet)。
- **依赖**：pdfplumber、pandas、openpyxl。
- **近期修改**：`clean_text()` 清理非法控制字符（此前修复 openpyxl 写入报错）；venv 中损坏的 `cffi` 已修复，使 `pdfplumber` 恢复可用。
- **注意**：纯图片扫描件（无文字层）提取不到，会友好提示且不崩溃，需先做 OCR。



#### `scripts/file_rename.py`　（脚本 C）

- **职责**：文件批量改名 + 自动分类。
  - 动作 `rename`，规则三选一：`prefix`(前缀+三位序号) / `date`(修改日期+原名) / `regex`(正则替换命中片段)。
  - 动作 `classify`：按扩展名分入 `图片 / 文档 / 表格 / 其他` 子目录（建于 `--input` 内部）。
- **关键机制**：**默认只打印预览，加** `--yes` **才真执行**（绝不静默删改）；仅处理目录一层文件，不递归。
- **命令行参数**：位置参数 `action`(renameclassify) · `--input`(必填) · `--rule` · `--prefix` · `--pattern` · `--repl` · `--yes`。
- **依赖**：仅 Python 标准库（pathlib / re / shutil / datetime）。
- **近期修改**：无。`CATEGORY` 映射见源码顶部。
- **⚠️ 已知不一致**：`docs/file_rename.md` 引用的 `examples/file_rename/input/`（9 个脱敏演示文件）当前仓库不存在。



#### `scripts/payroll.py`　（脚本 D）

- **职责**：从一张「总表」（每人一行）生成每个人的工资条。
  - `--format xlsx`：每个人一个文件（`姓名.xlsx`）。
  - `--format pdf`：合并成一个带分页的 PDF。
- **关键函数**：`build_one()`（拼「项目/金额」两列表）、`to_xlsx()`、`to_pdf()`。
- **可配置**：`DEFAULT_FIELDS = "姓名,部门,应发,扣款,实发"`；`FIELD_LABEL` 做中文标签映射；`--fields` 可挑选进工资条的列（需在总表中存在）。
- **命令行参数**：`--input`(总表) · `--output`(xlsx 为目录 / pdf 为文件) · `--format`(xlsxpdf) · `--fields`。
- **依赖**：pandas、openpyxl、reportlab（仅 PDF）、`cn_font`。
- **近期修改**：2026-08-08 `to_pdf()` 改用 `cn_font` 嵌入中文字体（原为 `Helvetica`，中文变方块/腾讯文档不显示），`examples/out_payroll.pdf` 已重新生成验证。
- **注意**：本脚本**无 split 模式**；xlsx 是「逐人生成」，不同于 `excel_batch.split`。



### 4.2 示例与产物 `examples/`



#### `examples/make_examples.py`

- **职责**：一键生成全部脱敏示例数据：分公司销售表、含重复行的部门表、工资条总表、10 页演示 PDF。
- **关键细节**：运行时会把 NDJSON 调试日志写入 `examples/debug.log`（含写死的 `SESSION_ID`）。
- **依赖**：pandas、reportlab；（⚠️ 含无用 `from PIL import Image`，隐性需要 Pillow 但未在 requirements 声明）。
- **近期修改**：2026-08-08 其 PDF 生成改为复用 `cn_font`（原为 `STSong-Light` 非嵌入字体）。
- **说明**：本脚本的 PDF 内容由 `random.seed(20250808)` 固定（确定但随机明细）；仓库中当前的 `sample_invoice.pdf` 由 `examples/pdf/generate_sample_invoice.py` 生成（内容稳定：2025 年 1–10 月采购对账报告）。二者均为有效脱敏演示。



#### `examples/debug.log`

- `make_examples.py` 的 NDJSON 调试日志（字段：sessionId / runId / hypothesisId / location / message / data / timestamp）。开发产物，非交付物；发布前可删。当前已被 git 跟踪（`.gitignore` 未忽略）。



#### `examples/excel/`


| 文件                                                  | 说明                                  |
| --------------------------------------------------- | ----------------------------------- |
| `sales_01.xlsx` / `sales_02.xlsx` / `sales_03.xlsx` | 分公司销售表（合并演示），列：姓名 / 区域 / 销售额        |
| `by_dept.xlsx`                                      | 含一条重复行的部门总表（拆分/去重演示），列：姓名 / 部门 / 工资 |
| `out_merged.xlsx`                                   | `merge` 产物                          |
| `out_concated.xlsx`                                 | `concat` 产物（列名带 `__表N` 后缀）          |
| `out_dedup.xlsx`                                    | `dedup` 产物（按姓名去重，删 1 行）             |
| `out_split/技术部.xlsx`、`市场部.xlsx`                     | 按「部门」拆分                             |
| `out_split_name/张三.xlsx`、`李四.xlsx`、`王五.xlsx`        | 按「姓名」拆分                             |




#### `examples/payroll/master.xlsx`

- 工资条总表（每人一行），列：姓名 / 部门 / 应发 / 扣款 / 实发，共 3 人（张三/李四/王五）。



#### `examples/out_payroll.pdf` 与 `examples/out_payroll/`

- `payroll.py --format pdf` → `out_payroll.pdf`（3 页，已嵌入字体，腾讯文档可显示）。
- `payroll.py --format xlsx` → `out_payroll/` 目录（张三.xlsx / 李四.xlsx / 王五.xlsx，各为「项目/金额」两列工资条）。



#### `examples/out_pdf_tables.xlsx` 与 `examples/out_pdf_text.xlsx`

- 对 `sample_invoice.pdf` 用 `pdf_extract.py` 提取表格 / 文本的产出。



#### `examples/pdf/generate_sample_invoice.py` 与 `examples/pdf/sample_invoice.pdf`

- `generate_sample_invoice.py`：**专用 PDF 生成器**，复用 `cn_font` 嵌入 SimHei 子集，内容稳定（2025 年 1–10 月「青松数字科技」采购对账报告，10 页，每页文本+表格，全脱敏）。是 `sample_invoice.pdf` 的权威生成器。
- `sample_invoice.pdf`：10 页演示 PDF，已嵌入字体，可在腾讯文档/浏览器正常显示。



### 4.3 文档 `docs/`


| 文件               | 内容                                                                               |
| ---------------- | -------------------------------------------------------------------------------- |
| `excel_batch.md` | 脚本 A 用法：4 种模式、参数、示例命令                                                            |
| `pdf_extract.md` | 脚本 B 用法：text/tables、`--pages`、`--per-page`、扫描件提示                                 |
| `file_rename.md` | 脚本 C **详版**：两个动作、三种改名规则、自动分类、参数速查、练手步骤（⚠️ 引用了暂不存在的 `examples/file_rename/input`） |
| `payroll.md`     | 脚本 D 用法：总表→工资条、xlsx/pdf、`--fields` 定制                                            |
| `COMPLIANCE.md`  | 脱敏与合规自检清单、红线（发布前逐条核对）                                                            |




### 4.4 站点 `index.html`

- GitHub Pages 在线展示页，**纯静态 HTML + 内联 CSS**，无构建步骤。含能力卡片、效果对比条、闲鱼/ GitHub 入口。
- 启用：仓库 `Settings → Pages` 选 `main` 分支、`/(root)`。



### 4.5 配置

- `requirements.txt`：`pandas`、`openpyxl`、`pdfplumber`、`reportlab`、`tqdm`；另列 `python-docx`（⚠️ 当前未在任何脚本中使用，闲置）。
  - ⚠️ 隐性缺失：`make_examples.py` 需要 `Pillow`，但未在此声明。
- `.gitignore`：忽略 `.venv/`、`__pycache__/`、`*.pyc`、`*.pyo`、`.DS_Store`、`*.tmp`。`examples/` 下的演示输入输出**故意保留**，作为能力证明（注意 `debug.log` 未被忽略，当前已提交）。

---



## 五、快速开始

```bash
# 1. 装依赖（建议用虚拟环境；注意 make_examples.py 还需单独 pip install pillow）
python -m venv .venv
. .venv/Scripts/activate         # Windows；Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
pip install pillow            # make_examples.py 隐性依赖（requirements 未含）

# 2. 生成脱敏示例数据（可选；会覆盖 examples 下演示文件）
python examples/make_examples.py

# 3. 跑起来看效果
python scripts/excel_batch.py --mode merge --input "examples/excel/sales_*.xlsx" --output examples/out_merged.xlsx
python scripts/pdf_extract.py  --input examples/pdf/sample_invoice.pdf --output examples/out_pdf_tables.xlsx --mode tables
python scripts/file_rename.py  classify --input ./待整理目录        # 先预览，加 --yes 才执行
python scripts/payroll.py      --input examples/payroll/master.xlsx --output examples/out_payroll --format xlsx
```

> 每个脚本都有 `--help`；逐文件用法见 `docs/` 目录。

---



## 六、技术服务说明

本仓库是**能力展示**用途。如果你有具体的办公自动化需求（Excel 报表、PDF 提取、批量处理、工资条等），
欢迎走闲鱼找我定制：**[https://m.tb.cn/h.8f3TO2g?tk=fKtsgxwuJyu](https://m.tb.cn/h.8f3TO2g?tk=fKtsgxwuJyu)**（简介挂了本仓库链接作为案例背书）。

- 先聊需求再报价，不乱收费
- 交付附简单使用说明
- 支持闲鱼担保交易，放心拍

---



## 七、免责声明

1. 本仓库所有示例数据均为**脱敏的虚构数据**（张三 / 李四 / 某科技公司），不含任何真实个人信息。
2. 脚本仅用于**合法办公场景**，不承接任何违规需求（破解、外挂、刷单、抢票、爬取非公开数据等均不接）。
3. 使用本仓库代码产生的任何后果由使用者自行承担，作者不对数据准确性做担保。

---



## 八、更新日志

- 新增 `scripts/cn_font.py`：统一中文嵌入字体模块（SimHei 子集），所有 PDF 生成脚本复用。
- 修复 `payroll.py` `to_pdf()` 中文不显示（原 `Helvetica` → 嵌入 SimHei），重生成 `examples/out_payroll.pdf` 并验证。
- 修复 `sample_invoice.pdf` 中文在腾讯文档不显示（原 `STSong-Light` 非嵌入 → 嵌入子集），由 `generate_sample_invoice.py` 重新生成。
- `make_examples.py` 的 PDF 生成改为复用 `cn_font`，防止重跑覆盖回坏版本。
- 全面重写 README，逐文件对齐当前代码状态；标注已知不一致（file_rename 示例目录缺失、python-docx 闲置、Pillow 隐性依赖未声明）。
- （早前）`pdf_extract.py` 增加 `clean_text()` 清理非法控制字符；修复 venv 中损坏的 `cffi`。

⭐ 如果这个仓库对你有帮助，点个 Star 支持一下～