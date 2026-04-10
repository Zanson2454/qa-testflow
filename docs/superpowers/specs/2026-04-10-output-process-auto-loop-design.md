# 输出流程自动闭环与自我修复机制设计稿

## 1. 设计目标

- 将当前工程从“人工维持流程”升级为“系统驱动流程”。
- 让项目围绕 `Goal -> Plan -> Execute -> Validate -> Repair -> Review -> Deliver` 运转，而不是围绕“临时会话记忆”运转。
- 在当前探索阶段优先实现 `B` 型闭环：
  - 自动产出
  - 自动校验
  - 自动诊断
  - 自动生成修复方案
  - 高风险决策才进入人工 gate
- 架构上预留升级到 `C` 型闭环的能力：仅对高确定性、低副作用问题执行自动修复与自动重试。

## 2. 设计边界

### 2.1 in scope

- 项目级输出过程
- `plan/change/review/retro/handoff/context/state` 的生成、校验与闭环
- 失败诊断、修复建议、自动重试与停止条件
- 通用 validator/repair loop

### 2.2 out of scope

- 具体业务执行器的实现细节
- Playwright 或其它单一测试框架的页面交互设计
- 某个特定产品需求的业务规则细节

## 3. 当前工程判断

当前仓库已经具备闭环骨架，但没有自动闭环引擎。

### 3.1 已有能力

- `task-state.json` 已定义主状态机与重试预算
- `workflow/check_quality.py` 已做基础文件与四件套守卫
- `workflow/run.py` 已做状态合法性守卫
- `AGENTS.md`、whitepaper、skills 已定义流程规范
- `harness/` 目录已经能沉淀 change/review/retro/handoff

### 3.2 当前断点

- 没有统一 orchestrator 驱动整轮执行
- 失败后没有自动进入 `diagnose -> repair -> retry`
- `review/retro/handoff` 目前更偏向“人类记录”，还不是“机器下一步输入”
- 缺少标准化的执行证据包，导致失败时容易先怀疑 prompt，而不是先看执行现场

## 4. 设计原则

### 4.1 先观测，再修复

任何失败都必须先看：

1. 执行过程
2. 执行状态
3. 执行环境
4. 校验规则命中
5. 产物内容
6. 最后才看 prompt

### 4.2 反馈闭环必须可机读

`change/review/retro/handoff/context` 既要保留人类可读形式，也要能被下一轮自动消费。

### 4.3 自动修复必须可停止

每次自动修复都必须显式记录：

- `failure_fingerprint`
- `retry_budget`
- `stop_condition`
- `escalation_rule`

### 4.4 执行器与治理器解耦

业务执行器负责“按 plan 做事”；治理层负责“判断是否做对、错了怎么办、是否继续”。

### 4.5 先做 B，再选择性升级到 C

探索阶段优先建立稳健的半自动闭环，再把高确定性问题逐步升级为全自动修复。

## 5. 目标架构

```mermaid
flowchart TD
    A[Goal Interpreter] --> B[Planner]
    B --> C[Executor]
    C --> D[Evidence Collector]
    D --> E[Validator Pipeline]
    E --> F{Passed?}
    F -- Yes --> G[Artifact Writer]
    G --> H[State Manager]
    H --> I[Deliver or Next Step]
    F -- No --> J[Diagnoser]
    J --> K[Repair Planner]
    K --> L{Policy Gate}
    L -- Auto Repair --> M[Repair Executor]
    M --> C
    L -- Human Gate --> N[Human Decision]
    N --> C
```

### 5.1 Goal Interpreter

输入：

- 当前用户目标
- `task-state.json`
- 最新 `change/review/retro/handoff/context`

输出：

- `iteration_context`

职责：

- 明确本轮目标、边界、风险与历史约束
- 形成本轮唯一上下文输入，避免会话漂移

### 5.2 Planner

输出：

- `plan artifact`

职责：

- 定义 steps
- 定义 done_criteria
- 定义 validation gates
- 定义 retry policy
- 定义 escalation points

### 5.3 Executor

输出：

