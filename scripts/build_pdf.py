# -*- coding: utf-8 -*-
"""把 book/chapters/*.md 排版为 O'Reilly 风格的 PDF（dist/codex_book.pdf）。

用法：python scripts/build_pdf.py
依赖：reportlab、matplotlib、Pillow（见 requirements.txt）
"""
import os, re, glob, html
from reportlab.lib.pagesizes import inch
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
                                NextPageTemplate, Table, TableStyle, KeepTogether, Image, Flowable,
                                CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fonts import register_pdf_fonts

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book")
CHAPTERS = os.path.join(BOOK, "chapters")
IMAGES = os.path.join(BOOK, "images")
PAGE_W, PAGE_H = 7 * inch, 9.19 * inch
ML, MR, MT, MB = 0.7 * inch, 0.66 * inch, 0.8 * inch, 0.72 * inch
FW = PAGE_W - ML - MR

NAVY = HexColor("#0B2545"); DEEP = HexColor("#1E5A8A"); PRI = HexColor("#C0E0FF"); ACC = HexColor("#38BDF8")
GRAY = HexColor("#F1F5F9"); MID = HexColor("#64748B"); LINE = HexColor("#CBD5E1"); INK = HexColor("#1F2937")
CODEBG = HexColor("#F4F7FB"); WARNC = HexColor("#F59E0B"); WARNBG = HexColor("#FFF7E6")
TIPC = HexColor("#10B981"); TIPBG = HexColor("#ECFDF5"); NOTEBG = HexColor("#EEF6FF")


def read_sources():
    files = sorted(glob.glob(os.path.join(CHAPTERS, "*.md")))
    return files, "\n\n".join(open(f, encoding="utf-8").read() for f in files)


FILES, ALL = read_sources()
FONTS = register_pdf_fonts(ALL)
BODY, BOLD, WRAP = FONTS["regular"], FONTS["bold"], FONTS["wordWrap"]
SYM = FONTS["symbols"]
FALLBACK = FONTS["fallback"]


def S(name, **kw):
    base = dict(fontName=BODY, fontSize=9.6, leading=14.9, textColor=INK, wordWrap=WRAP)
    base.update(kw)
    return ParagraphStyle(name, **base)


ST = {
    "body": S("body", alignment=TA_LEFT, spaceAfter=6.5, firstLineIndent=0),
    "h1": S("h1", fontSize=21, leading=28, textColor=NAVY, spaceAfter=4),
    "chapnum": S("chapnum", fontName="SansB", fontSize=12, leading=16, textColor=ACC),
    "h2": S("h2", fontSize=13.2, leading=18, textColor=NAVY, spaceBefore=10, spaceAfter=4),
    "h3": S("h3", fontSize=11.2, leading=16, textColor=DEEP, spaceBefore=8, spaceAfter=3),
    "li": S("li", alignment=TA_LEFT, leftIndent=16, bulletIndent=4, spaceAfter=2.5),
    "cap": S("cap", fontSize=8.8, leading=12.5, textColor=NAVY, alignment=TA_CENTER, spaceBefore=3),
    "src": S("src", fontSize=7.4, leading=10.5, textColor=MID, alignment=TA_CENTER, spaceAfter=8),
    "code": S("code", fontName="Mono", fontSize=7.9, leading=11.2, textColor=NAVY, wordWrap=WRAP),
    "th": S("th", fontSize=8.4, leading=11.5, textColor=white),
    "td": S("td", fontSize=8.4, leading=12, textColor=INK),
    "callout": S("callout", fontSize=9.2, leading=14.5, textColor=INK),
    "calllab": S("calllab", fontSize=9.2, leading=13, textColor=NAVY),
    "ref": S("ref", fontSize=8.2, leading=12.2, leftIndent=22, firstLineIndent=-22, spaceAfter=3, alignment=TA_LEFT),
}


# ---------------- inline markup ----------------
def fb(text):
    """escape + wrap fallback symbols."""
    out = []
    for ch in text:
        e = html.escape(ch, quote=False)
        out.append(f'<font name="{SYM}">{e}</font>' if ch in FALLBACK else e)
    return "".join(out)


