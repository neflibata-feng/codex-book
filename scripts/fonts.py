# -*- coding: utf-8 -*-
"""跨平台字体查找与注册。

查找顺序：环境变量 CODEX_BOOK_CJK_FONT → 常见系统字体 → 报错并给出提示。
等宽、西文无衬线与符号字体统一使用 matplotlib 自带的 DejaVu 字体，保证各平台一致。

注意：ReportLab 只支持 TrueType 轮廓（glyf）的字体。思源/Noto CJK 的 OTF/TTC 多为
CFF 轮廓，无法嵌入；请改用微软雅黑、宋体、AR PL UMing、文泉驿微米黑等 TrueType 字体。
"""
import os

CJK_CANDIDATES = [
    os.environ.get("CODEX_BOOK_CJK_FONT"),
    # Windows
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simsun.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    # macOS
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    # Linux
    "/usr/share/fonts/cjkuni-uming/uming.ttc",
    "/usr/share/fonts/truetype/arphic/uming.ttc",
    "/usr/share/fonts/wqy-microhei/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
]


def mpl_font(name):
    """matplotlib 自带字体的路径（DejaVuSans.ttf 等）。"""
    import matplotlib
    return os.path.join(matplotlib.get_data_path(), "fonts", "ttf", name)


def find_cjk_font():
    for p in CJK_CANDIDATES:
        if p and os.path.exists(p):
            return p
    raise FileNotFoundError(
        "未找到可用的中文 TrueType 字体。请设置环境变量 CODEX_BOOK_CJK_FONT 指向一个 .ttf/.ttc 文件，"
        "例如 Windows 上的 C:\\Windows\\Fonts\\msyh.ttc。")


def register_pdf_fonts(text=""):
    """为 ReportLab 注册字体，返回 dict(regular, bold, symbols, mono, sans_bold, fallback)。"""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    errors = []
    cjk_name = None
    for p in [c for c in CJK_CANDIDATES if c and os.path.exists(c)]:
        try:
            font = TTFont("BookCJK", p, subfontIndex=0) if p.lower().endswith(".ttc") else TTFont("BookCJK", p)
            pdfmetrics.registerFont(font)
            cjk_name = "BookCJK"
            print(f"[fonts] 中文字体：{p}")
            break
        except Exception as e:  # CFF 轮廓等无法嵌入的字体
            errors.append(f"{p}: {e}")
    if not cjk_name:
        raise RuntimeError("中文字体注册失败：\n" + "\n".join(errors or ["未找到候选字体"]) +
                           "\n请设置 CODEX_BOOK_CJK_FONT 指向 TrueType 字体。")

    pdfmetrics.registerFont(TTFont("BookSym", mpl_font("DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("Mono", mpl_font("DejaVuSansMono.ttf")))
    pdfmetrics.registerFont(TTFont("SansB", mpl_font("DejaVuSans-Bold.ttf")))

    # 中文字体缺失的字符改用符号字体绘制
    cmap = pdfmetrics.getFont(cjk_name).face.charToGlyph
    fallback = {ch for ch in set(text) if ord(ch) > 127 and ord(ch) not in cmap}
    fallback |= set("›✓✗⌘⇧⌥⌃→←↑↓①②③④⑤⑥⑦⑧⑨▸▾▶●•…")
    fallback = {ch for ch in fallback if ord(ch) not in cmap or ch in "›⌘⇧⌥⌃✓✗"}
    return {"regular": cjk_name, "bold": cjk_name, "symbols": "BookSym", "mono": "Mono",
            "sans_bold": "SansB", "wordWrap": "CJK", "fallback": fallback}
