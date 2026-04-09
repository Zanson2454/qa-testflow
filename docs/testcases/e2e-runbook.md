# E2E 运行手册（首版）

## 1. 前置准备

1. 复制环境变量模板：
  - `cp .env.example .env`
2. 填写环境变量：
  - `CONSOLE_BASE_URL`
  - `PORTAL_BASE_URL`
  - `CONSOLE_STORAGE_STATE`
3. 准备 Cookie 登录态文件：
  - 在 `.auth/console.storageState.json` 放入有效 storageState
4. 安装依赖并安装浏览器：
  - `npm install`
  - `npx playwright install`

## 2. 执行命令

- 全量执行：
  - `npm run test:e2e`
- 仅 P0：
  - `npm run test:e2e:p0`
- 查看报告：
  - `npm run test:e2e:report`

## 3. 与 PRD/用例版本对齐

- 当前 PRD：`PRD-001 v1`
- 当前用例集：`PRD-001 case_set v1`
- 当前脚本：
  - `tests/e2e/portal-public-page.p0.spec.ts`
- 若 PRD 升级到 v2，必须同步更新：
  - `docs/testcases/PRD-001-portal-public-page-case-mapping-v1.md`
  - 对应脚本中的 case_id 与断言逻辑

## 4. 证据标准

- 失败必备：截图 + trace
- 建议补充：失败页面关键日志与网络摘要
- 每轮验收结论写入 `harness/reviews/*`，并带上 `prd_version` 与 `case_set_version`