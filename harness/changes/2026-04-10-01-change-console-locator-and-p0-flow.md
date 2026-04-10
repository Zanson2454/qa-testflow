# 2026-04-10-01 change console locator and p0 flow

- files:
  - `tests/fixtures/env.ts`
  - `tests/pages/consolePublicPageConfigPage.ts`
  - `tests/pages/portalPublicPageView.ts`
  - `tests/e2e/portal-public-page.p0.spec.ts`
  - `.env.example`
- intent:
  - 强化 Console Page Object：支持可配置 testid、欢迎页检测、链接读取兼容 input/锚点。
  - 修复 P0-02：与 P0-01 一致走「选场景 → 保存 → 成功 → 读链接」完整链路。
  - Portal 根节点断言支持 `E2E_PORTAL_ROOT_TESTID` 与通用兜底。
- risks:
  - 真实页面若仍无匹配控件，需通过环境变量补充 testid 或继续探测 DOM。
  - `assertNotOnWelcomeScreen` 仅依据英文引导文案，若产品文案变更需同步调整。
- unresolved:
  - 需在目标环境执行 `npm run test:e2e:p0 -- --headed` 验证全绿并更新 review。
