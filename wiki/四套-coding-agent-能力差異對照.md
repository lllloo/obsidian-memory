---
title: 四套 coding agent 能力差異對照
description: Claude Code、Codex、OpenCode v2、pi 在指示檔、skill、hook、MCP、subagent、plugin、沙箱、session、worktree、SDK、provider、授權、client、壓縮、訂閱十五個維度的差異
created: 2026-09-22
updated: 2026-09-23
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - claude-code
  - agent-framework
---

2026-09-22 回答「Claude Code、Codex、pi、OpenCode 有哪些差異」的 Query 回存。四家各由一個 subagent 只讀官方文件蒐集（Claude Code：code.claude.com；Codex：developers.openai.com/codex；OpenCode：opencode.ai/docs 與 /v2/docs；pi：earendil-works/pi 的 README 與 docs），主 agent 彙整並就已知錯誤修正。**強度**：文件層事實「高」；「文件未載」不等於「沒有」；本頁不含實測。Claude Code 那份 subagent 回報有兩處與官方文件相反（PreToolUse 可否阻擋、模型清單過時），已按主 agent 知識修正並標註。

**一句話**：Codex 在 2026 年已把 Claude Code 的擴充面（hooks、subagent、plugin marketplace、skills）幾乎一比一補齊，兩者差在**閉源 vs Apache-2.0**與**訂閱能否借給第三方**；OpenCode 走 client-server 與 75+ provider，代價是 v2 剛重寫、plugin 生態歸零且暫失 LSP 與 sharing；pi 刻意六不做（MCP、subagent、permission、plan、todo、背景 bash），一切靠 in-process TypeScript extension。

## 總表

