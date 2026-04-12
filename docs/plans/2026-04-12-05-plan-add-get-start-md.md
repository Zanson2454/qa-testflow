# 2026-04-12-05 exec plan add GET_START.md

status: completed

## context

- 用户需要根目录 **`GET_START.md`** 作为**单独、详细**的上手文档，与 `docs/guides` 分篇并存。
- review 进一步发现：`docs/guides/03-new-iteration-manual-steps.md` 的 `Review First`、`context` 必需性与 commit/push 收尾要求未完全对齐 `AGENTS.md`。

## goal

- 新增 `GET_START.md`，覆盖环境、门禁行为、三条主线、目录、完整迭代检查表、Ralph 简介、状态机、Git 摘要、FAQ、延伸阅读。
- 将 `GET_START.md` 纳入 `check_quality` 必需文件；更新 README、`AGENTS.md`、`docs/guides/README.md`、skills、`workflow/README.md`。
- 同步修正 `GET_START.md` 与 `docs/guides/01/02/03` 的流程文案，使其与 `AGENTS.md` 保持一致。

## steps

1. 新增根目录详细上手文档，并同步更新入口引用
2. 对齐 `GET_START.md` 与 `docs/guides/01/02/03` 的迭代流程说明
3. 更新本轮 `change/review/retro/handoff/context`，记录文档治理与风险
4. 运行 `python3 workflow/check_quality.py` 与 `python3 workflow/run.py`

## done_criteria

- [x] `GET_START.md` 存在且为中文详细说明
- [x] `docs/guides/01/02/03` 与 `GET_START.md` 的迭代步骤已对齐 `AGENTS.md`
- [x] `check_quality` / `run.py` 通过
- [x] 本轮 harness 四件套落盘
