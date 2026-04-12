# Harness 与 Ralph Loop（外循环）

## 1. 术语

- **Harness（本仓库含义）**：在 `harness/` 中按约定落盘的 **change / review / retro / handoff**，以及必需的 **context**（不参与四件套门禁），再加上 `workflow/check_quality.py` 的结构校验，形成可审计的迭代证据包。
- **Ralph Loop（社区常见说法）**：在 AI 辅助开发里，用 **执行 → 验证是否完成 → 未通过则带反馈再试 → 在预算内停止** 的外层循环；往往配合「每轮独立上下文、文件系统持久化、尽量小步提交」。

二者不是互斥标签：**本模板用 Harness 落实「每轮可验证、可交接」**；与 Ralph Loop 在 **流程形状** 上可对齐，但 **自动化程度** 取决于你是否额外实现 orchestrator（见下文）。

## 2. 对照表

| Ralph Loop 常见环节 | 在本模板中的落点 |
|---------------------|------------------|
| 执行（做任务） | `docs/plans` 的 steps + 实际改动；`harness/changes` 记录意图与文件列表 |
| 验证完成度 | `harness/reviews`（`passed`）；门禁脚本只做 **结构/状态** 校验，不判断业务是否「真完成」 |
| 反馈再迭代 | `harness/retros`、`harness/handoffs`、`harness/contexts` 给下一轮；`AGENTS.md` 要求 Review First |
| 停止条件 | `task-state.json` 的 `max_iterations`、`max_retry`、`stop_conditions`；`workflow/run.py` 对部分越界给出提示 |
| 跨轮记忆 | Git 历史 + `harness/` + `docs/plans`，而非仅会话上下文 |

## 3. 本模板的边界（重要）

- **当前默认**：**规范驱动 + 门禁**，外循环由人或 Agent **按文档执行**，仓库内 **没有** 必须运行的「自动无限重试」脚本。
- **演进方向**：若需要机器编排的闭环（自动诊断、自动修复、消费 `history`），见 `docs/superpowers/specs/2026-04-10-output-process-auto-loop-design.md` 中的 B/C 型闭环讨论。

## 4. 实践建议

1. 每轮保持 **单一主题**（`AGENTS.md` Single Thread）。
2. 验收标准写进 plan 的 `done_criteria`，review 必须逐条对照。
3. 提交前跑 `check_quality`，避免四件套漂移。
4. 需要对外说明「我们采用 Harness + 类 Ralph 外循环」时，可直接引用本文与白皮书 `whitepaper-v2` 中的状态机章节。
