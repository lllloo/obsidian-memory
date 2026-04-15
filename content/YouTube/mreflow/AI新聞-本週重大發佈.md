---
title: AI 新聞：本週每個重大發佈
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-20
source: https://www.youtube.com/watch?v=V4un_4uTEHs
---

## MidJourney V8

- 新版本號稱改進了複雜指令遵循、個人化風格參考、文字渲染及畫面細節
- 新增 HD 模式（2K 解析度）；舊參數如 chaos、weird、raw 仍可用
- 實測：文字渲染仍不穩定，細節（手指、肢體比例）問題依然存在
- 網路評價不佳，速度快但整體表現落後 Flux、NightCafe 等競品

## Microsoft MAI-Image-2

- 微軟推出圖像生成模型，主打照片真實感、精準文字渲染、豐富場景細節
- 在 Text-to-Image Arena 排名第三（僅次於 OpenAI 和 Flux）
- 實測：細節遵循、文字準確度表現優於同期 MidJourney V8

## Google Stitch 「Vibe Design」

- 新 AI 原生設計畫布（類 Figma 介面），支援語音指令即時調整設計
- 可匯出 `design.md`（設計規則的 Markdown 檔），供 OpenClaw、Claude Code 等 agent 工具讀取
- 支援 MCP、skills、markdown 規則——明顯為 agent 工作流設計
- 可生成多個設計變體後直接匯入 Google AI Studio vibe coding 環境

## Google AI Studio Vibe Coding

- 直接貼入 Stitch 匯出的 `code.html` + `screen.png`，Gemini 可生成功能性網站原型
- 實測：動畫效果、基礎篩選功能可用；深色模式等進階功能需補充 prompt
- 設計（Stitch）→ 開發（AI Studio）已形成完整閉環

## Google Personal Intelligence 擴大開放

- 先前僅限付費方案，現在美國地區免費用戶可在 AI Search Mode 和 Gemini App 使用
- 可連接 Gmail、Google Photos、Calendar，讓 Gemini 提供個人化回應

## NVIDIA GTC 重點

- **Nemo Claw**：一鍵安裝 OpenClaw，附加安全與隱私層，並整合 Nvidia RTX/DGX 優化
- **DLSS5**：AI 即時升頻技術可套用於現有遊戲；遊戲開發者可控制啟用程度，玩家可手動關閉
- **Nvidia Space 1 Vera Rubin**：太空資料中心計畫，GPU 散熱問題尚未解決，無具體時程
- **1 兆美元預測**：Jensen 表示 2027 年前 GPU 銷售預估超過 1 兆美元，基於現有採購訂單（前一年約 5000 億）
- Nvidia 已深入所有主要 AI 雲端供應商（Google、AWS、Oracle、Microsoft、Coreweave）及各產業垂直領域

## OpenAI 新模型

- **GPT 5.4 Mini / Nano**：輕量版，速度更快、成本更低；適合 agent 背景任務；電腦使用能力與完整版相當
- **Claude 1M token context**：Opus 4.6 和 Sonnet 現可使用百萬 token 上下文

## Mistral Small 4

- 開放權重模型，可本地 fine-tune；coding 和 math 表現接近 Claude Haiku、Qwen 3.5 122B

## Cursor Composer 2

- Cursor 自研 coding 模型，成本效益高：接近 GPT 5.4 水準但便宜許多
- 建議作為 Cursor 預設模型，必要時再切換至 GPT 5.4

## MiniMax M2.7

- 聲稱「自我進化」：可自主觸發 log 閱讀、除錯、指標分析
- 處理了 30~50% 自身開發工作流；以 100+ 輪迭代優化自身程式碼
- 罕見地從開放權重轉為專有模型

## Mamba 3

- 非 Transformer 架構（State Space Model），維護「壓縮的動態內部狀態」而非重新審視所有 token
- 長對話下理論成本與速度優勢顯著

## Claude Co-work Dispatch

- 新功能：持續對話在背景執行，可從手機發送指令，回來找到已完成的工作
- 定位接近 OpenClaw 的離線代理體驗

## Manus My Computer

- Meta 收購 Manus 後推出桌面版，可執行終端機指令、讀取/編輯本地檔案、控制本地應用程式
- 功能定位與 Claude Co-work 高度重疊

## André Carpathy US Job Market Visualizer

- 視覺化哪些職位因 AI 而衰退（收銀員、客服、帳務）vs. 成長（廚師、軟體開發、電工、建築工）
- 整體仍是成長職位多於消失職位

## Uber × Rivian 自駕計畫

- 投資 12.5 億美元，部署 10,000 輛 Rivian R2 自駕計程車，與 Waymo、Tesla Cyber Cab 競爭

## Meta AI Glasses 隱私爭議

- 若未正確設定隱私，錄製內容會傳至非洲人工標注者審查，包含敏感畫面（浴室、信用卡）
- 英國 ICO 介入調查；美國紐澤西和加州提起訴訟

## Anthropic vs. Pentagon 後續

- 事件脈絡：Anthropic 設定兩條紅線（不得用於監控美國公民、不得用於全自主武器）；國防部拒絕並宣布 supply chain risk 指定
- OpenAI 同日接手合約，聲稱相同紅線加第三條（不得大規模國內監控）；但內部備忘錄顯示「不由 OpenAI 決定軍事行動的對錯」
- 結果：ChatGPT 解安裝量週末暴增 295%，Claude 躍升 App Store 下載第一；Anthropic 年化營收接近 200 億
- 企業端轉換：Ramp 數據顯示企業 AI 支出 Anthropic 已超越 OpenAI（去年 OpenAI 遠領先）
- Anthropic 表示正在和解談判，並稱將在法院挑戰 supply chain risk 指定
