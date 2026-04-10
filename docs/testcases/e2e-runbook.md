# E2E 运行手册（首版）

## 1. 前置准备

1. 复制环境变量模板：
  - `cp .env.example .env`
2. 填写环境变量（以 `.env` 为准）：
  - `CONSOLE_BASE_URL`（入口地址，脚本从此打开首页，**不再**使用 `CONSOLE_PUBLIC_PAGE_PATH`）
  - `PORTAL_BASE_URL`
  - `Cookie` 或 `CONSOLE_COOKIE`
3. 可选：未提供 Cookie 时，使用 `CONSOLE_STORAGE_STATE` 指向 `.auth/console.storageState.json`
4. 可选：菜单/文案与默认不一致时覆盖（见 `.env.example` 注释）：
  - `CONSOLE_LOGIN_SUCCESS_TEXT`、`CONSOLE_PLATFORM_VERSION`、`CONSOLE_PORTAL_*`、`CONSOLE_PUBLIC_PAGE_MENU_TEXT`
5. 可选：进入公开页后下拉场景名默认为 `AT_公开页面`，需改时设置 `CONSOLE_SCENE_PAGE_NAME`
6. 控件对不齐时，可设置 `E2E_PUBLIC_PAGE_*_TESTID`、`E2E_PORTAL_ROOT_TESTID`
7. 安装依赖并安装浏览器：
  - `npm install`
  - `npx playwright install`
8. 提交前执行：
  - `npm run check:harness`

## 2. Console 导航约定（与用例一致）

1. 访问 `CONSOLE_BASE_URL`，断言出现「欢迎登入系统~」（可配）
2. 点击左下角头像，断言平台版本号（默认 `3.0.2603-beta.0315`）
3. 点击「门户管理」，列表中存在目标门户（默认 `TERP 运营端`）
4. 点击该门户，断言出现「门户配置」
5. 点击「门户配置」展开后进入「公开页面」，再执行选场景、保存、读链接

## 3. 执行命令

- 全量执行：
  - `npm run test:e2e`
- 仅 P0：
  - `npm run test:e2e:p0`
- 可视调试：
  - `npm run test:e2e:headed` 或 `npx playwright test --grep @p0 --headed`
- 查看报告：
  - `npm run test:e2e:report`

## 4. 与 PRD/用例版本对齐

- 当前 PRD：`PRD-001 v1`
- 当前用例集：`PRD-001 case_set v1`
- 当前脚本：
  - `tests/e2e/portal-public-page.p0.spec.ts`
- 若 PRD 升级到 v2，必须同步更新：
  - `docs/testcases/PRD-001-portal-public-page-case-mapping-v1.md`
  - 对应脚本中的 case_id 与断言逻辑

## 5. 证据标准

- 失败必备：截图 + trace
- 建议补充：失败页面关键日志与网络摘要
- 每轮验收结论写入 `harness/reviews/*`，并带上 `prd_version` 与 `case_set_version`
