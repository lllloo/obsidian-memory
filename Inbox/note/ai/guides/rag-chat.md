---
title: "QA 系統的聊天回覆"
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/ai/guides/rag-chat
tags:
  - rag
  - ai-agent
  - api
  - javascript
  - best-practices
---

# QA 系統的聊天回覆

本文介紹 QA 系統中常見的聊天回覆方案，依是否需要向量資料庫分組，幫助你根據場景選擇合適的做法。

## 方案總覽

| 方案 | 每次查詢成本 | 實作複雜度 | 回覆彈性 | 適合規模 |
| --------------- | ------- | ----- | ---- | ---------- |
| 直接塞 Prompt | 高 | 最低 | 高 | < 200 條 |
| 直接塞 + Cache | 中低 | 最低 | 高 | < 200 條 |
| 分類器 + 規則 | 最低 | 中 | 最低 | 類別固定 |
| Embedding 比對 | 最低 | 低 | 低 | 不限 |
| RAG | 低 | 中 | 高 | 不限 |
| Fine-tuning | 低 | 高 | 中 | QA 穩定不變 |

### 如何選擇

| 條件 | 建議方案 |
| ------------------------------ | --------------- |
| QA < 200 條，快速上線 | 直接塞 Prompt |
| QA < 200 條，查詢頻繁 | 直接塞 + Cache |
| 問題類型固定且有限 | 分類器 + 規則 |
| 只需回傳固定答案，不需改寫 | Embedding 比對 |
| QA ≥ 200 條，需要語意理解 | RAG |
| QA 穩定不變，需統一風格 | Fine-tuning |

## 直接塞 Prompt

最簡單的做法：把所有 QA 問答對放進 system prompt，讓 LLM 直接比對回覆。

```text
使用者問題 + 全部 QA → LLM → 回覆
```

- **優點**：幾行程式就搞定，不需要額外基礎設施
- **缺點**：受 context window 限制，QA 太多塞不下；所有 QA 都送進去，token 費用高
- **適合**：QA 數量少（< 200 條）、快速 MVP

```javascript
import { GoogleGenerativeAI } from '@google/generative-ai'

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY)

const qaList = [
  { q: '營業時間？', a: '週一至週五 9:00–18:00' },
  { q: '退貨政策？', a: '購買後 7 天內可退換' },
]

const qaContext = qaList.map(({ q, a }) => `Q: ${q}\nA: ${a}`).join('\n\n')

const model = genAI.getGenerativeModel({
  model: 'gemini-2.0-flash',
  systemInstruction: `你是客服助手，請根據以下 QA 清單回答問題。找不到相關答案時，回覆「抱歉，無法回答」。\n\n${qaContext}`,
})

const result = await model.generateContent('你們幾點開始營業？')
console.log(result.response.text())
// 輸出：週一至週五 9:00–18:00
```

## 直接塞 Prompt + Prompt Caching

與上面相同做法，但利用 API 的 Prompt Caching 機制降低成本。重複的 system prompt 部分會被快取，cached input 享有折扣，查詢越頻繁效益越高。各平台的快取機制略有不同：

- **OpenAI**：自動快取，只要 system prompt 內容相同且長度 ≥ 1024 tokens，不需要改程式碼
- **Anthropic**：需在 API 請求中明確標記 `cache_control` breakpoint，指定哪些內容要快取
- **Gemini**：需先呼叫 Cache API 建立快取物件，再將其綁定到模型使用

```javascript
import { GoogleGenerativeAI } from '@google/generative-ai'
import { GoogleAICacheManager } from '@google/generative-ai/server'

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY)
const cacheManager = new GoogleAICacheManager(process.env.GEMINI_API_KEY)

const qaList = [
  { q: '營業時間？', a: '週一至週五 9:00–18:00' },
  { q: '退貨政策？', a: '購買後 7 天內可退換' },
]

const qaContext = qaList.map(({ q, a }) => `Q: ${q}\nA: ${a}`).join('\n\n')

// 建立快取，TTL 1 小時（需達最低 token 門檻）
const cache = await cacheManager.create({
  model: 'models/gemini-2.0-flash',
  systemInstruction: '你是客服助手，請根據以下 QA 清單回答問題。',
  contents: [{ role: 'user', parts: [{ text: qaContext }] }],
  ttlSeconds: 3600,
})

// 後續請求重用快取，節省 token 費用
const model = genAI.getGenerativeModelFromCachedContent(cache)
const result = await model.generateContent('你們幾點開始營業？')
console.log(result.response.text())
```

## 分類器 + 規則回覆

根據關鍵字規則將問題對應到類別，直接回傳預設答案，不需要 LLM。

- **優點**：成本最低、速度最快、回覆完全可控
- **缺點**：無法處理未知問題、關鍵字維護成本高、彈性最差
- **適合**：問題類型固定且有限的場景