def code_runs(text, size=None):
    out, cur, curf = [], [], None
    def flush():
        if cur:
            s = "".join(cur)
            out.append(f'<font name="{curf}">{s}</font>')
    for ch in text:
        if ch == " ":
            f = "Mono"; e = "&nbsp;"
        elif ord(ch) < 128:
            f = "Mono"; e = html.escape(ch, quote=False)
        elif ch in FALLBACK:
            f = SYM; e = html.escape(ch, quote=False)
        else:
            f = BODY; e = html.escape(ch, quote=False)
        if f != curf:
            flush(); cur = []; curf = f
        cur.append(e)
    flush()
    return "".join(out)


def inline(text):
    # 先标记粗体（粗体中可能含有行内代码），再处理行内代码
    text = text.replace("\\`", "\x03")  # Markdown 转义的反引号
    text = re.sub(r"\*\*(.+?)\*\*", "\x01\\1\x02", text)
    parts = re.split(r"(`[^`]+`)", text)
    res = []
    for p in parts:
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            res.append(f'<font color="#B4233C" size="-0.6">{code_runs(p[1:-1])}</font>')
        else:
            q = fb(p)
            q = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<i>\1</i>", q)
            q = re.sub(r"\[(\d+)\]", r'<font color="#1E5A8A" size="-1.5">[\1]</font>', q)
            res.append(q)
    s = "".join(res)
    return s.replace("\x01", '<font color="#0E4C86">').replace("\x02", "</font>").replace("\x03", "`")


def heading(text):
    """标题：行内代码用等宽字体显示，不保留反引号。"""
    out = []
    for p in re.split(r"(`[^`]+`)", text):
        out.append(code_runs(p[1:-1]) if p.startswith("`") and p.endswith("`") and len(p) > 1 else fb(p))
    return "".join(out)


# ---------------- flowables ----------------
class FauxBold(Flowable):
    """Draw a paragraph twice with a hair offset to simulate bold (no CJK bold face installed)."""
    def __init__(self, para, dx=0.32, toc=None, bookmark=None):
        super().__init__(); self.para = para; self.dx = dx; self.toc = toc; self.bookmark = bookmark
    def wrap(self, aw, ah):
        self.w, self.h = self.para.wrap(aw, ah); return self.w, self.h
    def getSpaceBefore(self): return self.para.getSpaceBefore()
    def getSpaceAfter(self): return self.para.getSpaceAfter()
    def draw(self):
        self.para.drawOn(self.canv, 0, 0); self.para.drawOn(self.canv, self.dx, 0)


def bold_para(text, style, **kw):
    return FauxBold(Paragraph(text, style), **kw)


class Rule(Flowable):
    def __init__(self, w, color=ACC, t=1.6, sb=2, sa=10):
        super().__init__(); self.rw, self.color, self.t, self.sb, self.sa = w, color, t, sb, sa
    def wrap(self, aw, ah): return aw, self.t + self.sb + self.sa
    def draw(self):
        self.canv.setStrokeColor(self.color); self.canv.setLineWidth(self.t)
        self.canv.line(0, self.sa, self.rw, self.sa)


class PartPage(Flowable):
    def __init__(self, label, title, desc):
        super().__init__(); self.label, self.title, self.desc = label, title, desc
    def wrap(self, aw, ah): self.aw = aw; return aw, ah - 2
    def draw(self):
        c = self.canv
        p = Paragraph(fb(self.label), S("pl", fontSize=13, leading=18, textColor=ACC))
        w, h = p.wrap(self.aw, 100); p.drawOn(c, 0, 330)
        t = Paragraph(fb(self.title), S("pt", fontSize=30, leading=38, textColor=white))
        w, h = t.wrap(self.aw, 200); t.drawOn(c, 0, 280); t.drawOn(c, 0.45, 280)
        c.setStrokeColor(ACC); c.setLineWidth(2.2); c.line(0, 268, 70, 268)
        d = Paragraph(fb(self.desc), S("pd", fontSize=10.5, leading=17, textColor=PRI))
        w, h = d.wrap(self.aw * 0.85, 200); d.drawOn(c, 0, 250 - h)


