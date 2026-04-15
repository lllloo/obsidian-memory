---
title: 100% 自我改進 AI Agent 實作展示
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-29
source: https://www.youtube.com/watch?v=EHlqRx0r4BI
---

## 概覽

- Hermes Agent 是 NousResearch 開發的開源 AI Agent，定位介於 Claude Code（開發者向）與 OpenClaw（大眾向）之間。
- 最大特色：**自我改進循環**——每約 15 次工具呼叫後，Agent 自動評估自身執行軌跡，從中學習並更新技能。
- 3 週內突破 15,000 GitHub stars，快速增長中。

## 核心技術：GEPA（Generic Evolution of Prompt Architectures）

- 讀取 Agent 的執行軌跡（工具呼叫結果、失敗原因）。
- 用演化/遺傳演算法改變（mutate）自己的 Prompt、Skill 和程式碼。
- 概念類似 Transformer 的反向傳播，但作用在 Prompt 和程式碼上。
- 結果：不需要使用者手動調整 Prompt，Agent 透過試錯自行進化。

## 記憶系統（四層）

1. **memory.md + user.md**：類似 OpenClaw 的 Markdown 文件。
2. **SQLite Session Archive**：為 Agent 最適化的資料格式——SQL 設計用於快速查詢大量資料，遠比 Markdown 適合 Agent。
3. **Procedural Memory（技能）**：Agent 從完成的任務中自動建立的程序性記憶，會隨使用而自我改進。
4. **Honcho User Modeling**（選配）：對話式問答了解使用者偏好的記憶層。

## 其他功能特色

- **File System Checkpoints**：在重要操作前自動建立類似 git commit 的備份。
- **Git Worktree 支援**：內建支援平行 Agent 工作流。
- **Intelligent Forgetting**：壓縮 context 前先提取重要知識，避免重要資訊因壓縮而遺失。
- **80+ 內建技能**：包含 Claude Code、Codex、OpenCode、Hermes 子 Agent、資料科學、Minecraft 伺服器等。

## 安裝步驟（VPS）

1. 在 VPS 建立新使用者：`adduser hermes`，加入 sudo 群組。
2. 複製 Hermes 快速安裝指令（來自 GitHub Readme）。
3. 在 Hostinger Terminal 貼上並執行：
   - 自動偵測 Linux + Ubuntu
   - 安裝 Python、Node.js、ffmpeg、ripgrep 等相依套件
4. 選擇模型提供商：**OpenRouter**（可用所有模型）。
5. 貼入 OpenRouter API key，選擇模型（推薦 Opus 4.6）。
6. 設定 Agent 迭代上限：建議 **150**（預設 90）。
7. Context 壓縮閾值：建議 **0.7**（預設 0.5 過於保守）。
8. 設定 Telegram Bot（透過 BotFather 建立 → 貼入 Token）。
9. 取得 Telegram 用戶 ID（向 UserInfoBot 發訊息取得）→ 加入白名單。
10. 安裝 Gateway 為 systemd service（開機自動啟動）。
11. 設定 Browser Use API key（browser.use 官網取得）。

## 啟動方式

- **終端機 TUI 模式**：`hermes`
- **Gateway 模式（Telegram 等）**：`hermes gateway start`
- **繼續上一個 Session**：`hermes -c`
- **重新執行安裝步驟**：`hermes setup`

## 從 OpenClaw 遷移

```bash
hermes claw migrate
```
- 自動將 OpenClaw 的設定遷移到 Hermes，不需從零開始。

## 支援的通訊頻道

Telegram、Discord、Slack、WhatsApp、Signal、CLI（與 OpenClaw 相同範圍）

## Hermes vs OpenClaw vs Agent Zero 比較

| 面向 | Hermes Agent | OpenClaw | Agent Zero |
|------|-------------|---------|-----------|
| 成熟度 | 最新，仍粗糙 | 中等 | 最成熟（2 年） |
| 自我改進 | 內建 GEPA 循環 | 無 | 無 |
| 記憶系統 | 4 層（含 SQLite） | Markdown | 向量 + Markdown |
| 目標族群 | 開發者為主 | 一般大眾 | 隱私優先進階用戶 |
| Heartbeat | 無 | 有（30 分鐘） | 無 |
| 開源 | 是 | 是 | 是 |

## 適合對象

- 不需要大量手動 Prompt Engineering、希望 Agent 隨使用自動變強的人。
- 開發者或願意嘗試新工具的進階使用者（目前仍有 Bug，UI 尚未打磨）。
- 已有 OpenClaw 的用戶：可用 `hermes claw migrate` 輕鬆轉移。

## 注意事項

- 目前約 1 個月新，UI 不如 Claude Code 或 Codex 精緻，預期有 Bug。
- 遇到問題時重新描述任務或等候修復，不要放棄。
- Hermes 的改進速度很快，短期內品質將大幅提升。
