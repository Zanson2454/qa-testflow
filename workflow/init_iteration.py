#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成本轮 harness 五件套（change / review / retro / handoff / context）最小骨架，降低「开箱后手写文件名」成本。

用法（在仓库根目录执行）：
  python3 workflow/init_iteration.py --summary my-feature-name
  python3 workflow/init_iteration.py --summary my-feature --context --date 2026-04-12 --seq 03
  python3 workflow/init_iteration.py --summary my-feature --dry-run

summary 须为小写英文、数字与连字符（kebab-case），与门禁正则一致。
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

# 与 workflow/check_quality.py 中 harness 文件名正则一致：summary 段
_SUMMARY_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _next_seq_for_date(root: Path, day: str) -> str:
    """给定 YYYY-MM-DD，扫描 harness/changes 下已有序号，返回下一个两位序号字符串。"""
    changes = root / "harness" / "changes"
    pattern = re.compile(rf"^{re.escape(day)}-(\d{{2}})-change-")
    seqs: list[int] = []
    if changes.is_dir():
        for p in changes.glob("*.md"):
            m = pattern.match(p.name)
            if m:
                seqs.append(int(m.group(1)))
    return f"{max(seqs) + 1:02d}" if seqs else "01"


def _prefix(day: str, seq: str) -> str:
    return f"{day}-{seq}"


def _validate_summary(name: str) -> None:
    if not _SUMMARY_RE.match(name):
        raise SystemExit(
            "参数 --summary 不符合命名规范：仅允许小写字母、数字与连字符（kebab-case）。"
            f" 当前值: {name!r}"
        )


def _render_change(prefix: str, summary: str) -> str:
    return (
        f"# {prefix} change {summary}\n\n"
        "- files:\n"
        "  - \n"
        "- intent:\n"
        "  - \n"
        "- risks:\n"
        "  - \n"
        "- unresolved:\n"
        "  - \n"
    )


def _render_review(prefix: str, summary: str) -> str:
    return (
        f"# {prefix} review {summary}\n\n"
        "passed: false\n\n"
        "- 对照本轮 plan 的 done_criteria 填写结论。\n"
    )


def _render_retro(prefix: str, summary: str) -> str:
    return (
        f"# {prefix} retro {summary}\n\n"
        "- \n"
    )


def _render_handoff(prefix: str, summary: str) -> str:
    return (
        f"# {prefix} handoff {summary}\n\n"
        "## 当前目标\n\n"
        "- \n\n"
        "## 下一会话建议\n\n"
        "1. \n\n"
        "## 元信息\n\n"
        "- **owner**: \n"
    )


def _render_context(prefix: str, summary: str) -> str:
    return (
        f"# {prefix} context {summary}\n\n"
        "- 承接上一轮：\n"
        "- 本轮范围：\n"
        "- 非目标：\n"
    )


def _write_if_absent(path: Path, content: str) -> None:
    if path.exists():
        raise SystemExit(f"文件已存在，跳过写入以避免覆盖: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"[OK] 已写入: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="初始化本轮 harness 五件套文件骨架。"
    )
    parser.add_argument(
        "--summary",
        required=True,
        help="英文短名 kebab-case，例如 add-login-guard",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="日期 YYYY-MM-DD，默认今天",
    )
    parser.add_argument(
        "--seq",
        default=None,
        help="两位序号 01-99；默认按 harness/changes 同日期自动递增",
    )
    parser.add_argument(
        "--context",
        action="store_true",
        help="兼容保留参数；当前默认也会创建 harness/contexts 下的 context 文件。",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印将要创建的路径，不写入文件",
    )
    args = parser.parse_args()

    _validate_summary(args.summary)

    root = _repo_root()
    day = args.date or date.today().isoformat()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", day):
        raise SystemExit("--date 须为 YYYY-MM-DD")

    seq = args.seq or _next_seq_for_date(root, day)
    if not re.match(r"^\d{2}$", seq):
        raise SystemExit("--seq 须为两位数字，例如 01")

    prefix = _prefix(day, seq)
    base_names = {
        "changes": f"{prefix}-change-{args.summary}.md",
        "reviews": f"{prefix}-review-{args.summary}.md",
        "retros": f"{prefix}-retro-{args.summary}.md",
        "handoffs": f"{prefix}-handoff-{args.summary}.md",
    }

    paths = {
        "changes": root / "harness" / "changes" / base_names["changes"],
        "reviews": root / "harness" / "reviews" / base_names["reviews"],
        "retros": root / "harness" / "retros" / base_names["retros"],
        "handoffs": root / "harness" / "handoffs" / base_names["handoffs"],
    }

    ctx_path = root / "harness" / "contexts" / f"{prefix}-context-{args.summary}.md"

    if args.dry_run:
        print(f"前缀: {prefix}  summary: {args.summary}")
        for label, p in paths.items():
            print(f"[dry-run] {label}: {p}")
        print(f"[dry-run] context: {ctx_path}")
        print("提示：创建后请执行 python3 workflow/check_quality.py 验证四件套交集。")
        return 0

    _write_if_absent(paths["changes"], _render_change(prefix, args.summary))
    _write_if_absent(paths["reviews"], _render_review(prefix, args.summary))
    _write_if_absent(paths["retros"], _render_retro(prefix, args.summary))
    _write_if_absent(paths["handoffs"], _render_handoff(prefix, args.summary))
    _write_if_absent(ctx_path, _render_context(prefix, args.summary))

    print(f"完成。本轮前缀: {prefix}")
    print("下一步：补全 change、编写/更新 docs/plans、执行实现后把 review.passed 改为 true，再运行：")
    print("  python3 workflow/check_quality.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
