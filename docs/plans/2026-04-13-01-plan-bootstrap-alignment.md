# 2026-04-13-01 exec plan bootstrap alignment

status: active

## context

- 承接 `2026-04-12-06`：上一轮已补齐 `doctor.py` 与 `init_iteration.py`，但 `context` 仍非默认产物，门禁也未校验最新轮次 `context` 与 `review.passed`。
- 本轮主线：把初始化脚手架、质量门禁和文档定位收口到“开箱即用的 Harness + Ralph-like manual loop”。

## goal

- 默认初始化完整五件套（含 `context`）。
- 为最新轮次补齐最小守卫：`context` 必须存在、`review` 必须有明确 `passed`。
- 统一 `AGENTS.md`、whitepaper 与上手文档口径。

## files

- modify: `workflow/init_iteration.py`
- modify: `workflow/check_quality.py`
- modify: `Makefile`
- modify: `AGENTS.md`
- modify: `docs/whitepaper/whitepaper-v1.md`
- modify: `docs/whitepaper/whitepaper-v2.md`
- modify: `GET_START.md`
- modify: `docs/guides/01-getting-started.md`
- modify: `docs/guides/03-new-iteration-manual-steps.md`
- modify: `workflow/README.md`
- create: `tests/test_bootstrap_alignment.py`

## steps

1. 先写失败测试：覆盖 `init_iteration --dry-run` 默认输出 `context`，以及 `check_quality` 对最新轮次 `context`/`review.passed` 的门禁要求。
2. 以最小改动实现脚手架与门禁收口，并保持历史轮次兼容。
3. 同步更新项目目标、whitepaper 定位与上手文档，明确当前是 `Harness + Ralph-like manual loop + guard scripts`。
4. 运行测试与门禁，更新本轮 change/review/retro/handoff/context。

## done_criteria

- `python3 -m unittest discover -s tests -p 'test_*.py' -v` 通过
- `python3 workflow/check_quality.py` 通过
- `python3 workflow/run.py` 通过
- `python3 workflow/init_iteration.py --summary sample-bootstrap --dry-run` 默认输出 `context`
- 文档已统一到当前仓库真实能力边界
