#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
脚本 D：工资条 / 对账单自动生成
功能：从一张「总表」(每人一行) 自动生成每个人的工资条。
  - 输出 xlsx：每个人一个文件
  - 输出 pdf ：合并成一个带分页的 PDF（需 reportlab，可选）
适用痛点：HR 每月手工做几十份工资条，易错又慢。
字段可用 --fields 配置（哪些列进工资条），默认 姓名/部门/应发/扣款/实发。
依赖：pandas / openpyxl（PDF 另需 reportlab）
"""
import argparse
import os

import pandas as pd


# 默认工资条字段（可用 --fields 覆盖，逗号分隔）
DEFAULT_FIELDS = "姓名,部门,应发,扣款,实发"
FIELD_LABEL = {
    "姓名": "员工姓名",
    "部门": "所属部门",
    "应发": "应发工资",
    "扣款": "各项扣款",
    "实发": "实发工资",
}


def build_one(row, fields):
    """把一行数据拼成工资条二维表（标签/值）。"""
    lines = []
    for f in fields:
        label = FIELD_LABEL.get(f, f)
        val = row.get(f, "")
        lines.append([label, val])
    return lines


def to_xlsx(df, fields, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    # 用「姓名」列命名，避免重名
    key = "姓名" if "姓名" in df.columns else df.columns[0]
    n = 0
    for _, row in df.iterrows():
        name = str(row.get(key, f"员工{n+1}")).replace("/", "_")
        lines = build_one(row, fields)
        out = pd.DataFrame(lines, columns=["项目", "金额"])
        out.to_excel(os.path.join(output_dir, f"{name}.xlsx"), index=False)
        n += 1
    return n


def to_pdf(df, fields, output_path):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError:
        raise SystemExit("❌ 生成 PDF 需要 reportlab，请先 pip install reportlab，或改用 --format xlsx")
    key = "姓名" if "姓名" in df.columns else df.columns[0]
    c = canvas.Canvas(output_path, pagesize=A4)
    w, h = A4
    for _, row in df.iterrows():
        c.setFont("Helvetica-Bold", 16)
        c.drawString(60, h - 80, f"工资条 - {row.get(key, '')}")
        c.setFont("Helvetica", 12)
        y = h - 120
        for label, val in build_one(row, fields):
            c.drawString(80, y, f"{label}：{val}")
            y -= 24
        c.showPage()
    c.save()
    return len(df)


def main():
    p = argparse.ArgumentParser(description="工资条 / 对账单自动生成")
    p.add_argument("--input", required=True, help="总表 .xlsx（每人一行）")
    p.add_argument("--output", required=True, help="xlsx 模式为目录；pdf 模式为文件")
    p.add_argument("--format", choices=["xlsx", "pdf"], default="xlsx")
    p.add_argument("--fields", default=DEFAULT_FIELDS, help="进工资条的列，逗号分隔")
    args = p.parse_args()

    if not os.path.exists(args.input):
        raise SystemExit(f"❌ 文件不存在：{args.input}")

    fields = [x.strip() for x in args.fields.split(",") if x.strip()]
    df = pd.read_excel(args.input)
    missing = [f for f in fields if f not in df.columns]
    if missing:
        raise SystemExit(f"❌ 字段 {missing} 不在总表中，可用列：{list(df.columns)}")

    if args.format == "xlsx":
        n = to_xlsx(df, fields, args.output)
        print(f"\n✅ 已生成 {n} 份工资条 → 目录 {args.output}")
    else:
        n = to_pdf(df, fields, args.output)
        print(f"\n✅ 已生成 {n} 份工资条 PDF → {args.output}")


if __name__ == "__main__":
    main()
