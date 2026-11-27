"""绘制第 4～10 章示意图。"""
from figlib import *

# ---------- 4-1 Local 与 Worktree 的 Handoff
fig, ax = canvas(6.4, 3.4)
box(ax, 1, 20, 62, 11, "", fc=PRI, ec=DEEP, r=1.0)
box(ax, 1, 3, 62, 13, "", fc=GRAY, ec=LINE, r=1.0)
T(ax, 3, 29, "前台 · Local（你的本地检出）", size=7.4, ha="left", bold=True)
T(ax, 3, 14.2, "后台 · Worktree（.git 共享，文件各自一份）", size=7.4, ha="left", bold=True)
box(ax, 4, 22, 14, 5, "你在 IDE 里\n继续手头工作", fc=WHITE, ec=DEEP, size=6.6)
box(ax, 46, 22, 15, 5, "验证、跑开发服务器\n用熟悉的工具检查", fc=WHITE, ec=DEEP, size=6.6)
wt = [(4, "Worktree A\n修复结账 Bug"), (19, "Worktree B\n新增筛选器"), (34, "Worktree C\n定时任务：周报")]
for x, s in wt:
    box(ax, x, 5, 12, 6.5, s, fc=WHITE, ec=NAVY, size=6.5)
arrow(ax, 25, 11.5, 48, 22, color=ACC, lw=1.6, rad=-0.25)
T(ax, 39, 18.2, "Hand off → Local", size=6.8, color=ACC, bold=True)
box(ax, 48, 5, 13, 6.5, "Create branch here\n→ 提交 · 推送 · PR", fc=NAVY, ec=NAVY, tc=WHITE, size=6.3)
arrow(ax, 16, 8, 48, 8, color=MID, ls="--", rad=0.0)
T(ax, 32, 1.4, "Git 规则：同一分支同一时间只能在一个检出中被 checkout——Handoff 替你处理这一步", size=6.2, color=MID)
save(fig, "fig4_1.png")

# ---------- 5-1 主线程与子代理线程
fig, ax = canvas(6.4, 4.0)
box(ax, 2, 14, 15, 8, "主线程\n需求 · 决策 · 最终结论", fc=NAVY, ec=NAVY, tc=WHITE, size=7.2, bold=True)
subs = [("explorer\n只读探索代码路径", 29), ("reviewer\n找正确性与安全风险", 20), ("worker\n实现最小修复", 11), ("docs_researcher\n经 MCP 核对文档", 2)]
for s, y in subs:
    box(ax, 27, y + 1, 15, 6.5, s, fc=PRI, ec=DEEP, size=6.5)
    arrow(ax, 17, 18, 27, y + 4.2, color=DEEP, lw=0.9)
    box(ax, 47, y + 2, 15, 4.5, "摘要（非原始日志）", fc=GRAY, ec=LINE, size=6.3)
    arrow(ax, 42, y + 4.2, 47, y + 4.2, color=ACC, lw=1.1)
T(ax, 22, 38.3, "派生（spawn）", size=6.5, color=DEEP)
T(ax, 54.5, 38.3, "回收（wait + summarize）", size=6.5, color=ACC)
T(ax, 9.5, 10.5, "噪声留在子线程：\n日志、堆栈、探索笔记", size=6.2, color=MID)
save(fig, "fig5_1.png")

# ---------- 5-2 四种编排模式
fig, ax = canvas(6.4, 4.2)
quads = [(1, 22, "A 扇出评审（并行·只读）"), (33, 22, "B 流水线（探索→实现→验证）"),
         (1, 1, "C Map-Reduce（大材料分片）"), (33, 1, "D 并行写入 + Worktree 隔离")]
for x, y, t in quads:
    box(ax, x, y, 30, 19.5, "", fc=WHITE, ec=LINE, r=1.0)
    T(ax, x + 1.5, y + 17.5, t, size=7.2, ha="left", bold=True)
