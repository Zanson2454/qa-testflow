import json
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
