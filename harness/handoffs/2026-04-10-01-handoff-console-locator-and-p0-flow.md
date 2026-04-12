# 2026-04-10-01 handoff console locator and p0 flow

## 1) 当前目标与范围

- **primary_goal**: 在真实环境下跑通 PRD-001 全部 P0（含 headed 可视调试）
- **in_scope**:
  - 校验 `.env` 中 `CONSOLE_PUBLIC_PAGE_PATH` 为公开页面配置页完整路由
  - 按需配置 `CONSOLE_SCENE_PAGE_NAME` 与 `E2E_*_TESTID`
  - 在项目侧 E2E 运行器中执行 `P0`（headed）并修复剩余定位问题
- **out_of_scope**:
  - P1 扩展与多 PRD 并行

## 2) 关键约束

- **hard_constraints**:
  - 仍以 Cookie + `.env` 为唯一环境来源
  - portal 仅访问 `PORTAL_BASE_URL`（脚本不追加路径）

## 3) 本轮代码变更摘要

- `ConsolePublicPageConfigPage`：`configureAndReadPublicLink`、欢迎页检测、可选 testid、链接多类型读取
- `PortalPublicPageView`：可选 `E2E_PORTAL_ROOT_TESTID` + main 兜底
- `P0-02`：与 P0-01 相同配置链路

## 4) 验证清单（下一轮起手）

1. `npm run check:harness`
2. 确认 `.env`：`CONSOLE_PUBLIC_PAGE_PATH`、`CONSOLE_SCENE_PAGE_NAME`、Cookie
3. 复跑 `P0`（headed，保留 trace）
4. 若失败：打开 `test-results/*/trace.zip` 或截图，补 `E2E_*` 后重试

## 5) 交接元信息

- **owner**: assistant
- **timestamp**: 2026-04-10
- **notes**: review 仍为 `passed: false`，待环境验证后更新。