class ChapterMark(Flowable):
    """Zero-size marker that records current chapter for running header & outline."""
    def __init__(self, title, key):
        super().__init__(); self.title, self.key = title, key
    def wrap(self, aw, ah): return 0, 0
    def draw(self):
        c = self.canv
        c.bookmarkPage(self.key); c.addOutlineEntry(self.title, self.key, level=0)
        c._doctemplate.cur_chapter = self.title


def callout(kind, text_lines):
    lab = {"TIP": ("提示", TIPC, TIPBG), "NOTE": ("注意", DEEP, NOTEBG), "WARNING": ("警告", WARNC, WARNBG)}[kind]
    paras = [bold_para(f'<font color="{lab[1].hexval().replace("0x", "#")}">{lab[0]}</font>', ST["calllab"])]
    body = " ".join(t.strip() for t in text_lines).strip()
    paras.append(Paragraph(inline(body), ST["callout"]))
    t = Table([[paras]], colWidths=[FW - 6])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), lab[2]), ("LINEBEFORE", (0, 0), (0, -1), 3, lab[1]),
                           ("LEFTPADDING", (0, 0), (-1, -1), 11), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return [Spacer(1, 4), t, Spacer(1, 8)]


def code_block(lines, lang=""):
    rows = [[Paragraph(code_runs(l.rstrip("\n")) if l.strip() else "&nbsp;", ST["code"])] for l in lines]
    t = Table(rows, colWidths=[FW - 4], splitByRow=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CODEBG), ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, 0), 6), ("BOTTOMPADDING", (0, -1), (-1, -1), 7)]))
    return [Spacer(1, 2), t, Spacer(1, 8)]


def md_table(rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], [r for r in cells[2:]]
    n = len(head)
    lens = [max(len(r[i]) if i < len(r) else 0 for r in [head] + body) for i in range(n)]
    lens = [min(max(l, 4), 40) for l in lens]
    tot = sum(lens); cw = [FW * l / tot for l in lens]
    data = [[bold_para(inline(h), ST["th"], dx=0.25) for h in head]]
    for r in body:
        data.append([Paragraph(inline(r[i] if i < len(r) else ""), ST["td"]) for i in range(n)])
    t = Table(data, colWidths=cw, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GRAY]),
                           ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE), ("BOX", (0, 0), (-1, -1), 0.6, NAVY),
                           ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                           ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                           ("FONTNAME", (0, 0), (-1, -1), BODY)]))
    return [Spacer(1, 4), t, Spacer(1, 10)]


def figure(cap, path, src):
    from PIL import Image as PI
    full = os.path.normpath(os.path.join(CHAPTERS, path))
    w, h = PI.open(full).size
    dw = FW * 0.9; dh = dw * h / w
    if dh > 3.5 * inch:
        dh = 3.5 * inch; dw = dh * w / h
    img = Image(full, width=dw, height=dh)
    return [Spacer(1, 4), KeepTogether([img, bold_para(fb(cap), ST["cap"], dx=0.22), Paragraph(inline(src), ST["src"])])]


