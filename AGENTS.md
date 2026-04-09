# Project Goal
[请在此处简述项目目标]

# Working Mode
- **Review First**: 每次开始工作必须先 review 最近一轮 change record，再进入本轮 plan。
- **Plan Driven**: 必须先生成 plan，再进行实现；严禁跳过 plan 直接实现。
- **Iterative Evidence**: 每轮必须生成完整的 change record、review 和 retro。
- **Review Continuity**: 下一轮必须显式说明对上一轮改动的 context。
- **Session Start Protocol**: 每次新会话默认执行“继续任务：先做 review first（读取最新 change/review/retro/handoff），再执行当前 plan”，除非用户明确指定其他起手方式。

# Required Outputs
- **exec plan**: 详尽的执行步骤与验收标准。
- **change record**: 包含改动文件、意图、风险及未解决问题。
- **review**: 基于验收标准的通过/失败结论。
- **retro**: 本轮总结与下轮建议。
- **context**: 对历史改动的回溯说明。

# Operational Rules
- **No Dirty Tests**: 不允许保留仅用于调试的一次性测试文件到本轮结束。
- **Formal Baselines**: 不允许只做临时验证而不沉淀正式验收测试或测试场景。
- **Single Thread**: 同一 iteration 不允许并行推进两个不同主题的主线。
- **State Truth**: `task-state.json` 是当前确认主线的唯一状态源，严禁无授权覆盖。
- **Done Criteria**: 当询问阶段是否完成时，必须显式对照 plan 的 `done_criteria`。
- **Governance**: 项目内核心能力（如 skill）的变更必须遵循 `docs/templates/` 下的规范。
- **Chinese Comments**: 新增文件必须包含有信息量的中文注释；修改文件时新增注释也默认使用中文，除非用户明确要求英文。

# Git & Sync Rules
- **Traceable Commits**: 每轮必须详细记录改动意图和风险。
- **Push on Success**: 只要本轮有代码改动且验收通过，结束前必须提交并推送到远程仓库。
- **Task-level Push**: 每次任务完成且测试通过后，必须立即执行一次提交并推送，禁止累计多个已通过任务再统一推送。
- **Environment Sync**: 开始工作前必须确保本地状态与远程仓库及最近一轮 change record 同步。

# Test & Baseline Rules
- **Cleanup**: 过程中新增的临时调试脚本必须在结束前收敛或删除。
- **Regression Foundation**: 每轮验收通过后，沉淀的正式测试即作为回归基线，后续迭代必须优先回归。
- **Impact Analysis**: 若本轮改动影响既有基线，必须同步更新基线测试并在 change record 中说明。

# Definition of Done
- [ ] 目标产物按 plan 完成。
- [ ] Review 结果为 `passed: true`。
- [ ] Change record、Retro、Context 完整落盘。
- [ ] 临时测试已收敛，正式回归测试基线已形成。
- [ ] 相关代码与配置已推送至远程仓库。
