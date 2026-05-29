---
title: Obsidian CLI 整合指南
created: 2026-03-17
updated: 2026-05-29
source: https://github.com/kepano/obsidian-skills
tags:
  - obsidian
  - claude-code
  - skill
  - cli
---

讓 AI agent 讀寫 Obsidian vault 的 CLI 整合，由 Obsidian CEO kepano（Steph Ango）維護於 `obsidian-skills` 集（遵循 AgentSkills.io 標準，多 AI harness 通用）。Claude Code 透過 `obsidian-cli` skill 呼叫，直接讀寫筆記、搜尋、操作 properties 與 daily notes。觸發情境：建立／搬移筆記、跨筆記搜尋、daily notes 操作（`/ob` 流程預設使用）；指令清單與語法以 `obsidian --help` 或官方 repo 為準。

## Windows 實作踩坑

CLI 從 Obsidian 1.12.7+ 隨桌面 app 內建，執行檔是 `C:\Program Files\Obsidian\Obsidian.com`——它是 **terminal redirector，不是 GUI launcher**（一度誤判成啟動器）。需先在 Obsidian → 設定 → General 啟用「Command line interface」並重開 terminal 才生效。

- **shell 差異**：PowerShell 經 `PATHEXT` 認 `.com`，可直接 `obsidian <cmd>`（Windows 預設）；Git Bash 不認 `.com`，要顯式 `Obsidian.com <cmd>` 或 `powershell.exe -Command "obsidian ..."`。
- **PATH snapshot**：Claude Code session 啟動時 snapshot PATH，新裝 CLI 在當前 session 看不到，要重開 session。
- **多行 content 寫入 silent fail**：官方 `create` 無 `--stdin` 旗標；`obsidian create content="多行..."` 經 shell 變數／命令替換傳多行內容時有無聲失敗風險，寫入後必須驗 size（`< 10` bytes 視為失敗，fallback Write）。
- CLI 偵測失敗時 `/ob` 流程自動 fallback Write/Edit（提醒在 Obsidian 按 `Ctrl+P → Reload app without saving`）。

## 連結

- Skills repo：<https://github.com/kepano/obsidian-skills>
- 官方 CLI 說明：<https://obsidian.md/help/cli>

## 相關

- [[bookmark-defuddle-網頁清洗CLI|defuddle]] — 同 kepano 維護
- [[daily-append-bug]] — `daily:append` 在特定環境失效
