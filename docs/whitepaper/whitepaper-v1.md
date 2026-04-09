# Agent Harness 白皮书（v1.0）

## 1. 概述

本文定义一个 AI First 的工程系统，目标是实现：

- 自主产物生成
- 自动化评估
- 自我反思与修复
- 可控的迭代闭环
- 人工最终审批

---

## 2. 核心架构

Goal → Generator → Evaluator → Reflector → Repair → State Machine → Budget Control → Loop → Human Gate

---

## 3. 产物规范

定义所有结构化输出。

### 通用字段

- id
- type
- stage
- status
- content

### 产物类型

- Goal
- Plan
- Design
- Implementation
- Test
- Evaluation
- Reflection
- Delivery
- Change
- Review Context

---

## 4. 评估规范

所有输出都必须可被机器评估。

### 评估器

- Schema
- Rule
- Static
- Runtime
- Human Gate

### 输出格式

- passed
- score
- errors
- suggestions

---

## 5. 执行协议

### 状态

created → planning → designing → implementing → testing → reviewing → repairing → approved

### 规则

- 不允许跳阶段
- 状态迁移前必须评估
- 必须执行重试上限控制

---

## 6. 状态机

定义合法状态迁移，防止无限循环。

---

## 7. 预算与停止策略

- 最大迭代次数
- 每阶段最大重试次数
- 升级/人工介入规则

---

## 8. 变更追踪规范

### Change Artifact

- commit range
- changed files
- intent
- risks
- unresolved issues

### Review Context

- previous changes
- evaluation results
- next focus

### Continuation Packet

作为下一轮迭代的标准输入。

---

## 9. 工具链定义

### 必需组件

- AI generator
- file system ops
- command execution
- test runner
- evaluation engine
- state tracker

---

## 10. 成功标准

- ≥80% 任务可自主完成
- 评估闭环稳定运行
- 重复错误持续下降
- 人工介入最小化

---

## 11. 结论

该体系把 AI 使用方式从“对话式提示”提升为“结构化、自我改进”的工程系统。