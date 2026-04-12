# 2026-04-12-02 handoff doc hygiene purge external tool names

## 当前状态

- 模板仓库内已对指定浏览器自动化商业工具名称完成全量清除（含历史审计中的命令片段与专用 plan 文件名）。
- 质量门禁：`workflow/check_quality.py`、`workflow/run.py` 已通过。

## 下一会话建议起手

1. 阅读本轮 plan：`docs/plans/2026-04-12-02-plan-doc-hygiene-purge-external-tool-names.md`
2. 若引入新的端到端或 UI 自动化能力，在业务仓库内自行选型；本模板不预绑定任何商业工具名称。

## 交接元信息

- **owner**: assistant
- **notes**: 若需「完全无 npm/Node 痕迹」等更强空白模板，应另开独立迭代并评估对历史 handoff 的删减范围。
