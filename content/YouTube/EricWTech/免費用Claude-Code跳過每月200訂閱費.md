---
title: "免費用 Claude Code，跳過每月 $200 訂閱費"
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-28
source: https://youtu.be/o85Y5omRQq0
---

**影片描述**：示範如何完全免費使用 Claude Code，不需要 Claude Max 或 Pro 訂閱方案，也不需要在本機安裝任何本地模型，而是透過 OpenRouter 連接免費或低成本的第三方 AI 模型，同時保留 Claude Code 的完整 sub-agent 功能。

**重點摘要：**
- **核心方法**：前往 openrouter.ai 建立免費帳號取得 API 金鑰，在專案根目錄的 `.claude/settings.local.json` 中設定 `ANTHROPIC_BASE_URL`（指向 OpenRouter API）、`ANTHROPIC_AUTH_TOKEN`（填入 OpenRouter API 金鑰）及目標模型名稱，Claude Code 即改向 OpenRouter 發出請求。
- **設定層級**：專案層級（設定放在專案資料夾的 `.claude/settings.local.json`，只影響該專案）vs 全域層級（設定在根目錄，對所有專案生效），兩者可獨立設定。
- **免費模型選項**：OpenRouter 提供「Free Models Router」（`openrouter/free`），隨機路由到可用的免費模型，但回應速度較慢（約 31 秒），準確率有限，只適合學習或 demo，不建議正式開發。
- **最佳中價位選擇**：OpenRouter 的 **AI Model Rankings** 頁面可依程式語言篩選熱門模型，Programming 類別排行榜第一名為 **MiniMax M2.5**，每百萬 token 不到 $2 美元；對比 Claude Sonnet 4.6 約 $18/百萬、Opus 4.6 約 $30/百萬 token，性價比顯著。
- **實際費用**：作者整個示範 session 的完整成本僅約 $0.20，驗證低成本可行性。
- **功能測試：sub-agents 仍可用**：使用 MiniMax M2.5 透過 OpenRouter 成功觸發 Claude Code 的 sub-agents 功能，示範以 4 個平行代理並行審查 QA 文件，找出未覆蓋的邊緣案例，輸出各 agent 的發現摘要與優先測試建議。
- **狀態列工具**：作者提到可安裝特定工具顯示目前使用的模型名稱與 context window 用量，便於監控。
- **適用情境**：預算有限的開發者、學習 Claude Code 功能的初學者、不需要頂級模型準確率的 demo 或原型開發；若追求高準確率正式開發，作者建議評估是否訂閱 Claude Pro 方案比 OpenRouter 使用 Claude Sonnet 更划算。
