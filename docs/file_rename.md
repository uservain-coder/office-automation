# 脚本 C：file_rename.py — 文件批量重命名 / 自动分类

**痛点**：下载文件夹一堆乱文件，要批量改名、按类型归类，手动拖到手软。

**核心能力**：一个脚本、两个动作。先把文件「批量改名」，或把文件「按类型自动归类」。

> 📁 配套脱敏示例：`../examples/file_rename/input/`
> 里面是 9 个**全假名**的演示文件（无任何真实隐私），专供你照着练手：
> ```
> IMG_001.jpg  IMG_002.jpg  IMG_003.png
> 销售_2023.pdf  销售_2024.pdf  说明文档.docx
> 会议笔记.txt  报表数据.csv  备份归档.zip
> ```

---

## 〇、执行前的固定姿势（重要）

```bash
# 1) 进入项目根目录（所有命令都从这里出发）
cd C:/Users/Baibaiusercoder/WorkBuddy/2026-07-31-09-24-24/office-automation

# 2) 用项目自带的 venv 跑（依赖都在这里，别用系统 Python）
.venv/Scripts/python.exe scripts/file_rename.py <参数>
```

**安全第一：脚本默认只打印预览，不修改/不移动任何文件。** 只有你显式加 `--yes` 才真动手。养成「先预览 → 核对 → 再加 `--yes`」的习惯，能救你无数次误删。

**作用范围**：只处理 `--input` 目录里的**一层文件**，不会递归进子文件夹。

---

## 一、动作 1：`rename`（批量改名）

按你选的「规则」把目录里所有文件名统一改造。需要三选一的规则：

| 规则 | 改名逻辑 | 必填附加参数 |
|------|---------|------------|
| `prefix` | 统一前缀 + 三位序号（资料_001） | `--prefix` |
| `date` | 文件修改日期 + 原名 | 无 |
| `regex` | 正则匹配替换（只换命中的片段） | `--pattern` + `--repl` |

### 1.1 规则 `prefix`：统一前缀 + 序号

给每个文件加上同一个前缀，后面跟 `001、002…` 三位序号（按目录里的排列顺序）。

**命令（预览）**
```bash
.venv/Scripts/python.exe scripts/file_rename.py rename ^
  --input ../examples/file_rename/input --rule prefix --prefix 资料
```
> 注：`^` 是 Windows 命令行换行符；在 Git Bash / PowerShell 里写一行即可，不用 `^`。

**真实预览输出**
```
🔍 预览（改名前请核对）：
   IMG_001.jpg   →  资料_001.jpg
   IMG_002.jpg   →  资料_002.jpg
   IMG_003.png   →  资料_003.png
   会议笔记.txt   →  资料_004.txt
   备份归档.zip   →  资料_005.zip
   报表数据.csv   →  资料_006.csv
   说明文档.docx  →  资料_007.docx
   销售_2023.pdf  →  资料_008.pdf
   销售_2024.pdf  →  资料_009.pdf

⚠ 以上为预览，未实际修改。确认无误请加 --yes 执行。
```

**真实执行（加 `--yes`）**
```bash
.venv/Scripts/python.exe scripts/file_rename.py rename ^
  --input ../examples/file_rename/input --rule prefix --prefix 资料 --yes
```
执行后目录变为：`资料_001.jpg … 资料_009.pdf`（共 9 个）。

**适用场景**：照片归档、资料统一编号、批量加项目前缀。

---

### 1.2 规则 `date`：修改日期 + 原名

用每个文件的「最后修改日期（YYYYMMDD）」做前缀，后面保留原名。适合按时间线整理。

**命令（预览）**
```bash
.venv/Scripts/python.exe scripts/file_rename.py rename ^
  --input ../examples/file_rename/input --rule date
```

**真实预览输出**
```
🔍 预览（改名前请核对）：
   IMG_001.jpg   →  20260808_IMG_001.jpg
   会议笔记.txt   →  20260808_会议笔记.txt
   报表数据.csv   →  20260808_报表数据.csv
   销售_2023.pdf  →  20260808_销售_2023.pdf
   ...（其余同理）

⚠ 以上为预览，未实际修改。确认无误请加 --yes 执行。
```

**真实执行**
```bash
.venv/Scripts/python.exe scripts/file_rename.py rename ^
  --input ../examples/file_rename/input --rule date --yes
```

**注意事项**
- 日期取的是**文件修改时间**，不是拍摄时间（照片拍摄时间需另用 EXIF 工具）。
- 同一天改的文件会全部带同一个日期前缀。

**适用场景**：把某天导出的截图/下载统一打上日期标记。

---

### 1.3 规则 `regex`：正则替换（只换命中的片段）

按正则表达式 `--pattern` 匹配文件名里的片段，替换成 `--repl`。**没匹配到的文件保持原名不动**。

