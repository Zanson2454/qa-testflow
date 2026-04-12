# workflow 脚本说明

本目录提供**零第三方依赖**（标准库即可）的本地守卫脚本，用于模板开箱校验与状态检查。

| 脚本 | 作用 |
|------|------|
| `check_quality.py` | 校验必需文件存在、`task-state.json` 关键字段、`current_plan` 文件存在、harness 四件套**同一日期前缀**、各 harness 文件名符合正则 |
| `run.py` | 读取 `state/task-state.json`，校验当前状态合法、迭代/重试未越界、`current_plan` 文件含 `status: active` |

**建议**：提交前执行 `check_quality.py`；开始工作前可执行 `run.py` 确认状态文件与 active plan 一致。

操作步骤与常见问题见 **[../docs/guides/01-getting-started.md](../docs/guides/01-getting-started.md)**。
