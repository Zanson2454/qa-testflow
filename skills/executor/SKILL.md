---
name: executor
description: 按白皮书状态机执行单轮迭代并沉淀证据
---

# executor

## 目标
围绕单一主题完成“计划 -> 实现 -> 验收 -> 复盘”的单轮闭环，并形成可追溯产物。

## 执行步骤
1. 读取并确认本轮 plan：
   - `docs/plans/iter-XXX-plan.md`
2. 实施改动并实时记录：
   - `harness/changes/YYYY-MM-DD-01-change-<summary>.md`
3. 执行验收并记录结果：
   - `harness/reviews/YYYY-MM-DD-01-review-<summary>.md`
   - 需要明确 `passed: true/false`
4. 输出反思与下一轮输入：
   - `harness/retros/YYYY-MM-DD-01-retro-<summary>.md`
   - `harness/handoffs/YYYY-MM-DD-01-handoff-<summary>.md`
5. 更新 `task-state.json`：
   - 仅推进合法状态迁移
   - 维护 `current_iteration`、`retry_count`、`history`
6. 再次执行：
   - `python3 workflow/check_quality.py`
   - `python3 workflow/run.py`

## 退出条件
- 本轮证据文件完整
- evaluation 已给出明确结论
- 状态文件通过守卫检查
