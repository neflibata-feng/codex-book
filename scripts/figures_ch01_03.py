"""绘制第 1～3 章示意图。"""
from figlib import *

# ---------- 1-1 入口全景
fig, ax = canvas(6.4, 3.7)
box(ax, 24, 14, 16, 8, "Codex 代理核心\n（Harness：代理循环\n+ 工具 + 沙箱）", fc=NAVY, ec=NAVY, tc=WHITE, size=8.5, bold=True, r=1.5)
items = [
 (3, 27, "ChatGPT 桌面应用", "多项目并行 · Worktree\n差异面板 · Computer Use"),
 (45, 27, "IDE 扩展", "VS Code / Cursor\nJetBrains / Xcode"),
 (3, 2, "Web · 移动端", "Codex Cloud 任务\n手机远程控制"),
 (45, 2, "CLI / SDK", "终端 TUI · codex exec\nTypeScript / Python SDK"),
]
for x, y, t, s in items:
    box(ax, x, y, 16, 7, "", fc=PRI, ec=DEEP, r=1.2)
    T(ax, x+8, y+5, t, size=8.2, bold=True)
    T(ax, x+8, y+2.3, s, size=6.4, color=DEEP)
arrow(ax, 19, 29, 25, 22, color=DEEP); arrow(ax, 45, 29, 39, 22, color=DEEP)
arrow(ax, 19, 7, 25, 14, color=DEEP); arrow(ax, 45, 7, 39, 14, color=DEEP)
T(ax, 32, 35.2, "同一套配置层：config.toml · AGENTS.md · Skills · MCP", size=7, color=MID)
T(ax, 32, 11.2, "共享会话 · 共享权限模型", size=6.5, color=MID)
save(fig, "fig1_1.png")

# ---------- 1-2 代理循环
fig, ax = canvas(6.4, 3.4)
nodes = [(8, 17, "① 用户输入\n任务与上下文"), (25, 27, "② 模型推理\n（Responses API）"),
         (46, 17, "③ 工具调用\n读文件·跑命令·改代码"), (25, 5, "④ 结果回填\n追加到提示")]
for x, y, s in nodes:
    box(ax, x, y, 13, 6, s, fc=PRI if "②" not in s else NAVY, ec=DEEP, tc=NAVY if "②" not in s else WHITE, size=7.4, bold=True)
arrow(ax, 21, 21.5, 26, 27, color=DEEP, rad=-0.2)
arrow(ax, 38, 29, 48, 23, color=DEEP, rad=-0.2)
arrow(ax, 50, 17, 38, 9, color=DEEP, rad=-0.2)
arrow(ax, 27, 11, 29, 27, color=ACC, rad=0.0, lw=1.4)
T(ax, 34, 17.5, "循环直到\n不再请求工具", size=6.8, color=ACC, bold=True)
box(ax, 2, 27.5, 18, 5, "⑤ 助手消息：\n“我已完成……”→ 交还控制权", fc=GRAY, ec=LINE, size=6.6)
arrow(ax, 25, 31, 20, 30.5, color=MID, ls="--")
T(ax, 52, 5.5, "一次“轮次”(turn) 可包含\n多次 推理↔工具 往返", size=6.5, color=MID)
save(fig, "fig1_2.png")

# ---------- 2-1 桌面应用界面分区
fig, ax = canvas(6.4, 4.0)
box(ax, 1, 1, 62, 38, "", fc=WHITE, ec=NAVY, lw=1.3, r=1.0)
box(ax, 1, 35, 62, 4, "", fc=GRAY, ec=NAVY, r=0.6)
T(ax, 4, 37, "● ● ●", size=6, color=MID, ha="left")
box(ax, 20, 35.6, 22, 2.8, "Hand off · 打开于 VS Code · ▶ Run", fc=PRI, ec=DEEP, size=6.2)
T(ax, 61, 37, "顶栏动作（本地环境 Actions）", size=6, color=DEEP, ha="right")
box(ax, 1, 1, 13, 34, "", fc=GRAY, ec=NAVY, r=0.6)
side = ["＋ 新建对话", "项目 ▸ storefront", "  · 修复结账 Bug", "  · 新增筛选器", "已置顶", "Code Review", "Scheduled", "Skills / Plugins", "设置"]
for i, s in enumerate(side):
    T(ax, 2.5, 32.5 - i*3.2, s, size=6.2, ha="left", color=NAVY if i else DEEP, bold=(i in (0, 1)))
box(ax, 15, 10, 28, 24.5, "", fc=WHITE, ec=LINE, r=0.6)
T(ax, 16, 32.5, "聊天区：计划、命令输出、子代理活动", size=6.5, ha="left", color=MID)
for i, (w, c) in enumerate([(20, PRI), (24, GRAY), (16, GRAY), (22, PRI)]):
    box(ax, 16.5 + (0 if c == GRAY else 4), 28 - i*4.2, w, 3, "", fc=c, ec=c, r=0.8)