# A
box(ax, 3, 28, 6, 4, "主", fc=NAVY, ec=NAVY, tc=WHITE, size=6.5)
for i, s in enumerate(["安全", "测试", "可维护"]):
    box(ax, 15, 33 - i*4.6, 8, 3.4, s, fc=PRI, ec=DEEP, size=6.2)
    arrow(ax, 9, 30, 15, 34.7 - i*4.6, color=DEEP, lw=0.8)
    arrow(ax, 23, 34.7 - i*4.6, 26.5, 30, color=ACC, lw=0.8)
box(ax, 25.5, 28, 4.5, 4, "汇总", fc=NAVY, ec=NAVY, tc=WHITE, size=5.8)
# B
for i, s in enumerate(["探索", "实现", "验证"]):
    box(ax, 35 + i*9, 27.5, 7, 5, s, fc=PRI if i != 1 else NAVY, ec=DEEP, tc=WHITE if i == 1 else NAVY, size=6.5)
    if i < 2: arrow(ax, 42 + i*9, 30, 44 + i*9, 30, color=DEEP)
T(ax, 48, 24.5, "上一阶段的结论 = 下一阶段的输入", size=6, color=MID)
# C
box(ax, 3, 8, 6, 5, "长文档\n日志", fc=GRAY, ec=LINE, size=5.8)
for i in range(4):
    box(ax, 13, 14 - i*3.3, 6, 2.6, f"片{i+1}", fc=PRI, ec=DEEP, size=5.8)
    arrow(ax, 9, 10.5, 13, 15.3 - i*3.3, color=DEEP, lw=0.7)
    arrow(ax, 19, 15.3 - i*3.3, 23, 10.5, color=ACC, lw=0.7)
box(ax, 23, 8, 7, 5, "要点\n归并", fc=NAVY, ec=NAVY, tc=WHITE, size=5.8)
# D
for i, s in enumerate(["Worktree A", "Worktree B"]):
    box(ax, 35, 12 - i*6, 11, 4, s, fc=PRI, ec=DEEP, size=6.2)
    arrow(ax, 46, 14 - i*6, 51, 11, color=DEEP, lw=0.8)
box(ax, 51, 8.5, 9, 5, "逐个评审\n后合并", fc=NAVY, ec=NAVY, tc=WHITE, size=6)
T(ax, 47, 3.0, "写入多时：一人一块文件，冲突最少", size=6, color=RED)
save(fig, "fig5_2.png")

# ---------- 6-1 浏览器 vs Computer Use 分工
fig, ax = canvas(6.4, 3.3)
box(ax, 22, 26, 20, 5.5, "要验证/操作的是什么？", fc=NAVY, ec=NAVY, tc=WHITE, size=7.4, bold=True)
opts = [(1, "本地开发中的 Web 应用", "内置浏览器", "预览页面 · 在页面上批注\n按站点设置 浏览/下载/上传 权限"),
        (22, "有插件 / MCP 的系统", "插件 · MCP", "结构化、可重复、最省 token\n优先选择"),
        (43, "只有图形界面的桌面应用", "Computer Use", "@Computer / @应用名\nWindows 上会占用前台")]
for x, q, a, d in opts:
    arrow(ax, 32, 26, x + 10, 21.5, color=DEEP)
    box(ax, x, 16, 20, 5.5, q, fc=GRAY, ec=LINE, size=6.6)
    arrow(ax, x + 10, 16, x + 10, 13.5, color=DEEP)
    box(ax, x, 8, 20, 5.5, a, fc=PRI, ec=DEEP, size=7.6, bold=True)
    T(ax, x + 10, 4.2, d, size=6.0, color=DEEP)
save(fig, "fig6_1.png")