**命令（预览）**
```bash
.venv/Scripts/python.exe scripts/file_rename.py rename ^
  --input ../examples/file_rename/input --rule regex --pattern "IMG" --repl "旅行"
```

**真实预览输出**
```
🔍 预览（改名前请核对）：
   IMG_001.jpg   →  旅行_001.jpg
   IMG_002.jpg   →  旅行_002.jpg
   IMG_003.png   →  旅行_003.png
   会议笔记.txt   →  会议笔记.txt        ← 没匹配 IMG，保持不变
   备份归档.zip   →  备份归档.zip        ← 没匹配，保持不变
   销售_2023.pdf  →  销售_2023.pdf       ← 没匹配，保持不变
   ...

⚠ 以上为预览，未实际修改。确认无误请加 --yes 执行。
```

**真实执行**
```bash
.venv/Scripts/python.exe scripts/file_rename.py rename ^
  --input ../examples/file_rename/input --rule regex --pattern "IMG" --repl "旅行" --yes
```

**注意事项**
- 这是「**替换命中文字**」，不是「整体重命名」。文件名里没有 `IMG` 这个片段的，原样不动（也不会报错）。
- `--pattern` 支持完整正则，比如想把 `销售_2023.pdf` 里的年份提掉：`--pattern "_\d{4}" --repl ""`。
- 想整批统一命名，用 `prefix` 规则更省心。

**适用场景**：把 `IMG_`、`sales`、`副本` 这类杂乱前缀统一替换成规范词。

---

## 二、动作 2：`classify`（按类型自动归类）

**不需要选规则**，直接给目录就行。脚本按扩展名把文件分进 4 个子文件夹（子文件夹会建在 `--input` 目录**内部**）：

| 子文件夹 | 收录扩展名 |
|---------|-----------|
| `图片` | .jpg .jpeg .png .gif .bmp .webp .svg |
| `文档` | .pdf .doc .docx .txt .md .ppt .pptx |
| `表格` | .xlsx .xls .csv |
| `其他` | 上面都没匹配的（兜底，比如 .zip .exe） |

**命令（预览）**
```bash
.venv/Scripts/python.exe scripts/file_rename.py classify ^
  --input ../examples/file_rename/input
```

**真实预览输出**
```
🔍 预览（分类前请核对）：
   IMG_001.jpg    →  图片/
   IMG_002.jpg    →  图片/
   IMG_003.png    →  图片/
   会议笔记.txt    →  文档/
   备份归档.zip    →  其他/
   报表数据.csv    →  表格/
   说明文档.docx   →  文档/
   销售_2023.pdf   →  文档/
   销售_2024.pdf   →  文档/

⚠ 以上为预览，未实际移动。确认无误请加 --yes 执行。
```

**真实执行（加 `--yes`，文件被真实移动到子目录）**
```bash
.venv/Scripts/python.exe scripts/file_rename.py classify ^
  --input ../examples/file_rename/input --yes
```
执行后目录结构：
```
input/
├── 图片/   IMG_001.jpg  IMG_002.jpg  IMG_003.png
├── 文档/   会议笔记.txt  说明文档.docx  销售_2023.pdf  销售_2024.pdf
├── 表格/   报表数据.csv
└── 其他/   备份归档.zip
```

**注意事项**
- `classify` 是**真实移动文件**到子目录，预览确认时重点看「其他」类里有没有你不想被混在一起的重要文件。
- 若目标子目录已存在同名文件，移动时会被**覆盖**。首次务必先预览。

**适用场景**：下载文件夹大扫除、桌面 999+ 文件按类型归位。

---

## 三、命令参数速查表

| 参数 | 必填 | 含义 |
|------|------|------|
| `rename` / `classify` | ✅ | 第一个位置参数，指定动作 |
| `--input` | ✅ | 目标目录（只处理其中一层文件） |
| `--rule` | rename 必填 | `prefix` / `date` / `regex` |
| `--prefix` | prefix 规则必填 | 前缀文字 |
| `--pattern` | regex 规则必填 | 匹配正则 |
| `--repl` | regex 规则必填 | 替换为 |
| `--yes` | 否 | 确认执行；**不加 = 仅预览** |

---

## 四、拿真实文件练手的建议步骤

1. **先备份**：把要整理的文件夹复制一份，在副本上操作。
2. **跑预览**：上述任意命令去掉 `--yes`，看打印的对照表。
3. **核对**：确认新旧名 / 分类归属无误。
4. **真执行**：末尾加 `--yes`。
5. **脱敏**：整理完敏感资料后，本地留一份即可，别 `git add` 进仓库。

---

## 五、适合谁用

任何被「桌面 999+ 文件」「下载文件夹一团乱」折磨过的同学。改脚本、加规则（比如新增文件类型映射）成本对你几乎为零——这也是你相比普通卖家的技术护城河。
