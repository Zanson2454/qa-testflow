# 2026-04-12-02 change doc hygiene purge external tool names

- files:
  - 删除：`docs/plans/2026-04-12-01-plan-template-remove-*.md`（专用 plan，已用本轮 plan 替代）
  - 删除：`harness/**/2026-04-12-01-*-template-remove-*.md`（上一轮专用审计四件套）
  - 修改：若干 `harness/**`、`docs/**` 中含第三方工具名称的历史记录与设计稿（中性化表述）
  - 新增：本轮 `2026-04-12-02` plan 与 harness 四件套
  - 修改：`README.md`、`docs/plans/index.md`
- intent:
  - 满足「仓库内完全不出现指定浏览器自动化工具名称」的硬要求，同时保留 Harness 治理与历史轮次可读性。
- risks:
  - 历史 handoff 中的具体命令被泛化后，读者需结合当时项目选型理解「E2E 运行器」指代。
- unresolved:
  - 无；验收以全库字符串零匹配与门禁脚本通过为准。
