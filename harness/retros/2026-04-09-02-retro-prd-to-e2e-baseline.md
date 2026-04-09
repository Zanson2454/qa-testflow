# 2026-04-09-02 retro prd to e2e baseline

root_causes:
  - 先搭脚手架后补需求确认，执行顺序一度偏离了预期协作方式。
  - 用例定位器采用占位设计，未在第一轮就完成真实页面探测，导致 P0 阻塞。
  - 提交时遗漏了 harness 证据文档落盘，流程约束执行不严谨。
fix_strategy:
  - 固化“先需求确认产物，后工程实现”的节奏，未确认前不进入代码实现。
  - 将真实 locator 探测纳入 P0 前置任务，先探测再编码断言。
  - 在每次提交前增加 checklist：`changes/reviews/retros/handoffs` 必须齐全。
next_focus:
  - 完成 console 真实定位器对齐并修复 `P0-01/P0-02`。
  - 复跑 `@p0`（headed）并补齐证据路径到 review 文档。
  - 若通过，更新 review 为 `passed: true` 并形成下一轮 handoff。
