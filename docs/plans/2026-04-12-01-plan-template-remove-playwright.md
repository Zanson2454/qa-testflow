# 2026-04-12-01 exec plan template remove playwright

status: completed

## context

- 承接上一轮对模板现状的 review：当前仓库具备 Harness 骨架，但 Playwright/E2E 资产属于业务示例，不是模板核心能力。
- `task-state.json` 仍以 `iter-001-plan.md` 作为当前 active plan，因此本轮新增计划文件只记录本次模板瘦身，不改写状态主线。
- 本轮主线单一：删除与模板核心无关的 Playwright/PRD/E2E 示例资产，保留 Harness 治理与审计骨架。

## goal

- 将仓库收敛为通用 Harness 模板，移除 Playwright 及其业务样例代码、依赖和文档，避免模板默认绑定某一测试框架与业务域。

## steps

1. 盘点并确认 Playwright/E2E 业务示例的影响面 -> 形成精确删除清单
2. 删除 Playwright/Node 执行链与业务样例文件 -> 清空非核心实现资产
3. 更新 README、`.gitignore` 与 active plan 文案 -> 让模板入口回到通用 Harness 说明
4. 补齐本轮 `context/change/review/retro/handoff` -> 形成可追溯审计记录
5. 运行 `python3 workflow/check_quality.py` 与 `python3 workflow/run.py` -> 验证模板骨架仍可工作

## done_criteria

- [x] `playwright.config.ts`、`tests/**`、`package*.json`、`tsconfig.json` 已从仓库移除
- [x] `docs/prd/**` 与 `docs/testcases/**` 的业务样例文档已移除
- [x] `README.md` 与 `docs/plans/iter-001-plan.md` 不再包含 Playwright/E2E 业务样例要求
- [x] `python3 workflow/check_quality.py` 与 `python3 workflow/run.py` 通过
