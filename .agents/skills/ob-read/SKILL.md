---
name: ob-read
description: 在 obsidian-memory vault 查詢既有筆記：找筆記、搜尋、查一下 vault 有沒有記過某主題、vault 裡關於 X 的筆記、之前記過什麼、查我的筆記。唯讀三層搜尋（vault-map → tag/路徑 → 正文 grep），回結構化命中清單。需要橫跨多篇、靠 tag/正文比對才找得到的實質查詢時用本 skill，不要自己零散 grep。寫入／建立／記一下新內容請改用 ob-write；查詢不寫入。僅當 cwd 為 vault root（有 vault-map.md）時可用。
---

# /ob-read — Obsidian Vault 查詢

唯讀搜尋 vault，找出與問題最相關的筆記。建立筆記請改用 `/ob-write`。

## 呼叫前置條件

cwd 必須是 vault root：

```bash
[ -f "vault-map.md" ] || { echo "ERROR: cwd 不在 vault root，請 cd 到 obsidian-memory 後再呼叫 /ob-read"; exit 1; }
```

check 失敗就告知用戶並停止，不要硬猜路徑。

## 執行

呼叫 Agent tool：

- `subagent_type`: `"general-purpose"`
- `prompt`: `references/query.md` 全文 + `\n\n## 本次查詢\n` + 使用者原始問題

拿到 JSON 後依下方「查詢命中呈現格式」呈現。

## 無 subagent 環境的 fallback

無 Agent 工具的環境（Cursor / Codex / Gemini CLI 等）由主 agent 直接 Read `references/query.md` 跑同一流程，query 流程的「唯讀工具契約」照常生效。

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

查完想回存成筆記 → 用 `/ob-write`。
