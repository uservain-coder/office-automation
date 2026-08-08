# -*- coding: utf-8 -*-
"""
统一注册「嵌入子集」的中文字体。

为什么需要它：
reportlab 默认字体（Helvetica 等）不含中文字形；用 CID 字体（如 STSong-Light）
虽能显示，但属于「非嵌入」字体，桌面阅读器自带字体包能看，网页阅读器
（腾讯文档 / 浏览器 PDF.js）没有该字体 → 中文整页空白 / 无法显示。

解决方案：注册一个本机 TrueType 中文字体（黑体）并「嵌入子集」，
字形数据直接打进 PDF，任何阅读器都能正常显示。所有生成 PDF 的脚本都
从这里取字体，保证「今后生成的 PDF 处处可显示」。
"""
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 字体名（PDF 内部引用名）
CN_FONT = "SimHei"

# 候选字体路径（Windows 常见中文字体，按优先级尝试）
_FONT_CANDIDATES = [
    (r"C:\Windows\Fonts\simhei.ttf", 0),   # 黑体（标准 TTF，首选）
    (r"C:\Windows\Fonts\simsun.ttc", 0),   # 宋体（TTC，需子字体索引）
    (r"C:\Windows\Fonts\msyh.ttc", 0),     # 微软雅黑（TTC，需子字体索引）
]


def register_cn_font():
    """注册并嵌入中文字体，返回字体名。重复调用安全（只注册一次）。"""
    if CN_FONT in pdfmetrics.getRegisteredFontNames():
        return CN_FONT
    for path, idx in _FONT_CANDIDATES:
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(CN_FONT, path, subfontIndex=idx))
            return CN_FONT
    raise SystemExit(
        "❌ 未在本机找到中文字体（simhei / simsun / msyh），"
        "无法生成可显示中文的 PDF。请安装任一中文 TrueType 字体后重试。"
    )


if __name__ == "__main__":
    print("字体名:", register_cn_font())
