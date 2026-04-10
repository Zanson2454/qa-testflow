# 2026-04-10-04 retro output loop fixed protocols

root_causes:
  - 上一轮设计稿已经形成完整架构，但对“谁是权威源、谁能写、何时停手、谁驱动决策”还不够收口。
  - 若不先定死这些治理协议，后续实施时容易退回人工仲裁或出现无意义自动重试。
fix_strategy:
  - 先以设计文档形式固定协议，再把这些协议转成后续实施 plan 的硬约束。
  - 保持 V1 收敛：先做单 runner、单控制面真相源、三层重试、`quality gate` 命名统一。
next_focus:
  - 等待用户再次评审修订后的设计稿。
  - 若评审通过，再进入实施 plan，优先落状态 schema 与 validator/quality gate 管道。
