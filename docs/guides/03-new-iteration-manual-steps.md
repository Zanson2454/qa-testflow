# 新一轮迭代：纯文档操作步骤（无脚本）

本页描述 **不依赖任何初始化脚本**、仅通过新建与编辑 Markdown 完成一轮 Harness 的标准顺序。若你尚未读过 [01-getting-started.md](./01-getting-started.md)，建议先完成「克隆后验证门禁」一节。

## 1. 约定本轮前缀

- 取 **当天日期** + **当日序号** `01/02/…`，组成前缀：`YYYY-MM-DD-NN`（与四件套文件名一致）。
- **summary** 使用小写英文短名 + 连字符，例如 `fix-login-guard`、`add-api-checklist`。

## 2. 承接上一轮（Review First）

1. 打开最新 `harness/changes/`，确认上一轮改了什么、风险和未解决项是什么。
2. 打开最新 `harness/reviews/`，确认上一轮验收结论与未通过项。
3. 打开最新 `harness/retros/` 与 `harness/handoffs/`，确认下一轮建议、风险与起手顺序。
4. 打开最新 `harness/contexts/`，确认历史承接关系、本轮边界与非目标。
5. 在脑中确认：**本轮单一主题**（不与并行主线混写）。

## 3. 新建本轮 Plan

1. 复制 `docs/plans/plan-template.md` 为 `docs/plans/YYYY-MM-DD-NN-plan-<summary>.md`。
2. 填写 `goal`、`steps`、`done_criteria`；将 `status` 设为 `draft`，定稿并要执行时再改为 `active`。
3. 编辑 `docs/plans/index.md`：增加一行，标明 `status: active` 或 `draft/completed`。
4. 若本轮切换执行主线：编辑 `workflow/state/task-state.json` 的 `current_plan` 指向新 plan；**同时只能有一份 plan 为 `status: active`**（`run.py` 只认 `current_plan` 指向的文件里含 `status: active`）。

## 4. 本轮 Context（必需）

新建 `harness/contexts/YYYY-MM-DD-NN-context-<summary>.md`，写清：承接关系、范围、非目标、与上一轮差异。`context` 虽然**不进入四件套门禁**，但在本仓库中属于 `AGENTS.md` 明确要求的必需产物，不应省略。

## 5. 新建四件套（与前缀一致）

在下列四个目录各新建 **一个** 文件，**文件名前缀必须相同**：

| 目录 | 文件名模式 |
|------|----------------|
| `harness/changes/` | `YYYY-MM-DD-NN-change-<summary>.md` |
| `harness/reviews/` | `YYYY-MM-DD-NN-review-<summary>.md` |
| `harness/retros/` | `YYYY-MM-DD-NN-retro-<summary>.md` |
| `harness/handoffs/` | `YYYY-MM-DD-NN-handoff-<summary>.md` |

最小可填内容：

- **change**：`files` 列表、`intent`、`risks`、`unresolved`（可随迭代补充）。
- **review**：第一行或醒目处写 `passed: true` 或 `passed: false`（门禁不解析业务，但这是验收真相）；完成判断时需显式对照本轮 plan 的 `done_criteria`。
- **retro**：本轮做得好的点、改进点、下轮建议。
- **handoff**：下一手建议阅读顺序、未决事项、元信息。

可参考仓库内历史同前缀文件作格式样例。

## 6. 实现与修改 change

- 进行代码或文档修改时，**同步更新**本轮 `change` 文件中的文件列表与意图，避免提交与记录脱节。

## 7. 提交前自检

在仓库根目录执行：

```bash
python3 workflow/check_quality.py
```

常见失败与处理：

- **四件套前缀不一致**：四个目录中必须存在 **同一** `YYYY-MM-DD-NN` 前缀；删除旧轮或补全新轮（勿留空目录无文件——每目录至少要有一个合法命名文件参与交集，见门禁实现）。
- **文件名不符合正则**：`summary` 仅允许小写字母、数字、连字符；勿用下划线或中文段落在文件名里。
- **缺 guides 等必需文件**：勿从模板中删除 `docs/guides/` 下被门禁声明的文件。

再执行：

```bash
python3 workflow/run.py
```

确认 `current_plan` 存在且含 `status: active`。

## 8. 任务完成后的收尾

1. 回到本轮 `review`，确认是否已按 `done_criteria` 给出通过/失败结论。
2. 确认本轮 `change/review/retro/handoff/context` 已全部落盘且前缀一致。
3. 若本轮改动已验收通过，按仓库规则立即执行一次提交并推送，不要累计多个已通过任务再统一推送。
4. 若本轮未通过，则在 `review`、`retro`、`handoff` 中明确失败点、风险与下轮建议，不要把未完成状态伪装成完成。

## 9. 与「自动化初始化」的关系

- 本页刻意 **不写** 任何生成脚本；若后续引入脚本，应与本步骤 **语义等价**，且不替代人类对 plan/review 的判断。
- 概念背景见 [02-harness-and-ralph-loop.md](./02-harness-and-ralph-loop.md)。
