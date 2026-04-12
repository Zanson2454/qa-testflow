# 2026-04-12-01 retro template remove playwright

root_causes:
  - 早期仓库把具体业务的 PRD、测试用例和 Playwright 执行链直接放进模板主路径，导致模板与样例耦合。
  - `task-state.json` 指向的 active plan 也带有业务化目标，放大了“模板默认即业务样例”的误导。
fix_strategy:
  - 将非核心样例资产整体移除，只保留 Harness 治理、状态机与审计骨架。
  - 把 README 与 active plan 改回通用表述，确保模板入口不再暗示特定技术栈。
next_focus:
  - 若继续做模板治理，可评估是否把历史业务化审计资产迁出主仓库或转入示例区。
  - 若开始实践 `ralph-loop`，下一轮应基于当前精简后的模板直接进入 schema/orchestrator 实施 plan。
