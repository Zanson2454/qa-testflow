# 交接模板（handoff）

> 用途：在新会话中快速恢复上下文，避免重复摸底。  
> 原则：只写“当前仍有效”的事实，失效过程请标注为历史信息。

## 1) 当前目标与范围

- **primary_goal**: [本轮/下一轮主目标]
- **in_scope**:
  - [范围内事项 1]
  - [范围内事项 2]
- **out_of_scope**:
  - [明确不承接事项]

## 2) 关键约束与决策

- **hard_constraints**:
  - [硬约束 1]
  - [硬约束 2]
- **fixed_decisions**:
  - [已定方案及原因]

## 3) 当前状态快照

- **task_id**: [task-xxx]
- **iteration**: [YYYY-MM-DD-01 / iter-xxx]
- **current_plan**: [docs/plans/xxx.md]
- **state**: [created/planning/...]
- **whitepaper_version**: [v1/v2]

## 4) 本轮产物与变更

- **changes_file**: [harness/changes/xxx.md]
- **review_file**: [harness/reviews/xxx.md]
- **retro_file**: [harness/retros/xxx.md]
- **summary**:
  - [关键改动摘要]

## 5) 验证结果

- **verified**:
  - [已验证内容]
- **not_verified**:
  - [未验证内容]
- **quality_checks**:
  - [执行过的检查命令与结果]

## 6) 风险与阻塞

- **risks**:
  - [风险项]
- **blockers**:
  - [阻塞项；无则写 无]
- **rollback**:
  - [回滚点/回滚方式]

## 7) 决定性证据

- [证据 1：命令输出 / 文件路径 / commit]
- [证据 2：命令输出 / 文件路径 / commit]

## 8) 下一会话起手顺序

1. [先做什么]
2. [再做什么]
3. [优先验证什么]

## 9) 交接元信息

- **owner**: [当前负责者]
- **timestamp**: [YYYY-MM-DD HH:mm]
- **notes**: [补充说明]
