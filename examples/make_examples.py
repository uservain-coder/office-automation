#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成脱敏示例数据（仅用于演示，不含任何真实个人信息）。"""
import os
import sys
import json
import time

# Debug log configuration (hard‑coded for this session)
DEBUG_LOG_PATH = os.path.join(os.path.dirname(__file__), "debug.log")
SESSION_ID = "4c1ee771-70b0-487e-9815-162742c1d589"

def _write_debug_log(message, data=None, hypothesisId="A", location="make_examples.py"):
    """Append a single NDJSON line to the session log.
    Fields required by the system: sessionId, runId, hypothesisId, location,
    message, data, timestamp.
    """
    payload = {
        "sessionId": SESSION_ID,
        "runId": "run1",
        "hypothesisId": hypothesisId,
        "location": location,
        "message": message,
        "data": data or {},
        "timestamp": int(time.time() * 1000),
    }
    try:
        with open(DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
    except Exception as exc:
        # If logging fails we silently ignore to avoid breaking the script
        pass

# Log start of script
_write_debug_log("Starting make_examples.py", location="make_examples.py:1")
_write_debug_log(f"Python version: {sys.version}", location="make_examples.py:2")
_write_debug_log(f"Python executable: {sys.executable}", location="make_examples.py:3")

# ------------------- Import checks -------------------
# pandas
_write_debug_log("Attempting pandas import", hypothesisId="A", location="make_examples.py:7")
try:
    import pandas as pd
    _write_debug_log("pandas import succeeded", data={"version": pd.__version__}, hypothesisId="A", location="make_examples.py:9")
except Exception as e:
    _write_debug_log("pandas import failed", data={"error": str(e)}, hypothesisId="A", location="make_examples.py:11")
    raise

# reportlab
_write_debug_log("Attempting reportlab import", hypothesisId="B", location="make_examples.py:13")
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    _write_debug_log("reportlab import succeeded", hypothesisId="B", location="make_examples.py:15")
except Exception as e:
    _write_debug_log("reportlab import failed", data={"error": str(e)}, hypothesisId="B", location="make_examples.py:17")
    raise

# Pillow (PIL)
_write_debug_log("Attempting PIL import", hypothesisId="C", location="make_examples.py:19")
try:
    from PIL import Image
    _write_debug_log("PIL import succeeded", hypothesisId="C", location="make_examples.py:21")
except Exception as e:
    _write_debug_log("PIL import failed", data={"error": str(e)}, hypothesisId="C", location="make_examples.py:23")
    raise

# reportlab platypus
_write_debug_log("Attempting reportlab.platypus import", hypothesisId="D", location="make_examples.py:25")
try:
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    _write_debug_log("reportlab.platypus import succeeded", hypothesisId="D", location="make_examples.py:27")
except Exception as e:
    _write_debug_log("reportlab.platypus import failed", data={"error": str(e)}, hypothesisId="D", location="make_examples.py:29")
    raise

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

# ---- 示例4：10 页 PDF（每页含文本+表格，用于 pdf_extract 测试）----
# 场景：虚构公司「青松数字科技」2025 年 1–10 月采购对账报告（全脱敏，无真实业务信息）
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak

pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
_CN = "STSong-Light"

_pdf_styles = getSampleStyleSheet()
_title_style = ParagraphStyle("CNTitle", parent=_pdf_styles["Title"], fontName=_CN, fontSize=15, spaceAfter=6)
_para_style = ParagraphStyle("CNPara", parent=_pdf_styles["Normal"], fontName=_CN, fontSize=10.5, leading=16, spaceAfter=8)

import random
random.seed(20250808)
_items_pool = [
    ("笔记本电脑", 1, 5200), ("显示器", 2, 1099), ("机械键盘", 3, 199),
    ("无线鼠标", 5, 89), ("A4打印纸(箱)", 4, 150), ("人体工学椅", 1, 680),
    ("企业路由器", 1, 320), ("U盘 64G", 10, 45), ("插线板", 2, 60),
    ("打印机墨盒", 3, 130), ("云服务器(月)", 1, 299), ("激光硒鼓", 2, 210),
]
_months = [f"2025年{i}月" for i in range(1, 11)]
_bullets = [
    "以办公设备更新为主，兼顾日常耗材补充。",
    "新增项目组入驻，临时增配外设若干。",
    "季度采购，批量下单以获取更低单价。",
    "以打印与网络耗材为主，设备支出较少。",
    "年中盘点后补全短缺物资。",
    "配合系统上云，增加服务器与存储投入。",
    "暑期运维窗口，集中更换老化设备。",
    "按预算执行，支出平稳。",
    "为下半年项目储备耗材。",
    "年末结算，清理剩余预算并补采。",
]
_story = []
for idx, month in enumerate(_months):
    _rows = random.sample(_items_pool, k=random.randint(4, 5))
    _total = 0
    _table_data = [["物品", "数量", "单价(元)", "小计(元)"]]
    for name, qty, price in _rows:
        subtotal = qty * price
        _total += subtotal
        _table_data.append([name, str(qty), f"{price:,}", f"{subtotal:,}"])
    _tbl = Table(_table_data, colWidths=[150, 60, 90, 90])
    _tbl.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), _CN),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, (0, 0, 0)),
        ("BACKGROUND", (0, 0), (-1, 0), (0.85, 0.9, 0.95)),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ]))
    _story.append(Paragraph(f"青松数字科技 · 采购对账报告（{month}）", _title_style))
    _story.append(Paragraph(
        f"本月公司共采购物资 {len(_rows)} 项，合计支出 ¥{_total:,}。"
        f"采购说明：{_bullets[idx]}各项明细如下表所示，"
        f"本报告所有数据均为演示用途，不含任何真实业务信息。",
        _para_style))
    _story.append(_tbl)
    if idx != len(_months) - 1:
        _story.append(PageBreak())

pdf_path = os.path.join(PDF_DIR, "sample_invoice.pdf")
doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                        leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
doc.build(_story)

print("✅ 脱敏示例数据已生成：")
print("  examples/excel/sales_0{1,2,3}.xlsx  (合并演示)")
print("  examples/excel/by_dept.xlsx         (拆分/去重演示)")
print("  examples/payroll/master.xlsx        (工资条演示)")
print("  examples/pdf/sample_invoice.pdf     (PDF 提取演示)")

# Log script completion
_write_debug_log("make_examples.py completed successfully", location="make_examples.py:120")
