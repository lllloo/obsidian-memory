---
title: Codex Windows App 與 WSL 共用對話
description: Windows 桌面 App 與 WSL CLI 共用對話的本機設定紀錄，含獨立 SQLite 資料庫避開 migration 衝突的方法與驗證邊界
created: 2026-10-13
updated: 2026-10-13
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - dev-environment
  - wsl
---

## 問題與原理

Windows App 預設使用 `%USERPROFILE%\.codex`，WSL CLI 預設使用 Linux 的 `~/.codex`，所以登入同一帳號也不會自動共用本地對話。`codex resume --all` 解除工作目錄篩選，不能自行跨到另一份 Codex home。官方提供以 `CODEX_HOME` 指向 Windows 資料夾的共用方法，見 [Windows 官方說明](https://learn.chatgpt.com/docs/windows/windows-app#share-config-auth-and-sessions-with-wsl)。**證據：官方文件；行為仍須依目前安裝版本驗證。**

## 本機設定（2026-10-13）

WSL 的 `~/.zshrc`、`~/.bashrc`、`~/.profile` 已加入：

```bash
export CODEX_HOME="/mnt/c/Users/Joe/.codex"
export CODEX_SQLITE_HOME="/home/barney/.local/state/codex-wsl-shared"
```

第一行讓 Windows App 與 WSL CLI 共用 Windows 的設定、登入資料與對話檔；第二行讓 WSL 使用獨立資料庫。專案與 CLI 程式執行仍可留在 WSL。上述帳號與路徑是本機值，換機須替換。

直接共用 Windows 資料庫時，WSL app-server 回報 `failed to initialize sqlite state runtime`。唯讀比較確認 Windows 與 Linux 資料庫的 migration checksum 不同，與 [社群 issue #23251](https://github.com/openai/codex/issues/23251) 的問題吻合；**本次未追查底層完整錯誤，因此不能把 checksum 差異當成已證明的唯一根因**。改用獨立 `CODEX_SQLITE_HOME` 後 app-server 正常啟動並可列出對話。**證據：單一本機實測；不是所有版本通用保證。**

已備份三個 shell 設定檔，檔名為原名加 `.codex-share-backup-<時間戳>`。原本 `/home/barney/.codex` 保留，未刪除、未合併；Windows 的既有資料庫未作修復或搬移。

## 使用與驗證結果

開新 WSL 終端後執行：

```bash
codex resume --all
```

- 新的 zsh 已驗證讀到上述兩個環境變數；既有 shell／已啟動的對話不會自動切換。
- app-server 的 `thread/list` 實測成功列出 Windows `sessions/` 下的 3 筆對話，回傳來源為 `vscode`。
- 使用者於 2026-10-13 回覆「看起來可以」，確認此設定能解決當下看不到紀錄的需求。
- **未驗證全部 App 對話都會列出，也未逐筆測試續接成功；不能宣稱兩邊完整同步。** 獨立資料庫是本機 workaround，未確認所有索引與其他狀態的跨端一致性。

若看得到對話卻無法續接，應保留錯誤訊息再排查；另有 [Windows／WSL 路徑轉換 issue #42292](https://github.com/openai/codex/issues/42292)，不應先刪除資料庫。回復原本 WSL home 時，移除上述兩行並開新終端；若父程序仍傳入 `CODEX_HOME`，也須清除該環境變數。

## 延伸

- [[四套-coding-agent-能力差異對照]] 提供 Codex CLI 與其他 client 的能力背景；本頁補充 Windows／WSL 本地 session 儲存的實測。
- [[WSL-剪貼簿貼圖到-Claude-Code]] 是另一個 Windows／WSL 邊界案例：同一部電腦的兩個環境仍須處理不同的資料與介面。
