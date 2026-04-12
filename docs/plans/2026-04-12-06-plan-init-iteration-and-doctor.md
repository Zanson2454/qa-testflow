# 2026-04-12-06 exec plan init iteration and doctor

status: completed

## context

- 承接「开箱即用初始化工程」方向：在文档与门禁之外，提供可执行脚手架，降低首轮 harness 与克隆自检成本。

## goal

- 新增 `workflow/doctor.py`：依次执行 `check_quality` + `run`。
- 新增 `workflow/init_iteration.py`：按门禁命名规则生成四件套（可选 context）；支持 `--dry-run`、日期与序号自动递增。
- 更新 `Makefile`、`GET_START`、`guides`、`README`、`AGENTS`、skills、`workflow/README.md`。

## done_criteria

- [x] `python3 workflow/doctor.py` 与 `python3 workflow/init_iteration.py --help` 可用
- [x] `python3 workflow/check_quality.py` 与 `python3 workflow/run.py` 通过
- [x] 本轮 harness 四件套与 plan 落盘