# ---------- 6-2 技能—定时任务关系
fig, ax = canvas(6.4, 2.8)
steps = [("① 普通对话\n反复调试提示", GRAY), ("② 沉淀为技能\nSKILL.md（方法）", PRI), ("③ 打包为插件\n分享给团队", PRI), ("④ 定时任务\nScheduled（节奏）", NAVY)]
for i, (s, c) in enumerate(steps):
    box(ax, 1.5 + i*15.7, 11, 13.5, 9, s, fc=c, ec=DEEP, tc=WHITE if c == NAVY else NAVY, size=7, bold=True)
    if i < 3: arrow(ax, 15 + i*15.7, 15.5, 17.2 + i*15.7, 15.5, color=DEEP)
T(ax, 32, 6.5, "经验法则：技能定义“怎么做”，定时任务定义“何时做”。还需大量人工引导的流程，先做成技能，再上定时。", size=6.4, color=MID)
T(ax, 32, 3.2, "定时任务在 Git 仓库中可选择运行在独立 Worktree，避免改动你未完成的本地工作。", size=6.4, color=MID)
save(fig, "fig6_2.png")

# ---------- 7-1 多 Harness 协作拓扑
fig, ax = canvas(6.4, 4.0)
box(ax, 22, 30, 20, 7, "主控 Harness（Orchestrator）\nAWS Quick · Claude Code · Kiro\n或 Codex 自己", fc=NAVY, ec=NAVY, tc=WHITE, size=6.6, bold=True)
chan = [(1, "ACP\ncodex-acp 适配器", "编辑器/助手内\n嵌入 Codex 会话"), (17, "SDK\nTS · Python", "在程序中\n启动/续跑线程"),
        (33, "app-server\nJSON-RPC", "自建富客户端\n审批 · 事件流"), (49, "exec\n脚本 / CI", "一次性任务\nJSONL · Schema")]
for x, a, b in chan:
    box(ax, x, 18, 14, 6.5, a, fc=PRI, ec=DEEP, size=6.6, bold=True)
    T(ax, x + 7, 15, b, size=5.9, color=DEEP)
    arrow(ax, 32, 30, x + 7, 24.5, color=DEEP, lw=0.9)
box(ax, 8, 3, 48, 7, "", fc=GRAY, ec=LINE, r=1.0)
T(ax, 32, 8, "Codex 执行者：本地沙箱中读写代码、跑测试，必要时再派生子代理", size=6.8, bold=True)
T(ax, 32, 5, "产出：Worktree 分支 · 差异 · HANDOFF.md 交接报告 · 结构化结果", size=6.3, color=DEEP)
for x, _, _ in chan:
    arrow(ax, x + 7, 13, x + 7 if x < 40 else x + 2, 10.2, color=MID, lw=0.8)
arrow(ax, 58, 6.5, 44, 31, color=ACC, lw=1.3, rad=0.35)
T(ax, 56, 31.5, "结果回收 · 交叉评审", size=6.3, color=ACC, bold=True)
save(fig, "fig7_1.png")

# ---------- 7-2 派工—交接—回收时序
fig, ax = canvas(6.4, 3.8)
lanes = [("主控", 8), ("Codex 执行者", 26), ("评审者（异构）", 43), ("人", 57)]
for n, x in lanes:
    box(ax, x - 6, 33, 12, 3.5, n, fc=NAVY, ec=NAVY, tc=WHITE, size=6.6, bold=True)
    ax.plot([x, x], [2, 33], color=LINE, lw=0.8, ls="--")
msgs = [(8, 26, 30, "① 任务契约：目标/范围/完成标准/分支名"), (26, 26, 26.5, "② 在 Worktree 中实现并自测"),
        (26, 8, 23, "③ HANDOFF.md + 差异摘要"), (8, 43, 19.5, "④ 请求交叉评审（只读）"),
        (43, 8, 16, "⑤ 发现清单 P0/P1"), (8, 26, 12.5, "⑥ 修复指令（续跑同一线程）"),
        (26, 8, 9, "⑦ 修复完成 + 测试结果"), (8, 57, 5.5, "⑧ 合并前人工确认")]
