# 脚本 C：file_rename.py — 文件批量重命名 / 自动分类

**痛点**：下载文件夹一堆乱文件，要批量改名、按类型归类，手动拖到手软。

## 两种动作
| 动作 | 作用 |
|------|------|
| `rename` | 按规则批量改名 |
| `classify` | 按扩展名自动归类到 图片/文档/表格/其他 子目录 |

## rename 三种规则
| 规则 | 说明 | 附加参数 |
|------|------|----------|
| `prefix` | 前缀 + 序号（报表_001.pdf） | `--prefix` |
| `date` | 修改日期 + 原名 | — |
| `regex` | 正则替换 | `--pattern` `--repl` |

## 示例命令
```bash
# 正则改名（预览，不加 --yes 不执行）
python scripts/file_rename.py rename --input ./待整理 --rule regex --pattern "sales" --repl "报表"

# 按类型分类（预览）
python scripts/file_rename.py classify --input ./待整理
```

## ⚠️ 安全第一
**默认只打印预览，绝不修改文件**。确认无误后加 `--yes` 才真正执行。避免误删误改。

## 适合谁用
任何被「桌面 999+ 文件」折磨过的同学。