| 維度 | Claude Code | Codex CLI | OpenCode v2 | pi |
|---|---|---|---|---|
| 指示檔 | `CLAUDE.md`／`AGENTS.md` 階層、`@` 匯入、`.claude/rules/*.md` 的 `paths` glob | `AGENTS.md` 每目錄一檔、root→cwd 串接、32 KiB 靜默截斷、無 `@`、無 glob | 只認 `AGENTS.md`（v2 不再 fallback `CLAUDE.md`）；子目錄檔在 agent 讀到該區時**延遲載入**；`instructions` 陣列 v2 接受但**不解析** | `AGENTS.md`／`CLAUDE.md` cwd 往上串接；`SYSTEM.md` 整個取代 system prompt、`APPEND_SYSTEM.md` 附加 |
| Skills | `SKILL.md`，personal／project／plugin 三層，`allowed-tools` 預核，`${CLAUDE_SKILL_DIR}` | `SKILL.md`，`.agents/skills` 每層＋`~/.agents/skills`＋`/etc/codex/skills`，自動偵測變更，`$skill` 顯式呼叫 | `SKILL.md` 六個來源（含 `.claude/skills`、`.agents/skills`），另可指 HTTP catalog；`permission.skill` 可 allow/ask/deny | `SKILL.md`（agentskills.io），`settings.json` 可指到 `~/.claude/skills`、`~/.codex/skills` 借用；`/reload` 熱重載 |
| Hooks | PreToolUse／PostToolUse／UserPromptSubmit／Stop／SubagentStop／PreCompact／SessionStart／SessionEnd／Notification／PermissionRequest 等；`settings.json`；PreToolUse 可阻擋 | 事件名與 Claude Code 幾乎同名（SessionStart／UserPromptSubmit／PreToolUse／PostToolUse／PreCompact／PostCompact／SubagentStart／SubagentStop／Stop／Interrupt 等）；`hooks.json`；handler 可為 command 或 mcp_tool；非受管 hook 須先 `/hooks` 信任；相容 `CLAUDE_PLUGIN_ROOT` 環境變數 | plugin 的 `ctx.*.hook()`：session（prompt／context／compaction／generate）、permission evaluate、shell create.before、tool execute.before/after；事件走 `ctx.event.subscribe()`；**v1 plugin 在 v2 不能跑** | extension 40 個事件，`tool_call` 可擋、`tool_result` 可改、`context` 可改送模型內容、可改 TUI 任何區塊；jiti 直接載 `.ts` |
| MCP | stdio／HTTP／SSE（棄用）／WebSocket，OAuth，local／project／user 三 scope | stdio／Streamable HTTP，OAuth 含 DCR，`codex mcp add`，每工具 `approval_mode` | `mcp.servers`，stdio／Streamable HTTP，remote 預設開 OAuth（PKCE、DCR） | **無內建**，官方立場「CLI＋README 取代 MCP」，要用裝社群 bridge package |
| Subagent | `.claude/agents/*.md`，Agent 工具，內建 Explore／Plan／general-purpose，可背景 | 內建 default／worker／explorer，自訂 `~/.codex/agents/*.toml`，`/agents` 總覽，繼承父沙箱 | 內建 build／plan／general／explore（v2 無 scout），`subagent` tool 與同名 permission，`.opencode/agents/*.md` | **無內建**，官方建議 tmux 開多個 pi 或裝第三方 `pi-subagents` |
| Plugin 分發 | `.claude-plugin/plugin.json`，官方與社群 marketplace，`/plugin install` | 可攜 `plugin.json`（agent-plugins.org schema），舊 `.codex-plugin/` 仍相容；marketplace 為 `.agents/plugins/marketplace.json`，與 ChatGPT 共用目錄；`codex plugin marketplace add` | `plugins` 陣列接 npm 名／版本／git spec／本機路徑，`opencode plugin add`；**無官方 marketplace**，只有 ecosystem 清單 | `package.json` 的 `pi` 欄位，`pi install npm:／git:`；無專屬 registry，pi.dev/packages 只是 npm keyword 目錄 |
| 權限與沙箱 | permission mode（default／acceptEdits／plan／bypassPermissions／auto／dontAsk）、allow／deny 規則；沙箱 bwrap（Linux）／seatbelt（macOS） | approval `on-request`／`never`；sandbox `read-only`／`workspace-write`／`danger-full-access`；Seatbelt／bubblewrap／Windows 原生兩模式；**Guardian**：越界請求交另一個 Codex reviewer 依政策自動審 | `permissions` 有序陣列 `{action, resource, effect}`，shell 指令以 tree-sitter 解析；**OS 級沙箱文件未載** | **無 permission 提示、無沙箱**（明言 intentional）；官方要你跑容器（micro-VM／Docker／OpenShell）；project trust 只是載入守門 |
| Session | JSONL 存 `~/.claude/projects/`，`--resume`／`--continue`，`/branch`／`--fork-session` | JSONL rollout 存 `$CODEX_HOME/sessions/`，`codex resume`／`fork`／`archive`，`--ephemeral` 不落地 | 一個共用背景 service 持有全部 session，多分頁（`cli.json` `tabs`）；**v2 尚不支援 sharing**；跨裝置同步文件未載 | JSONL **單檔內樹狀分支**，`/tree`／`/fork`／`/clone`，`/export` HTML、`/share` gist |
| Worktree | `--worktree <name>`、EnterWorktree 工具、`.worktreeinclude` | 桌面 app 有 Worktree 與 Handoff；CLI：0.154 release notes 稱實驗性 `--worktree`／`/worktree`，但文件站 CLI 指令表查無（兩說並列） | v2 內建，Git 為預設 strategy，API `/api/worktree`，plugin 可註冊自訂 strategy | **文件未載** |
| Headless／SDK | `claude -p`、`--output-format json`／`stream-json`、`--bare`；Agent SDK（TS／Python） | `codex exec`（`--json`、`--output-schema`）；app-server JSON-RPC（stdio／WebSocket／Unix socket）；`@openai/codex-sdk`、Python `openai-codex` | `opencode run`／`mini`；共用 service（`--standalone`／`--server`）；`@opencode/client`（HTTP）與 `@opencode/sdk`（in-memory，不開 listener） | `-p` print、`--mode json`、`--mode rpc`（JSONL 協定）；SDK `createAgentSession`；OpenClaw 為 SDK 實例 |
| 模型與 provider | Anthropic API、Bedrock、Vertex、Foundry；只跑 Claude | 內建 openai／ollama／lmstudio，`[model_providers]` 接任何 OpenAI 相容端點，Bedrock 走 AWS 認證 | catalog 來自 models.dev，自動探索 Ollama／LM Studio／vLLM；v1 稱 75+ | 訂閱 3 家＋API key 32 條；llama.cpp router 一等支援（`/llama` 下載 GGUF）；MLX 文件未載 |
| 授權 | **閉源** | **Apache-2.0**（CLI、SDK、app-server；IDE extension 與 cloud 不開源） | **MIT** | **MIT**（Earendil Inc.） |
| Client | CLI、Desktop、VS Code、JetBrains、Web、GitHub Action、Slack、Chrome | CLI、IDE（VS Code／Cursor／Windsurf／Xcode／JetBrains）、ChatGPT desktop app（Linux preview）、Web、iOS／Android 遙控、GitHub review、Slack／Linear | TUI、Desktop（Electron，beta）、Web、IDE extension、ACP（Zed）、GitHub Action | **只有 TUI**；`pi-server`／`pi-client` 為實驗性多前端基礎 |
| Context 壓縮 | auto compact、`/compact [指令]`、resume 時可選 summary | `/compact`、`model_auto_compact_token_limit`、`compact_prompt` 可覆寫、PreCompact／PostCompact hook；實驗性 notes＋可搜尋歷史模式（限 ChatGPT 登入） | checkpoint 式，舊訊息保存，`keep.tokens` 預設約 15k；v1 的 `prune`／`tail_turns` v2 忽略 | 自動＋`/compact`，明言有損，完整歷史留 JSONL 可 `/tree` 回看；extension 可接管 |
| 訂閱／登入 | Pro／Max OAuth 或 API key；**訂閱不可給第三方 harness** | Sign in with ChatGPT 或 API key（API key 無 cloud 功能）；額度給第三方：文件未載（另見定價頁的「Codex for Open Source」） | `/connect` ChatGPT Plus／Pro 可；**Claude 訂閱：官方明寫 Anthropic 禁止**，1.3.0 起不再內建該 plugin；Go $10/月開放權重模型 | `/login` OAuth：ChatGPT、Claude Pro／Max（**走 extra usage 按 token 計費、不算 plan 額度**）、Copilot、xAI、OpenRouter 等 |

