# 开箱即用：快速上手

本模板不绑定具体业务代码或测试框架；克隆后按下面顺序即可跑通 **质量门禁** 并开始 **第一轮 Harness 迭代**。

## 1. 环境要求

- Python 3（用于 `workflow/` 下脚本，无需额外 pip 依赖）
- Git

## 2. 克隆后立刻执行（验证模板完好）

在仓库根目录执行：

```bash
python3 workflow/doctor.py
```

（等价于连续执行下面两条；亦可手动分步执行。）

```bash
python3 workflow/check_quality.py
python3 workflow/run.py
```

- `doctor.py`：依次调用门禁与状态守卫，适合克隆后一键确认环境。
- `check_quality.py`：检查必需文件、`task-state.json` 字段、harness **四件套**（同一日期的 change/review/retro/handoff）是否齐全、最新轮次 `context` 是否存在、最新 `review` 是否写明 `passed`，以及 plan 文件命名等。
- `run.py`：校验当前 `workflow/state/task-state.json` 中的状态、迭代预算、`current_plan` 是否存在且标记为 **active**。

若失败，按终端提示修正后再跑。也可使用 `make check` / `make run`（见根目录 `Makefile`）。

## 3. 理解三条主线

1. **真相源**：`workflow/state/task-state.json` —— 当前任务、状态、白皮书版本、预算。
2. **本轮计划**：`docs/plans/` 下的 markdown，须含 `status: active`（与 `run.py` 守卫一致）；索引用 `docs/plans/index.md`。
3. **本轮证据**：`harness/` 下按日期前缀对齐的四类文件 + 必需的 `harness/contexts/`（`context` 不参与四件套门禁，但属于仓库流程要求）。

## 4. 开启新一轮迭代（最小步骤）

概要如下；**逐步清单、命名与自检**见 **[03-new-iteration-manual-steps.md](./03-new-iteration-manual-steps.md)**（纯文档、无脚本）。当前模板采用 **Harness + Ralph-like manual loop + guard scripts**。

1. **Review**：阅读上一轮 `harness/changes/`、`harness/reviews/`、`harness/retros/`、`harness/handoffs/` 与 `harness/contexts/`（若有）。
2. **Plan**：复制 `docs/plans/plan-template.md` 为新文件，改标题与 `status`，填写 `goal` / `steps` / `done_criteria`；更新 `docs/plans/index.md`；将 `task-state.json` 的 `current_plan` 指向新 plan（若本轮切换主线）。
3. **Context**（必需）：在 `harness/contexts/` 新增本轮上下文说明。
4. **实现**：改代码或文档，并写 `harness/changes/<前缀>-change-<summary>.md`。
5. **验收**：写 `harness/reviews/`，必须包含 `passed: true` 或 `passed: false`。
6. **收尾**：`harness/retros/`、`harness/handoffs/`；必要时更新 `task-state.json`。
7. **提交前**：再次执行 `python3 workflow/check_quality.py`，确保四件套前缀一致。

文件命名约定：`YYYY-MM-DD-NN-<type>-<summary>.md`，四类目录使用**同一**日期前缀表示同一轮。

## 5. 与 Agent / Skills 的配合

- 人类或 Agent 均应以 `AGENTS.md` 为最高流程约定。
- 建议让 Agent 先加载 `skills/bootstrap/SKILL.md`，再加载 `skills/executor/SKILL.md`，与上述步骤一致。

## 6. 常见问题

**Q：`check_quality` 报四件套不齐或缺少 `context/review.passed`？**
A：先补齐 `harness/changes`、`reviews`、`retros`、`handoffs` 中**同一天前缀**的四个文件，再补上同前缀 `context`，并在最新 `review` 中写明 `passed: true` 或 `passed: false`。

**Q：`run.py` 报 plan 未 active？**  
A：打开 `current_plan` 指向的文件，确保正文中有单独一行 `status: active`（全小写）。

**Q：概念上这和「外循环 / Ralph Loop」什么关系？**  
A：见 [02-harness-and-ralph-loop.md](./02-harness-and-ralph-loop.md)。
