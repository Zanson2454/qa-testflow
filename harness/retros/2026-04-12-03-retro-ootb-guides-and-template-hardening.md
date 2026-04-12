# 2026-04-12-03 retro ootb guides and template hardening

- 文档与工程分层：先 guides 再 Makefile/门禁，避免「只有 README 一段话」的弱引导。
- 将 guides 纳入 `REQUIRED_FILES` 会强制模板完整性；若未来提供「极简版」分支，需同步维护 `check_quality` 的 profile 或文档说明。
- 下轮可评估：在 `workflow/run.py` 中于通过时打印 `docs/guides` 一行提示（可选，避免打扰 CI）。
