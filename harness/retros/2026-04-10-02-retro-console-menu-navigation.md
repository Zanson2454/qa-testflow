# 2026-04-10-02 retro console menu navigation

root_causes:
  - 先前假设可通过深层 path 直达配置页，与实际「从首页菜单进入」不符。
fix_strategy:
  - 将导航步骤显式编码为 Page Object 方法，并用环境变量收敛可变的展示文案。
next_focus:
  - 真实环境跑通 P0；必要时为头像/子菜单补充更稳的 role 或 testid。
