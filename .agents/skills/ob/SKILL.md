---
name: ob
description: Obsidian vault 筆記建立與查詢入口：依使用者需求分派到 write 或 query 流程。write 涵蓋「建立筆記」、「新增」、「記一下」、「寫一篇」、「筆記關於…」、「日記」、「daily 日記」；query 涵蓋「找筆記」、「搜尋筆記」、「有沒有」、「查」。使用時機：使用者提及 vault / Obsidian / 筆記 / 日記操作，或關鍵字「ob」、「/ob」時，務必透過本 skill 分派；非筆記建立或查詢的 vault 維護任務改用更合適的 repo-local skill 或 CLAUDE.md 規則。
---

# /ob — Obsidian Vault 筆記入口

依使用者需求判斷模式後分派到 write / query 流程；本 skill 只負責筆記建立與查詢。

## 呼叫前置條件

分派前先檢查 cwd 是 vault root：

```bash
[ -f "vault-map.md" ] || { echo "ERROR: cwd 不在 vault root，請 cd 到 obsidian-memory 後再呼叫 /ob"; exit 1; }
```

check 失敗就告知用戶並停止，不要硬猜路徑。

## 分派

### 模式判斷

| 使用者意圖 | 流程 |
|---|---|
| 建立筆記、新增、記一下、寫一篇、筆記關於、日記、daily 日記 | write |
| 找筆記、搜尋筆記、有沒有、查 | query |
| 查一下並整理成筆記、找資料後回存 | 先 query；只有使用者明確要求寫入時，再走 write |
| vault 健檢、YouTube 同步、daily updates、結構維護 | 不走 `/ob`；改用對應 repo-local skill 或 `CLAUDE.md` 規則 |

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

最多問一個真正影響方向的澄清問題，例如：「你要查現有筆記，還是建立新筆記？」

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
