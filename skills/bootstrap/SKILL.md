---
name: bootstrap
description: 新一轮开始前的项目状态对齐与启动检查
---

# bootstrap

## 目标
在每轮开始前完成最小闭环检查，确保本地状态、白皮书版本与上一轮证据一致，再进入 planning。

## 文档

- 详细上手（单一入口）：根目录 `GET_START.md`
- 开箱步骤与命令说明：`docs/guides/01-getting-started.md`
- Harness 与 Ralph Loop 对照：`docs/guides/02-harness-and-ralph-loop.md`
- 新一轮迭代步骤：`docs/guides/03-new-iteration-manual-steps.md`
- 生成四件套骨架：`python3 workflow/init_iteration.py --summary <kebab-name>`

## 执行步骤
1. 读取 `workflow/state/task-state.json`，确认：
   - `current_iteration`
   - `current_state`
   - `whitepaper_version`
2. 运行：
   - `python3 workflow/check_quality.py`
   - `python3 workflow/run.py`
3. 回顾上一轮证据（若存在）：
   - `harness/changes/YYYY-MM-DD-01-change-<summary>.md`
   - `harness/reviews/YYYY-MM-DD-01-review-<summary>.md`
   - `harness/retros/YYYY-MM-DD-01-retro-<summary>.md`
   - `harness/handoffs/YYYY-MM-DD-01-handoff-<summary>.md`
4. 在本轮 `docs/plans/` 产出 plan（包含 `status` 字段），明确 `done_criteria`。

## 退出条件
- 质量门禁通过
- 状态守卫通过
- 本轮 plan 已创建并可执行
