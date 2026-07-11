---
title: "Hermes Agent Kanban（多 Agent 任務協作板）"
description: Hermes Agent 官方文件：SQLite 存儲的多 profile／多 worker 持久任務佇列，與 delegate_task 互補的協作機制
created: 2026-07-11
updated: 2026-07-11
source: "https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban"
published:
tags:
  - clippings
---

# Hermes Kanban Board

> 本檔為 hermes-agent.nousresearch.com 官方文件 `user-guide/features/kanban` 擷取彙整，作為 raw 事實來源。這是 Hermes 存放待辦事項／任務／roadmap 的機制，與有界核心記憶 `MEMORY.md`／`USER.md`（見 [[Hermes-Agent-NousResearch]]）是分開的子系統。

## 定位

Kanban 是持久化的多 profile 任務佇列：每次交接是一列任何 profile（或人）都能看到、編輯的資料。與更簡單的 `delegate_task`（RPC 式、父層阻擋等子層返回）區分開來。

## 資料儲存

- 預設位置：`~/.hermes/kanban.db`（SQLite，WAL 模式）
- 多板：`~/.hermes/kanban/boards/<slug>/kanban.db`
- 工作區目錄：`~/.hermes/kanban/workspaces/<id>/` 或 `~/.hermes/kanban/boards/<slug>/workspaces/<id>/`
- 附件：`<hermes-home>/kanban/attachments/<task_id>/`（可用 `HERMES_KANBAN_ATTACHMENTS_ROOT` 自訂）
- 日誌：`~/.hermes/kanban/logs/`
- 儀表板、CLI、worker 工具三個介面都走同一個 per-board SQLite DB

## Task 欄位與狀態機

狀態生命週期：`triage → todo → ready → running → blocked → done → archived`

核心欄位：`title`、`body`、`assignee`（profile 名稱）、`status`、`tenant`（可選命名空間）、`idempotency_key`（重試去重）、`priority`（數字）、`workspace`（scratch/dir:\<path\>/worktree）、`branch`（worktree 用 git 分支名）、`max_runtime_seconds`、`max_retries`（電路斷路器）、`scheduled_at`（延遲派發時間戳）、`goal_mode`（布林，啟用目標循環）、`current_run_id`。`workflow_template_id`、`current_step_key` 保留給 v2。

相關表：`task_links`（parent_id → child_id 依賴）、`task_comments`（inter-agent 協議執行緒）、`task_runs`（每次嘗試一行：outcome/summary/metadata）、`task_events`（append-only 審計日誌）、`task_attachments`（檔案元資料）。

## CLI（`hermes kanban ...`，節錄常用子命令）

`init`、`create`（`--body --assignee --parent --tenant --workspace --branch --priority --triage --idempotency-key --max-runtime --max-retries --goal --skill`）、`list`（`--mine --assignee --status --tenant --archived --sort`）、`show`、`assign`／`reassign`、`edit`、`promote`、`schedule --at`、`link`／`unlink`、`claim --ttl`、`comment`、`complete`（`--result --summary --metadata`）、`block`／`unblock`、`archive`、`tail`、`watch`、`heartbeat`、`runs`、`assignees`、`dispatch`（`--dry-run --max --failure-limit`）、`stats`、`log`、`context`、`specify`、`decompose`、`gc`、`notify-subscribe`／`notify-list`／`notify-unsubscribe`、`swarm --workers --verifier --synthesizer`。多板管理：`boards list/create/switch/show/rename/rm`；`--board <slug>` 可作用在非當前板。

## Agent 可用工具（`kanban_*`）

Dispatcher 為每個 worker 設 `HERMES_KANBAN_TASK=t_<id>` 環境變數，工具由系統提示的 `KANBAN_GUIDANCE` block 自動啟用；orchestrator profile 需在 toolsets config 顯式啟用 `kanban` toolset。

