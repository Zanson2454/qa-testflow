# 便于开箱即用：无 Python 依赖，仅封装常用 workflow 命令。
.PHONY: check run doctor help init

help:
	@echo "make check   - 运行 workflow/check_quality.py（harness 四件套与门禁）"
	@echo "make run     - 运行 workflow/run.py（task-state 守卫）"
	@echo "make doctor  - 依次执行 check + run（克隆后自检）"
	@echo "make init    - 生成本轮 harness 骨架，需传 SUMMARY=kebab-case，例: make init SUMMARY=my-feature"

check:
	python3 workflow/check_quality.py

run:
	python3 workflow/run.py

doctor:
	python3 workflow/doctor.py

init:
	@test -n "$(SUMMARY)" || (echo "用法: make init SUMMARY=your-feature-name" && exit 1)
	python3 workflow/init_iteration.py --summary $(SUMMARY)
