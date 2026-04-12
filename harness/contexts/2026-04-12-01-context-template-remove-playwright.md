# 2026-04-12-01 context template remove playwright

## 上一轮上下文

- 上一轮先完成了 `review first`，并确认当前仓库对于 `Harness + ralph-loop` 只具备骨架能力，尚未进入自动 loop 实施。
- 在这次 review 中进一步确认：Playwright/E2E 资产主要用于某个具体业务样例，不属于通用 Harness 模板的核心能力。

## 本轮上下文

- 用户明确要求将仓库收敛为“其他工程可复用的模板”，并直接删除无用文件或代码。
- 用户已明确判断 Playwright 为非必须能力，因此本轮将按“整套移除”处理，而不是仅删除单个配置文件。

## 本轮约束

- 保持单主线：只做模板瘦身，不同时推进 `ralph-loop` 实施。
- 不回退已确认的 Harness 治理设计与历史审计记录。
- 保证 `workflow/check_quality.py` 与 `workflow/run.py` 在删除后仍可通过。
