# 2026-04-13-01 change bootstrap-alignment

- files:
  - 修改：`workflow/init_iteration.py`、`workflow/check_quality.py`、`Makefile`
  - 修改：`AGENTS.md`、`GET_START.md`、`docs/guides/01-getting-started.md`、`docs/guides/03-new-iteration-manual-steps.md`、`workflow/README.md`
  - 修改：`docs/whitepaper/whitepaper-v1.md`、`docs/whitepaper/whitepaper-v2.md`
  - 修改：`docs/plans/index.md`、`docs/plans/iter-001-plan.md`、`workflow/state/task-state.json`
  - 新增：`docs/plans/2026-04-13-01-plan-bootstrap-alignment.md`、`tests/test_bootstrap_alignment.py`
- intent:
  - 让 `init_iteration` 默认生成 `context`，把初始化入口收口为开箱即用的五件套脚手架。
  - 让 `check_quality` 对最新轮次补充 `context` 与 `review.passed` 最小守卫，减少“门禁通过但流程未闭环”的情况。
  - 统一 `AGENTS`、whitepaper 与上手文档定位，明确当前模板是 `Harness + Ralph-like manual loop + guard scripts`。
- risks:
  - 新门禁只校验最新轮次；若未来希望对全量历史记录追溯治理，还需额外设计迁移策略。
  - `task-state.json` 当前主线已切到本轮 plan，后续新任务若切换主线需同步更新 `current_plan` 与状态。
- unresolved:
  - 暂未引入更强的状态迁移守卫或自动 orchestrator；这仍属于后续演进范围。
