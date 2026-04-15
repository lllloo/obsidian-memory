---
title: 用 AI SaaS 賺錢的方法
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-17
source: https://www.youtube.com/watch?v=nS62guAxeGA
---

## 選擇點子

- 要做止痛藥，不是維他命——找到真實痛點並解決，而非錦上添花的功能。
- 選擇你有專業的產業，不要進入完全陌生的領域。
- 避開過度熱門的方向（如 AI 交易機器人、配對 App 的 AI 版）。
- 尋找點子的地方：Reddit 的使用者抱怨、Y Combinator 投資方向、Twitter/X 趨勢、或直接靠靈感。

## AI 工具選擇

- 程式開發：Claude Code 或 OpenCode（自主 AI Agent）
- IDE：Cursor 或 VS Code
- 除錯：Codex（比 Claude Code 更不懶惰，非常擅長找 bug）
- 雜務自動化：Agent Zero（轉換 logo、檔案分析等）
- 網路搜尋與深度研究：Perplexity
- 會議轉錄：Fireflies
- CI/CD 程式碼審查：Code Rabbit 或 Bugbot
- 重點是**精通少數工具**，不要過度堆疊工具。

## 技術棧

- 前端：Next.js + Tailwind CSS + shadcn/ui
- AI 推論：OpenRouter（涵蓋所有主流模型）或 Venice AI（注重隱私）
- 後端：Node.js 或 Python + FastAPI
- 資料庫：PostgreSQL，需要快取加 Redis
- 選擇主流技術棧，訓練資料豐富，AI 更能協助開發。

## 學習方法

- 善用深度研究工具（Perplexity、Claude、Gemini）理解複雜主題。
- 複雜問題送 GPT-5.2 Pro 做詳盡分析。
- 持續訂閱優質 AI 頻道，跟上最新工具發展。

## 推薦 AI 模型

- 開發首選：Opus 4.5（最強但較貴）
- App 內推論：Gemini Free Flash（便宜）
- 前端設計：Gemini Free Pro
- 除錯：GPT-5.2 Codex
- 開源微調：GLM 4.7（目前最佳開源模型）

## GitHub 使用

- 所有程式碼務必放 GitHub，不要用 zip 傳檔。
- 設置 main（正式）與 dev（開發）分支。
- 善用 GitHub Actions 做 CI/CD。

## 推廣與行銷

- **推廣與建產品同等重要**，甚至更重要。
- 上線前就要開始推廣：建立等候名單或預售。
- 每天至少花 2 小時在推廣上，包含發內容、DM 潛在客戶。
- **專注單一管道**：YouTube 長片、Twitter、或 LinkedIn 文章，選一個深耕。
- 創作有價值的內容，而非直接宣傳產品功能——透過教學或分析帶入產品。

## 部署

- 前端：Vercel
- 後端：Render.com 或 Railway
- 資料庫：Supabase
- VPS 主機：Hostinger
- 不要過度工程化，不要在早期就用 AWS——除非你真的有百萬用戶的規模問題。

## 付款系統

- **不要用 Stripe**（非 Merchant of Record，需自行處理全球稅務）。
- 推薦：Polar、Lemon Squeezy、Paddle——這些是 Merchant of Record，自動處理全球 VAT、GST 等稅務合規。
- 費率略高於 Stripe，但省去大量法律和會計麻煩。

## 定價策略

- 多數人定價太低，應適度提高定價，維持 70–95% 毛利率。
- 推銷年付或兩年付方案，而非月付——讓客戶一次付更多，讓你有更多資金投入廣告。
- 盡量走高客單價與 B2B 路線：賣給有錢的企業或富裕個人，收取四到五位數費用。
- 閱讀 Alex Hormozi 的書來學習如何打造有吸引力的產品方案。

## 驗證與用戶身份

- 推薦 Supabase Auth（最簡單）或 Clerk。
- 不要過度複雜化身份驗證，複雜系統容易引入安全漏洞。

## 數據分析

- 產品數據：PostHog（點擊、留存、功能使用）
- 錯誤監控：Sentry
- LLM 可觀測性：Langfuse（監控 token 用量）
- 沒有數據就沒有辦法做出理性決策。

## Prompt 與 Context Engineering

- 你的 App 本質上是一個 wrapper，但好的 wrapper 可以賣到天價（例：Casetext 以 6.5 億美元出售）。
- 使用 XML 標籤區分提示詞的不同段落。
- 在程式碼根目錄建立 agents.md 定義 AI 行為規則。

## 常見錯誤

1. **太愛自己的點子**——點子賺到錢才算好點子，未成功前不要有情感依附。
2. **只建不推**——推廣是你每天前 60 分鐘最重要的任務。
3. **解決沒人願意付費的問題**——在動手做之前先確認市場付費意願。
4. **試圖服務所有人**——選定清晰的目標客群，深耕小眾市場。
5. **永遠兩週後才要上線**——設定截止日並嚴格執行，bug 也要上線。
6. **進入衰退市場**——確保你的市場在成長。
7. **不善用 AI 學習**——AI 最強的用途之一是加速你自己的學習與判斷力。
8. **過度花費在 API 上**——監控 API 成本，保持毛利率 50% 以上。
9. **功能過度膨脹**——MVP = 一到兩個核心功能，多了就是 feature bloat。

## 其他建議

- 找真實測試者（家人、朋友、目標用戶），最好親眼看他們使用產品。
- Landing page 要簡潔，Sign Up 按鈕放右上角，說清楚解決什麼問題。
- 新用戶 onboarding 要快，用 Frigade 做漸進式引導。
- 付費升級要順暢——免費用戶常看到升級橫幅，付費功能旁要有升級按鈕。
- 必須有服務條款與隱私政策（找律師處理，不要只靠 AI）。
- 成立 LLC 可用 Stripe Atlas（不需要去美國）。
