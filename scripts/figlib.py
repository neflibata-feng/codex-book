"""示意图公共绘图函数（matplotlib）。"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.font_manager import FontProperties
import matplotlib.patheffects as pe

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fonts import find_cjk_font
FONT = find_cjk_font()
from matplotlib import font_manager as _fm
_fm.fontManager.addfont(FONT)
_name = FontProperties(fname=FONT).get_name()
FP = FontProperties(family=[_name, "DejaVu Sans"])
NAVY = "#0B2545"; PRI = "#C0E0FF"; ACC = "#38BDF8"; GRAY = "#F1F5F9"; MID = "#64748B"
LINE = "#94A3B8"; WARN = "#F59E0B"; OK = "#10B981"; RED = "#EF4444"; WHITE = "#FFFFFF"
DEEP = "#1E5A8A"

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "book", "images")
os.makedirs(OUT, exist_ok=True)


def canvas(w=6.4, h=3.6):
    fig = plt.figure(figsize=(w, h), dpi=220)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w * 10); ax.set_ylim(0, h * 10); ax.axis("off")
    return fig, ax


def T(ax, x, y, s, size=8, color=NAVY, bold=False, ha="center", va="center", **kw):
    t = ax.text(x, y, s, fontproperties=FP, fontsize=size, color=color, ha=ha, va=va, **kw)
    if bold:
        t.set_path_effects([pe.withStroke(linewidth=0.55, foreground=color)])
    return t


def box(ax, x, y, w, h, text="", fc=WHITE, ec=NAVY, size=8, tc=NAVY, bold=False, lw=1.0, r=1.2, ls="-", z=2):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, ls=ls, zorder=z)
    ax.add_patch(p)
    if text:
        T(ax, x + w / 2, y + h / 2, text, size=size, color=tc, bold=bold, zorder=z + 1)
    return p


def arrow(ax, x1, y1, x2, y2, color=NAVY, lw=1.1, style="-|>", rad=0.0, ls="-", ms=9, z=1):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms, color=color, lw=lw,
                        connectionstyle=f"arc3,rad={rad}", ls=ls, zorder=z)
    ax.add_patch(a)
    return a


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=220, facecolor="white")
    plt.close(fig)
    return p
