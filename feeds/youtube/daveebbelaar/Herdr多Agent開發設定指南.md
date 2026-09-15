---
title: 如何設定 Herdr 進行多 Agent 開發（完整指南）
description: 作者用一週把 Herdr 調成日常主力，涵蓋持久 session、space 與 tab、agent 整合、config.toml、快捷鍵、skill 委派與 Neovim、Lazygit 補齊 IDE 體驗
created: 2026-09-15
updated: 2026-09-15
source: https://www.youtube.com/watch?v=Shqtk_2Jd3c
published: 2026-09-11
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
  - workflow
  - sub-agent
  - claude-code
  - codex
---

## 為什麼用 Herdr

- Herdr 在開發者社群討論度高，DHH 在 Lex Fridman podcast 提到，並在 Omarchy Linux 發行版中預設內建。
- 作者原本主要用 Claude Code 桌面版與 Codex 桌面版，只用單一工具時很好用；但他會混用不同 harness 與模型（Grok、GPT、Anthropic），甚至讓某些 agent review 其他 agent 的成果，多個桌面 app 並用時就變得凌亂——這時 Herdr 這類工具就不可或缺。
- 開箱即強，但要成為日常主力需要額外設定與搭配工具；作者整理了一份指南，可直接複製其設定，但更建議自行客製。

## 安裝與持久 session

- 在任一終端機或 PowerShell 執行安裝指令（Linux／Mac／Windows 皆有），再執行 `herdr` 就會進入 server。
- 最接近的類比是 tmux：可同時操作多個終端 session 並保持**持久**——關掉視窗後 session 仍在跑，再開回來一切原封不動。
- 建議的第一個練習：在 Herdr 內開一個 Claude session 送個 prompt，完全關掉終端機，再開新終端執行 `herdr` 並指定 session（如 demo），會回到同一個畫面與 prompt。
- 對比一般終端直接跑 CLI：要自己管多個分頁視窗，誤關後雖可用指令找回歷史，但難記又亂。

## 終端機選擇：Ghostty

- 作者原本用 iTerm，但 iTerm 會擋掉 Herdr 部分滑鼠功能與快捷鍵。
- 建議選一個好客製的終端機；功能異常時，請 Claude 或 Codex 查該終端機是否有可調整的覆寫設定。
- 作者現用 Ghostty（他認為只有 Mac 與 Linux 版）。其設定是單一檔案，可直接叫 agent 改配色、尺寸等。

## Space 與 Tab 的心智模型

- 進入 Herdr 後處於一個 **space**；`cd` 到專案目錄，該 space 就代表這個專案——等同 Codex 桌面版「新增專案並選資料夾」的概念。
- 支援滑鼠操作：右鍵選單、關閉、分割窗格（向右分割等），對不熟終端機鍵盤操作的人很友善。
- 一個 space 內可開多個 tab，例如一個跑 Codex、另一個跑 Grok。
- 預設側欄：上方是 spaces（專案），下方 agents 區列出有啟動 agent 的 session；純終端 tab 不會出現在 agents 區。

## 連接 coding agent

- 選單 → settings：可調主題、指示器、音效等。
- **Integrations** 頁列出所有支援的 agent harness，可從 UI 安裝（作者裝了 Grok、Codex，Claude 有新更新需重選）。
- 也可用指令一次安裝：

```
herdr integration install claude codex grok
```

- 建議優先完成，讓 Herdr 與各 harness 整合更好。

## 多專案與多 session

- 新建 space 時預設沿用上一個路徑，可再 `cd` 到其他專案（例如上一層的 FastAPI tutorial），形成另一個 space 並啟動 agent。
- 首次需要一次性把專案逐一加入，之後關掉 Ghostty 再開都還在。
- 可建立多個 **session**，把相關 repo 分組：
  - `herdr --session <名稱>`：不存在就建立，已存在就進入。
  - `herdr session list`：列出所有 session；直接執行 `herdr` 會進 default session。
  - `herdr --help`：列出所有指令；AI agent 也能執行這些指令。
- 作者下一步打算拆成多個 session，每個 session 放一個專案的多個 repo。

## 外觀：config.toml

- 所有外觀、手感、快捷鍵都在 `config.toml` 設定。
- 作者沒讀過其中任何一行，而是把 agent 指向這個檔案與 Herdr 文件，問「能改什麼、我想要什麼」，讓 Codex 代改配色、元素間距等。

