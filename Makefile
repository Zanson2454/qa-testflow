# 便于开箱即用：无 Python 依赖，仅封装常用 workflow 命令。
.PHONY: check run help

help:
	@echo "make check  - 运行 workflow/check_quality.py（harness 四件套与门禁）"
	@echo "make run    - 运行 workflow/run.py（task-state 守卫）"

check:
	python3 workflow/check_quality.py

run:
	python3 workflow/run.py
