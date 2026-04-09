import json
import shutil
from pathlib import Path


def create_harness(project_name):
    root = Path(project_name)
    display_name = root.resolve().name if project_name in {".", "./"} else project_name

    # 0. 清理历史遗留目录（避免新旧结构并存）
    legacy_dirs = [
        root / "docs/exec-plans",
        root / "docs/governance",
        root / "orchestrator",
        root / ".cursor/skills",
        root / "skills/project-bootstrap",
        root / "skills/iteration-executor",
        root / "harness/evaluations",
        root / "harness/reflections",
        root / "harness/review-contexts",
        root / "harness/contexts",
    ]
    for legacy in legacy_dirs:
        if legacy.exists():
            shutil.rmtree(legacy)
    legacy_files = [
        root / "harness/changes/iter-001-change.md",
    ]
    for legacy_file in legacy_files:
        if legacy_file.exists():
            legacy_file.unlink()

    # 1. 核心目录结构 (根据参考文件要求，增加 templates 等目录)
    dirs = [
        "docs/plans",
        "docs/templates",
        "docs/whitepaper",
        "skills/bootstrap",
        "skills/executor",
        "harness/changes", "harness/reviews", "harness/retros", "harness/handoffs",
        "workflow/state", "workflow/prompts",
        "src", "tests"
    ]
    for d in dirs:
        (root / d).mkdir(parents=True, exist_ok=True)
        (root / d / ".gitkeep").touch()

    # 2. 抽象出的公共高标准 AGENTS.md
    agents_md = """# Project Goal
[请在此处简述项目目标]

# Working Mode
- **Review First**: 每次开始工作必须先 review 最近一轮 change record，再进入本轮 plan。
- **Plan Driven**: 必须先生成 plan，再进行实现；严禁跳过 plan 直接实现。
- **Iterative Evidence**: 每轮必须生成完整的 change record、review 和 retro。
- **Review Continuity**: 下一轮必须显式说明对上一轮改动的 context。

# Required Outputs
- **exec plan**: 详尽的执行步骤与验收标准。
- **change record**: 包含改动文件、意图、风险及未解决问题。
- **review**: 基于验收标准的通过/失败结论。
- **retro**: 本轮总结与下轮建议。
- **context**: 对历史改动的回溯说明。

# Operational Rules
- **No Dirty Tests**: 不允许保留仅用于调试的一次性测试文件到本轮结束。
- **Formal Baselines**: 不允许只做临时验证而不沉淀正式验收测试或测试场景。
- **Single Thread**: 同一 iteration 不允许并行推进两个不同主题的主线。
- **State Truth**: `task-state.json` 是当前确认主线的唯一状态源，严禁无授权覆盖。
- **Done Criteria**: 当询问阶段是否完成时，必须显式对照 plan 的 `done_criteria`。
- **Governance**: 项目内核心能力（如 skill）的变更必须遵循 `docs/templates/` 下的规范。

# Git & Sync Rules
- **Traceable Commits**: 每轮必须详细记录改动意图和风险。
- **Push on Success**: 只要本轮有代码改动且验收通过，结束前必须提交并推送到远程仓库。
- **Environment Sync**: 开始工作前必须确保本地状态与远程仓库及最近一轮 change record 同步。

# Test & Baseline Rules
- **Cleanup**: 过程中新增的临时调试脚本必须在结束前收敛或删除。
- **Regression Foundation**: 每轮验收通过后，沉淀的正式测试即作为回归基线，后续迭代必须优先回归。
- **Impact Analysis**: 若本轮改动影响既有基线，必须同步更新基线测试并在 change record 中说明。

# Definition of Done
- [ ] 目标产物按 plan 完成。
- [ ] Evaluation 结果为 `passed: true`。
- [ ] Change record、Retro、Context 完整落盘。
- [ ] 临时测试已收敛，正式回归测试基线已形成。
- [ ] 相关代码与配置已推送至远程仓库。
"""
    (root / "AGENTS.md").write_text(agents_md, encoding="utf-8")

    # 3. 初始状态文件
    state = {
        "task_id": "task-001",
        "current_iteration": 1,
        "current_state": "created",
        "current_goal": "Initial setup and first iteration planning",
        "current_plan": "docs/plans/iter-001-plan.md",
        "whitepaper_version": "v2",
        "allowed_states": [
            "created", "planning", "designing", "implementing", "testing", "reviewing", "repairing", "approved"
        ],
        "transition_rules": {
            "created": ["planning"],
            "planning": ["designing", "repairing"],
            "designing": ["implementing", "repairing"],
            "implementing": ["testing", "repairing"],
            "testing": ["reviewing", "repairing"],
            "reviewing": ["approved", "repairing"],
            "repairing": ["planning", "implementing", "testing", "reviewing"],
            "approved": []
        },
        "retry_count": 0,
        "max_iterations": 8,
        "max_retry": 3,
        "stop_conditions": ["repeated failure", "critical error"],
        "history": []
    }
    (root / "workflow/state/task-state.json").write_text(
        json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 4. 治理模板 (白皮书中的结构化产物要求)
    templates = {
        "plan.md": """# Plan Template

## goal
- [本轮目标]

## steps
1. [步骤名称] -> [预期产物]
2. [步骤名称] -> [预期产物]

## done_criteria
- [ ] [验收标准 1]
- [ ] [验收标准 2]
""",
        "review.md": """# Evaluation Template

passed: false
score: 0
errors:
  - [错误描述]
suggestions:
  - [改进建议]
""",
        "retro.md": """# Reflection Template

root_causes:
  - [根因]
fix_strategy:
  - [修复策略]
next_focus:
  - [下一轮重点]
""",
        "changes.md": """# Change Template

iteration: iter-XXX
commits:
  - [commit hash / range]
files:
  - [changed file]
summary: [本轮改动摘要]
risks:
  - [风险项]
unresolved:
  - [未解决问题]
""",
        "handover.md": """# Handoff Template

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
""",
    }
    for file_name, content in templates.items():
        (root / "docs/templates" / file_name).write_text(content, encoding="utf-8")

    # 5. 项目级 skills（将规则沉淀为可复用执行手册）
    project_skills = {
        "skills/bootstrap/SKILL.md": """---
name: bootstrap
description: 新一轮开始前的项目状态对齐与启动检查
---

# bootstrap

## 目标
在每轮开始前完成最小闭环检查，确保本地状态、白皮书版本与上一轮证据一致，再进入 planning。

## 执行步骤
1. 读取 `workflow/state/task-state.json`，确认：
   - `current_iteration`
   - `current_state`
   - `whitepaper_version`
2. 运行：
   - `python3 workflow/check_quality.py`
   - `python3 workflow/run.py`
3. 回顾上一轮证据（若存在）：
   - `harness/changes/YYYY-MM-DD-01-change-<summary>.md`
   - `harness/reviews/YYYY-MM-DD-01-review-<summary>.md`
   - `harness/retros/YYYY-MM-DD-01-retro-<summary>.md`
   - `harness/handoffs/YYYY-MM-DD-01-handoff-<summary>.md`
4. 在本轮 `docs/plans/` 产出 plan（包含 `status` 字段），明确 `done_criteria`。

## 退出条件
- 质量门禁通过
- 状态守卫通过
- 本轮 plan 已创建并可执行
""",
        "skills/executor/SKILL.md": """---
name: executor
description: 按白皮书状态机执行单轮迭代并沉淀证据
---

# executor

## 目标
围绕单一主题完成“计划 -> 实现 -> 验收 -> 复盘”的单轮闭环，并形成可追溯产物。

## 执行步骤
1. 读取并确认本轮 plan：
   - `docs/plans/iter-XXX-plan.md`
2. 实施改动并实时记录：
   - `harness/changes/YYYY-MM-DD-01-change-<summary>.md`
3. 执行验收并记录结果：
   - `harness/reviews/YYYY-MM-DD-01-review-<summary>.md`
   - 需要明确 `passed: true/false`
4. 输出反思与下一轮输入：
   - `harness/retros/YYYY-MM-DD-01-retro-<summary>.md`
   - `harness/handoffs/YYYY-MM-DD-01-handoff-<summary>.md`
5. 更新 `task-state.json`：
   - 仅推进合法状态迁移
   - 维护 `current_iteration`、`retry_count`、`history`
6. 再次执行：
   - `python3 workflow/check_quality.py`
   - `python3 workflow/run.py`

## 退出条件
- 本轮证据文件完整
- evaluation 已给出明确结论
- 状态文件通过守卫检查
""",
    }
    for rel_path, content in project_skills.items():
        (root / rel_path).write_text(content, encoding="utf-8")

    # 6. 生成示例资产（让首轮迭代可直接开跑）
    starter_assets = {
        "docs/plans/iter-001-plan.md": """# iter-001 plan

status: active

## goal
- 完成项目初始化后的第一轮规划与执行约束确认。

## steps
1. 对齐 `AGENTS.md` 与 `docs/whitepaper/` 规范
2. 编写首轮 change/review/retro/context
3. 更新 `task-state.json` 并确认下一轮 focus

## done_criteria
- [ ] 已生成并评审 iter-001 plan
- [ ] 已产出首轮 change/review/retro/context
- [ ] `review` 结果为 `passed: true`
""",
        "docs/plans/index.md": """# Plans Index

- current: `iter-001-plan.md`

## plans
- `iter-001-plan.md` - status: active
""",
        "harness/changes/2026-04-09-01-change-init-scaffold.md": """# 2026-04-09-01 change init scaffold

- files:
  - [列出本轮改动文件]
- intent:
  - [本轮改动意图]
- risks:
  - [风险项]
- unresolved:
  - [未解决问题]
""",
        "harness/reviews/2026-04-09-01-review-init-scaffold.md": """# 2026-04-09-01 review init scaffold

passed: false
score: 0
errors:
  - [待补充]
suggestions:
  - [待补充]
""",
        "harness/retros/2026-04-09-01-retro-init-scaffold.md": """# 2026-04-09-01 retro init scaffold

root_causes:
  - [待补充]
fix_strategy:
  - [待补充]
next_focus:
  - [待补充]
""",
        "harness/handoffs/2026-04-09-01-handoff-next-focus.md": """# 2026-04-09-01 handoff next focus

previous_changes:
  - [待补充]
evaluation_summary:
  - [待补充]
next_focus:
  - [待补充]
""",
    }
    for rel_path, content in starter_assets.items():
        (root / rel_path).write_text(content, encoding="utf-8")

    # 7. 生成状态守卫脚本 (状态机/预算/停止策略检查)
    run_py = """import json
from pathlib import Path

def _validate_state(state):
    errors = []
    current_state = state.get("current_state")
    allowed_states = state.get("allowed_states", [])
    transition_rules = state.get("transition_rules", {})
    retry_count = state.get("retry_count", 0)
    max_retry = state.get("max_retry", 0)
    current_iteration = state.get("current_iteration", 1)
    max_iterations = state.get("max_iterations", 1)
    current_plan = state.get("current_plan")

    if current_state not in allowed_states:
        errors.append(f"current_state 不在 allowed_states 中: {current_state}")

    if current_state not in transition_rules:
        errors.append(f"transition_rules 缺少当前状态定义: {current_state}")

    if retry_count > max_retry:
        errors.append(
            f"retry_count({retry_count}) 超过 max_retry({max_retry})，建议人工介入。"
        )

    if current_iteration > max_iterations:
        errors.append(
            f"current_iteration({current_iteration}) 超过 max_iterations({max_iterations})，建议暂停并复盘。"
        )

    if not current_plan:
        errors.append("current_plan 未设置。")
    else:
        plan_path = Path(current_plan)
        if not plan_path.exists():
            errors.append(f"current_plan 不存在: {current_plan}")
        else:
            plan_text = plan_path.read_text(encoding="utf-8")
            if "status: active" not in plan_text:
                errors.append(f"current_plan 未标记为 active: {current_plan}")

    return errors


def next_step():
    state_file = Path("workflow/state/task-state.json")
    state = json.loads(state_file.read_text())
    print(f"Current Iteration: {state.get('current_iteration')}")
    print(f"Current State: {state.get('current_state')}")
    print(f"Whitepaper Version: {state.get('whitepaper_version', 'unknown')}")
    print("-" * 20)

    errors = _validate_state(state)
    if errors:
        print("[Guard] 状态校验未通过：")
        for item in errors:
            print(f"- {item}")
        print("请先修复状态文件，再继续迭代。")
        return

    next_states = state.get("transition_rules", {}).get(state.get("current_state"), [])
    print("[Guard] 状态校验通过。")
    print(f"Allowed Next States: {next_states}")
    print("Please follow AGENTS.md and whitepaper rules to proceed.")

if __name__ == "__main__":
    next_step()
"""
    (root / "workflow/run.py").write_text(run_py, encoding="utf-8")

    # 8. 生成质量门禁脚本
    quality_py = """import json
from pathlib import Path

REQUIRED_FILES = [
    "AGENTS.md",
    "workflow/state/task-state.json",
        "skills/bootstrap/SKILL.md",
        "skills/executor/SKILL.md",
    "docs/templates/plan.md",
    "docs/templates/review.md",
    "docs/templates/retro.md",
    "docs/templates/changes.md",
    "docs/templates/handover.md",
]

DATE_NAME_PATTERNS = {
    "harness/changes": r"^\d{4}-\d{2}-\d{2}-\d{2}-change-[a-z0-9-]+\.md$",
    "harness/reviews": r"^\d{4}-\d{2}-\d{2}-\d{2}-review-[a-z0-9-]+\.md$",
    "harness/retros": r"^\d{4}-\d{2}-\d{2}-\d{2}-retro-[a-z0-9-]+\.md$",
    "harness/handoffs": r"^\d{4}-\d{2}-\d{2}-\d{2}-handoff-[a-z0-9-]+\.md$",
}


def main():
    missing = [p for p in REQUIRED_FILES if not Path(p).exists()]
    if missing:
        print("[FAIL] 缺少必需文件：")
        for item in missing:
            print(f"- {item}")
        raise SystemExit(1)

    state = json.loads(Path("workflow/state/task-state.json").read_text(encoding="utf-8"))
    required_keys = [
        "current_state",
        "current_iteration",
        "current_plan",
        "allowed_states",
        "transition_rules",
        "max_iterations",
        "max_retry",
        "whitepaper_version",
    ]
    absent_keys = [k for k in required_keys if k not in state]
    if absent_keys:
        print("[FAIL] task-state.json 缺少关键字段：")
        for item in absent_keys:
            print(f"- {item}")
        raise SystemExit(1)

    current_plan = Path(state["current_plan"])
    if not current_plan.exists():
        print(f"[FAIL] current_plan 不存在: {state['current_plan']}")
        raise SystemExit(1)

    import re
    for dir_path, pattern in DATE_NAME_PATTERNS.items():
        p = Path(dir_path)
        if not p.exists():
            continue
        for file in p.glob("*.md"):
            if not re.match(pattern, file.name):
                print(f"[FAIL] 文件命名不符合规范: {file}")
                print(f"       期望正则: {pattern}")
                raise SystemExit(1)

    print("[PASS] 基础质量门禁通过。")


if __name__ == "__main__":
    main()
"""
    (root / "workflow/check_quality.py").write_text(quality_py, encoding="utf-8")

    # 9. 生成初始化 README.md
    readme_md = f"""# {display_name}

基于 Agent Harness 的工程化项目骨架，支持 **Plan-Driven** 迭代开发、证据留痕与回归基线沉淀。

## 项目结构

```text
{display_name}/
├── AGENTS.md
├── docs/
│   ├── plans/
│   ├── templates/
│   └── whitepaper/
├── skills/
│   ├── bootstrap/SKILL.md
│   └── executor/SKILL.md
├── harness/
│   ├── changes/
│   ├── reviews/
│   ├── retros/
│   └── handoffs/
├── workflow/
│   ├── state/task-state.json
│   ├── prompts/
│   ├── run.py
│   └── check_quality.py
├── src/
└── tests/
```

## 快速开始

1. 初始化后进入项目根目录：
   - `cd {display_name}`
2. 查看当前任务状态：
   - `python3 workflow/run.py`
3. 执行基础质量门禁：
   - `python3 workflow/check_quality.py`
4. 按规范开始第一轮迭代：
   - 在 `docs/plans/` 创建本轮 plan（含 `status` 字段）
   - 在 `harness/changes/`、`harness/reviews/`、`harness/retros/`、`harness/handoffs/` 写入本轮产物
5. 参考示例资产开始首轮：
   - `docs/plans/iter-001-plan.md`
   - `docs/plans/index.md`
   - `harness/changes/2026-04-09-01-change-init-scaffold.md`
   - `harness/reviews/2026-04-09-01-review-init-scaffold.md`
   - `harness/retros/2026-04-09-01-retro-init-scaffold.md`
   - `harness/handoffs/2026-04-09-01-handoff-next-focus.md`
6. 更新主线状态：
   - 修改 `workflow/state/task-state.json`

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

## 迭代建议流程

1. 读取 `task-state.json`，确认当前迭代和目标。
2. 编写并评审执行计划（`docs/plans/`），并更新 `status` 与 `index.md`。
3. 按计划实现并记录变更（`harness/changes/`）。
4. 执行验收并写结论（`harness/reviews/`，`passed: true` 才能标记完成）。
5. 复盘与下一轮输入（`harness/retros/` 与 `harness/handoffs/`）。

## 注意事项

- 不保留一次性调试脚本或脏测试到迭代结束。
- 验收通过后形成正式回归基线，后续迭代优先回归。
- 若影响既有基线，需同步更新并在 change record 中说明影响。
"""
    (root / "README.md").write_text(readme_md, encoding="utf-8")

    # 10. 初始化白皮书文件与索引（如果不存在则创建）
    whitepaper_files = {
        "whitepaper-v1.md": """# Whitepaper v1

## Purpose
初版白皮书，定义 Agent Harness 的基础流程与产物规范。

## Notes
- 本文件建议作为历史基线，不再新增复杂规则。
""",
        "whitepaper-v2.md": """# Whitepaper v2

## Purpose
工程化增强版白皮书，作为当前默认执行规范。

## Notes
- 推荐与 `workflow/state/task-state.json` 中 `whitepaper_version` 保持一致。
- 若规则升级，请新增版本并在索引中说明差异。
""",
    }
    for name, content in whitepaper_files.items():
        path = root / "docs/whitepaper" / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    whitepaper_index = root / "docs/whitepaper/README.md"
    if not whitepaper_index.exists():
        whitepaper_index.write_text(
            "# Whitepaper Index\n\n- 在此目录维护项目白皮书与版本演进文档。\n- `whitepaper-v1.md`：初版规范\n- `whitepaper-v2.md`：工程化增强版规范（当前默认参考）\n",
            encoding="utf-8",
        )

    print(f"✨ 高标准 Harness 环境 '{display_name}' 初始化完成！")
    print(f"👉 核心规范已就绪：{display_name}/AGENTS.md")

if __name__ == "__main__":
    import sys
    create_harness(sys.argv[1] if len(sys.argv) > 1 else "new-project")
