# 2026-04-12-03 change ootb guides and template hardening

- files:
  - 新增：`docs/guides/README.md`、`01-getting-started.md`、`02-harness-and-ralph-loop.md`
  - 新增：`docs/plans/plan-template.md`、`Makefile`、`workflow/README.md`
  - 修改：`README.md`、`AGENTS.md`、`docs/whitepaper/whitepaper-v2.md`、`docs/templates/plan.md`
  - 修改：`skills/bootstrap/SKILL.md`、`skills/executor/SKILL.md`、`workflow/check_quality.py`
  - 新增：`docs/plans/2026-04-12-03-plan-ootb-guides-and-template-hardening.md`；更新 `docs/plans/index.md`
- intent:
  - 实现 **开箱即用**：命令、首轮步骤、概念对照有文档；工程侧提供 Makefile、workflow 说明、plan 复制模板与门禁加固。
- risks:
  - `REQUIRED_FILES` 增加后，若使用方删除 guides 会导致门禁失败——符合「模板完整性」预期，需在 fork 时自行调整门禁列表。
- unresolved:
  - 无。
