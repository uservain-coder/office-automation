# 脚本 D：payroll.py — 工资条 / 对账单自动生成

**痛点**：HR 每月从总表手工做几十份工资条，复制粘贴易错又慢。

## 功能

从一张「每人一行」的总表，自动生成每个人的工资条。

- 输出 `xlsx`：每个人一个文件
- 输出 `pdf`：把所有人合并成一份带分页的 PDF(适合打印后裁开发放)（需 `reportlab`）

## 示例命令

```bash
# 生成 xlsx（每人一份）
python scripts/payroll.py --input examples/payroll/master.xlsx --output examples/out_payroll --format xlsx

# 生成合并 PDF
python scripts/payroll.py --input examples/payroll/master.xlsx --output examples/out_payroll.pdf --format pdf
```

## 参数

- `--input`：总表 xlsx（每人一行）
- `--output`：xlsx 模式为目录；pdf 模式为文件路径
- `--format`：`xlsx` / `pdf`
- `--fields`：进工资条的列，逗号分隔（默认 `姓名,部门,应发,扣款,实发`）

## 自定义字段

列名与中文标签映射见脚本顶部 `FIELD_LABEL`。要加「社保」「个税」等列，在总表里加列，再把列名加到 `--fields` 即可。

## 适合谁用

每月做工资条 / 对账单的 HR、行政同学。

**对比区分：**

- 想「**一张总表按某列拆成几份子表**」→ 用 `excel_batch split`;
- 想「**给每个人单独生成一份只含本人信息的文件，如工资条/对账单等**」→ 用 `payroll xlsx`;

