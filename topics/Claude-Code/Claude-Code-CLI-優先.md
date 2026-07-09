---
title: Claude Code CLI 優先
created: 2026-04-24
updated: 2026-05-29
tags:
  - claude-code
  - cli
---

新增工具整合到 Claude Code 時，**優先選 CLI、退而才選 MCP**。原因有三層：

**架構層**：CLI 與 Claude Code 同住 terminal，呼叫就是直接 spawn process；MCP 通常是常駐 server + IPC，多一層橋接的 overhead 與失敗模式。

**Token 層**：未啟用 Tool Search 時，MCP server 的 tool descriptions 啟動就占 context（多伺服器設定可達數萬 token），每次呼叫的 response 也帶 wrapping。2026 起 Claude Code 預設以 Tool Search 把 MCP 工具設為 deferred、按需載入（官方稱省 85%+），啟動不再全載——但工具被搜出展開後仍占 context，加上 server / IPC 橋接開銷，同任務下 CLI 通常仍較省上下文。

**生態層**：CLI 是工具的主介面，功能最完整；MCP 多半是後補包裝。CLI 通常配套 skill 一起發佈——一行指令同時裝 CLI + skill 到 `.claude/`，比設定 MCP server 啟動參數簡單。

## 安裝模式

複製 GitHub repo URL 貼進 Claude Code，說「照這個安裝 \<工具名\> CLI」——Claude Code 會自動跑安裝 + 認證流程，不用看 README 一步步抄。

## 例外：MCP 比 CLI 合適時

- 工具只給 MCP 沒 CLI（罕見）
- 需在多 session 共享狀態（MCP server 持有狀態，CLI 無狀態）
- 需要 streaming 或雙向通訊（CLI stdout 一次性不適用）

## 相關主題

- [[Claude-Code-Skills]] — CLI 工具通常與 skill 綁在一起發布
- [[Harness-Engineering]] — 強化開源 CLI 與 harness 架構
