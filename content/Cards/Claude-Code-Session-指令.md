---
title: Claude Code Session 指令
created: 2026-04-24
updated: 2026-04-25
tags:
  - claude-code
  - cli
---

Claude Code 內建的 session 層指令，管理對話節奏、context 與通知。

## 指令速查

### `/insights` — 工作習慣分析

官方內建 command，分析 Claude Code sessions，整理互動模式、常碰到的 friction points 與可改善的工作流。適合週期性回看，把值得長期保留的規則整理進 `CLAUDE.md`。

### `/btw`（by the way）— 側邊對話

- 看得到**完整主 session context**
- **不會進主 conversation history**
- **沒有 tool access**，只能回答當前 session 已知內容
- 即使主任務正在跑，也能獨立發問

適合查名詞、補問前文、確認某個決策，不適合需要讀檔或跑指令的新研究工作。

### `/statusline` — 常駐狀態列

官方內建 command，可自然語言描述你想看的資訊。常用組合：model name、context percentage、git branch / dirty state、cost / duration。

**建議至少常駐 context %**，比憑感覺判斷該不該 `/compact` 靠譜得多。

### Notification hook + `/hooks`

1. 在 `settings.json` 設 `Notification` hook
2. 用系統通知指令（macOS `osascript`）在 Claude 完成或需要回應時提醒
3. 用 `/hooks` 檢查目前已載入的 hook 配置

多 session 並行時很有感。

### `/recap` — 回來先看一行摘要

Claude Code 會在你離開終端一段時間後自動準備 one-line session recap；也可手動用 `/recap` 立即生成。適合中斷後快速找回節奏。

## 其他 session 指令

- `/clear` — 開新對話，清空 context
- `/compact` — 壓縮目前對話，保留主線
- `/rewind` — 回到某個 checkpoint，還原 conversation / code / 或只做 targeted summary
- `/context` — 看目前 context 用量與重點耗用來源

## 來源

- [Commands](https://code.claude.com/docs/en/commands)
- [Interactive mode](https://code.claude.com/docs/en/interactive-mode)
- [Customize your status line](https://code.claude.com/docs/en/statusline)
- [Checkpointing](https://code.claude.com/docs/en/checkpointing)
