# GET_START — 详细上手说明

本文是 **qa-testflow** 仓库的**单一详细入口**：从克隆验证、核心概念、目录说明，到「新一轮迭代」的完整文档步骤与常见问题。  
更轻量的分篇说明仍在 `docs/guides/`；协作强制规则以 **`AGENTS.md`** 为准。

---

## 1. 本仓库是什么

- **定位**：基于 **Agent Harness** 的通用工程化模板，强调 **Plan-Driven**、证据留痕、状态守卫与审计闭环；当前形态是 **Harness + Ralph-like manual loop + guard scripts**。
- **不预绑定**：具体业务代码、测试框架（如 UI/E2E）、运行时依赖由使用方按需添加；模板提供 **流程、目录、门禁与文档骨架**。
- **白皮书**：工程约定见 `docs/whitepaper/`，执行时 **`workflow/state/task-state.json` 中的 `whitepaper_version`** 应与所选白皮书版本一致（通常为 `v2`）。

---

## 2. 环境要求

| 项 | 说明 |
|----|------|
| Python 3 | 仅用于运行 `workflow/` 下脚本，**无需** `pip install` 项目依赖即可跑门禁 |
| Git | 用于版本管理与协作 |
| Make（可选） | 仓库根目录提供 `Makefile`，封装 `make check` / `make run` / `make doctor` 等 |

---

## 3. 克隆后第一件事（约 5 分钟）

### 3.0 推荐：一键自检（等价于连续执行 check + run）

```bash
python3 workflow/doctor.py
# 或
make doctor
```

### 3.1 分步执行（与上等价）

在**仓库根目录**执行：

```bash
python3 workflow/check_quality.py
python3 workflow/run.py
```

或使用：

```bash
make check
make run
```

### 3.2 `check_quality.py` 做什么

- 校验一批**必需文件**存在（含 `AGENTS.md`、`docs/guides/*`、plan 模板等，见脚本内 `REQUIRED_FILES`）。
- 校验 `workflow/state/task-state.json` 含关键字段。
- 校验 `current_plan` 指向的文件**存在**。
- 校验 `harness/changes`、`reviews`、`retros`、`handoffs` 下文件名符合正则，且存在**同一前缀** `YYYY-MM-DD-NN` 的 **四件套**（change / review / retro / handoff 各至少一个同前缀文件）。
- 校验最新轮次存在对应 `harness/contexts` 记录，且最新 `review` 写明 `passed: true` 或 `passed: false`。

### 3.3 `run.py` 做什么

- 读取 `task-state.json`，检查当前 `current_state` 是否在允许集合内、`retry_count` / `current_iteration` 是否超出预算等。
- 检查 **`current_plan`** 指向的 markdown 文件**正文**中含一行 **`status: active`**（全小写）。  
  因此：**守卫的是「当前主 plan」**，不是 `docs/plans/` 下所有文件。

若任一步失败：根据终端英文/中文提示逐项修正后再执行。

---

## 4. 三条主线（必须先建立心智模型）

1. **状态真相源**：`workflow/state/task-state.json`  
   - 任务 id、当前状态、当前迭代、**当前主 plan 路径**、白皮书版本、`max_iterations` / `max_retry`、状态迁移规则等。

2. **本轮执行计划**：`docs/plans/*.md`  
   - 至少有一份被 `current_plan` 指向，且含 `status: active`。  
   - 索引用 `docs/plans/index.md`；新建计划可复制 `docs/plans/plan-template.md`。

3. **本轮审计证据（Harness）**：`harness/`  
   - **四件套**（必参与门禁交集）：`changes` / `reviews` / `retros` / `handoffs`，文件名前缀须一致。  
   - **必需**：`harness/contexts/`（上下文，不参与四件套交集，但属于仓库流程要求）。

---

## 5. 目录与文件速查

```text
AGENTS.md                 # 人机协作强制规则（优先级最高）
GET_START.md              # 本文：详细上手（根目录单一入口）
docs/guides/              # 分篇指南（轻量/专题）
docs/plans/               # 执行计划与 index
docs/templates/           # change/review/plan 等结构化模板
docs/whitepaper/          # 白皮书
skills/                   # bootstrap / executor，供 Agent 按步骤加载
harness/                  # 每轮审计证据（change/review/retro/handoff + contexts）
workflow/
  state/task-state.json   # 状态机与当前 plan 指针
  check_quality.py        # 质量门禁
  run.py                  # 状态与 active plan 守卫
  README.md               # 脚本级说明
src/                      # 业务代码占位（按需扩展）
```

---

## 6. 协作与 Agent：建议顺序

1. 人类与 Agent 均遵守 **`AGENTS.md`**（Review First、Plan Driven、Iterative Evidence、State Truth 等）。
2. 建议 Agent 加载顺序：  
   `skills/bootstrap/SKILL.md` → `skills/executor/SKILL.md`  
   与本文「新一轮迭代」步骤一致。
3. **单一主线**：同一迭代内不要并行两个无关大主题（见 `AGENTS.md` Single Thread）。

---

## 7. 新一轮迭代 — 文档步骤 + 可选脚手架

手工步骤与 **`docs/guides/03-new-iteration-manual-steps.md`** 一致；亦可先用脚本生成五件套骨架再编辑：

```bash
python3 workflow/init_iteration.py --summary my-feature-name
# 默认同时生成 context；仅预览路径：加 --dry-run
# 或：make init SUMMARY=my-feature-name
```

### 7.1 约定前缀

- 形式：`YYYY-MM-DD-NN-<type>-<summary>.md`  
- `NN`：当日序号（`01`、`02`…）。  
- `summary`：**小写英文**、连字符、无空格，例如 `add-login-guard`。

