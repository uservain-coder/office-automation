# 脚本 A：excel_batch.py — Excel 批量处理

**痛点**：每月要把 10 个分公司报表合并成总表，或按部门拆分工单，手动复制粘贴又慢又错。

## 四种模式
| 模式 | 作用 | 必须参数 |
|------|------|----------|
| `merge` | 多文件纵向合并成一张总表 | — |
| `concat` | 多文件按行号横向拼接 | — |
| `split` | 按某一列的值拆成多个文件 | `--key` |
| `dedup` | 按某一列去重 | `--key` |

## 示例命令
```bash
# 合并某个目录下所有 xlsx
python scripts/excel_batch.py --mode merge --input "examples/excel/sales_*.xlsx" --output examples/out_merged.xlsx

# 按「部门」列拆分
python scripts/excel_batch.py --mode split --input examples/excel/by_dept.xlsx --output examples/out_split --key 部门

# 按「姓名」去重
python scripts/excel_batch.py --mode dedup --input examples/excel/by_dept.xlsx --output examples/out_dedup.xlsx --key 姓名
```

## 参数
- `--input`：目录 或 通配符（如 `./data/*.xlsx`）
- `--output`：输出文件（split 模式为输出目录）
- `--key`：split/dedup 用的列名
- `--sheet`：指定读取的 sheet 名（默认第一个）

## 输出
合并/去重 → 单个 xlsx；拆分 → 按列值命名的多个 xlsx。运行时会打印每个文件的行数与空值数。

## 适合谁用
每月要汇总多家分公司 / 多个部门报表的财务、运营同学。
