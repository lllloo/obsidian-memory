---
title: Perplexity 電腦操控功能展示
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-15
source: https://www.youtube.com/watch?v=tJ-INHRf8SY
---

## 概覽

- Perplexity Computer 是一個雲端 AI Agent，能像人類一樣操作瀏覽器、建立各類型檔案、生成圖片與影片、整合超過 400 種服務，並可啟動子 Agent。
- 最接近的比較對象：Manus（去年爆紅的雲端 Agent），但 Perplexity 更進階。
- 定位：**適合非技術使用者的 OpenClaw**——不需要 VPS 設定、API key、任何技術知識。

## 核心技術優勢：如何繞過封鎖

- **問題**：大多數 AI Agent 使用資料中心 IP，很多網站會封鎖這類流量。
- Agent Zero / OpenCode：在本機電腦執行，使用住宅 IP，不會被封鎖。
- **Perplexity Computer 解法**：
  - 雲端托管但透過 VM（虛擬機器）+ 數千個代理伺服器繞過封鎖。
  - 兩個獨立 VM：Firecracker MicroVM（125ms 啟動、會話結束後銷毀）+ Cloud Browser VM（不同 IP、完全隔離）。
  - 即使發生程式碼注入，也不會影響瀏覽器 VM。

## 架構：Orchestrator + 子 Agent

- 主 Orchestrator 預設為 **Opus 4.6**（可切換）。
- Orchestrator 存取 19 個不同 AI 模型，根據任務類型自動路由：

| 任務類型 | 使用模型 |
|---------|---------|
| 編排（Orchestration） | Opus 4.6 |
| 研究（Research） | Sonnet 4.6 |
| 資產建立（Asset Creation） | Opus 4.6 |
| 程式開發（Code） | GPT-5.4（Codex） |

- Orchestrator 可派發多個子 Agent **平行執行**，最終彙整結果。
- 子 Agent 各有獨立 context window，但**共享同一個工作區檔案系統**。

## 記憶系統

- 內建向量資料庫，支援語義搜尋。
- 記憶跨會話持續，不需要每次都說「記住這件事」。

## 超過 400 種整合

- 類似 OpenClaw 支援 WhatsApp、Telegram、Slack，Perplexity Computer 支援更多：
  - Slack、Gmail、Google Calendar、Notion、GitHub、Linear 等
- 在介面中點擊「+」→「Connectors」認證一次，憑證永久保存。

## 排程系統

- 支援 Cron Job（定時任務）。
- 架構特色：**每次執行都使用全新隔離 VM**，零跨回合記憶，防止幻覺累積。
- 支援 Push 通知：若掃描 Twitter 有人 tag 你，只有在真的被 tag 時才發送通知（Agent 做智慧篩選）。

## 實測案例：研究複雜主題並生成視覺化

- **任務**：研究「波蘭槍枝許可證申請流程」，輸出清楚的 PDF 指南。
- 執行過程：
  - 同時用英文和波蘭文搜尋多個來源（EU 官網、波蘭協會）。
  - 讀取技能（skill）了解如何建立 PDF。
  - 撰寫 Python 程式碼生成 PDF。
- **結果**：8 頁格式精美的 PDF，包含步驟說明、費用表、時程（最長 6 個月）、可合法擁有的槍枝類型、關鍵網址與所有來源連結。
- **對比 ChatGPT**：同樣的任務 ChatGPT 跑了 9 分鐘，PDF 設計差、內容也更短。

## 實測案例：地緣政治互動儀表板

- **任務**：分析「荷姆茲海峽封閉對全球經濟的影響」，建立互動式網頁應用。
- 結果：含以下互動視覺化：
  - 油價歷史趨勢（50 年）
  - 各封閉場景的油價預測（$100 → $120 → $140 → $170）
  - 各產業受衝擊程度（航空、石化最高；科技、金融最低）
  - 一桶石油的成分分解圖

## Perplexity Computer 的 Skill 系統

- 根據對話主題**自動載入對應 Skill**（如討論 PDF 就載入 PDF 操作 Skill）。
- 這是一種 context 最佳化技術：只在需要時載入相關指令，節省 context window。
- 使用者也可新增或自訂 Skill。

## GitHub 整合

- 連接 GitHub 後，可讓 Perplexity Computer 直接讀寫 Repo。
- 注意：Perplexity 要求的 GitHub 權限範圍很廣（管理所有 Repo、Gists、Projects）。
- **建議**：為 AI Agent 建立獨立的 GitHub 帳號，不要用主帳號。

## 定價評估

- Perplexity Max（$200/月）附帶 10,000 點基本額度，另有贈送點數。
- **作者評價**：10,000 點不夠用，即使日常使用也很快燒完，CP 值不如：
  - ChatGPT Pro（$200/月）——功能最多（Codex、手機 App 等），額度最寬鬆
  - Claude Max（$100/月）——最強模型、最值得
  - 若只有 $100 預算，Claude Max 優先；$200 額外預算可考慮 ChatGPT Pro

## 安全與隱私注意事項

- Perplexity **不是開源、不以隱私為優先**——歷史上有大量數據收集爭議。
- Agent Zero 是開源且以隱私為導向的替代方案（本機執行）。
- 不建議授予 Perplexity Computer 訪問敏感數據的能力（如完整 GitHub、個人郵件）。