## 快捷鍵

- 同時操作多個 agent、頻繁切換時，快捷鍵是關鍵；從 tab 到 space 都可用鍵盤導覽。
- 預設採 **prefix key** 模式（Mac 預設 `Ctrl+B`，按下會顯示可用快捷鍵，再按 `C` 開新 tab），類似 tmux／Vim；作者不確定 Windows 預設是否相同。
- 作者不喜歡 prefix，改成一般 app 的操作方式：
  - `Cmd+T` 開新 tab、`Cmd+W` 關閉
  - 修飾鍵 + 上下方向鍵切換專案，左右切換 tab
  - 另設熱鍵直接跳到「已完成工作」的 agent（agent 完成時會提示）
  - `Cmd+K` 開啟面板跳到任意 workspace，輸入 `/` 可搜尋
- 作者的實際流程：熱鍵叫出 Herdr → `Cmd+K`、`/fastapi` 進專案 → `Cmd+T` 開新 tab → 啟動 Codex、選模型（GPT-6 Astra high）→ 用聽寫工具口述 prompt → Enter。
- 從只用 Codex 或 Claude Code 轉過來有學習曲線，但習慣後很快。

## Agent 委派：Herdr skill

- Herdr 提供一個 skill 檔，教 agent 如何使用 Herdr CLI：開新 agent、建 session、開多個 tab。
- 需要為**每個要用的 harness 全域安裝**這個 skill（作者裝在 Grok、Codex、Claude）；如此對任一 agent 說「用 Herdr skill 開另一個 agent 做某事」它都知道怎麼做。
- 示範：在 FastAPI 專案開 Codex（GPT-6 Astra，因昂貴調成 medium）當 orchestrator／reviewer，要求它「用 Herdr skill 在這個 session 右側 tab 開另一個 agent，用 Opus 5 review 這個 codebase」。Codex 會讀 skill 檔、透過 Herdr CLI 建新 tab、啟動 Claude Code 並選 Opus 5、送出 prompt。
- 可擴展成一次開多個 session、混用不同模型。
- tab 之間也能透過 Herdr CLI 溝通：子 agent 完成後可回報，並讓原 session 繼續。所有 session 過程都完全可見、可瀏覽。

## 補齊 IDE 體驗：Neovim 與 Lazygit

- 從 Cursor／VS Code 轉來後的斷層：在哪個 branch？agent 動了哪些檔？work tree 有什麼未提交？這兩個工具與 Herdr 無關，是一般終端工具。
- **Neovim**：作者請 AI 協助完成設定，執行 `nvim .` 並把該 tab 移到第一個，當作檔案瀏覽與搜尋器；快捷鍵仍在學。
- **Lazygit**：終端版 git 介面，可 push、pull、commit；作者另設熱鍵在任一 session 一鍵叫出，看目前 branch 與變更。
- 版面規劃：agents tab、檔案檢視 tab、跑 dev server 的終端 tab 等，全都保存在 session 中。
- 作者的目標：只需要這一個畫面——口述給 AI、讓 agent 跑、review，然後去做別的事。

## 快速切換資料夾：zoxide

- 新增 space 時不必複製路徑再 `cd`，改用 zoxide：
  - `zi` 後 Enter：列出可搜尋的目錄清單，直接挑選跳轉。
  - `z` 加目錄名再按 Tab：自動補全。

## 用 Glaido 遠端操控 Herdr

- 核心洞見：Herdr 的一切都能透過 CLI 完成，因此可以從外部觸發。
- 作者在聽寫工具 Glaido（影片工商）中建了自訂 MCP server 連到 Herdr：在任何頁面或 Slack 訊息中複製內容，口述「在 executive assistant 開一個 Herdr agent 幫我處理」，允許 MCP 執行後即在背景啟動工作，不必開其他 app。
- 因為是自訂的，可決定預設 agent 與 harness；未來可傳選取文字或截圖。
- Glaido 的 command mode 目前為 beta，需在帳號 general 設定開啟 beta 功能。

## 結語

- 作者只用了一週，仍在實驗階段；Herdr 高度可客製，而且可以叫 agent 代為設定，不必自己啃文件。