box(ax, 16.5, 11.5, 24, 2.6, "▸ 子代理 3 个运行中（展开 / 停止）", fc=WHITE, ec=ACC, size=6.0, tc=DEEP)
box(ax, 15, 2, 28, 7.5, "", fc=WHITE, ec=NAVY, lw=1.2, r=0.8)
T(ax, 16.5, 7.4, "描述任务，@ 引用文件，/ 斜杠命令，$ 调用技能", size=6.1, ha="left", color=MID)
chips = ["Local ▾", "请求审批 ▾", "Sol ▾", "推理 中 ▾"]
x = 16.2
for c in chips:
    wdt = 1.0 + len(c)*0.9
    box(ax, x, 2.8, wdt, 2.4, c, fc=PRI, ec=DEEP, size=5.6, r=0.8)
    x += wdt + 0.6
box(ax, 44, 2, 19, 32.5, "", fc=GRAY, ec=NAVY, r=0.6)
T(ax, 45, 32.5, "差异面板 (Diff)", size=6.8, ha="left", bold=True)
for i in range(9):
    c = "#DCFCE7" if i % 3 == 1 else ("#FEE2E2" if i % 4 == 2 else WHITE)
    box(ax, 45, 29.2 - i*2.6, 17, 2.1, "", fc=c, ec=LINE, lw=0.5, r=0.3)
box(ax, 45, 3, 17, 3, "暂存 · 提交 · 推送 · 创建 PR", fc=NAVY, ec=NAVY, tc=WHITE, size=6.0)
box(ax, 15, 0.2, 0.1, 0.1, "", ec=WHITE)
for (x0, y0, lab) in [(7.5, 0.0, "A 侧栏"), (29, 0.0, "B 聊天区 / C 输入框与控件条"), (53.5, 0.0, "D 差异与 Git")]:
    pass
# callouts
for (x0, y0, lab) in [(7.5, 34.2, "A"), (29, 34.2, "B"), (29, 9.2, "C"), (53.5, 34.2, "D")]:
    ax.add_patch(Circle((x0, y0), 1.2, fc=ACC, ec=WHITE, zorder=5)); T(ax, x0, y0, lab, size=6.5, color=WHITE, bold=True, zorder=6)
save(fig, "fig2_1.png")

# ---------- 2-2 差异面板与行内批注
fig, ax = canvas(6.4, 3.3)
box(ax, 1, 1, 40, 31, "", fc=WHITE, ec=NAVY, r=0.8)
T(ax, 2.5, 30, "src/retry.ts   +6 −2", size=7, ha="left", bold=True)
lines = [(" ", "export async function retryOperation(fn, retries = 3) {", WHITE),
         (" ", "  let attempt = 0;", WHITE),
         ("−", "    await wait(200 * 2 ** attempt);", "#FEE2E2"),
         ("−", "    if (attempt >= retries) break;", "#FEE2E2"),
         ("+", "    if (attempt >= retries) break;", "#DCFCE7"),
         ("+", "    await wait(nextDelay(200, attempt));", "#DCFCE7"),
         (" ", "    attempt++;", WHITE)]
for i, (m, s, c) in enumerate(lines):
    y = 25.5 - i*3.0
    box(ax, 2, y, 38, 2.6, "", fc=c, ec=c, r=0.2)
    T(ax, 3, y+1.3, m, size=7, ha="left", color=MID)
    ax.text(5, y+1.3, s, fontsize=6.0, family="monospace", color=NAVY, va="center")
box(ax, 9, 3, 30, 5.2, "", fc="#FFF7E6", ec=WARN, r=0.8)
T(ax, 10, 6.6, "［批注］：退避延迟改为带抖动的 nextDelay，", size=6.2, ha="left", color=NAVY)
T(ax, 10, 4.3, "并补一个“重试耗尽不再等待”的测试。", size=6.2, ha="left", color=NAVY)
arrow(ax, 20, 8.4, 20, 10.3, color=WARN)
steps = [("① 逐块浏览差异", PRI), ("② 不满意的块：撤销", "#FEE2E2"), ("③ 满意的块：暂存", "#DCFCE7"),
         ("④ 写行内批注 → 作为\n下一轮的上下文", "#FFF7E6"), ("⑤ 提交 · 推送 · 建 PR", NAVY)]
for i, (s, c) in enumerate(steps):
    box(ax, 44, 26 - i*6, 19, 4.6, s, fc=c, ec=DEEP, size=6.6, tc=WHITE if c == NAVY else NAVY, bold=True)
    if i < 4: arrow(ax, 53.5, 26 - i*6, 53.5, 26 - i*6 - 1.4, color=DEEP)
