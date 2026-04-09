# Agent Harness 白皮书 v2（工程版）

## 1. 目的

本文定义一个可落地运行的 AI 工程体系，具备：

- 自主生成能力
- 结构化评估能力
- 迭代自修复能力
- 状态机驱动执行能力
- 基于 Git 的迭代记忆能力

---

## 2. 核心系统模型

Goal → Plan → Design → Implement → Test → Evaluate → Reflect → Repair → Loop → Deliver

---

## 3. 产物规范

所有产物必须遵循结构化 schema。

### 通用 Schema

artifact:
  id: string
  type: string
  stage: string
  status: draft|validated|failed|approved
  content: {}

---

### Plan 模板

plan:
  goal: string
  steps:
    - name: string
      output: string
  done_criteria: []

---

### Evaluation 模板

evaluation:
  passed: boolean
  score: number
  errors: []
  suggestions: []

---

### Reflection 模板

reflection:
  root_causes: []
  fix_strategy: []

---

### Change Artifact

change:
  iteration: string
  commits: []
  files: []
  summary: string
  risks: []
  unresolved: []

---

### Continuation Packet

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
- 状态迁移前必须完成评估
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