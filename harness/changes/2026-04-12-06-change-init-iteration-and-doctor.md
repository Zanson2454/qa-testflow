# 2026-04-12-06 change init iteration and doctor

- files:
  - 新增：`workflow/doctor.py`、`workflow/init_iteration.py`
  - 修改：`Makefile`、`GET_START.md`、`README.md`、`AGENTS.md`、`docs/guides/01-getting-started.md`、`docs/guides/03-new-iteration-manual-steps.md`、`skills/bootstrap/SKILL.md`、`skills/executor/SKILL.md`、`workflow/README.md`
  - 新增：`docs/plans/2026-04-12-06-plan-init-iteration-and-doctor.md`；更新 `docs/plans/index.md`
- intent:
  - 提供克隆后一键自检与新一轮 harness 骨架生成，落实「开箱即用的初始化工程」。
- risks:
  - `init_iteration` 仅生成空文件；若与已有同前缀文件冲突会报错退出，需使用者指定 `--date`/`--seq`。