## 值得單獨記的差異

- **Codex 補齊擴充面的速度**：hooks 事件名、`CLAUDE_PLUGIN_ROOT` 相容、`.claude/skills` 路徑相容（OpenCode、pi 也讀），三家都在往 Claude Code 的目錄慣例靠攏。Claude Code 專屬且三家都沒有的只剩 `.claude/rules/` 的 `paths` glob 與 `@` 匯入，細節見 [[Coding-agent-指示檔與規則載入機制對照]]。
- **Codex 的 `rules` 是另一個東西**：`~/.codex/rules/*.rules` 是 Starlark 寫的 exec policy（哪些指令可在沙箱外跑），與 Claude Code 的規則檔同名不同物，查文件時別混。
- **自動審核是 Codex 獨有**：Guardian／auto_review 把越界 approval 交給另一個 Codex agent 依政策審，其他三家都是人審或不審。
- **OpenCode v2 的暫時性退化**：不跑 LSP、無診斷；不支援 sharing；`instructions` 不解析；v1 plugin 全數失效。挑 OpenCode 時要分清看的是 v1 還 v2 文件。
- **pi 的 Claude 訂閱登入是灰色地帶**：文件說可登入但走 extra usage 計費；OpenCode 文件則直接引 Anthropic 禁止條款而下架。兩家對同一件事的處理相反，引用前看清楚各自措辭。
- **Claude Code 是唯一閉源**，也是唯一只跑單一模型家族的。

## 關聯

- [[pi-與-OpenCode-v2-比較]]——該頁是兩家的取捨摘要；本頁把兩家放進四家矩陣，並更正該頁「OpenCode 有 LSP 診斷、跨裝置同步」兩項（v2 文件查無）。
- [[Coding-agent-指示檔與規則載入機制對照]]——本頁「指示檔」列的展開版，含 Cursor 與 Copilot。
- [[LLM-方案定價與-coding-agent-比較]]——本頁「訂閱／登入」列只記能否登入；額度規則與價格在該頁。
- [[訊息平台到-coding-agent-的獨立-gateway]]——四家 client 列之外的第三方訊息橋盤點，依與 agent 綁定的緊密度分層。
