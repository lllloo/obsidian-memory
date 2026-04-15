---
title: 投資 AI 前必懂的 7 個術語
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 
source: https://www.youtube.com/watch?v=hKC_pI_yhZc
---

## 1. AI Agents（AI 代理）

LLM 直接輸出回覆 = workflow，沒有真正的「代理性」。  
Agent = LLM 在環境中循環執行動作、獲得反饋，直到達成停止條件。

比喻：給實習生一個任務，他自己去嘗試、犯錯、修正，只在完成或卡住時回報。

## 2. Vector Databases（向量資料庫）

LLM 只懂訓練時的資料，對內部文件一無所知。  
解法：
1. 把文件餵入 embedding model → 轉成向量（數字序列，代表語義）
2. 向量存入向量資料庫（Chroma、LanceDB、Weaviate、pgvector）
3. 查詢時做 similarity search，找出語義最相近的內容

向量資料庫 = 依語義組織的知識庫，等於給 AI 長期記憶。

## 3. RAG（Retrieval Augmented Generation）

使用向量資料庫的完整流程：
1. 使用者提問
2. 問題同樣轉成向量
3. 在向量資料庫做 similarity search 找出相關段落
4. 問題 + 相關段落一起送進 LLM
5. LLM 基於檢索到的真實資料生成回答

比喻：開卷考試——考生不需要背所有東西，只需翻課本找到對應章節，再用理解力組織答案。

## 4. MCP（Model Context Protocol）

Anthropic 於 2024 年底發布的標準協定，統一大語言模型與外部工具（Slack、GitHub、資料庫等）的整合方式。

沒有 MCP 前：每個開發者自己搞每個工具的 API，重複造輪子。  
有了 MCP 後：工具只要實作一次 MCP 介面，所有支援 MCP 的 LLM 都能用。

比喻：萬能遙控器，一個介面操作所有裝置。

本質是 tool calling 的標準化——LLM 在工具調用層統一了。

## 5. Context Engineering（情境工程）

LLM 回答品質直接受 context window 內的內容影響：太少→答不出來；太多→幻覺增加。

Context Engineering = 決定在 context window 中放什麼、不放什麼，讓 LLM 有「剛好足夠」的資訊。

不只是 prompt engineering（怎麼問），而是整體設計什麼資訊進 LLM。

## 6. Fine-tuning（微調）

在預訓練模型的基礎上，用自訂資料集繼續訓練，調整模型的行為或知識。

適合：需要特定語調、專業術語、固定格式輸出的場景。  
不適合：知識更新頻繁的情境（用 RAG 更好）。

三種主要方式：
- 全量微調（Full fine-tuning）：更新所有參數，成本高
- LoRA：只更新少量低秩矩陣，效率高
- RLHF（Reinforcement Learning from Human Feedback）：用人類偏好資料強化學習（ChatGPT 就是這樣訓練的）

## 7. Guardrails（護欄）

在 AI 系統輸入/輸出加設的安全與品質檢查機制：
- Prompt injection 防禦：阻擋惡意注入指令
- 內容過濾：過濾有害或不當內容
- 輸出驗證：確保格式正確、符合業務規範
- 人工審核觸發：高風險情況升級給人類

判斷結果：允許通過 → 送給用戶；不允許 → 給預設回覆或升級處理。
