---
title: Harness Engineer 長期自主 Agent 設計
tags:
  - youtube
  - ai-agent
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: 2026-03-05
source: https://www.youtube.com/watch?v=kJPvfoLtFFY
parent: "[[01.index]]"
---

## 背景：2025 年 12 月的轉折

2025 年 12 月起，AI 模型首次具備執行長期自主任務的能力，從 AutoGPT 的基礎想法演進到真正可運作的長時間 autonomous agent，代表由 co-pilot 走向全自主系統的典範轉移。

## 什麼是 Harness Engineer

Harness Engineer 是 Context Engineer 的進化版——不再只優化單次 agent session 的 prompt，而是設計跨 session、跨 agent 的整體工作流程與工具體系。

核心關注：
- 如何讓每個 sub-agent session 都能快速理解當前環境狀態
- 如何設計驗證機制讓 agent 有效確認自己的輸出
- 如何給予 agent 最合適的工具組合

## 三個關鍵學習

### 可讀環境（Legible Environment）

Anthropic 實驗中觀察到的兩個預設失敗行為：
- Agent 傾向一次完成所有功能（one-shot），導致 context 用盡後下一個 session 無從銜接
- Agent 傾向過早宣稱任務完成

解法：
- 初始化 agent 先建立環境骨架：`init.sh`（啟動 dev server）+ `progress.txt`（進度日誌）+ git commit
- 後續 coding agent 每個 session：讀取 feature list → 挑選高優先任務 → 做增量進展 → 更新進度並 commit
- Feature list 以 JSON 鎖定（200+ 功能，預設全為 fail 狀態），強制 agent 逐一確認

OpenAI 的做法：
- `agents.md` 作為 table of contents，底下分層放 architecture、design docs、DB schema 等
- 把 Google Docs、Slack 訊息也匯入 repo，讓 agent 能存取所有相關資訊
- 程式碼設計為可按 git worktree 啟動，供 Codex 同時驅動多個 instance

### 快速回饋迴圈與驗證

- 不能只靠 unit test，需要端對端測試工具（Puppeteer MCP、Chrome DevTools）
- OpenAI 實驗：agent 自動重現 bug → 錄製失敗影片 → 修正 → 驗證 → 錄製通過影片 → merge

### 使用通用工具

Vercel 的 text-to-SQL agent 重構案例：
- 原本：複雜的專用工具 + 大量 prompt engineering → 脆弱、需頻繁維護
- 改為：單一 batch command 工具
- 結果：速度快 3.5 倍、token 少 37%、成功率從 80% → 100%

原則：LLM 對程式碼原生工具（grep、npm、git）的訓練資料遠多於自訂 JSON schema，因此通用工具表現更好。

## Open Claw 的架構啟示

Open Claw 的簡單但有效設計：
- 文件層：core information 的結構化文件
- 工具：只有 read / write / edit files、batch commands、send messages
- Skill library：可擴展的能力庫，contextual 載入
