import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class InitIterationDefaultsTest(unittest.TestCase):
    def test_dry_run_includes_context_by_default(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "workflow/init_iteration.py",
                "--summary",
                "sample-bootstrap",
                "--dry-run",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[dry-run] context:", result.stdout)


class CheckQualityLatestBundleTest(unittest.TestCase):
    # 这些测试只构造门禁运行所需的最小仓库骨架，避免污染真实工作区。
    def _make_minimal_repo(self, review_text: str, include_context: bool) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        root = Path(temp_dir.name)

        (root / "workflow").mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO_ROOT / "workflow/check_quality.py", root / "workflow/check_quality.py")

        required_files = [
            "AGENTS.md",
            "GET_START.md",
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
            "docs/plans/current.md",
            "workflow/README.md",
        ]
        for relative_path in required_files:
            file_path = root / relative_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            if relative_path == "docs/plans/current.md":
                file_path.write_text("# current plan\n\nstatus: active\n", encoding="utf-8")
            else:
                file_path.write_text("placeholder\n", encoding="utf-8")

        state_path = root / "workflow/state/task-state.json"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            json.dumps(
                {
                    "current_state": "planning",
                    "current_iteration": 1,
                    "current_plan": "docs/plans/current.md",
                    "allowed_states": ["planning"],
                    "transition_rules": {"planning": ["designing"]},
                    "max_iterations": 8,
                    "max_retry": 3,
                    "whitepaper_version": "v2",
                }
            ),
            encoding="utf-8",
        )

        prefix = "2026-04-13-01"
        harness_files = {
            "harness/changes": f"{prefix}-change-bootstrap-alignment.md",
            "harness/reviews": f"{prefix}-review-bootstrap-alignment.md",
            "harness/retros": f"{prefix}-retro-bootstrap-alignment.md",
            "harness/handoffs": f"{prefix}-handoff-bootstrap-alignment.md",
        }
        for directory, filename in harness_files.items():
            folder = root / directory
            folder.mkdir(parents=True, exist_ok=True)
            content = "placeholder\n"
            if directory == "harness/reviews":
                content = review_text
            (folder / filename).write_text(content, encoding="utf-8")

        if include_context:
            context_dir = root / "harness/contexts"
            context_dir.mkdir(parents=True, exist_ok=True)
            (context_dir / f"{prefix}-context-bootstrap-alignment.md").write_text(
                "placeholder\n",
                encoding="utf-8",
            )

        return root

    def test_check_quality_fails_when_latest_context_missing(self) -> None:
        repo_root = self._make_minimal_repo(review_text="passed: true\n", include_context=False)

        result = subprocess.run(
            [sys.executable, "workflow/check_quality.py"],
            cwd=repo_root,
            text=True,
            capture_output=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("context", result.stdout)

    def test_check_quality_fails_when_latest_review_has_no_passed_marker(self) -> None:
        repo_root = self._make_minimal_repo(review_text="review without passed field\n", include_context=True)

        result = subprocess.run(
            [sys.executable, "workflow/check_quality.py"],
            cwd=repo_root,
            text=True,
            capture_output=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