for a, b, y, s in msgs:
    if a == b:
        box(ax, a - 5, y - 1.3, 10, 2.6, "", fc=PRI, ec=DEEP, r=0.5)
        T(ax, a + 6, y, s, size=6.0, ha="left", color=NAVY)
    else:
        arrow(ax, a, y, b, y, color=DEEP if b > a else ACC, lw=1.0)
        T(ax, (a + b) / 2, y + 1.2, s, size=6.0, color=NAVY)
save(fig, "fig7_2.png")

# ---------- 8-1 云端任务生命周期
fig, ax = canvas(6.4, 3.4)
st = [("创建容器\n检出分支", "universal 镜像"), ("setup 脚本\n安装依赖", "可联网 · 可读 secrets"),
      ("移除 secrets\n应用联网策略", "代理阶段默认断网"), ("代理循环\n改代码·跑检查", "遵循 AGENTS.md"),
      ("产出答案\n+ 差异", "开 PR / 追问 / 拉回本地")]
for i, (a, b) in enumerate(st):
    x = 1 + i*12.7
    box(ax, x, 17, 11.3, 9, a, fc=NAVY if i == 3 else PRI, ec=DEEP, tc=WHITE if i == 3 else NAVY, size=6.7, bold=True)
    T(ax, x + 5.65, 13.5, b, size=5.9, color=DEEP if i != 2 else RED)
    if i < 4: arrow(ax, x + 11.3, 21.5, x + 12.7, 21.5, color=DEEP)
box(ax, 1, 3, 37, 6, "容器缓存最长约 12 小时：恢复时跑可选的“维护脚本”；\n改 setup/维护脚本、环境变量或 secrets 会自动失效缓存", fc=GRAY, ec=LINE, size=6.1)
box(ax, 40, 3, 23, 6, "secrets 只在 setup 阶段可用，\n代理阶段之前即被移除", fc="#FEE2E2", ec=RED, size=6.1)
T(ax, 32, 30.5, "Codex Cloud 任务的五个阶段", size=7.6, bold=True)
save(fig, "fig8_1.png")

# ---------- 9-1 云边协同全景
fig, ax = canvas(6.4, 4.0)
box(ax, 1, 21, 22, 17, "", fc=PRI, ec=DEEP, r=1.0); T(ax, 12, 36, "边（你的电脑）", size=7.6, bold=True)
box(ax, 41, 21, 22, 17, "", fc=GRAY, ec=LINE, r=1.0); T(ax, 52, 36, "云（Codex Cloud）", size=7.6, bold=True)
for i, s in enumerate(["桌面应用 · IDE · CLI", "本地 Worktree / 定时任务", "私有数据 · 本机工具", "最终验证与合并"]):
    box(ax, 3, 31 - i*3.4, 18, 2.8, s, fc=WHITE, ec=DEEP, size=6.2)
for i, s in enumerate(["已发布的云环境", "并行多任务 · 多次尝试", "不占本机资源与电量", "差异 → PR"]):
    box(ax, 43, 31 - i*3.4, 18, 2.8, s, fc=WHITE, ec=LINE, size=6.2)
arrow(ax, 23, 31, 41, 31, color=DEEP, lw=1.3); T(ax, 32, 32.6, "/cloud 交给云端", size=6.3, color=DEEP)
arrow(ax, 41, 25, 23, 25, color=ACC, lw=1.3); T(ax, 32, 26.6, "差异拉回本地验证", size=6.3, color=ACC)
box(ax, 1, 3, 19, 13, "", fc=WHITE, ec=NAVY, r=1.0); T(ax, 10.5, 14, "手机（远程控制）", size=7, bold=True)
T(ax, 10.5, 8.5, "扫码配对电脑\n查看进度 · 审批\n追加指令", size=6.2, color=DEEP)
box(ax, 44, 3, 19, 13, "", fc=WHITE, ec=NAVY, r=1.0); T(ax, 53.5, 14, "事件入口", size=7, bold=True)
T(ax, 53.5, 8.5, "GitHub @codex review\nSlack @ChatGPT\n事件触发的定时任务", size=6.2, color=DEEP)
arrow(ax, 12, 16, 12, 21, color=MID, ls="--"); arrow(ax, 53, 16, 53, 21, color=MID, ls="--")
box(ax, 23, 6, 18, 7, "同一账号 · 同一工作区\n共享配置 · AGENTS.md", fc=NAVY, ec=NAVY, tc=WHITE, size=6.4, bold=True)
save(fig, "fig9_1.png")

