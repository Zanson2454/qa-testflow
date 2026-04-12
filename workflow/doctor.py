#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开箱自检：在仓库根目录依次运行质量门禁与状态守卫，用于克隆后或提交前快速确认环境可用。

用法：python3 workflow/doctor.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    py = sys.executable
    steps = [
        ("check_quality.py", [py, str(root / "workflow" / "check_quality.py")]),
        ("run.py", [py, str(root / "workflow" / "run.py")]),
    ]
    for name, cmd in steps:
        print(f"--- 运行 {name} ---", flush=True)
        r = subprocess.run(cmd, cwd=str(root))
        if r.returncode != 0:
            print(f"[FAIL] {name} 退出码 {r.returncode}")
            return r.returncode
    print("[PASS] doctor：门禁与状态守卫均通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