| 工具 | 用途 |
|---|---|
| `kanban_show()` | 讀取當前任務（標題、本體、父層交接、先前嘗試、註解串、完整 worker_context）——worker 生命週期第一步 |
| `kanban_list()` | 列出任務摘要，可篩 assignee/status/tenant/archived/limit |
| `kanban_complete()` | 完成並交接 summary + metadata，進入 `done` |
| `kanban_block()` | 停止工作，依 `kind` 路由：`dependency`（自動恢復）／`needs_input`/`capability`/`transient`（呈現給人）；同 kind 重複會升級至 `triage` |
| `kanban_heartbeat()` | 長操作中的活躍信號，防止 1 小時無心跳被回收 |
| `kanban_comment()` | 附加持久備註到任務執行緒，inter-agent 協議基礎 |
| `kanban_create()` | 扇出子任務（協調員用），指定 assignee／parents／skills |
| `kanban_link()` | 事後補 parent_id → child_id 依賴邊 |
| `kanban_unblock()` | 移動阻擋任務回 `ready` |

## Kanban vs. `delegate_task`

| 面向 | `delegate_task` | Kanban |
|---|---|---|
| 形態 | RPC（fork → join） | 持久訊息佇列 + 狀態機 |
| 父層行為 | 阻擋直到子層返回 | create 後 fire-and-forget |
| 子層身份 | 匿名子 agent | 具名 profile、持久記憶 |
| 可恢復性 | 無，失敗就失敗 | block → unblock → 重執行；崩潰可回收 |
| 人工介入 | 不支援 | 任何時點可 comment/unblock |
| 審計軌跡 | 隨上下文壓縮遺失 | SQLite 永久持久列 |
| 協調方式 | 分層（呼叫者→被呼叫者） | 對等，任何 profile 讀寫任何任務 |

官方建議：短推理答案、無人工涉入、結果要回父上下文 → 用 `delegate_task`；工作跨 agent 邊界、需存活重啟、可能需人工輸入、可能換角色接手、需事後可探知 → 用 Kanban。

## 多 Profile／多 Worker 協作機制

- **Dispatcher**：長期迴圈，預設每 60 秒一次（`kanban.dispatch_interval_seconds`），預設內嵌於網關（`kanban.dispatch_in_gateway: true`）。職責：回收陳舊聲明（TTL 過期無心跳）、回收崩潰 worker（PID 消失但 TTL 未過期）、當所有父層 `done` 時升級子層 `todo → ready`（`kanban.auto_promote_children`，預設啟用）、原子性聲明並生成指派的 profile。
- **工作區隔離三型**：`scratch`（預設，短暫 tmp，完成即刪）；`dir:<path>`（既有共用目錄，必須絕對路徑，完成保留）；`worktree`（git worktree under `.worktrees/<id>/`，完成保留）。
- **並行度控制**：`kanban.max_in_progress`（全板上限）、`kanban.max_in_progress_per_profile`（每 assignee 上限），兩者都滿足才生成。
- **失敗處理**：`kanban.failure_limit`（預設 2）連續失敗後自動阻擋；per-task 可覆蓋 `--max-retries`；異常狀態（auth 失敗、429、近期成功、活躍 PR）觸發 `respawn_guarded` 延遲重生。
- **租戶隔離（軟邊界）**：`--tenant <name>` 標記任務，worker 從 `$HERMES_TENANT` 讀取並以前置詞隔離記憶寫入；板與 dispatcher 共用，資料靠工作區路徑與記憶鍵隔離。板本身是硬隔離邊界（不同主機/不同 DB）。
- 迴圈依賴檢測在伺服器端拒絕，不允許跨板連結。

## 適用情境（`delegate_task` 無法覆蓋）

Research triage（平行研究員+分析員+寫手，人工在環）、scheduled ops（週期性建構）、digital twins（持久具名助手累積記憶）、engineering pipelines（分解→平行 worktree 實施→審查→PR）、fleet work（一專家管理 N 個主題）、human-in-the-loop（阻擋等人工輸入後恢復）、多租戶運營、事件驅動自動化（webhook + idempotency key）。

九個標準協作模式：P1 Fan-out（N 同角色兄弟）、P2 Pipeline（角色鏈）、P3 Voting/quorum（N 兄弟+1 聚合器）、P4 Long-running journal（同 profile+共用目錄+cron）、P5 Human-in-the-loop、P6 @mention 內聯路由、P7 Thread-scoped workspace、P8 Fleet farming、P9 Triage specifier（一句話→triage→展開成 spec'd task）。