### 7.2 Review First

- 阅读最新 `harness/changes/`，确认上一轮改动、风险与未解决项。
- 阅读最新 `harness/reviews/`，确认上一轮验收结论与未通过项。
- 阅读最新 `harness/retros/` 与 `harness/handoffs/`，确认下一轮建议、风险与起手顺序。
- 阅读最新 `harness/contexts/`，确认承接关系、本轮边界与非目标。

### 7.3 Plan

1. 复制 `docs/plans/plan-template.md` → `docs/plans/YYYY-MM-DD-NN-plan-<summary>.md`。  
2. 填写 `goal`、`steps`、`done_criteria`；需要执行时再设 `status: active`。  
3. 更新 `docs/plans/index.md`。  
4. 若切换主线：修改 `task-state.json` 的 **`current_plan`** 指向新文件；且 **`run.py` 只校验该文件** 内含 `status: active`。

### 7.4 Context（必需）

- 新建 `harness/contexts/YYYY-MM-DD-NN-context-<summary>.md`，写明承接关系、范围、非目标与本轮差异。`context` 虽不参与四件套门禁，但不应省略。

### 7.5 四件套（同一前缀）

| 目录 | 示例 |
|------|------|
| `harness/changes/` | `…-change-<summary>.md` |
| `harness/reviews/` | `…-review-<summary>.md`（须含 `passed: true` 或 `passed: false`，并对照 `done_criteria`） |
| `harness/retros/` | `…-retro-<summary>.md` |
| `harness/handoffs/` | `…-handoff-<summary>.md` |

实现过程中同步更新 **change** 中的文件列表与意图。

### 7.6 提交前

```bash
python3 workflow/check_quality.py
python3 workflow/run.py
```

### 7.7 任务完成后的收尾

1. 回到本轮 `review`，确认是否已按 `done_criteria` 给出通过/失败结论。
2. 确认本轮 `change/review/retro/handoff/context` 已全部落盘且前缀一致。
3. 若本轮改动已验收通过，按仓库规则立即执行一次提交并推送，不要累计多个已通过任务再统一推送。
4. 若本轮未通过，则在 `review`、`retro`、`handoff` 中明确失败点、风险与下轮建议，不要把未完成状态伪装成完成。

---

## 8. Harness 与 Ralph Loop（外循环）— 一句话 + 延伸阅读

- **Harness**：把每轮证据落在 `harness/`，用门禁保证「四件套齐全、命名合法」，并对最新轮次补充 `context` 与 `review.passed` 守卫。
- **Ralph Loop**：社区常见的「执行 → 验证完成度 → 反馈再迭代 → 预算内停止」；本模板用 **review + 门禁 + task-state 预算** 对齐其**形状**，当前是 **manual loop + guard scripts**，**不**默认自带自动无限重试的编排脚本。
- 详细对照见 **[docs/guides/02-harness-and-ralph-loop.md](docs/guides/02-harness-and-ralph-loop.md)**。

---

## 9. 白皮书状态机（与 `task-state.json`）

典型状态链（概念上）：

`created → planning → designing → implementing → testing → reviewing → repairing → approved`

具体允许迁移见 `task-state.json` 的 `transition_rules`。  
**注意**：当前仓库的 `run.py` 主要做**合法性检查**与下一状态提示；**不会**替你自动推进状态机，推进仍由人与流程约定完成。

---

## 10. Git 与完成定义（摘要）

完整条款见 **`AGENTS.md`**，摘要如下：

- 每轮应有可追踪的提交说明；验收通过后按任务粒度推送（见 `AGENTS.md`）。  
- **Definition of Done**：目标按 plan 完成、`review` 结论明确、change/retro/context 等按规范落盘、门禁通过等。

---

## 11. 常见问题（FAQ）

**Q：`check_quality` 提示四件套不齐？**  
A：四个目录中必须存在**同一** `YYYY-MM-DD-NN` 前缀；若只有旧前缀，需新建本轮四件套或按团队规则处理历史文件（勿破坏命名正则）。

**Q：`run.py` 提示 plan 未 active？**  
A：打开 `task-state.json` 里 `current_plan` 指向的文件，确保正文有一行 **`status: active`**。

**Q：能否删掉 `docs/guides/` 里的某些页？**  
A：若该路径仍在 `check_quality.py` 的 `REQUIRED_FILES` 中，删除会导致门禁失败；fork 后若需精简，应同步修改门禁列表并自担一致性风险。

**Q：自动闭环 / orchestrator 在哪里？**  
A：演进讨论见 **`docs/superpowers/specs/2026-04-10-output-process-auto-loop-design.md`**；当前模板以**规范 + 门禁**为主。

---

## 12. 延伸阅读（按顺序）

| 文档 | 用途 |
|------|------|
| [AGENTS.md](AGENTS.md) | 强制工作方式与 Done 定义 |
| [docs/guides/README.md](docs/guides/README.md) | 分篇指南索引 |
| [docs/guides/01-getting-started.md](docs/guides/01-getting-started.md) | 精简快速上手 |
| [docs/guides/03-new-iteration-manual-steps.md](docs/guides/03-new-iteration-manual-steps.md) | 新一轮迭代步骤（与第 7 节一致，含 `init_iteration` 说明） |
| [docs/whitepaper/whitepaper-v2.md](docs/whitepaper/whitepaper-v2.md) | 产物与状态机 schema |
| [workflow/README.md](workflow/README.md) | 脚本行为说明 |

---

**文档版本说明**：若你修改了流程或门禁，请同步更新 **本文**、`docs/guides/` 与 `workflow/check_quality.py` 中的必需文件列表，避免「文档与行为不一致」。
