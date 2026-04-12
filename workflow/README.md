# workflow 脚本说明

详细上手（含概念与 FAQ）见 **[../GET_START.md](../GET_START.md)**。

本目录提供**零第三方依赖**（标准库即可）的本地守卫脚本，用于模板开箱校验与状态检查。

| 脚本 | 作用 |
|------|------|
| `doctor.py` | 依次执行 `check_quality.py` 与 `run.py`，克隆后或提交前**一键自检** |
| `check_quality.py` | 校验必需文件存在、`task-state.json` 关键字段、`current_plan` 文件存在、harness 四件套**同一日期前缀**、各 harness 文件名符合正则 |
| `run.py` | 读取 `state/task-state.json`，校验当前状态合法、迭代/重试未越界、`current_plan` 文件含 `status: active` |
| `init_iteration.py` | 生成本轮 **change/review/retro/handoff** 空骨架（可选 `--context`）；**不**创建 plan、不修改 `task-state.json` |

**建议**：克隆后执行 `python3 workflow/doctor.py`；提交前执行 `check_quality.py`。

**初始化新一轮 harness 骨架**：

```bash
python3 workflow/init_iteration.py --summary my-feature-name
python3 workflow/init_iteration.py --summary my-feature-name --context
python3 workflow/init_iteration.py --summary my-feature-name --dry-run
# 或：make init SUMMARY=my-feature-name
```

日期默认当天；`--seq` 默认按 `harness/changes` 下同日期最大序号 +1。

操作步骤与常见问题见 **[../docs/guides/01-getting-started.md](../docs/guides/01-getting-started.md)**。  
新一轮迭代步骤与脚本关系见 **[../docs/guides/03-new-iteration-manual-steps.md](../docs/guides/03-new-iteration-manual-steps.md)**。
