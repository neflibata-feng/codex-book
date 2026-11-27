# Codex 实战指南：图形界面、子代理、跨 Harness 派工与云边协同

一本 O'Reilly 风格的中文开源技术书，讲如何清晰、安全、高效地使用 OpenAI Codex。

- **以图形界面为主线**：主要讲 ChatGPT 桌面应用里的 Codex，以及 IDE 扩展、Web 和移动端；命令行只在第 10 章做一页速成。
- **三个重点**：子代理编排、跨 Harness 派工（Codex 既能被调度，也能去调度别人）、云边协同。
- **图文并茂**：18 幅原创示意图，每幅都有图题和来源说明；书末附 35 条参考文献（GB/T 7714 格式）。
- **篇幅**：PDF 共 65 页。内容依据 2026 年 11 月公开的 OpenAI 官方文档。

📖 **直接阅读：[dist/codex_book.pdf](dist/codex_book.pdf)** · 仓库地址：https://github.com/neflibata-feng/codex-book

## 目录

| 部分 | 章节 |
|---|---|
| 前言 | 本书适合谁 · 如何组织 · 排版约定 · 版本说明 |
| 第一部分 GUI 入门 | 第 1 章 认识 Codex<br>第 2 章 桌面应用上手：界面导览与第一个任务<br>第 3 章 把话说清楚，把权放对 |
| 第二部分 并行与子代理 | 第 4 章 并行工作：多会话、Worktree 与本地环境<br>第 5 章 子代理：把一个代理变成一支团队 |
| 第三部分 GUI 进阶能力 | 第 6 章 让 Codex 看见并操作：浏览器、Computer Use、评审与扩展 |
| 第四部分 跨 Harness 派工 | 第 7 章 跨 Harness 派工：被调度与去调度 |
| 第五部分 云边协同 | 第 8 章 Codex Cloud：把任务交给云端<br>第 9 章 云边协同工作流 |
| 补充 | 第 10 章 IDE、CLI 速成与最佳实践 |
| 附录 | A 斜杠命令与快捷键速查 · B 配置样例 · 参考文献与图片来源 |

## 仓库结构

```
codex-book/
├── book/
│   ├── chapters/          # 正文 Markdown 源稿（按文件名顺序拼接成书）
│   └── images/            # 示意图（PNG）与封面插图
├── scripts/
│   ├── build_pdf.py       # Markdown → PDF 排版
│   ├── build_figures.py   # 重新绘制全部示意图
│   ├── figures_ch01_03.py # 第 1～3 章示意图
│   ├── figures_ch04_10.py # 第 4～10 章示意图
│   ├── figlib.py          # 绘图公共函数
│   └── fonts.py           # 跨平台字体查找
├── dist/
│   └── codex_book.pdf     # 构建好的成品
├── LICENSE                # CC BY-NC 4.0（禁止商用）
├── LICENSE-CONTENT.md     # 许可的中文说明
├── NOTICE.md              # 商标、图片来源与免责声明
└── requirements.txt
```

## 自行构建

需要 Python 3.10 或更高版本。

```bash
pip install -r requirements.txt

# （可选）修改了示意图脚本后，重新绘图
python scripts/build_figures.py

# 排版生成 dist/codex_book.pdf
python scripts/build_pdf.py
```

### 中文字体

脚本会按以下顺序自动查找中文字体：环境变量 `CODEX_BOOK_CJK_FONT`，然后是 Windows 的微软雅黑或宋体、macOS 的宋体（Songti）或 Arial Unicode、Linux 的 AR PL UMing 或文泉驿微米黑。

ReportLab 只能嵌入 **TrueType 轮廓**的字体。思源黑体和 Noto Sans CJK 这类 OTF/TTC 字体多为 CFF 轮廓，无法使用。如果自动查找失败，请手动指定字体：

```powershell
# Windows PowerShell
$env:CODEX_BOOK_CJK_FONT = "C:\Windows\Fonts\msyh.ttc"
python scripts/build_pdf.py
```

```bash
# macOS / Linux
CODEX_BOOK_CJK_FONT=/path/to/font.ttc python scripts/build_pdf.py
```

等宽字体、西文字体和符号字体统一使用 matplotlib 自带的 DejaVu 字体，无需另外安装。换一种中文字体后，分页可能与 `dist/` 里的成品略有不同。

### 写作约定

源稿使用标准 Markdown，在 GitHub 上可以直接预览。另外有几条本书专用的约定：

| 写法 | 含义 |
|---|---|
| `# 第 N 章 标题` | 新起一章（另起一页，并加入目录） |
| `<!-- part: 第X部分 \| 标题 \| 说明 -->` | 插入深色的“部分”扉页 |
| `> [!TIP]` / `> [!NOTE]` / `> [!WARNING]` | 提示框、注意框、警告框（GitHub 也能渲染） |
| `![图 X-Y 图题](../images/x.png "来源：……")` | 插图：图题放在方括号里，来源说明写在引号里 |
| `[12]` | 引用书末第 12 条参考文献 |

## 许可

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

本仓库全部内容（正文、插图、PDF 与脚本）采用 [CC BY-NC 4.0](LICENSE-CONTENT.md) 许可：**可以自由分享和改编，但须署名，且禁止商业用途**。如需商业授权，请先[提交 Issue](https://github.com/neflibata-feng/codex-practical-guide/issues) 联系作者。

商标、封面插图来源与免责声明见 [NOTICE.md](NOTICE.md)。

## 贡献

Codex 迭代很快，欢迎提交 Issue 或 PR 来更正过时的内容。提交 PR 即表示你同意你的贡献以 CC BY-NC 4.0 许可发布。提交时请：

1. 在相应的 `book/chapters/*.md` 中修改；新增的事实陈述请附上参考文献编号；
2. 新增参考文献时，按 GB/T 7714 格式追加到“参考文献”一节末尾，并保持编号连续；
3. 新增示意图时，在 `scripts/figures_*.py` 中绘制，并在“图片版权与来源”表中登记；
4. 本地运行 `python scripts/build_pdf.py`，确认 PDF 能正常生成。

## 声明

本书是独立出版物，与 OpenAI 没有关联，也未获其背书。书中界面示意图由作者根据官方文档绘制，**不是产品截图**。产品界面、模型名称和默认值以应用内显示和官方文档为准。