- `execution result`
- 原始日志
- 产物 diff

职责：

- 执行当前 plan step
- 不负责解释失败，不直接推进主状态

### 5.4 Evidence Collector

输出：

- `execution evidence package`

标准证据包至少包含：

- `process_snapshot`
- `state_snapshot`
- `environment_snapshot`
- `artifact_snapshot`
- `validator_results`

### 5.5 Validator Pipeline

固定顺序：

1. `schema`
2. `rule`
3. `state`
4. `static`
5. `runtime`
6. `review gate`

输出：

- `validation_report`

### 5.6 Diagnoser

职责：

- 对失败做分类，不直接修复

建议失败类型：

- `schema_failure`
- `rule_failure`
- `state_failure`
- `environment_failure`
- `runtime_failure`
- `artifact_quality_failure`
- `unknown_failure`

输出：

- `failure_class`
- `failure_fingerprint`
- `root_cause_hypothesis`

### 5.7 Repair Planner

职责：

- 基于失败类型输出修复方案

输出：

- `repair_plan`
- `repair_scope`
- `expected_effect`
- `risk_level`
- `auto_repair_allowed`

### 5.8 Policy Gate / Escalation Gate

职责：

- 决定自动修复、人工确认或终止升级

判定依据：

- 风险等级
- 修改范围
- 是否触达主状态定义
- 是否涉及外部环境
- 是否超过 retry budget

## 6. 目标工作流

```mermaid
flowchart TD
    A[读取目标与历史上下文] --> B[生成 iteration_context]
    B --> C[生成 Plan]
    C --> D[执行当前 Step]
    D --> E[采集 Evidence]
    E --> F[运行 Validator Pipeline]
    F --> G{是否通过}
    G -- 是 --> H[生成 Change Review Retro Handoff Context]
    H --> I[推进 Task State]
    I --> J{是否满足 done_criteria}
    J -- 是 --> K[交付 提交 推送]
    J -- 否 --> D
    G -- 否 --> L[Diagnoser 分类失败]
    L --> M[Repair Planner 生成修复方案]
    M --> N{是否允许自动修复}
    N -- 是 --> O[执行 Auto Repair]
    O --> P[增加 retry_count]
    P --> D
    N -- 否 --> Q[人工 Gate]
    Q --> D
```

## 7. Feedback Loop 设计

### 7.1 闭环位置

Feedback Loop 必须放在每次 validator 失败之后立即触发，而不是等到下一轮会话才处理。

正确闭环：

`execute -> evidence -> validate -> diagnose -> repair -> retry`

### 7.2 闭环层级

建议分三层：

- `step loop`：只修当前 step 的失败
- `iteration loop`：修本轮 plan 未达标问题
- `task loop`：修主线方向性偏差

### 7.3 闭环输入

- 最近失败的 `validation_report`
- 当前 `task-state`
- 最近一次 `retro`
- 最近一次 `handoff`
- 最近一次成功基线或基准产物

### 7.4 闭环输出

- 失败类型
- 修复策略
- 是否自动执行
- 当前重试次数
- 是否升级人工

## 8. 失败诊断顺序

为避免遇到问题就先改 prompt，诊断顺序固定如下。

### 8.1 执行过程

回答：

- 实际执行了哪些步骤
- 最后成功步骤是什么
- 失败发生在哪一步
- 是否发生跳步、重复或中断

### 8.2 执行状态

回答：

- 当前状态是否合法
- 状态是否与 plan 匹配
- 是否发生非法迁移
- `retry_count` 是否接近上限

### 8.3 执行环境

回答：

- 使用了什么配置
- 外部依赖是否可用
- 环境变量是否完整
- 权限、文件系统、网络是否满足前提

### 8.4 校验规则

回答：

- 哪个 validator 失败
- 属于哪一类失败
- 是阻断型还是可修复式

### 8.5 产物内容

回答：

- 缺了什么
- 格式错了什么
- 为何未通过验收

### 8.6 Prompt

只有前五项解释不通时，才检查 prompt 是否有歧义、上下文缺失或边界定义错误。

