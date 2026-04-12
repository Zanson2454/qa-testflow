# 2026-04-12-05 change add GET_START.md

- files:
  - 新增：`GET_START.md`
  - 修改：`workflow/check_quality.py`、`README.md`、`AGENTS.md`、`docs/guides/README.md`
  - 修改：`docs/guides/01-getting-started.md`、`docs/guides/02-harness-and-ralph-loop.md`、`docs/guides/03-new-iteration-manual-steps.md`
  - 修改：`skills/bootstrap/SKILL.md`、`skills/executor/SKILL.md`、`workflow/README.md`
  - 新增：`docs/plans/2026-04-12-05-plan-add-get-start-md.md`；更新 `docs/plans/index.md`（本 plan 标记为 completed）
- intent:
  - 提供根目录详细上手文档，降低仅依赖分篇 guides 时的跳转成本。
  - 修正 `GET_START.md` 与 `docs/guides/01/02/03` 的流程说明，使其和 `AGENTS.md` 的 `Review First`、`context`、commit/push 规则一致。
- risks:
  - 若未来大幅改流程，需同步更新 `GET_START.md` 与 `docs/guides`，避免双处漂移。
