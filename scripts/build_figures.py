"""重新绘制全部示意图到 book/images/。

用法：python scripts/build_figures.py
（封面插图 cover_octopus.png 为 AI 生成，不由脚本绘制。）
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

for name in ("figures_ch01_03.py", "figures_ch04_10.py"):
    path = os.path.join(HERE, name)
    with open(path, encoding="utf-8") as fh:
        code = compile(fh.read(), path, "exec")
    exec(code, {"__file__": path, "__name__": "__main__"})
print("示意图已更新：book/images/")
