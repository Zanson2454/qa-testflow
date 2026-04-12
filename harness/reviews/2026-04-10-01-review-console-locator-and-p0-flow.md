# 2026-04-10-01 review console locator and p0 flow

passed: false
score: 72
errors:
  - 本轮未在 CI/本地连接真实 terminus 环境执行完整 P0，无法确认用例已全绿。
  - 用户侧需将 CONSOLE_PUBLIC_PAGE_PATH 配到「公开页面」功能真实路由，否则仍会在项目引导页失败。
suggestions:
  - 本地执行 `npm run check:harness` 后，使用有效 .env 跑通 `P0`（headed）并保留 trace。
  - 若控件仍不匹配，按 `.env.example` 逐项配置 E2E_* testid 覆盖。
