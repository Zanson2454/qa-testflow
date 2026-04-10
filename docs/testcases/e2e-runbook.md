# E2E 运行手册（首版）

## 环境变量：以谁为准

- **运行时唯一来源**：项目根目录的 **`.env`**（由 `dotenv` 加载，已被 `.gitignore` 忽略，不会进仓库）。
- **`.env.example` 的作用**：仅作**首次复制模板**与**字段名/默认值说明**；执行测试时**不会**读取该文件。日常增删改一律写在 **`.env`**。

首次初始化：

```bash
cp .env.example .env
```

之后在 **`.env`** 中维护真实值即可。

---

## 1. 前置准备

1. 确保存在 **`.env`**（内容以你本机为准）。
2. **必填**（写在 `.env`）：
   - `CONSOLE_BASE_URL`（入口地址，从首页按菜单进入「公开页面」）
   - `PORTAL_BASE_URL`
   - `Cookie` 或 `CONSOLE_COOKIE`（`name=value` 形式；代码会自动去掉首尾单/双引号）
3. **可选**：未提供 Cookie 时，使用 `CONSOLE_STORAGE_STATE` 指向 `.auth/console.storageState.json`
4. **可选**：菜单/文案与默认不一致时，在 **`.env`** 中设置：
   - `CONSOLE_LOGIN_SUCCESS_TEXT`、`CONSOLE_PLATFORM_VERSION`、`CONSOLE_PORTAL_MENU_TEXT`、`CONSOLE_PORTAL_ENTRY_NAME`、`CONSOLE_PORTAL_CONFIG_TEXT`、`CONSOLE_PUBLIC_PAGE_MENU_TEXT`
   - （变量含义与示例见 `.env.example` 注释，**仅作文档**）
5. **可选**：进入公开页后下拉场景名默认为 `AT_公开页面`，需改时在 **`.env`** 设置 `CONSOLE_SCENE_PAGE_NAME`
6. **可选**：控件对不齐时，在 **`.env`** 设置 `E2E_PUBLIC_PAGE_*_TESTID`、`E2E_PORTAL_ROOT_TESTID`
7. 安装依赖与浏览器：
   - `npm install`
   - `npx playwright install`
8. 提交前执行：
   - `npm run check:harness`

### 与当前自动化无关的变量

- 例如 **`IAM_BASE_URL`**：可保留在 `.env` 供人工或其它脚本使用；**当前 Playwright 用例未读取**，不影响执行。

---

## 2. Console 导航约定（与用例一致）

1. 访问 `CONSOLE_BASE_URL`，断言出现登录成功特征文案（默认「欢迎登入系统~」）
2. 点击左下角头像，断言平台版本号（默认 `3.0.2603-beta.0315`）
3. 点击「门户管理」，列表中存在目标门户（默认 `TERP 运营端`）
4. 点击该门户，断言出现「门户配置」
5. 点击「门户配置」展开后进入「公开页面」，再执行选场景、保存、读链接

---

## 3. 执行命令

- 全量执行：
  - `npm run test:e2e`
- 仅 P0：
  - `npm run test:e2e:p0`
- 可视调试：
  - `npm run test:e2e:headed` 或 `npx playwright test --grep @p0 --headed`
- 查看报告：
  - `npm run test:e2e:report`

---

## 4. 与 PRD/用例版本对齐

- 当前 PRD：`PRD-001 v1`
- 当前用例集：`PRD-001 case_set v1`
- 当前脚本：
  - `tests/e2e/portal-public-page.p0.spec.ts`
- 若 PRD 升级到 v2，必须同步更新：
  - `docs/testcases/PRD-001-portal-public-page-case-mapping-v1.md`
  - 对应脚本中的 case_id 与断言逻辑

---

## 5. 证据标准

- 失败必备：截图 + trace
- 建议补充：失败页面关键日志与网络摘要
- 每轮验收结论写入 `harness/reviews/*`，并带上 `prd_version` 与 `case_set_version`