```javascript
const rules = [
  {
    keywords: ['營業', '開門', '幾點', '時間'],
    answer: '週一至週五 9:00–18:00',
  },
  {
    keywords: ['退貨', '退款', '換貨'],
    answer: '購買後 7 天內可退換',
  },
]

function classify(question) {
  for (const rule of rules) {
    if (rule.keywords.some((kw) => question.includes(kw))) {
      return rule.answer
    }
  }
  return '抱歉，請聯繫客服人員'
}

console.log(classify('你們幾點開門？'))
// 輸出：週一至週五 9:00–18:00
```

## Embedding 直接比對

用 embedding 計算使用者問題與 QA 問題的相似度，直接回傳最相似的答案，完全不經過 LLM。

```text
使用者問題 → embedding → 比對 QA 問題向量 → 回傳對應答案
```

- **優點**：成本最低（只需 embedding 費用）、速度最快
- **缺點**：無法整合多條 QA 回覆、答案不能改寫或補充
- **適合**：標準客服問答、FAQ 機器人

```javascript
import { GoogleGenerativeAI } from '@google/generative-ai'

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY)
const embeddingModel = genAI.getGenerativeModel({ model: 'text-embedding-004' })

const qaList = [
  { q: '營業時間？', a: '週一至週五 9:00–18:00' },
  { q: '退貨政策？', a: '購買後 7 天內可退換' },
]

// 建立向量索引
const embedResults = await Promise.all(
  qaList.map((qa) => embeddingModel.embedContent(qa.q)),
)
const index = qaList.map((qa, i) => ({ ...qa, vector: embedResults[i].embedding.values }))

function cosineSimilarity(a, b) {
  const dot = a.reduce((sum, v, i) => sum + v * b[i], 0)
  const mag = (v) => Math.sqrt(v.reduce((s, x) => s + x * x, 0))
  return dot / (mag(a) * mag(b))
}

// 查詢
const userQuery = '你們何時開門？'
const queryResult = await embeddingModel.embedContent(userQuery)
const queryVector = queryResult.embedding.values

const best = index.reduce(
  (top, qa) => {
    const score = cosineSimilarity(queryVector, qa.vector)
    return score > top.score ? { score, qa } : top
  },
  { score: -1, qa: null },
)

console.log(best.score > 0.7 ? best.qa.a : '抱歉，找不到相關答案')
// 輸出：週一至週五 9:00–18:00
```

## RAG（檢索增強生成）

RAG（Retrieval-Augmented Generation）結合「資訊檢索」與「文字生成」，先從知識庫中檢索相關文件，再將檢索結果作為上下文提供給 LLM 生成回覆。

```text
文件切割 → 向量嵌入 → 檢索 → 增強生成
```

1. **文件切割（Chunking）**：將原始文件拆分成適當大小的片段
2. **向量嵌入（Embedding）**：使用 Embedding 模型將文字片段轉換為向量，存入向量資料庫
3. **檢索（Retrieval）**：根據使用者問題，從向量資料庫中找出最相關的文件片段
4. **增強生成（Augmented Generation）**：將檢索到的片段與使用者問題一起送入 LLM，生成回覆

```javascript
import { GoogleGenerativeAI } from '@google/generative-ai'

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY)
const embeddingModel = genAI.getGenerativeModel({ model: 'text-embedding-004' })

const documents = [
  '本公司營業時間為週一至週五 9:00 至 18:00，週六日休息。',
  '退貨政策：商品購買後 7 天內，未拆封可申請全額退款。',
  '客服信箱：support@example.com，回覆時間為 1–2 個工作天。',
]

// 建立向量索引
const embedResults = await Promise.all(documents.map((doc) => embeddingModel.embedContent(doc)))
const index = documents.map((doc, i) => ({ doc, vector: embedResults[i].embedding.values }))

function cosineSimilarity(a, b) {
  const dot = a.reduce((sum, v, i) => sum + v * b[i], 0)
  const mag = (v) => Math.sqrt(v.reduce((s, x) => s + x * x, 0))
  return dot / (mag(a) * mag(b))
}

async function rag(query) {
  // 檢索相關文件
  const queryResult = await embeddingModel.embedContent(query)
  const queryVector = queryResult.embedding.values

  const context = index
    .map((item) => ({ ...item, score: cosineSimilarity(queryVector, item.vector) }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 2)
    .map((item) => item.doc)
    .join('\n')

  // 生成回覆
  const chatModel = genAI.getGenerativeModel({
    model: 'gemini-2.0-flash',
    systemInstruction: `根據以下資料回答問題，找不到相關資訊時回覆「抱歉，無法回答」。\n\n${context}`,
  })
  const result = await chatModel.generateContent(query)
  return result.response.text()
}

console.log(await rag('你們什麼時候上班？'))
```

