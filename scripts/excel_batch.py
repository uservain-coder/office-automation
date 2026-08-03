#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
脚本 A：Excel 批量处理
功能：把多个 .xlsx 按四种模式处理
  - merge  : 纵向合并（多表上下拼成一张总表）
  - concat : 横向拼接（按行号左右拼）
  - split  : 按某一列的值拆分到多个文件
  - dedup  : 按某一列去重
适用痛点：每月要把 10 个分公司报表合并、或按部门拆分工单。
依赖：pandas / openpyxl / tqdm
用法见文件底部示例。
"""
import argparse
import glob
import os
import sys
from tqdm import tqdm

import pandas as pd


def collect_files(input_path):
    """把输入的「目录」或「通配符」收集成文件列表。"""
    if os.path.isdir(input_path):
        files = sorted(glob.glob(os.path.join(input_path, "*.xlsx")))
        # 排除临时文件（~$ 开头是 Excel 打开中的锁文件）
        files = [f for f in files if not os.path.basename(f).startswith("~$")]
    else:
        files = sorted(glob.glob(input_path))
    files = [f for f in files if f.lower().endswith((".xlsx", ".xls"))]
    if not files:
        raise SystemExit("❌ 没找到任何 Excel 文件，请检查 --input 路径")
    return files


def load_all(files, sheet):
    """逐个读取并打印空值统计，返回 DataFrame 列表。"""
    frames = []
    print(f"📂 读取 {len(files)} 个文件：")
    for f in tqdm(files, desc="读取"):
        df = pd.read_excel(f, sheet_name=sheet if sheet else 0)
        na = int(df.isna().sum().sum())
        frames.append(df)
        tqdm.write(f"   ✓ {os.path.basename(f)}  行数={len(df)} 空值={na}")
    return frames


def do_merge(frames, output):
    big = pd.concat(frames, ignore_index=True)
    big.to_excel(output, index=False)
    return len(big), len(frames)


def do_concat(frames, output):
    # 横向拼接：补齐列名避免冲突
    renamed = []
    for i, df in enumerate(frames):
        df = df.copy()
        df.columns = [f"{c}__表{i+1}" for c in df.columns]
        renamed.append(df)
    big = pd.concat(renamed, axis=1)
    big.to_excel(output, index=False)
    return big.shape[0], len(frames)


def do_split(frames, output, key):
    big = pd.concat(frames, ignore_index=True)
    if key not in big.columns:
        raise SystemExit(f"❌ 拆分列 '{key}' 不在数据中，可用列：{list(big.columns)}")
    os.makedirs(output, exist_ok=True)
    n = 0
    for val, grp in tqdm(big.groupby(key), desc="拆分"):
        safe = str(val).replace("/", "_").replace("\\", "_")
        grp.to_excel(os.path.join(output, f"{safe}.xlsx"), index=False)
        n += 1
    return n, len(big)


def do_dedup(frames, output, key):
    big = pd.concat(frames, ignore_index=True)
    if key not in big.columns:
        raise SystemExit(f"❌ 去重列 '{key}' 不在数据中，可用列：{list(big.columns)}")
    before = len(big)
    big = big.drop_duplicates(subset=[key], keep="first")
    big.to_excel(output, index=False)
    return before - len(big), len(big)


def main():
    p = argparse.ArgumentParser(description="Excel 批量处理：合并/拼接/拆分/去重")
    p.add_argument("--mode", required=True, choices=["merge", "concat", "split", "dedup"],
                   help="处理模式")
    p.add_argument("--input", required=True, help="Excel 文件所在目录，或通配符如 './data/*.xlsx'")
    p.add_argument("--output", required=True, help="输出文件路径（split 模式为输出目录）")
    p.add_argument("--key", help="split/dedup 模式用的列名")
    p.add_argument("--sheet", help="指定读取的 sheet 名（默认第一个）")
    args = p.parse_args()

    files = collect_files(args.input)
    frames = load_all(files, args.sheet)

    if args.mode == "merge":
        rows, n = do_merge(frames, args.output)
        print(f"\n✅ 合并完成：{n} 个文件 → {rows} 行，已存 {args.output}")
    elif args.mode == "concat":
        rows, n = do_concat(frames, args.output)
        print(f"\n✅ 横向拼接完成：{n} 个文件 → {rows} 行，已存 {args.output}")
    elif args.mode == "split":
        if not args.key:
            raise SystemExit("❌ split 模式必须指定 --key 列名")
        n, total = do_split(frames, args.output, args.key)
        print(f"\n✅ 拆分完成：共 {total} 行 → 按 '{args.key}' 拆成 {n} 个文件，目录 {args.output}")
    elif args.mode == "dedup":
        if not args.key:
            raise SystemExit("❌ dedup 模式必须指定 --key 列名")
        removed, kept = do_dedup(frames, args.output, args.key)
        print(f"\n✅ 去重完成：删除 {removed} 行重复，保留 {kept} 行，已存 {args.output}")


if __name__ == "__main__":
    main()
