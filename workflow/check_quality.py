import json
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
