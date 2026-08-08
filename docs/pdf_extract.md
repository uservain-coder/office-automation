# 脚本 B：pdf_extract.py — PDF ↔ Excel 提取

**痛点**：发票、对账单、报表是 PDF，要录进 Excel 只能肉眼抄，慢且易错。

## 两种模式


| 模式       | 作用                           |
| -------- | ---------------------------- |
| `tables` | 提取每页表格 → 每页一个 sheet（默认）      |
| `text`   | 提取每页文本 → 单 sheet 或每页一个 sheet |


## 示例命令

```bash
# 提取表格（带网格线的 PDF 才能被识别）
python scripts/pdf_extract.py --input examples/pdf/sample_invoice.pdf --output examples/out_pdf_tables.xlsx --mode tables

# 提取全文（每页一个 sheet）
python scripts/pdf_extract.py --input examples/pdf/sample_invoice.pdf --output examples/out_pdf_text.xlsx --mode text --per-page
```

## 参数

- `--input`：PDF 路径
- `--output`：输出 xlsx
- `--mode`：`text` / `tables`
- `--pages`：页码范围，如 `1,3,5-7`（默认全部）
- `--per-page`：text 模式下每页一个 sheet



## 注意

- **扫描件（纯图片、无文字层）提取不到**，脚本会友好提示，不会崩溃；这种情况需先做 OCR。
- 表格识别依赖 PDF 里的表格线（网格），自由排版文本用 `--mode text` 更稳。



## 适合谁用

采购、财务、行政，经常要把纸质/PDF 单据录成电子表的同学。