# ---------------- markdown parser ----------------
def parse(md, chapter_counter):
    story = []
    lines = md.split("\n")
    i = 0; para = []
    if lines and lines[0].strip() == "---":
        j = lines.index("---", 1); i = j + 1

    def flush_para():
        nonlocal para
        if para:
            story.append(Paragraph(inline(" ".join(x.strip() for x in para)), ST["body"]))
            para = []

    while i < len(lines):
        ln = lines[i]; s = ln.strip()
        if s.startswith("<!-- part:"):
            flush_para()
            inner = s[len("<!-- part:"):-3].strip()
            lab, title, desc = [x.strip() for x in inner.split("|")]
            story += [NextPageTemplate("part"), PageBreak(), PartPage(lab, title, desc), NextPageTemplate("body")]
            i += 1; continue
        if s.startswith("<!--"):
            i += 1; continue
        if s.startswith("```"):
            flush_para(); lang = s[3:].strip(); buf = []; i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i]); i += 1
            story += code_block(buf, lang); i += 1; continue
        if s.startswith("# "):
            flush_para(); title = s[2:].strip()
            m = re.match(r"(第 \d+ 章|附录 [A-Z])\s*(.*)", title)
            chapter_counter[0] += 1; key = f"ch{chapter_counter[0]}"
            story += [NextPageTemplate("body"), PageBreak(), ChapterMark(title, key), Spacer(1, 0.35 * inch)]
            if m:
                story.append(Paragraph(m.group(1).replace(" ", " ").upper(), S("cn", fontSize=12.5, leading=17, textColor=ACC)))
                story.append(Spacer(1, 6))
                story.append(bold_para(fb(m.group(2)), ST["h1"], dx=0.45, toc=(0, title)))
            else:
                story.append(bold_para(fb(title), ST["h1"], dx=0.45, toc=(0, title)))
            story += [Rule(FW * 0.22), Spacer(1, 8)]
            i += 1; continue
        if s.startswith("## "):
            flush_para(); t = s[3:].strip()
            story.append(CondPageBreak(0.8 * inch))
            story.append(bold_para(heading(t), ST["h2"], dx=0.36, toc=(1, t.replace("`", ""))))
            i += 1; continue
        if s.startswith("### "):
            flush_para(); t = s[4:].strip()
            story.append(CondPageBreak(0.6 * inch))
            story.append(bold_para(heading(t), ST["h3"], dx=0.28))
            i += 1; continue
        m = re.match(r'!\[(.+?)\]\((.+?)\s+"(.+?)"\)', s)
        if m:
            flush_para(); story += figure(m.group(1), m.group(2), m.group(3)); i += 1; continue
        if s.startswith("> [!"):
            flush_para(); kind = re.match(r"> \[!(\w+)\]", s).group(1); buf = []; i += 1
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip()); i += 1
            story += callout(kind, buf); continue
        if s.startswith("|"):
            flush_para(); buf = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                buf.append(lines[i]); i += 1
            story += md_table(buf); continue
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", ln)
        if m and not s.startswith("**"):
            flush_para(); indent = len(m.group(1)); bullet = m.group(2); text = m.group(3)
            i += 1
            while i < len(lines) and lines[i].startswith("  ") and lines[i].strip() and not re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                text += " " + lines[i].strip(); i += 1
            b = "•" if bullet in "-*" else bullet
            st = ParagraphStyle("lix", parent=ST["li"], leftIndent=16 + indent * 6, bulletIndent=4 + indent * 6)
            story.append(Paragraph(inline(text), st, bulletText=b if b != "•" else None) if b != "•" else
                         Paragraph(inline(text), st, bulletText="•"))
            continue
        m = re.match(r"^\[(\d+)\]\s+(.*)", s)
        if m:
            flush_para(); story.append(Paragraph(f"[{m.group(1)}]&nbsp;&nbsp;" + inline(m.group(2)), ST["ref"])); i += 1; continue
        if not s:
            flush_para(); i += 1; continue
        para.append(s); i += 1
    flush_para()
    return story


# ---------------- document ----------------
class BookDoc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        super().__init__(fn, pagesize=(PAGE_W, PAGE_H), leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
                         title="Codex 实战指南", author="neflibata", subject="图形界面、子代理、跨 Harness 派工与云边协同", **kw)
        self.cur_chapter = ""
        fr = Frame(ML, MB, FW, PAGE_H - MT - MB, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        frp = Frame(ML + 0.1 * inch, MB, FW, PAGE_H - MT - MB, id="p", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate("cover", [fr], onPage=draw_cover),
                               PageTemplate("plain", [fr], onPage=lambda c, d: None),
                               PageTemplate("front", [fr], onPage=draw_front),
                               PageTemplate("part", [frp], onPage=draw_part),
                               PageTemplate("body", [fr], onPageEnd=draw_body)])

    def afterFlowable(self, f):
        if isinstance(f, FauxBold) and f.toc:
            lvl, text = f.toc
            self.notify("TOCEntry", (lvl, fb(text), self.page))


