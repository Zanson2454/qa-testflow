# 2026-04-10-03 retro output loop design doc

root_causes:
  - 当前工程虽有流程规范，但“执行、校验、修复、重试”仍主要依赖人工脑内串联。
  - 闭环信息以 markdown 为主，机器可消费程度不足，导致自我修复难以落地。
fix_strategy:
  - 先将目标机制正式文档化，统一术语、边界与模块职责。
  - 后续若进入实施，优先补齐 evidence、validator、diagnoser、repair planner 四类能力。
next_focus:
  - 等待用户评审设计稿。
  - 若设计通过，再编写实施 plan，并决定第一批自动修复的准入范围。
