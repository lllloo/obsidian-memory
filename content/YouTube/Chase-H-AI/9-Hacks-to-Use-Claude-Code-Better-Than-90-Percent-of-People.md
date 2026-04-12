---
title: 9 Hacks to Use Claude Code Better Than 90% of People (In 9 Minutes)
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/XkSBO-CZDFs
---

9 個高槓桿、易實作的 Claude Code 技巧，幫助超越 90% 使用者。

## 9 個技巧

1. **CLI 優先於 MCP**：CLI 在終端機運行，與 Claude Code 天然整合，token 消耗更低、功能更多；使用 CLI 時搭配 skill 教導 Claude Code 使用方式

2. **`/btw` 側邊對話**：在 Claude Code 執行任務期間可同步對話，且不計入 context window，是大 context 下的效率工具

3. **`/hook` 完成音效**：設定任務完成時播放提示音，避免忘記查看結果而浪費時間（`/hook` → 「完成時播放聲音」）

4. **`/clear` 早用勤用**：重置 context window 以對抗 context rot；context 超過 20-25% 即應清除（256K tokens 時效率 91%，1M tokens 時降至 65%）

5. **狀態列（Status Line）**：`/status line` 設定常駐顯示目錄、模型名稱、context 使用率

6. **Skill Creator Skill**：Anthropic 官方 skill，可建立/修改/測試 skill，提供量化效能比較

7. **Agent Teams（實驗功能）**：需手動啟用，讓 sub-agent 之間互相協調溝通（非各自為政），輸出品質更高但 token 略多；需明確說「create an agent team」才會啟用

8. **Plan Mode 開放式提問**：用「我沒想到什麼？」、「專家會考慮什麼？」等問題獲得更深層的規劃引導

9. **Claude Code + Obsidian 第二大腦**：Obsidian 免費，將 vault 資料夾開在 Claude Code 中，讓 AI 建立 markdown 筆記並透過 Obsidian 視覺化管理

## 補充

- Agent Teams 文件：搜尋「agent teams claude code documentation」複製給 Claude Code 啟用
- Obsidian 適用場景：大量 markdown 文件的個人助理型專案，而非傳統 coding 專案
