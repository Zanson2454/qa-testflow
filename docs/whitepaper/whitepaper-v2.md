# 智能体工程白皮书 v2（工程版）

## 1. 目的

本文定义一个可落地运行的 AI 工程体系，具备：

- 自主生成能力
- 结构化评估能力
- 迭代自修复能力
- 状态机约束与人工驱动执行能力
- 基于 Git 的迭代记忆能力

### 1.1 当前模板实现边界

当前仓库的默认形态是 **Harness + Ralph-like manual loop + guard scripts**：

- `harness/` 负责沉淀每轮证据；
- `workflow/check_quality.py` 与 `workflow/run.py` 负责最小结构与状态守卫；
- `AGENTS.md`、plan、review 负责流程执行与完成判断。

当前模板**不是**自动 orchestrator，不默认提供自动状态推进、自动重试或自动修复。

---

## 2. 核心系统模型

目标（Goal）→ 计划（Plan）→ 设计（Design）→ 实现（Implement）→ 测试（Test）→ 评估（Evaluate）→ 反思（Reflect）→ 修复（Repair）→ 迭代（Loop）→ 交付（Deliver）

### 2.1 与 Ralph Loop（外循环）的关系

社区常见的 **Ralph Loop** 可概括为：执行 → **验证是否真正完成** → 未通过则注入反馈再迭代 → 在预算内停止。与本白皮书中的阶段可作如下对照（不必逐字绑定工具名）：

- **执行**：Plan / Implement 阶段产出与代码变更。
- **验证**：Evaluate / Review；在模板仓库中由 **门禁脚本（结构、状态）** 与 **harness/reviews（业务/任务完成度）** 共同承担，二者职责不同。
- **反馈再迭代**：Reflect / Repair 与下一轮 Plan；模板通过 `harness/retros`、`harness/handoffs` 与 `AGENTS.md` 的 Review First 承接。
- **停止**：`max_iterations`、`max_retry`、`stop_conditions`（见 `workflow/state/task-state.json`）。

模板仓库将上述外循环 **落实为 Harness 证据目录 + 状态文件 + 质量门禁**；是否叠加全自动 orchestrator 属于演进选项，见 `docs/superpowers/specs/2026-04-10-output-process-auto-loop-design.md`。面向使用者的操作说明见 `docs/guides/`。

---

## 3. 产物规范

所有产物必须遵循结构化 schema。

### 通用规范（Schema）

artifact（产物）:
  id: string
  type: string
  stage: string
  status: draft|validated|failed|approved
  content: {}

---

### 计划模板（Plan）

plan:
  goal: string
  steps:
    - name: string
      output: string
  done_criteria: []

---

### 评估模板（Evaluation）

evaluation:
  passed: boolean
  score: number
  errors: []
  suggestions: []

---

### 复盘模板（Reflection）

reflection:
  root_causes: []
  fix_strategy: []

---

### 变更产物（Change Artifact）

change:
  iteration: string
  commits: []
  files: []
  summary: string
  risks: []
  unresolved: []

---

### 续接包（Continuation Packet）

continuation:
  task_id: string
  commit_range: string
  last_change: string
  evaluation_summary: string
  unresolved: []
  next_focus: []

---

## 4. 评估规范

### 评估器

- 模式校验（schema）
- 规则校验（rule）
- 静态检查（lint）
- 测试验证（test）
- 集成验证（integration）

### 执行顺序

Schema → Rule → Static → Runtime

---

## 5. 执行协议

### 状态

created → planning → designing → implementing → testing → reviewing → repairing → approved

### 规则

- 不允许跳阶段
- 状态迁移前必须完成评估；在当前模板中，这主要通过 review、plan 与 guard scripts 协同落实
- 允许修复循环，但必须有上限

---

## 6. 状态机

状态迁移需要同时满足：

- 成功条件（success conditions）
- 失败路由（failure routing）
- 重试上限（retry caps）

---

## 7. 预算与停止策略

预算上限（limits）:
  max_iterations: 8
  max_retry: 3

停止条件（stop_conditions）:

- 重复失败（repeated failure）
- 严重错误（critical error）

---

## 8. 变更追踪系统

每轮必须记录：

- 代码差异（git diff）
- 影响模块（affected modules）
- 评估结果（evaluation results）
- 未解决问题（unresolved issues）

---

## 9. 工具链

必需能力（Required）:

- AI 生成器（AI generator）
- 文件系统访问（file system access）
- 命令执行（command execution）
- 测试执行器（test runner）
- 评估引擎（evaluator engine）
- 状态跟踪器（state tracker）

---

## 10. 示例流程（API 测试框架）

1. 生成计划
2. 评估计划
3. 生成 client + schema
4. 运行测试
5. 修复失败项
6. 重复直到通过

---

## 11. 成功标准

- 自动化比例 ≥80%
- 迭代闭环稳定
- 错误复发率持续下降

---

## 12. 结论

该体系让 AI 在结构化约束下，以可审计、可迭代、自我改进的方式完成工程任务。