save(fig, "fig2_2.png")

# ---------- 3-1 好提示的解剖
fig, ax = canvas(6.4, 3.2)
parts = [("目标 Goal", "要改什么、做出什么", "修复结账页在优惠券为空时\n抛出的 TypeError"),
         ("上下文 Context", "相关文件、文档、报错", "@src/checkout/coupon.ts\n附上浏览器控制台截图"),
         ("约束 Constraints", "规范、架构、禁区", "不改公共 API；\n不新增依赖"),
         ("完成标准 Done when", "怎样算做完", "新增回归测试通过；\npnpm test 全绿")]
for i, (a, b, c) in enumerate(parts):
    x = 1.5 + i*15.6
    box(ax, x, 18, 14.5, 12, "", fc=NAVY if i == 0 else PRI, ec=DEEP, r=1.0)
    T(ax, x+7.25, 26.5, a, size=8, bold=True, color=WHITE if i == 0 else NAVY)
    T(ax, x+7.25, 21.5, b, size=6.6, color=WHITE if i == 0 else DEEP)
    box(ax, x, 3, 14.5, 12, c, fc=GRAY, ec=LINE, size=6.6, r=1.0)
    arrow(ax, x+7.25, 18, x+7.25, 15.2, color=MID)
T(ax, 32, 0.9, "上排：四要素 ｜ 下排：一个具体示例", size=6.4, color=MID)
save(fig, "fig3_1.png")

# ---------- 3-2 权限控件与沙箱对应
fig, ax = canvas(6.4, 3.6)
cols = ["界面选项", "沙箱 sandbox_mode", "审批 approval_policy", "适合场景"]
rows = [("只读（/permissions）", "read-only", "on-request", "只想聊、读代码、做计划", "#E0F2FE"),
        ("请求审批（默认）", "workspace-write", "on-request", "日常开发：工作区内自由，\n越界或联网先问你", "#DCFCE7"),
        ("替我审批", "workspace-write", "on-request + 自动审查", "减少打扰，越界请求\n交给自动审查", "#FEF9C3"),
        ("完全访问", "danger-full-access", "never", "仅限隔离的虚拟机/容器", "#FEE2E2")]
xs = [1, 14.5, 29, 43.5]; ws = [13.5, 14.5, 14.5, 16.5]
for j, c in enumerate(cols):
    box(ax, xs[j], 30, ws[j], 4.5, c, fc=NAVY, ec=NAVY, tc=WHITE, size=7, bold=True, r=0.4)
for i, r in enumerate(rows):
    y = 23.5 - i*7
    for j in range(4):
        box(ax, xs[j], y, ws[j], 6.2, r[j], fc=r[4] if j == 0 else WHITE, ec=LINE, size=6.4, r=0.4, bold=(j == 0))
arrow(ax, 62, 29, 62, 3, color=RED, lw=1.4)
T(ax, 63.6, 16, "自\n主\n性\n↑\n风\n险\n↑", size=6, color=RED, ha="right")
save(fig, "fig3_2.png")

# ---------- 3-3 AGENTS.md 发现链
fig, ax = canvas(6.4, 3.4)
lv = [("全局 ~/.codex/AGENTS.md", "个人习惯：用 pnpm、改完跑测试", 26, PRI),
      ("仓库根 AGENTS.md", "团队规范：lint、测试命令、PR 要求", 18, PRI),
      ("services/payments/AGENTS.override.md", "子目录专用：用 make test-payments", 10, NAVY)]
for i, (a, b, y, c) in enumerate(lv):
    x = 3 + i*6
    box(ax, x, y, 30, 6, "", fc=c, ec=DEEP, r=0.8)
    T(ax, x+15, y+3.9, a, size=7.2, bold=True, color=WHITE if c == NAVY else NAVY)
    T(ax, x+15, y+1.7, b, size=6.3, color=WHITE if c == NAVY else DEEP)
    if i < 2: arrow(ax, x+10, y, x+14, y-2, color=DEEP)
box(ax, 44, 8, 19, 24, "", fc=GRAY, ec=LINE, r=1.0)
T(ax, 53.5, 29.5, "合并规则", size=7.5, bold=True)
rules = ["从根目录一路走到当前目录", "每层最多取 1 个文件", "override 优先于同层 AGENTS.md", "越靠近当前目录越靠后\n→ 优先级越高", "合计上限 32 KiB（可调）"]
for i, s in enumerate(rules):
    T(ax, 45, 26 - i*4.2, "• " + s, size=6.3, ha="left", va="top")
T(ax, 22, 4.5, "最终提示 = 全局 + 根目录 + 子目录（按顺序拼接）", size=6.8, color=ACC, bold=True)
save(fig, "fig3_3.png")

