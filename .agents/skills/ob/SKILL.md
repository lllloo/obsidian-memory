---
name: ob
description: Obsidian vault 操作入口：用於使用者明確要求操作個人 vault，例如 /ob、建立/追加/整理單篇 Obsidian 筆記、記到 vault、建立日記/daily note、找 vault 筆記、搜尋 vault 內容。依需求分派到建檔流程或查詢流程。不應觸發：一般技術問答中只是提到「筆記」或「daily」、純知識查詢（主流程會並行查 vault + web）、跨多篇筆記整合（用 vault-topic-moc）、批次 YouTube/Reddit 同步（用對應 sync skill）。
---

# /ob — Obsidian Vault 操作入口

依使用者需求判斷模式後分派。**分派採用「general-purpose subagent + references prompt」模式**，不依賴命名 agent，可在跨工具環境間移植。

## 分派

### 建檔（「建立筆記」、「新增」、「記一下」、「寫一篇」、「筆記關於…」、「日記」、「daily」）

呼叫 Agent tool：

- `subagent_type`: `"general-purpose"`
- `prompt`: `references/write.md` 全文 + `\n\n## 本次需求\n` + 使用者原始輸入

### 查詢（「找筆記」、「搜尋筆記」、「有沒有」、「查 vault」、「查筆記」）

呼叫 Agent tool：

- `subagent_type`: `"general-purpose"`
- `prompt`: `references/query.md` 全文 + `\n\n## 本次查詢\n` + 使用者原始問題

拿到 JSON 後依下方「查詢命中呈現格式」呈現。

### 模式不明確

向使用者確認。不做 WebSearch（全域協議會在其他場景自動並行）。

## 無 subagent 環境的 fallback

若執行環境沒有 Agent / subagent 能力（例如 Cursor、Codex、Gemini CLI 等），主 agent 直接 Read 對應 `references/*.md` 並依其指示執行同一流程。

- write 流程：直接執行 `references/write.md`，依當前工具與 shell 選擇 CLI 或直寫 fallback。
- query 流程：先依 `references/query.md` 產生同 schema 的 JSON 作為內部中介資料，再由主 agent 依下方「查詢命中呈現格式」回覆使用者；不要把 raw JSON 當作最終回覆。query 流程**仍必須遵守 references 內的「唯讀工具契約」**——禁止 Write/Edit、禁止寫入命令、無法確認唯讀即停止。

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