## 9. 通用 Validator / Repair Loop

不建议把机制收窄为 `ruff loop`。更好的抽象是 `validator loop`，其中 `ruff` 只是某一个 validator。

### 9.1 标准循环协议

```text
1. execute
2. collect evidence
3. run validators
4. classify failure
5. generate repair plan
6. apply repair
7. rerun impacted validators
8. pass -> finalize
9. fail -> retry or escalate
```

### 9.2 Validator 接口

每个 validator 至少返回：

- `validator_name`
- `stage`
- `passed`
- `severity`
- `fingerprint`
- `message`
- `affected_artifacts`
- `repair_hint`

### 9.3 Repair 接口

每个 repair action 至少包含：

- `repair_id`
- `target`
- `failure_fingerprint`
- `action_type`
- `risk_level`
- `can_auto_apply`
- `rollback_hint`

### 9.4 自动修复准入规则

仅当同时满足以下条件时允许自动修复：

- 单点失败，边界清晰
- 修复动作局部且可预测
- 不改变主目标与主状态定义
- 不依赖业务人工判断
- 不涉及高风险外部操作
- 未超过 retry budget

## 10. 产物模型升级建议

当前产物主要是 markdown，适合人读，但不利于系统消费。建议升级为“双轨产物”。

### 10.1 human-readable

- `plan.md`
- `change.md`
- `review.md`
- `retro.md`
- `handoff.md`
- `context.md`

### 10.2 machine-readable

- `iteration-context.json`
- `validation-report.json`
- `failure-record.json`
- `repair-plan.json`
- `execution-evidence.json`

### 10.3 最关键的结构化对象

- `iteration_context`
- `validation_report`
- `failure_record`
- `repair_plan`

### 10.4 review 的角色升级

`review` 不应只是结论记录，而应明确：

- 哪些 validator 通过或失败
- 当前风险等级
- 是否允许自动 repair
- 是否允许推进状态

## 11. 人工介入点设计

最少人工干预不等于零人工。建议只保留以下人工 gate：

1. 目标变更
2. 高风险修复
3. 多次自动修复失败
4. 外部环境异常或权限问题

除此之外，应尽量由系统自动完成。

## 12. 推荐演进路径

### Phase 1：观测化

先补齐：

- execution log
- state snapshot
- environment snapshot
- artifact snapshot

目标：

- 失败可以稳定复盘
- 不再第一时间怀疑 prompt

### Phase 2：标准化校验

把现有检查统一收敛为 validator pipeline：

- schema
- rule
- state
- static
- runtime

目标：

- 所有失败都能进入统一分类

### Phase 3：半自动 repair

引入 repair planner，但先只自动给方案，不自动执行。

目标：

- 建立稳健的 `B` 型闭环

### Phase 4：选择性自动修复

将高确定性失败升级为自动修复：

- 命名不规范
- 文件缺失
- schema 不满足
- 低风险状态修正建议

目标：

- 向 `C` 型闭环演进

## 13. 成功标准

该机制上线后，应满足：

- 每次执行自动生成完整证据包
- 每次失败都能被分类，而不是笼统归因为“结果不对”
- 每次失败都有 repair plan
- 高确定性问题可自动修复并自动重试
- 人工介入点收敛到关键决策场景
- `review/retro/handoff/context` 能成为下一轮自动输入
- 系统具备明确停止条件，不出现无意义循环

## 14. 本设计的核心判断

- 当前最推荐的目标形态是 `B` 型闭环，而不是直接全自动 `C`
- `Feedback Loop` 必须成为运行时机制，而不是事后总结机制
- 失败定位必须优先看执行过程、执行状态、执行环境
- `ruff loop` 应升级为更通用的 `validator/repair loop`

## 15. 评审关注点

本设计稿提交后，建议优先评审以下问题：

1. `iteration_context`、`validation_report`、`repair_plan` 是否足以支撑后续自动化
2. 人工 gate 是否过多或过少
3. 哪些失败类型适合第一批自动修复
4. 现有 `harness` 文档是否需要同步演进为 markdown + json 双轨
