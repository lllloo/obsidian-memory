---
title: MCP2CLI — 用 CLI 工具解決 MCP Context 膨脹問題
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: ""
source: https://www.youtube.com/watch?v=LqN_ItMqovA
---

## MCP 的核心問題

MCP（Model Context Protocol）有兩個主要問題：

1. **Context 膨脹**：連接大量 MCP 時，所有工具描述都常駐 context window，佔用大量 token
2. **大輸出問題**：MCP 工具回傳的大型輸出直接進 context window，無法控制

各方解決方案對比：

| 解法 | 提出者 | 問題 |
|------|--------|------|
| Code Mode（JavaScript 直接呼叫 MCP） | Docker | 鎖定 Docker 配置的 MCP，本地/遠端 MCP 有限制，無法存成函式 |
| TypeScript 轉換 | Cloudflare | 需逐一轉換每個 MCP，耗時且容易出錯 |
| Claude Code `--no-mcp-upfront` | Anthropic | 只解決前期膨脹，大輸出仍進 context |
| CLI hub | 開源社群 | Build time 轉換，MCP 更新後需手動同步 |

## MCP2CLI 的解法

**核心概念：把所有 MCP server 轉為 CLI 工具（bash 指令）**

- **Runtime 轉換**：工具在實際呼叫時才轉換，MCP 更新自動反映，無需手動同步
- **1 小時快取**：頻繁使用的工具快取至本機，兼顧即時性與效能
- **建構在 MCP Python SDK 之上**：與所有現有 MCP server 天然相容
- **支援 OpenAPI/REST API**：沒有 MCP server 的 API 也可透過同一 CLI 介面使用
- **安全性**：敏感資料（API key、access token）不放 command line 參數，透過環境變數、檔案路徑或 secret manager 注入

## 安裝與基本使用

```bash
# 使用 pip 安裝（或不安裝直接執行）
pip install mcp2cli

# 安裝配套的 skill（讓 agent 知道工具怎麼用）
# skill 會在 agent context 中直接載入工具說明、範例和使用時機
```

**建議：用 skill 而非 `CLAUDE.md` 管理工具說明**——skill 的描述直接進 agent context，agent 主動知道何時該用，而不是被動讀取指令。

## 實際工作流程

### 1. 連接 MCP

以 Supabase MCP 為例：

```bash
# 先取得 access token（必要，否則會報錯）
# skill 會自動配置 MCP，無需手動設定
```

確認連接後應看到所有可用工具列表（範例：4 個 MCP 共 78 個工具）。

### 2. 防止舊版 API 問題

連接 Context7 MCP 後，在 `CLAUDE.md` 中加入指示：

```
使用 Context7 MCP 之前，先查閱最新文件再寫程式碼。
```

或更好的做法：為每個 MCP 建立專屬 skill，說明工具清單、使用方式、適用時機。

### 3. 控制輸出格式

MCP2CLI 支援多種輸出格式：

- **JSON**：標準 JSON 格式
- **raw**：原始輸出
- **tune**（推薦）：結合縮排與 CSV 格式，資訊密度最高，token 效率最佳

在 `CLAUDE.md` 加入：

```
使用 Context7 MCP 時，一律使用 tune 格式輸出，避免不必要的 token 消耗。
```

### 4. 將大輸出重導向至檔案

因為 MCP 現在是 bash 指令，可以用 shell 重導向：

```bash
# 在 CLAUDE.md 中加入：
# 任何 MCP 工具產生大量輸出時，將輸出重導向至指定路徑，再用 grep 提取需要的資料
mcp_tool <args> > /path/to/output.txt
grep "pattern" /path/to/output.txt
```

這複製了 Cursor 的「MCP 結果作為檔案」工作流程，但在 Claude Code 中因 MCP 是原生整合而無法實現——改成 CLI 後就可以了。

## 測試策略建議

用 Puppeteer MCP 做端對端測試時，遇到「每次呼叫都開新瀏覽器、無法保持 session」的問題。

**建議：優先用 MCP 做測試（MCP 是 persistent process，可跨呼叫保持狀態），而非 headless browser 工具。**

Claude 的瀏覽器擴充功能也比 headless 方式更適合需要保持 session 的端對端測試。
