# 2026-04-12-05 exec plan fix guide agents alignment

status: active

## context

- 承接 `2026-04-12-03` 的 guides 加固与后续对 `docs/guides/03-new-iteration-manual-steps.md` 的 review。
- review 发现该 guide 与 `AGENTS.md` 存在 3 处不一致：`Review First` 范围过窄、`context` 被写成可选、缺少 commit/push 收尾要求。
- 本轮只修文档一致性，不修改 `task-state.json`、状态机逻辑或门禁脚本。

## goal

- 修复 `docs/guides/03-new-iteration-manual-steps.md`，使其与 `AGENTS.md`、`workflow/run.py`、`workflow/check_quality.py` 的当前约束保持一致。

## steps

1. 回读相关约束与 guide 现状 -> 锁定需修的 3 处流程冲突
2. 修改 guide 文案 -> 补全 `Review First`、`context` 必需、commit/push 收尾
3. 视需要同步更新索引或关联说明 -> 避免入口文案与正文不一致
4. 补齐本轮 `context/change/review/retro/handoff` -> 形成可追溯证据
5. 运行 `python3 workflow/check_quality.py` 与 `python3 workflow/run.py` -> 验证模板仍通过门禁

## done_criteria

- [ ] `docs/guides/03-new-iteration-manual-steps.md` 已覆盖 `change/review/retro/handoff/context` 的 `Review First`
- [ ] `context` 不再被描述为可选产物
- [ ] guide 已明确任务完成后的 commit/push 要求
- [ ] `python3 workflow/check_quality.py` 与 `python3 workflow/run.py` 通过