# ---------- 9-2 规划-并行-合并
fig, ax = canvas(6.4, 3.4)
box(ax, 1, 13, 12, 9, "① 本地\n/plan 拆解需求\n写清完成标准", fc=PRI, ec=DEEP, size=6.5, bold=True)
for i, s in enumerate(["云任务 A：API 改造", "云任务 B：前端筛选器", "云任务 C：迁移脚本"]):
    box(ax, 18, 25 - i*8, 17, 5.5, s, fc=GRAY, ec=LINE, size=6.4)
    arrow(ax, 13, 17.5, 18, 27.7 - i*8, color=DEEP, lw=0.9)
    arrow(ax, 35, 27.7 - i*8, 40, 17.5, color=ACC, lw=0.9)
T(ax, 26.5, 32.5, "② 云端并行（可多次尝试择优）", size=6.6, color=DEEP, bold=True)
box(ax, 40, 13, 11, 9, "③ 本地\n拉回差异\n跑完整测试", fc=PRI, ec=DEEP, size=6.5, bold=True)
arrow(ax, 51, 17.5, 53, 17.5, color=DEEP)
box(ax, 53, 13, 10, 9, "④ PR\n@codex review\n人工合并", fc=NAVY, ec=NAVY, tc=WHITE, size=6.3, bold=True)
T(ax, 32, 3, "要诀：任务之间不共享文件；每个云任务带上同一份 AGENTS.md 与完成标准", size=6.4, color=MID)
save(fig, "fig9_2.png")

# ---------- 10-1 IDE 扩展工作区
fig, ax = canvas(6.4, 3.4)
box(ax, 1, 1, 62, 32, "", fc=WHITE, ec=NAVY, lw=1.2, r=0.8)
box(ax, 1, 1, 4, 32, "", fc=GRAY, ec=NAVY, r=0.4)
for i in range(5):
    ax.add_patch(Circle((3, 29 - i*4), 1.0, fc=ACC if i == 2 else LINE, ec="none"))
box(ax, 5, 1, 36, 32, "", fc=WHITE, ec=LINE, r=0.2)
T(ax, 6.5, 31, "retry.ts", size=6.6, ha="left", bold=True)
for i in range(10):
    c = PRI if i in (4, 5) else GRAY
    box(ax, 7, 27.5 - i*2.4, 18 + (i % 4)*4, 1.6, "", fc=c, ec=c, r=0.3)
T(ax, 33, 16.5, "← 选中代码\n自动成为上下文", size=6.2, color=DEEP)
box(ax, 41, 1, 22, 32, "", fc=GRAY, ec=NAVY, r=0.4)
T(ax, 42.5, 31, "Codex 侧栏", size=6.8, ha="left", bold=True)
box(ax, 42.5, 21, 19, 8, "Fixed successfully.\n重试耗尽后不再等待；\n聚焦测试已通过", fc=WHITE, ec=LINE, size=6.0)
box(ax, 42.5, 14, 19, 5.5, "就地差异：保留 / 丢弃", fc=PRI, ec=DEEP, size=6.2)
box(ax, 42.5, 8, 19, 4.5, "长任务 → 交给云端", fc=WHITE, ec=ACC, size=6.2)
box(ax, 42.5, 2.5, 19, 4.5, "输入框 · 权限 · 模型", fc=WHITE, ec=NAVY, size=6.2)
save(fig, "fig10_1.png")

