---
name: ob
description: Obsidian vault 操作入口：依使用者需求分派建檔或查詢。建檔涵蓋「建立筆記」、「新增」、「記一下」、「寫一篇」、「筆記關於…」、「日記」、「daily 日記」；查詢涵蓋「找筆記」、「搜尋筆記」、「有沒有」、「查」。使用時機：使用者提及 vault / Obsidian / 筆記 / 日記操作，或關鍵字「ob」、「/ob」時，務必透過本 skill 分派而非直接動檔。
---

# /ob — Obsidian Vault 操作入口

依使用者需求判斷模式後分派到 build / query 流程。

## 分派

### 建檔（「建立筆記」、「新增」、「記一下」、「寫一篇」、「筆記關於…」、「日記」、「daily 日記」）

呼叫 Agent tool：

- `subagent_type`: `"general-purpose"`
- `prompt`: `references/write.md` 全文 + `\n\n## 本次需求\n` + 使用者原始輸入

subagent 完成後直接回報結果（建檔路徑、是否走 fallback 等）。

### 查詢（「找筆記」、「搜尋筆記」、「有沒有」、「查」）

呼叫 Agent tool：

- `subagent_type`: `"general-purpose"`
- `prompt`: `references/query.md` 全文 + `\n\n## 本次查詢\n` + 使用者原始問題

拿到 JSON 後依下方「查詢命中呈現格式」呈現。

### 模式不明確

向使用者確認。

## 無 subagent 環境的 fallback

無 Agent 工具的環境（Cursor / Codex / Gemini CLI 等）由主 agent 直接 Read 對應 `references/*.md` 跑同一流程，query 流程的「唯讀工具契約」照常生效。

## 查詢命中呈現格式

**命中：**

```
Vault 命中 N 筆：

1. [[<title>]] — <path>
   <summary>
```

（relevance 標註：`★` high、`·` medium、`-` low，列於 summary 前）

**未命中：**

```
Vault 無相關筆記。
原因：<miss_reason>
```
