# -*- coding: utf-8 -*-
"""
重新生成 sample_invoice.pdf —— 关键修复：
原文件中文使用 reportlab 的 STSong-Light（非嵌入 CID 字体），
桌面阅读器自带 Adobe 中日韩字体包能显示，但腾讯文档等网页版 PDF
渲染引擎（PDF.js）没有该字体，导致中文整页空白/无法显示。

本脚本改用本地 TrueType 中文字体（SimHei 黑体）并“嵌入子集”，
让字形自包含，任何阅读器（含腾讯文档）均可正常显示。
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                Table, TableStyle, HRFlowable, PageBreak)

# ---------- 1. 注册并嵌入中文字体（复用统一模块，保证处处可显示） ----------
import sys as _sys
_sys.path.insert(0, os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts")))
from cn_font import register_cn_font, CN_FONT
register_cn_font()  # 嵌入子集，自包含字形

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "sample_invoice.pdf")

# ---------- 2. 数据（忠实还原原 10 页内容） ----------
DATA = [
    ("2025年1月", "以办公设备更新为主，兼顾日常耗材补充。",
     [("机械键盘", 3, 199, 597), ("打印机墨盒", 3, 130, 390),
      ("企业路由器", 1, 320, 320), ("U盘 64G", 10, 45, 450),
      ("笔记本电脑", 1, 5200, 5200)]),
    ("2025年2月", "新增项目组入驻，临时增配外设若干。",
     [("U盘 64G", 10, 45, 450), ("插线板", 2, 60, 120),
      ("机械键盘", 3, 199, 597), ("打印机墨盒", 3, 130, 390),
      ("人体工学椅", 1, 680, 680)]),
    ("2025年3月", "季度采购，批量下单以获取更低单价。",
     [("激光硒鼓", 2, 210, 420), ("打印机墨盒", 3, 130, 390),
      ("人体工学椅", 1, 680, 680), ("A4打印纸(箱)", 4, 150, 600)]),
    ("2025年4月", "以打印与网络耗材为主，设备支出较少。",
     [("A4打印纸(箱)", 4, 150, 600), ("企业路由器", 1, 320, 320),
      ("机械键盘", 3, 199, 597), ("无线鼠标", 5, 89, 445)]),
    ("2025年5月", "年中盘点后补全短缺物资。",
     [("A4打印纸(箱)", 4, 150, 600), ("U盘 64G", 10, 45, 450),
      ("打印机墨盒", 3, 130, 390), ("无线鼠标", 5, 89, 445)]),
    ("2025年6月", "配合系统上云，增加服务器与存储投入。",
     [("插线板", 2, 60, 120), ("企业路由器", 1, 320, 320),
      ("激光硒鼓", 2, 210, 420), ("U盘 64G", 10, 45, 450),
      ("机械键盘", 3, 199, 597)]),
    ("2025年7月", "暑期运维窗口，集中更换老化设备。",
     [("人体工学椅", 1, 680, 680), ("机械键盘", 3, 199, 597),
      ("无线鼠标", 5, 89, 445), ("打印机墨盒", 3, 130, 390)]),
    ("2025年8月", "按预算执行，支出平稳。",
     [("A4打印纸(箱)", 4, 150, 600), ("云服务器(月)", 1, 299, 299),
      ("插线板", 2, 60, 120), ("显示器", 2, 1099, 2198),
      ("机械键盘", 3, 199, 597)]),
    ("2025年9月", "为下半年项目储备耗材。",
     [("激光硒鼓", 2, 210, 420), ("显示器", 2, 1099, 2198),
      ("人体工学椅", 1, 680, 680), ("无线鼠标", 5, 89, 445)]),
    ("2025年10月", "年末结算，清理剩余预算并补采。",
     [("企业路由器", 1, 320, 320), ("A4打印纸(箱)", 4, 150, 600),
      ("激光硒鼓", 2, 210, 420), ("打印机墨盒", 3, 130, 390)]),
]

# ---------- 3. 样式 ----------
styles = getSampleStyleSheet()
title_style = ParagraphStyle("CNTitle", parent=styles["Title"], fontName=CN_FONT,
                             fontSize=18, leading=24, alignment=TA_CENTER,
                             textColor=colors.HexColor("#1a3c5e"))
intro_style = ParagraphStyle("CNIntro", parent=styles["Normal"], fontName=CN_FONT,
                             fontSize=10.5, leading=16, textColor=colors.HexColor("#333333"))
cell_style = ParagraphStyle("CNCell", parent=styles["Normal"], fontName=CN_FONT,
                            fontSize=10, leading=14)
cell_center = ParagraphStyle("CNCellC", parent=cell_style, alignment=TA_CENTER)
footer_style = ParagraphStyle("CNFooter", parent=styles["Normal"], fontName=CN_FONT,
                              fontSize=8, alignment=TA_CENTER,
                              textColor=colors.HexColor("#999999"))

def build():
    doc = SimpleDocTemplate(OUT, pagesize=A4,
                            leftMargin=22 * mm, rightMargin=22 * mm,
                            topMargin=20 * mm, bottomMargin=18 * mm,
                            title="青松数字科技-采购对账报告",
                            author="办公自动化脚本示例")
    story = []
    for idx, (month, desc, items) in enumerate(DATA, start=1):
        total = sum(r[3] for r in items)
        story.append(Paragraph(f"青松数字科技 · 采购对账报告（{month}）", title_style))
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=1.2,
                                color=colors.HexColor("#1a3c5e")))
        story.append(Spacer(1, 8))
        intro = (f"本月公司共采购物资 {len(items)} 项，合计支出 "
                 f"¥{total:,}。采购说明：{desc}各项明细如下表所示，"
                 f"本报告所有数据均为演示用途，不含任何真实业务信息。")
        story.append(Paragraph(intro, intro_style))
        story.append(Spacer(1, 10))

        header = [Paragraph(t, cell_center) for t in ["物品", "数量", "单价(元)", "小计(元)"]]
        rows = [header]
        for name, qty, price, sub in items:
            rows.append([
                Paragraph(name, cell_style),
                Paragraph(str(qty), cell_center),
                Paragraph(f"{price:,}", cell_center),
                Paragraph(f"{sub:,}", cell_center),
            ])
        rows.append([Paragraph("合计", cell_center), "", "",
                     Paragraph(f"{total:,}", cell_center)])

        tbl = Table(rows, colWidths=[55 * mm, 25 * mm, 35 * mm, 35 * mm], repeatRows=1)
        ts = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3c5e")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bbbbbb")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#eef3f8")]),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#dce6f1")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
        tbl.setStyle(ts)
        story.append(tbl)
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"第 {idx} / {len(DATA)} 页 · 演示数据，仅供测试", footer_style))
        if idx < len(DATA):
            story.append(PageBreak())
    doc.build(story)
    print("OK ->", OUT, "size=", os.path.getsize(OUT), "bytes")

if __name__ == "__main__":
    build()
