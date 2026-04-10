# 2026-04-10-02 change console menu navigation

- files:
  - `tests/fixtures/env.ts`
  - `tests/pages/consolePublicPageConfigPage.ts`
  - `tests/e2e/portal-public-page.p0.spec.ts`
  - `.env.example`
  - `docs/testcases/e2e-runbook.md`
  - `docs/testcases/PRD-001-portal-public-page-case-mapping-v1.md`
- intent:
  - 移除对 `CONSOLE_PUBLIC_PAGE_PATH` 的依赖，仅从 `CONSOLE_BASE_URL` 进入并按业务步骤导航至「公开页面」。
  - 固化 STEP1～STEP5：欢迎文案、头像版本、门户管理、TERP 运营端、门户配置、公开页面。
  - `CONSOLE_SCENE_PAGE_NAME` 改为可选默认值，不要求用户必配。
- risks:
  - 菜单层级或文案因环境/权限不同可能需通过环境变量覆盖。
  - 头像、子菜单定位在 UI 改版后需调整 locator。
- unresolved:
  - 需在目标环境 headed 跑通 P0 后更新 review 为 passed。