def draw_front(c, d):
    c.saveState(); c.setFont(BODY, 8.5); c.setFillColor(MID)
    c.drawCentredString(PAGE_W / 2, 0.45 * inch, str(d.page)); c.restoreState()


def toroman(n):
    vals = [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]; r = ""
    for v, s in vals:
        while n >= v: r += s; n -= v
    return r


def draw_body(c, d):
    c.saveState()
    pn = c.getPageNumber()
    c.setStrokeColor(LINE); c.setLineWidth(0.5)
    c.line(ML, PAGE_H - 0.55 * inch, PAGE_W - MR, PAGE_H - 0.55 * inch)
    c.setFont(BODY, 8); c.setFillColor(MID)
    if pn % 2 == 0:
        c.drawString(ML, PAGE_H - 0.48 * inch, "Codex 实战指南")
        c.drawRightString(PAGE_W - MR, PAGE_H - 0.48 * inch, d.cur_chapter)
    else:
        c.drawString(ML, PAGE_H - 0.48 * inch, d.cur_chapter)
        c.drawRightString(PAGE_W - MR, PAGE_H - 0.48 * inch, "Codex 实战指南")
    c.setFillColor(NAVY); c.setFont("SansB", 9)
    c.drawCentredString(PAGE_W / 2, 0.45 * inch, str(pn))
    c.setFillColor(ACC); c.rect(PAGE_W / 2 - 9, 0.38 * inch - 4, 18, 1.4, stroke=0, fill=1)
    c.restoreState()


def draw_part(c, d):
    c.saveState(); c.setFillColor(NAVY); c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(ACC); c.rect(0, PAGE_H - 0.18 * inch, PAGE_W, 0.18 * inch, stroke=0, fill=1)
    c.restoreState()


def draw_cover(c, d):
    c.saveState()
    c.setFillColor(white); c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # top band
    c.setFillColor(NAVY); c.rect(0, PAGE_H - 0.5 * inch, PAGE_W, 0.5 * inch, stroke=0, fill=1)
    c.setFillColor(white); c.setFont("SansB", 9.5)
    c.drawString(0.45 * inch, PAGE_H - 0.31 * inch, "AI ENGINEERING IN PRACTICE")
    c.setFont(BODY, 9); c.drawRightString(PAGE_W - 0.45 * inch, PAGE_H - 0.31 * inch, "面向开发者的编程代理实战")
    # illustration
    img = os.path.join(IMAGES, "cover_octopus.png")
    if os.path.exists(img):
        c.drawImage(img, 0.95 * inch, PAGE_H - 4.95 * inch, width=5.1 * inch, height=4.3 * inch, preserveAspectRatio=True, mask="auto")
    # title block
    bh = 3.15 * inch
    c.setFillColor(PRI); c.rect(0, 0.95 * inch, PAGE_W, bh, stroke=0, fill=1)
    c.setFillColor(ACC); c.rect(0, 0.95 * inch + bh, PAGE_W, 0.07 * inch, stroke=0, fill=1)
    t = Paragraph("Codex 实战指南", S("ct", fontSize=40, leading=48, textColor=NAVY))
    t.wrap(PAGE_W - 0.9 * inch, 100); y = 0.95 * inch + bh - 0.95 * inch
    for dx in (0, 0.5, 1.0): t.drawOn(c, 0.45 * inch + dx, y)
    sub = Paragraph(fb("图形界面 · 子代理 · 跨 Harness 派工 · 云边协同"), S("cs", fontSize=14.5, leading=20, textColor=DEEP))
    sub.wrap(PAGE_W - 0.9 * inch, 100); sub.drawOn(c, 0.45 * inch, y - 0.45 * inch); sub.drawOn(c, 0.45 * inch + 0.3, y - 0.45 * inch)
    tag = Paragraph(fb("与 AI 编程代理高效协作：从第一个任务到一支代理团队"), S("cg", fontSize=10.5, leading=15, textColor=NAVY))
    tag.wrap(PAGE_W - 0.9 * inch, 100); tag.drawOn(c, 0.45 * inch, y - 1.05 * inch)
    c.setStrokeColor(NAVY); c.setLineWidth(1.2); c.line(0.45 * inch, y - 1.35 * inch, 1.6 * inch, y - 1.35 * inch)
    # footer
    c.setFillColor(NAVY); c.rect(0, 0, PAGE_W, 0.95 * inch, stroke=0, fill=1)
    c.setFillColor(white); c.setFont(BODY, 13); c.drawString(0.45 * inch, 0.5 * inch, "neflibata　著")
    c.setFont(BODY, 9); c.setFillColor(PRI)
    c.drawRightString(PAGE_W - 0.45 * inch, 0.52 * inch, "第 1 版 · 2026 年 11 月")
    c.restoreState()


