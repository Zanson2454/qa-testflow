# 2026-04-12-03 exec plan ootb guides and template hardening

status: completed

## context

- 承接 `2026-04-12-02` 文档卫生结论；用户要求 **先文档、后工程模板**，目标为 **开箱即用 + 文档指导**，并与 Harness / Ralph Loop 口径对齐。

## goal

- 提供可执行的 **guides**（快速上手、概念对照），并更新白皮书与 README 入口。
- 增强工程模板：`Makefile`、`workflow/README`、plan 复制模板、门禁必需文件列表与失败提示。

## steps

1. 新增 `docs/guides/`（索引、快速上手、Harness+Ralph 对照）→ 可独立阅读完成上手
2. 更新 `README.md`、`whitepaper-v2`、`docs/templates/plan.md`、`AGENTS.md`、skills → 统一入口
3. 新增 `Makefile`、`docs/plans/plan-template.md`、`workflow/README.md` → 降低命令记忆成本
4. 扩展 `check_quality.py` 必需文件与失败提示 → 防止删掉指南后仍自称「模板完整」
5. 运行 `check_quality` / `run` → 验收；沉淀本轮 harness 四件套

## done_criteria

- [x] `docs/guides/` 三文件齐全且 README 可导航
- [x] 白皮书含 Ralph Loop 与模板的对应说明（无绑定具体商业工具）
- [x] `make check` / `make run` 可用；`workflow/README.md` 说明脚本职责
- [x] `python3 workflow/check_quality.py` 与 `python3 workflow/run.py` 通过
- [x] 本轮 harness 四件套与 plan 已落盘
