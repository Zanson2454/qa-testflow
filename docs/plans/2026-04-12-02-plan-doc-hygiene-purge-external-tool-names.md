# 2026-04-12-02 exec plan doc hygiene purge external tool names

status: completed

## context

- 承接 `2026-04-12-01` 对模板收敛的方向：历史审计文档中仍残留某浏览器自动化商业工具名称，与「完全空白、无历史业务痕迹」的模板目标不一致。
- 用户明确：仓库内**完全不出现**该工具名称（大小写不敏感）。

## goal

- 全库移除该工具名称字符串；删除仅用于记录「移除该工具」的上一轮专用 plan/审计文件，避免文件名与正文再次引入名称。
- 对其余历史 handoff/review/plan 中的命令与表述做中性化（浏览器 E2E / 项目侧运行器），保留审计语义。

## steps

1. 全库检索工具名称字符串 -> 确认影响面（仅 Markdown 与索引）。
2. 删除 `2026-04-12-01` 专用 plan 与 harness 四件套文件 -> 去除自指文档。
3. 逐文件改写仍含该名称的历史审计与设计稿 -> 中性表述。
4. 更新 `docs/plans/index.md`、`README.md` 示例引用 -> 指向本轮 context。
5. 运行 `python3 workflow/check_quality.py` 与 `python3 workflow/run.py` -> 验证门禁未被破坏。
6. 再次全库检索确认零匹配 -> 作为硬验收。

## done_criteria

- [x] 全库对该工具名称（不区分大小写）零匹配。
- [x] `workflow/check_quality.py` 与 `workflow/run.py` 通过。
- [x] 本轮 `plan/change/review/retro/context/handoff` 已落盘。