def front_matter():
    st = []
    # cover occupies first page via template 'cover'
    st += [Spacer(1, 1), NextPageTemplate("plain"), PageBreak()]
    # copyright page
    cp = ["<b>Codex 实战指南：图形界面、子代理、跨 Harness 派工与云边协同</b>",
          "作者：neflibata",
          "版次：第 1 版，2026 年 11 月",
          "源文件：本书以 Markdown 撰写，源码见 book/chapters/*.md，排版与绘图脚本见 scripts/。",
          "许可：本书采用知识共享 署名-非商业性使用 4.0 国际许可协议（CC BY-NC 4.0）发布，可自由分享与改编，须署名，禁止商业用途。商业授权请联系作者。",
          "开源地址：https://github.com/neflibata-feng/codex-practical-guide",
          "内容依据：OpenAI 于 2026 年 11 月公开的 Codex 官方文档，具体条目见书末参考文献。产品界面、模型名称与默认值可能随版本变化，请以应用内显示与官方文档为准。",
          "图片说明：书中示意图均由作者依据参考文献原创绘制，非产品真实截图；封面版画风格插图由 AI 图像生成工具创作。详见附录“图片版权与来源”。",
          "商标声明：OpenAI、ChatGPT、Codex 是 OpenAI 的商标；GitHub、Slack、Visual Studio Code、JetBrains、Xcode、Zed、Kiro、AWS 等名称为其各自所有者的商标。本书为独立出版物，与上述公司无关联，亦未获其背书。",
          "免责声明：作者已尽力确保内容准确，但对因使用本书信息造成的任何损失不承担责任。在生产环境中授予编程代理权限前，请务必理解其安全模型并做好备份。"]
    st += [Spacer(1, 0.9 * inch), bold_para("Codex 实战指南", S("tt", fontSize=26, leading=34, textColor=NAVY), dx=0.45), Spacer(1, 6), Paragraph(fb("图形界面、子代理、跨 Harness 派工与云边协同"), S("ts", fontSize=12.5, leading=18, textColor=DEEP)), Rule(FW * 0.25, sb=6, sa=12), Paragraph("neflibata　著", S("ta", fontSize=11, leading=16, textColor=INK)), Spacer(1, 1.6 * inch)]
    for p in cp:
        st.append(Paragraph(fb(p).replace("&lt;b&gt;", '<font color="#0B2545">').replace("&lt;/b&gt;", "</font>"),
                            S("cp", fontSize=8.2, leading=13, textColor=MID, spaceAfter=5)))
    st += [NextPageTemplate("front"), PageBreak()]
    # TOC
    toc = TableOfContents()
    toc.levelStyles = [S("t0", fontSize=10, leading=15, textColor=NAVY, leftIndent=0, spaceBefore=3),
                       S("t1", fontSize=8.4, leading=11.6, textColor=INK, leftIndent=18)]
    toc.dotsMinLevel = 0
    st += [Spacer(1, 0.3 * inch), bold_para("目录", ST["h1"], dx=0.45), Rule(FW * 0.22), Spacer(1, 6), toc]
    return st


def build(out_name="codex_book.pdf", final=True):
    story = front_matter()
    counter = [0]
    for f in FILES:
        story += parse(open(f, encoding="utf-8").read(), counter)
    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    out = os.path.join(ROOT, "dist", out_name)
    doc = BookDoc(out)
    if final:
        doc.multiBuild(story, maxPasses=4)
    else:
        doc.build(story)
    return out


if __name__ == "__main__":
    path = build()
    print(f"已生成：{path}")
