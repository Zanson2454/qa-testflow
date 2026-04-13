import json
import re
from pathlib import Path

REQUIRED_FILES = [
    "AGENTS.md",
    "GET_START.md",
    "workflow/state/task-state.json",
    "skills/bootstrap/SKILL.md",
    "skills/executor/SKILL.md",
    "docs/templates/plan.md",
    "docs/templates/review.md",
    "docs/templates/retro.md",
    "docs/templates/changes.md",
    "docs/templates/handover.md",
    "docs/guides/README.md",
    "docs/guides/01-getting-started.md",
    "docs/guides/02-harness-and-ralph-loop.md",
    "docs/guides/03-new-iteration-manual-steps.md",
    "docs/plans/plan-template.md",
    "workflow/README.md",
]

DATE_NAME_PATTERNS = {
    "harness/changes": r"^\d{4}-\d{2}-\d{2}-\d{2}-change-[a-z0-9-]+\.md$",
    "harness/reviews": r"^\d{4}-\d{2}-\d{2}-\d{2}-review-[a-z0-9-]+\.md$",
    "harness/retros": r"^\d{4}-\d{2}-\d{2}-\d{2}-retro-[a-z0-9-]+\.md$",
    "harness/handoffs": r"^\d{4}-\d{2}-\d{2}-\d{2}-handoff-[a-z0-9-]+\.md$",
}

REVIEW_PASSED_PATTERN = re.compile(r"passed:\s*(true|false)")


def _extract_prefix(file_name: str) -> str:
    # 文件命名前缀固定为 YYYY-MM-DD-XX，用于对齐同一轮证据四件套。
    matched = re.match(r"^(\d{4}-\d{2}-\d{2}-\d{2})-", file_name)
    return matched.group(1) if matched else ""


def _validate_harness_bundle() -> str:
    bucket = {}
    for dir_path in DATE_NAME_PATTERNS:
        files = sorted(Path(dir_path).glob("*.md"))
        if not files:
            print(f"[FAIL] {dir_path} 缺少记录文件，无法形成证据闭环。")
            _hint_docs()
            raise SystemExit(1)
        bucket[dir_path] = {_extract_prefix(file.name) for file in files if _extract_prefix(file.name)}

    shared_prefix = set.intersection(*bucket.values())
    if not shared_prefix:
        print("[FAIL] 未发现同一轮次同时存在 change/review/retro/handoff 四件套。")
        print("       请补齐 harness 记录后再提交。")
        _hint_docs()
        raise SystemExit(1)

    latest_prefix = sorted(shared_prefix)[-1]
    print(f"[PASS] harness 四件套已对齐，最新轮次前缀: {latest_prefix}")
    return latest_prefix


def _validate_latest_context(prefix: str) -> None:
    context_files = sorted(Path("harness/contexts").glob(f"{prefix}-context-*.md"))
    if not context_files:
        print(f"[FAIL] 最新轮次缺少 context 记录: {prefix}")
        print("       请补齐 harness/contexts 下同前缀文件后再提交。")
        _hint_docs()
        raise SystemExit(1)


def _validate_latest_review(prefix: str) -> None:
    review_files = sorted(Path("harness/reviews").glob(f"{prefix}-review-*.md"))
    valid_files = []
    for review_file in review_files:
        review_text = review_file.read_text(encoding="utf-8")
        if REVIEW_PASSED_PATTERN.search(review_text):
            valid_files.append(review_file)

    if not valid_files:
        print(f"[FAIL] 最新轮次 review 缺少明确的 passed: true/false 结论: {prefix}")
        print("       请在 review 文件中写明 passed 状态后再提交。")
        _hint_docs()
        raise SystemExit(1)


def _hint_docs():
    print("提示：请先阅读 docs/guides/01-getting-started.md（开箱步骤与常见问题）。")


def main():
    missing = [p for p in REQUIRED_FILES if not Path(p).exists()]
    if missing:
        print("[FAIL] 缺少必需文件：")
        for item in missing:
            print(f"- {item}")
        _hint_docs()
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
        _hint_docs()
        raise SystemExit(1)

    current_plan = Path(state["current_plan"])
    if not current_plan.exists():
        print(f"[FAIL] current_plan 不存在: {state['current_plan']}")
        _hint_docs()
        raise SystemExit(1)

    for dir_path, pattern in DATE_NAME_PATTERNS.items():
        p = Path(dir_path)
        if not p.exists():
            continue
        for file in p.glob("*.md"):
            if not re.match(pattern, file.name):
                print(f"[FAIL] 文件命名不符合规范: {file}")
                print(f"       期望正则: {pattern}")
                _hint_docs()
                raise SystemExit(1)

    latest_prefix = _validate_harness_bundle()
    _validate_latest_context(latest_prefix)
    _validate_latest_review(latest_prefix)
    print("[PASS] 基础质量门禁通过。")


if __name__ == "__main__":
    main()
