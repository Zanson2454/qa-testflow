# 开箱即用的 Harness + Ralph-Loop 初始化收口设计

## 1. 目标

- 将当前仓库收口为“开箱即用的 Harness + Ralph-like 外循环工程脚手架”。
- 让初始化入口、质量门禁与治理文档保持最小一致，避免“文档要求一套、工具行为另一套”。
- 在不引入自动 orchestrator 的前提下，补齐最小闭环守卫。

## 2. 设计边界

### 2.1 In Scope

- 调整 `workflow/init_iteration.py`，默认生成 `context`。
- 调整 `Makefile` 的 `make init`，确保默认初始化行为与脚本一致。
- 调整 `workflow/check_quality.py`，对最新轮次增加以下最小守卫：
  - 最新四件套前缀必须存在对应的 `context`
  - 最新 `review` 必须包含明确的 `passed: true` 或 `passed: false`
- 更新 `AGENTS.md`、`docs/whitepaper/whitepaper-v1.md`、`docs/whitepaper/whitepaper-v2.md`、`GET_START.md`、`docs/guides/01-getting-started.md`、`docs/guides/03-new-iteration-manual-steps.md`、`workflow/README.md`，统一仓库定位与初始化说明。

### 2.2 Out of Scope

- 不新增自动状态推进或自动重试 orchestrator。
- 不扩展 `run.py` 为更强的状态迁移守卫。
- 不对历史所有 harness 记录做全面迁移；新守卫仅约束“最新轮次”。

## 3. 当前问题

### 3.1 初始化入口与治理规则不一致

- `AGENTS.md` 将 `context` 视为必需产物，但 `init_iteration.py` 目前只在显式传 `--context` 时才生成。
- `make init` 也不会默认生成 `context`，导致“开箱即用”的主入口无法直接产出完整闭环骨架。

### 3.2 门禁校验不足

- `workflow/check_quality.py` 目前只检查四件套同前缀，不检查该轮是否存在 `context`。
- `review` 当前只要求文件存在，不要求写出明确的 `passed` 结论，无法支撑最小验收真相。

### 3.3 文档定位存在偏差

- `whitepaper-v2` 的叙述强于当前实现，容易让使用者误以为仓库已具备更强的系统驱动执行能力。
- `whitepaper-v1` 仍以现行规范口吻出现，容易与当前模板能力边界混淆。
- `AGENTS.md` 顶部 `Project Goal` 仍为占位内容，仓库对外定位不够清晰。

## 4. 设计方案

### 4.1 脚手架默认生成完整五件套

- `workflow/init_iteration.py` 改为默认创建：
  - `change`
  - `review`
  - `retro`
  - `handoff`
  - `context`
- 保留 `--context` 参数兼容已有使用习惯，但其语义调整为“显式声明也会生成 `context`”，不再是默认关闭的开关。
- `--dry-run` 输出中默认展示 `context` 路径，帮助使用者在真正写入前确认行为。

### 4.2 门禁只约束最新轮次的最小闭环

- `workflow/check_quality.py` 在已有四件套交集基础上，继续取最新前缀。
- 对该最新前缀追加检查：
  - `harness/contexts/` 下必须存在同前缀 `context` 文件
  - `harness/reviews/` 下对应最新前缀的 `review` 文件内容必须匹配 `passed:\s*(true|false)`
- 仅检查最新轮次，避免历史占位文件或旧格式记录阻塞当前初始化体验。

### 4.3 文档明确“当前实现不是自动 orchestrator”

- `AGENTS.md`：补全项目目标，明确本仓库是“开箱即用的 Harness + Ralph-like 外循环脚手架”。
- `whitepaper-v2`：保留状态机、预算、外循环概念，但明确当前实现主要由文档约定与守卫脚本承接，不是全自动流程编排器。
- `whitepaper-v1`：改为历史/演进背景说明，避免继续承担当前执行规范角色。
- 上手与指南文档统一以下口径：
  - 初始化默认生成完整五件套
  - `check_quality.py` 会检查最新轮次的 `context` 与 `review.passed`
  - 当前仓库采用 Harness + Ralph-like manual loop + guard scripts

## 5. 影响文件

- 修改：`workflow/init_iteration.py`
- 修改：`workflow/check_quality.py`
- 修改：`Makefile`
- 修改：`AGENTS.md`
- 修改：`docs/whitepaper/whitepaper-v1.md`
- 修改：`docs/whitepaper/whitepaper-v2.md`
- 修改：`GET_START.md`
- 修改：`docs/guides/01-getting-started.md`
- 修改：`docs/guides/03-new-iteration-manual-steps.md`
- 修改：`workflow/README.md`

## 6. 验证方案

- 运行 `python3 workflow/check_quality.py`
- 运行 `python3 workflow/run.py`
- 运行 `python3 workflow/init_iteration.py --summary sample-bootstrap --dry-run`，确认默认输出包含 `context` 路径
- 补充最小测试，验证：
  - 最新轮次缺少 `context` 时 `check_quality.py` 失败
  - 最新轮次 `review` 未写 `passed: true|false` 时 `check_quality.py` 失败

## 7. 风险与控制

- 风险：旧记录格式不统一，可能与新门禁冲突。
  - 控制：守卫范围仅限定在“最新轮次”。
- 风险：脚本默认行为变化后，文档若不同步会造成认知错位。
  - 控制：同一轮同步更新所有初始化入口与说明文档。
- 风险：使用者误以为本轮会引入更强的自动化状态机。
  - 控制：在 whitepaper 与指南中明确“不做 orchestrator 扩展”。

## 8. 验收标准

- `init_iteration.py` 默认生成 `context`
- `make init` 与脚本默认行为一致
- `check_quality.py` 能守住“最新轮次必须有 context”和“最新 review 必须有 passed”
- `AGENTS.md` 与两版 whitepaper 对仓库定位不再冲突
- 上手文档能清楚说明当前模板的真实能力边界
