# 2026-04-10-03 context output loop design

## 上一轮上下文

- 最近一轮完整记录为 `2026-04-10-02`
- 该轮主线是 console 菜单导航与公开页面入口修正
- 上一轮 `review` 结论为 `passed: false`
- 未通过原因是“真实环境 P0 全量验证尚未完成”

## 本轮上下文切换

- 经用户明确指令，本轮不再以 Playwright 执行链路为主线
- 本轮转为审视“项目输出过程本身”的自动闭环、自我修复与最少人工干预机制
- 设计目标已收敛为：优先建设 `B` 型闭环，并预留升级到 `C` 型闭环的能力

## 当前仓库边界

- `workflow/check_quality.py` 与 `workflow/run.py` 仅承担守卫职责，不承担编排职责
- `review/retro/handoff` 仍偏向人类记录，尚未成为统一机器输入
- `task-state.json` 定义了重试预算，但仓库内尚无真正消费该预算的 loop controller

## 本轮约束

- 不进入实施 plan
- 不改业务执行器
- 不触碰当前工作区中的 Playwright 未提交改动
- 先沉淀正式设计稿，再由用户评审是否进入实施阶段
