#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
脚本 C：文件批量重命名 / 自动分类
功能1（rename）：按三种规则批量改名
  - prefix : 前缀 + 序号（如 报告_001.pdf）
  - date   : 日期(修改时间) + 原名
  - regex  : 正则替换（--pattern / --repl）
功能2（classify）：按扩展名自动归类到 图片/文档/表格/其他 子目录
安全第一：重命名前先 --dry-run 打印预览，加 --yes 才真执行，绝不静默删改。
依赖：仅标准库（pathlib / re）
"""
import argparse
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

CATEGORY = {
    "图片": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "文档": {".pdf", ".doc", ".docx", ".txt", ".md", ".ppt", ".pptx"},
    "表格": {".xlsx", ".xls", ".csv"},
    "其他": set(),  # 兜底
}


def preview_rename(files, rule, prefix, pattern, repl):
    plan = []
    for i, f in enumerate(files, 1):
        p = Path(f)
        if rule == "prefix":
            new = f"{prefix}_{i:03d}{p.suffix}"
        elif rule == "date":
            mt = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y%m%d")
            new = f"{mt}_{p.name}"
        elif rule == "regex":
            new = re.sub(pattern, repl, p.name)
        else:
            new = p.name
        plan.append((p.name, new))
    return plan


def preview_classify(files):
    plan = []
    for f in files:
        p = Path(f)
        ext = p.suffix.lower()
        cate = "其他"
        for name, exts in CATEGORY.items():
            if ext in exts:
                cate = name
                break
        plan.append((p.name, cate))
    return plan


def main():
    p = argparse.ArgumentParser(description="文件批量重命名 / 分类")
    p.add_argument("action", choices=["rename", "classify"], help="rename=改名 / classify=按类型归类")
    p.add_argument("--input", required=True, help="目标目录")
    p.add_argument("--rule", choices=["prefix", "date", "regex"], help="rename 规则")
    p.add_argument("--prefix", help="prefix 规则用的前缀")
    p.add_argument("--pattern", help="regex 规则：匹配正则")
    p.add_argument("--repl", help="regex 规则：替换为")
    p.add_argument("--yes", action="store_true", help="确认执行（不加只预览）")
    args = p.parse_args()

    if not os.path.isdir(args.input):
        raise SystemExit(f"❌ 目录不存在：{args.input}")

    files = [str(p) for p in Path(args.input).iterdir() if p.is_file()]

    if args.action == "rename":
        if not args.rule:
            raise SystemExit("❌ rename 需要 --rule")
        if args.rule == "prefix" and not args.prefix:
            raise SystemExit("❌ prefix 规则需要 --prefix")
        if args.rule == "regex" and not (args.pattern and args.repl):
            raise SystemExit("❌ regex 规则需要 --pattern 和 --repl")
        plan = preview_rename(files, args.rule, args.prefix, args.pattern, args.repl)
        print("🔍 预览（改名前请核对）：")
        for old, new in plan:
            print(f"   {old}  →  {new}")
        if not args.yes:
            print("\n⚠ 以上为预览，未实际修改。确认无误请加 --yes 执行。")
            return
        for old, new in plan:
            shutil.move(os.path.join(args.input, old), os.path.join(args.input, new))
        print(f"\n✅ 已重命名 {len(plan)} 个文件")

    else:  # classify
        plan = preview_classify(files)
        print("🔍 预览（分类前请核对）：")
        for name, cate in plan:
            print(f"   {name}  →  {cate}/")
        if not args.yes:
            print("\n⚠ 以上为预览，未实际移动。确认无误请加 --yes 执行。")
            return
        for name, cate in plan:
            dst = os.path.join(args.input, cate)
            os.makedirs(dst, exist_ok=True)
            shutil.move(os.path.join(args.input, name), os.path.join(dst, name))
        print(f"\n✅ 已分类 {len(plan)} 个文件")


if __name__ == "__main__":
    main()
