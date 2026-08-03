#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成脱敏示例数据（仅用于演示，不含任何真实个人信息）。"""
import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

BASE = os.path.dirname(os.path.abspath(__file__))
EXCEL_DIR = os.path.join(BASE, "excel")
PAY_DIR = os.path.join(BASE, "payroll")
PDF_DIR = os.path.join(BASE, "pdf")
os.makedirs(EXCEL_DIR, exist_ok=True)
os.makedirs(PAY_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# ---- 示例1：分公司销售表（用于合并）----
branches = {
    "sales_01.xlsx": [("张三", "华北", 12000), ("李四", "华北", 9500)],
    "sales_02.xlsx": [("王五", "华东", 15000), ("赵六", "华东", 8800)],
    "sales_03.xlsx": [("钱七", "华南", 11000), ("孙八", "华南", 10200)],
}
for fname, rows in branches.items():
    pd.DataFrame(rows, columns=["姓名", "区域", "销售额"]).to_excel(
        os.path.join(EXCEL_DIR, fname), index=False)

# ---- 示例2：按部门拆分/去重的总表（含一条重复）----
master = [
    ("张三", "技术部", 12000), ("李四", "市场部", 9500),
    ("王五", "技术部", 15000), ("张三", "技术部", 12000),  # 重复行
]
pd.DataFrame(master, columns=["姓名", "部门", "工资"]).to_excel(
    os.path.join(EXCEL_DIR, "by_dept.xlsx"), index=False)

# ---- 示例3：工资条总表 ----
payroll = [
    ("张三", "技术部", 12000, 1500, 10500),
    ("李四", "市场部", 9500, 1200, 8300),
    ("王五", "技术部", 15000, 2000, 13000),
]
pd.DataFrame(payroll, columns=["姓名", "部门", "应发", "扣款", "实发"]).to_excel(
    os.path.join(PAY_DIR, "master.xlsx"), index=False)

# ---- 示例4：带网格表格的 PDF（用于 pdf_extract 测试）----
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
pdf_path = os.path.join(PDF_DIR, "sample_invoice.pdf")
doc = SimpleDocTemplate(pdf_path, pagesize=A4)
data = [["物品", "数量", "单价"],
        ["键盘", "2", "199"],
        ["鼠标", "5", "89"],
        ["显示器", "1", "1099"]]
tbl = Table(data, colWidths=[120, 80, 80])
tbl.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, (0, 0, 0)),
    ("BACKGROUND", (0, 0), (-1, 0), (0.9, 0.9, 0.9)),
    ("FONTSIZE", (0, 0), (-1, -1), 11),
]))
doc.build([tbl])

print("✅ 脱敏示例数据已生成：")
print("  examples/excel/sales_0{1,2,3}.xlsx  (合并演示)")
print("  examples/excel/by_dept.xlsx         (拆分/去重演示)")
print("  examples/payroll/master.xlsx        (工资条演示)")
print("  examples/pdf/sample_invoice.pdf     (PDF 提取演示)")
