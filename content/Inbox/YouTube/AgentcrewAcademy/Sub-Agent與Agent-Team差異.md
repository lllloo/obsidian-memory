---
title: Claude Code 使用技巧：讓 AI 再幫你指揮 AI —— Sub Agent 跟 Agent Team 差在哪？
created: 2026-04-27
updated: 2026-04-27
source: https://www.youtube.com/watch?v=GPuDxpiicLU
published: 2026-04-21
parent: "[[01.index]]"
tags:
  - youtube
---

## Sub Agent 基本概念

Claude Code 中的 Sub Agent 指主 agent 派出的「工讀生」，能自主執行任務、達成並行處理或協作加成。目前在 Claude Code 內有兩種形式：

- **平行 Sub Agent**：多個小 agent 各自獨立處理任務，彼此不溝通
- **Agent Team**：由 manager 統籌、team member 之間能互相傳訊溝通

## 平行 Sub Agent 適用情境

判斷一個任務是否該丟給平行 Sub Agent，看三個條件：

1. **任務可並行**：彼此沒有依賴（例：分別處理 a、b 兩個資料夾）
2. **不需橫向溝通**：兩邊內容互不關聯
3. **非持久化**：只需要回傳摘要，中間過程不需要佔用主 agent 上下文

每個 Sub Agent 擁有獨立上下文，做完只把摘要結果回傳，主 agent 不會被中間細節塞滿。

## 平行 Sub Agent 的三大好處

- **節省上下文**：中間過程不污染主 agent，保持主 agent 上下文精簡
- **避免球員兼裁判**：用獨立 Sub Agent 來審查主 agent 的成果，比讓同一模型在同一對話裡自驗更公平
- **差異化模型搭配**：主 agent 用 Opus，把長文件、低難度任務派給 Haiku Sub Agent 處理（例：200 多頁文件用 Haiku 讀完回傳摘要，省 token 又避免長文造成的注意力缺失）

長文件處理可進一步把文件切段，每段一個 Sub Agent 負責，最後再請一個 agent 會診結果。

## Agent Team 協作模式

Agent Team 與平行 Sub Agent 最大差別：**team member 之間可互相傳訊溝通**。

- 有 manager 統籌全局、分派任務
- Team member 既能互相對話交換資訊，也能直接與 manager / 主使用者對話
- 適合需要高度協作的任務（例：系統重構、文件重整），任務之間關鍵地方需要交換資訊

## 設定與管理 Agent

- 終端機輸入 `/agents` 可查看目前設定
- 每個 agent 是一個 `.md` 檔，定義四件事：
  - **基本介紹（描述）**：模型靠這個描述決定何時呼叫
  - **可用工具**
  - **使用模型**
  - **提示詞**：定義 agent 扮演的角色與任務
- 不需親自編寫，可直接請 Claude Code 幫忙建立 agent

可建立的常態型 agent 範例：

- 程式碼審查（例：Python 專屬）
- 安全檢查
- 量化分析
- 財務審查
- 語氣審查
- 文件修正
- 呼叫 Gemini 處理長文字以節省 Pro 額度

## 平行 Sub Agent 實戰示範

任務：請 Claude Code 整理桌面與下載資料夾。

- 兩個資料夾相互獨立 → 適合平行
- 只需要整理建議、不需細節塞進主 agent 上下文
- 按下 enter 後 Claude Code 自動派出兩個 agent 各自調查
- 任務進行中可按 `Ctrl + B` 把它們丟到背景
- 任一 agent 完成會把摘要自動回傳給主 agent

## Agent Team 實戰示範

任務：兩個 agent 一個管下載、一個管桌面，且必須溝通決定哪些檔案該換放。

- Claude Code 切換成 team 介面：一個 manager、兩個 team member
- 可單獨點 team member 與其對話，也可回到主 agent
- Team member 之間自動互相對話對接分類建議，產出協商報告
- Manager 會定時催進度（畫面上看到 manager 對 member 「你們趕快」「給我最終清單」），很像真實團隊在 Slack 對話
- 結論達成後 team 自動關閉，組員解散，主 agent 接手整理最終結果

## 兩種模式的選用總結

| 模式             | 適合情境                                                       |
| ---------------- | -------------------------------------------------------------- |
| 平行 Sub Agent   | 任務可並行、無需橫向溝通、臨時、只需要結果摘要、不想佔主上下文 |
| Agent Team       | 組織型任務、任務之間需協同溝通、需要互相驗證                   |
