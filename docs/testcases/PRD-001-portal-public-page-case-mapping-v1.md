# PRD-001 用例映射（v1）

> 说明：本文将 PRD 条目映射为可执行的端到端用例。每条用例必须可追踪到 PRD、脚本和证据。

## 1. 版本策略

- `prd_id`: `PRD-001`
- `prd_version`: `v1`
- `case_set_version`: `v1.1`（菜单导航替代 CONSOLE_PUBLIC_PAGE_PATH）
- 单用例版本字段：`case_version`（示例：`r1`、`r2`）

## 2. Console 前置步骤（自动化已实现）

自 `case_set_version` v1.1 起，不再配置 `CONSOLE_PUBLIC_PAGE_PATH`。从 `CONSOLE_BASE_URL` 进入后顺序为：

1. 断言「欢迎登入系统~」（可配 `CONSOLE_LOGIN_SUCCESS_TEXT`）
2. 点头像断言版本 `3.0.2603-beta.0315`（可配 `CONSOLE_PLATFORM_VERSION`）
3. 「门户管理」→ 列表含「TERP 运营端」（可配 `CONSOLE_PORTAL_*`）
4. 进入门户 → 含「门户配置」→ 展开并进入「公开页面」
5. 再执行选场景、保存、复制/读取链接（场景名默认 `AT_公开页面`，可配 `CONSOLE_SCENE_PAGE_NAME`）

## 3. 用例映射矩阵


| case_id          | priority | prd_ref | 场景描述                | 关键断言（页面层）           | 关键断言（数据层信号）           | 预期证据             |
| ---------------- | -------- | ------- | ------------------- | ------------------- | --------------------- | ---------------- |
| E2E-PRD001-P0-01 | P0       | 2.2     | console 配置公开页面并保存成功 | 保存成功提示可见，链接字段可见且可复制 | 生成链接后 portal 打开无登录跳转  | 步骤截图、保存后截图、trace |
| E2E-PRD001-P0-02 | P0       | 2.1/2.2 | 未登录访问公开链接可正常浏览      | 关键页面元素可见            | 关键业务数据加载成功，无401/403提示 | 页面截图、网络摘要、trace  |
| E2E-PRD001-P0-03 | P0       | 2.1     | 未公开页面链接访问被拦截        | 无权限/不可访问提示可见        | 关键请求被拒绝或无可用数据展示       | 拦截页面截图、trace     |
| E2E-PRD001-P1-01 | P1       | 2.2     | 取消公开后历史链接行为         | 访问结果符合产品定义（拦截或失效页）  | 不再出现公开数据成功信号          | 前后对比截图、trace     |


## 4. 执行规则

- P0 是发布前必跑集合。
- 新需求进入时先更新本矩阵，再更新自动化脚本。
- 用例新增或变更必须更新 `case_version` 与 `change_reason`。

## 5. 自动化状态字段（维护模板）

每条用例需要补齐以下元数据：

- `automation_status`: draft | automated | flaky | blocked
- `script_path`: 对应 `tests/e2e/*` 路径
- `evidence_path`: 对应执行产物路径
- `last_verified_at`: 最近一次通过时间
- `change_reason`: 本次版本变更原因

