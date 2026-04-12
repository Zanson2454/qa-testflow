# qa-testflow

基于 Agent Harness 的通用工程化模板，聚焦 **Plan-Driven** 迭代开发、证据留痕、状态守卫与审计闭环。

## 文档入口（推荐先读）

| 资源 | 说明 |
|------|------|
| [docs/guides/README.md](docs/guides/README.md) | **开箱即用**：命令、首轮迭代步骤、与 Ralph Loop 的对照 |
| [AGENTS.md](AGENTS.md) | Agent 与人类协作的强制流程 |
| [docs/whitepaper/whitepaper-v2.md](docs/whitepaper/whitepaper-v2.md) | 状态机与产物 schema：`task-state.json` 中 `whitepaper_version` 应对齐 |

## 项目结构

```text
qa-testflow/
├── AGENTS.md
├── docs/
│   ├── guides/          # 开箱步骤与 Harness / Ralph Loop 说明
│   ├── plans/
│   ├── templates/
│   └── whitepaper/
├── skills/
│   ├── bootstrap/SKILL.md
│   └── executor/SKILL.md
├── harness/
│   ├── changes/
│   ├── contexts/
│   ├── reviews/
│   ├── retros/
│   └── handoffs/
├── workflow/
│   ├── state/task-state.json
│   ├── prompts/
│   ├── run.py
│   └── check_quality.py
└── src/
```

## 快速开始

1. 进入仓库根目录：`cd qa-testflow`
2. 跑通门禁与状态守卫：
   - `python3 workflow/check_quality.py`
   - `python3 workflow/run.py`  
   （或 `make check`、`make run`）
3. 跟做「首轮迭代」与概念说明：**[docs/guides/01-getting-started.md](docs/guides/01-getting-started.md)**
4. 新建一轮计划时，可复制 `docs/plans/plan-template.md`，更新 `docs/plans/index.md` 与 `workflow/state/task-state.json` 中的 `current_plan`
5. 参考示例（历史轮次，仅作格式参考）：
   - `docs/plans/iter-001-plan.md`
   - `harness/contexts/2026-04-12-03-context-ootb-guides-and-template-hardening.md`（本轮：开箱文档与模板加固）
   - `harness/changes/2026-04-09-01-change-init-scaffold.md` 等早期 `harness/*` 样例

## Agent 工作模式

请以 `AGENTS.md` 为准，核心原则包括：

- **Review First**：先回顾上一轮变更，再开启本轮计划。
- **Plan Driven**：先 plan 后实现，禁止跳过 planning。
- **Iterative Evidence**：每轮必须沉淀 change/review/retro/context。
- **State Truth**：`task-state.json` 是当前主线状态唯一真相源。
- **Done Criteria**：完成判断必须对照 plan 中 `done_criteria` 与 review 结果。

## 项目级 Skills

- `bootstrap`：每轮开始前进行状态对齐、质量门禁与上一轮证据回顾。
- `executor`：按白皮书状态机执行单轮闭环并落盘证据。
- 存放路径：`skills/`
- 建议顺序：先执行 `bootstrap`，再执行 `executor`

## 白皮书对齐

- 白皮书规范入口：`docs/whitepaper/`
- 白皮书执行版本：`task-state.json -> whitepaper_version`
- 执行状态机：`created -> planning -> designing -> implementing -> testing -> reviewing -> repairing -> approved`
- 预算与停止策略：默认 `max_iterations=8`、`max_retry=3`，命中停止条件需人工介入
- 结构化产物模板：`docs/templates/*.md`
- 建议文件命名：`YYYY-MM-DD-01-<type>-<summary>.md`
- 业务实现、测试框架与运行依赖不在模板中预绑定，应由使用方项目按需补入

## 迭代建议流程

1. 读取 `task-state.json`，确认当前迭代和目标。
2. 编写并评审执行计划（`docs/plans/`），并更新 `status` 与 `index.md`。
3. 补齐本轮上下文（`harness/contexts/`），明确承接关系与边界。
4. 按计划实现并记录变更（`harness/changes/`）。
5. 执行验收并写结论（`harness/reviews/`，`passed: true` 才能标记完成）。
6. 复盘与下一轮输入（`harness/retros/` 与 `harness/handoffs/`）。

## 注意事项

- 不保留一次性调试脚本或脏测试到迭代结束。
- 验收通过后形成正式回归基线，后续迭代优先回归。
- 若影响既有基线，需同步更新并在 change record 中说明影响。
- 提交前必须通过 harness 四件套校验（change/review/retro/handoff）。
- 模板仓库默认只保留 Harness 核心骨架，不内置特定业务样例或特定测试框架实现。
