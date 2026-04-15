---
title: Google Embedding 2 多模態 RAG 架構
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-12
source: https://www.youtube.com/watch?v=gmbW_lXXIkc
---

## 核心誤解澄清

Google Embedding 2 是首個原生多模態 embedding 模型，支援直接嵌入影片、圖片、音訊、文件。**但多數教學都弄錯了一件事：**

> 能把影片嵌入向量資料庫 ≠ 能在向量資料庫裡分析影片

直接把 Embedding 2 接上現有 RAG 系統，問影片內容的問題，得到的回應是「這裡有一段 2 分鐘的影片片段，答案在裡面」——而不是文字分析。這沒什麼用。

## RAG 基本架構說明

**向量是什麼**：文件通過 embedding 模型轉換成一串數字（如 1,526 個數字），代表這份文件在高維空間中的位置。語義相近的文件，位置也相近。

**查詢流程**：
1. 問題也被轉換成向量
2. LLM 在向量資料庫中找最近的向量
3. 取出對應的原始資料
4. 用原始資料增強 LLM 的回答

**問題所在（影片場景）**：
- 文字文件被嵌入後，LLM 取出的是可閱讀的文字 → 可以用來生成答案
- 影片被嵌入後，LLM 取出的是 MP4 檔案 → LLM 無法直接解析，只能丟回一段影片片段

## 正確的多模態 RAG 架構

解決方案：**在前端 ingestion 階段讓 Gemini 分析非文字內容，生成文字說明一併儲存**。

```
影片 → Gemini 3.1 Flash → 文字說明 + transcript
      ↓
Embedding 2 → 向量（配對：影片 + 文字說明）
      ↓
向量資料庫
```

查詢時，取出的是「影片 + 文字說明」，LLM 可用文字說明生成完整答案，同時提供影片片段作為參考。

**為何要在前端做**：只需分析一次，不是每次查詢都讓 Gemini 即時分析影片（那會太慢太貴）。

## Embedding 2 限制

- 影片：每次最多 120 秒
- 文字：最多 8,192 tokens

（大多有變通方案）

## 影片 Chunking 問題

類似文字 chunking，影片也需要切段。目前尚未有完美解法。作者採用的簡單方案：
- 每 2 分鐘切一段
- 相鄰段落有 30 秒重疊

這是從文字 chunking 移植過來的方法，不一定最優，但有效。

## 實作方式

**作者提供的 GitHub repo** 包含完整 RAG 架構，兩種啟用方式：

1. Clone repo → 用 Claude Code 指向它，說「我想重建這個架構」
2. 複製 `claude_code_blueprint.md` 的內容貼入 Claude Code，讓它自動執行

**依賴項**：
- Python（更新版本）
- FFmpeg（影片處理）
- Supabase CLI（向量資料庫，可替換為 Pinecone 等）
- Gemini API key
- Supabase project

**Supabase API keys 取得位置**：
- Project Settings → API Keys → Legacy anon role API keys → anon public
- URL：Connect → scroll down

## 效果展示

正確架構的回答：完整文字分析 + 相關影片片段 + 匹配圖片

錯誤架構（多數教學）的回答：「資訊不足，這裡有幾個 source file」

這不只是微小改善，而是能不能實際使用的根本差距。
