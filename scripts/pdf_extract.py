#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
脚本 B：PDF ↔ Excel 数据提取
功能：
  - text  : 把 PDF 每页文本提取，整本合并到一个 sheet，或每页一个 sheet
  - tables: 用 pdfplumber 提取每页表格 → 写入 Excel（每页一个 sheet）
适用痛点：发票、对账单、报表 PDF 转成可编辑的 Excel。
依赖：pdfplumber / pandas / openpyxl
注意：纯图片扫描件（无文字层）提取不到，会给出友好提示，不会崩溃。
"""
import argparse
import os

import pandas as pd
import pdfplumber


def extract_tables(pdf_path, pages):
    """逐页提取表格，返回 [(页码, DataFrame)]。"""
    results = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        target = parse_pages(pages, total)
        for i in target:
            page = pdf.pages[i]
            tables = page.extract_tables()
            if not tables:
                print(f"   ⚠ 第 {i+1} 页未检测到表格（可能是扫描件/图片）")
                continue
            for t in tables:
                if not t:
                    continue
                # 第一行当表头
                header = [str(h).strip() if h is not None else f"列{j+1}"
                          for j, h in enumerate(t[0])]
                df = pd.DataFrame(t[1:], columns=header)
                results.append((i + 1, df))
    return results


def extract_text(pdf_path, pages, per_page):
    """提取文本。per_page=True 时每页一个 sheet。"""
    sheets = {}
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        target = parse_pages(pages, total)
        for i in target:
            txt = pdf.pages[i].extract_text() or ""
            if not txt.strip():
                print(f"   ⚠ 第 {i+1} 页无文字层（可能是扫描件）")
            if per_page:
                sheets[f"第{i+1}页"] = pd.DataFrame({"内容": txt.splitlines()})
            else:
                sheets.setdefault("全文", pd.DataFrame())
                sheets["全文"] = pd.concat(
                    [sheets["全文"], pd.DataFrame({"内容": txt.splitlines()})],
                    ignore_index=True)
    return sheets


def parse_pages(pages, total):
    """把 '1,3,5-7' 这样的页码表达式解析成 0-based 索引列表。"""
    if not pages:
        return list(range(total))
    idx = set()
    for part in pages.split(","):
        if "-" in part:
            a, b = part.split("-")
            idx.update(range(int(a) - 1, int(b)))
        else:
            idx.add(int(part) - 1)
    return sorted(i for i in idx if 0 <= i < total)


def main():
    p = argparse.ArgumentParser(description="PDF 提取文本/表格到 Excel")
    p.add_argument("--input", required=True, help="PDF 文件路径")
    p.add_argument("--output", required=True, help="输出 .xlsx 路径")
    p.add_argument("--mode", choices=["text", "tables"], default="tables",
                   help="提取文本还是表格（默认 tables）")
    p.add_argument("--pages", help="页码范围，如 '1,3,5-7'（默认全部）")
    p.add_argument("--per-page", action="store_true", help="text 模式下每页一个 sheet")
    args = p.parse_args()

    if not os.path.exists(args.input):
        raise SystemExit(f"❌ 文件不存在：{args.input}")

    if args.mode == "tables":
        rows = extract_tables(args.input, args.pages)
        if not rows:
            raise SystemExit("❌ 该 PDF 未检测到任何表格。若为扫描件，请先做 OCR 再处理。")
        with pd.ExcelWriter(args.output, engine="openpyxl") as writer:
            for page_no, df in rows:
                sheet = f"P{page_no}"[:31]
                df.to_excel(writer, sheet_name=sheet, index=False)
        print(f"\n✅ 表格提取完成：{len(rows)} 个表格 → {args.output}")
    else:
        sheets = extract_text(args.input, args.pages, args.per_page)
        if not sheets:
            raise SystemExit("❌ 未提取到任何文字，可能是扫描件，请先做 OCR。")
        with pd.ExcelWriter(args.output, engine="openpyxl") as writer:
            for name, df in sheets.items():
                df.to_excel(writer, sheet_name=name[:31], index=False)
        print(f"\n✅ 文本提取完成 → {args.output}")


if __name__ == "__main__":
    main()
