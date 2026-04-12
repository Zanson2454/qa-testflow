# 2026-04-12-04 exec plan doc only new iteration guide

status: completed

## context

- 承接 `2026-04-12-03` 开箱与模板加固；用户明确 **先仅文档步骤**——补充「新一轮迭代」纯文档操作说明，不引入初始化脚本。

## goal

- 新增 `docs/guides/03-new-iteration-manual-steps.md`，与 `01` 分工：`01` 保持轻量，`03` 承载可照做的完整顺序与自检。
- 更新索引、README、`AGENTS.md`、skills；将新 guide 纳入 `check_quality` 必需文件。

## done_criteria

- [x] `03` 文档可独立指导「复制 plan → 四件套 → 提交前自检」
- [x] `workflow/check_quality.py` 与 `workflow/run.py` 通过
- [x] 本轮 harness 四件套与 plan 已落盘
