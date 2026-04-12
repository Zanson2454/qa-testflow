# 2026-04-12-05 context fix guide agents alignment

## 上一轮上下文

- `2026-04-12-03` 补充了 `docs/guides/`、`Makefile`、`workflow/README.md` 与门禁加固，目标是让模板开箱即用。
- `2026-04-12-04` 新增了 `docs/guides/03-new-iteration-manual-steps.md`，用于描述“无脚本的新一轮迭代步骤”。

## 本轮上下文

- 针对 `03-new-iteration-manual-steps.md` 的 review 发现：该 guide 在 `Review First`、`context` 必需性和 commit/push 收尾上与 `AGENTS.md` 不一致。
- 用户明确要求先修掉这些文档问题。

## 本轮约束

- 只修 guides 文档一致性，不引入脚本，不改状态文件。
- 保持单主题：不同时处理历史业务痕迹清理或 `ralph-loop` 实施。
