# 2026-04-10-01 retro console locator and p0 flow

root_causes:
  - P0-02 原先未执行配置与保存，仅打开页面读链接，与业务步骤不一致。
  - 占位 testid 与真实低代码页面差距大，需要可配置兜底与明确「功能路由」约束。
fix_strategy:
  - 抽取 configureAndReadPublicLink 复用主流程；环境变量暴露 testid 与场景名称。
  - 欢迎页检测提示用户修正 CONSOLE_PUBLIC_PAGE_PATH，减少无效超时。
next_focus:
  - 真实环境跑通 P0 全绿后，将 review 更新为 passed: true 并归档 trace 路径。