### 與純 LLM 回覆的差異

| 比較項目 | 純 LLM 回覆 | RAG 回覆 |
| -------- | --------------- | --------------- |
| 知識來源 | 模型訓練資料 | 即時檢索的外部文件 |
| 時效性 | 受限於訓練截止日期 | 可隨時更新知識庫 |
| 幻覺風險 | 較高，可能編造答案 | 較低，基於實際文件回覆 |
| 可追溯性 | 無法追溯來源 | 可標示引用來源 |
| 領域適用 | 通用知識 | 可針對特定領域客製化 |

### 文件切割策略

文件切割是 RAG 品質的關鍵。常見的切割參數：

- **Chunk Size**：每個片段的大小，通常 200–1000 tokens
- **Overlap**：相鄰片段的重疊區域，通常為 chunk size 的 10%–20%

切割策略的選擇建議：

- **固定大小切割**：簡單直接，適合結構統一的文件
- **遞迴字元切割**：按分隔符號層級切割，保留語意完整性
- **語意切割**：根據語意相似度分段，品質最好但計算成本較高

### 向量資料庫選型

| 資料庫 | 特點 | 適用場景 |
| -------- | -------------------- | ---------------------- |
| Chroma | 輕量、易上手、支援本地部署 | 開發測試、小型專案 |
| Pinecone | 全託管、高效能、自動擴展 | 生產環境、大規模應用 |
| Qdrant | 開源、支援過濾、豐富的 API | 需要進階過濾的場景 |
| Weaviate | 開源、支援混合搜尋 | 需要關鍵字 + 語意混合搜尋 |
| pgvector | PostgreSQL 擴充、無需額外基礎設施 | 已使用 PostgreSQL 的專案 |

### 檢索策略

- **相似度搜尋**：最基礎的檢索方式，透過計算查詢向量與文件向量的餘弦相似度來排序結果
- **混合搜尋（Hybrid Search）**：結合關鍵字搜尋（BM25）與語意搜尋（向量），兩者互補提升檢索準確度。BM25 是基於詞頻與文件長度的經典排序演算法，擅長精確匹配；語意搜尋則擅長理解同義詞與上下文

### 提示詞設計

好的 system prompt 能有效引導 LLM 根據檢索結果回覆，避免幻覺。設計重點：

- 明確指示 LLM **僅根據提供的參考資料回答**
- 找不到相關資訊時，要求 LLM **誠實告知**而非編造
- 要求回答時**標示引用來源**，方便使用者查閱原始文件

### 回退策略

當檢索不到足夠相關的文件時，應有明確的處理邏輯：

- 設定相似度**門檻值（threshold）**，過濾掉低相關性的結果
- 當沒有文件通過門檻時，回傳預設的「無法回答」訊息，而非讓 LLM 自行發揮
- 建議使用者嘗試不同關鍵字，或引導至人工客服

### 多輪對話

在多輪對話中，需要維護歷史訊息以保持對話連貫性。常見做法：

- **視窗記憶體（Window Memory）**：保留最近 N 輪對話作為上下文，避免歷史訊息無限增長導致 token 超出限制
- **查詢改寫（Query Rewriting）**：將使用者的後續問題結合對話歷史改寫成完整的獨立問題，再用於檢索。例如使用者先問「RAG 是什麼？」再問「它的缺點呢？」，改寫後變成「RAG 的缺點是什麼？」，提升檢索準確度

## Fine-tuning

把 QA 資料微調進模型，推論時不需要額外塞 context。

```text
QA 資料 → 訓練資料集 → 微調模型 → 使用者問題 → 回覆
```

- **優點**：推論時 input tokens 最少、回覆風格一致
- **缺點**：訓練成本高、更新 QA 要重新訓練、幻覺難控制
- **適合**：QA 穩定不常變動、需要統一語氣風格的場景

訓練資料通常為 JSONL 格式，每筆包含 prompt（問題）與 completion（答案）。當 QA 內容更新時，需要重新準備資料集並重新訓練，因此不適合頻繁變動的知識庫。

```javascript
import { GoogleGenerativeAI } from '@google/generative-ai'

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY)

// 使用 fine-tuned 模型推論，用法與一般模型相同
const model = genAI.getGenerativeModel({
  model: 'tunedModels/your-model-id', // 替換為你的 fine-tuned 模型 ID
})

const result = await model.generateContent('你們幾點開始營業？')
console.log(result.response.text())
```

## 參考資源

- [LangChain.js 官方文件](https://js.langchain.com/docs/introduction/)
- [LlamaIndex.TS 官方文件](https://ts.llamaindex.ai/)
- [Gemini Embeddings API](https://ai.google.dev/gemini-api/docs/embeddings)
- [Chroma 官方文件](https://docs.trychroma.com/)
- [RAG 論文 - Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
