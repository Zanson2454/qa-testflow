# 2026-04-10-02 handoff console menu navigation

## 当前目标

- 在真实环境下验证五步菜单导航 + 公开页配置 + P0 全绿。

## 环境注意

- `.env` 仅需 `CONSOLE_BASE_URL` + `PORTAL_BASE_URL` + Cookie；勿再使用 `CONSOLE_PUBLIC_PAGE_PATH`。
- 版本、门户名、菜单文案可通过 `CONSOLE_*` 可选变量覆盖。

## 起手命令

1. `npm run check:harness`
2. 在项目侧 E2E 运行器中执行 `P0`（headed）

## 交接元信息

- **owner**: assistant
- **notes**: 用例矩阵已补充「Console 前置步骤」与 `case_set_version v1.1` 说明。
