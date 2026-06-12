---
name: ob-read
disable-model-invocation: true
description: 在 obsidian-memory vault 查詢既有筆記：找筆記、搜尋、查一下 vault 有沒有記過某主題、vault 裡關於 X 的筆記、之前記過什麼、查我的筆記。唯讀三層搜尋（vault-map → tag/路徑 → 正文 grep），回結構化命中清單。需要橫跨多篇、靠 tag/正文比對才找得到的實質查詢時用本 skill，不要自己零散 grep。寫入／建立／記一下新內容請改用 ob-write；查詢不寫入。任何專案可呼叫，skill 內部判 cwd 決定查詢模式（本地直接搜／跨專案經 obsidian CLI 定位 vault 後唯讀搜尋）。
---

# /ob-read — Obsidian Vault 查詢

唯讀搜尋 vault，找出與問題最相關的筆記。建立筆記請改用 `/ob-write`。

## 模式判斷（必先執行）

查詢分兩種模式，先判 cwd——用 `Read vault-map.md` 確認存在（harness-native，不經 shell、不分 PowerShell/bash）：讀得到 → `MODE=local`；讀不到 → `MODE=cross`。

- `MODE=local`：cwd 已是 vault root → 路徑 cwd-relative，直接搜。
- `MODE=cross`：cwd 在其他專案 → 經 obsidian CLI 定位 vault root 並硬 gate 身分；CLI 不可用或身分不符即回未命中、不降級亂搜（細節在 `query.md`）。

## 執行

呼叫 Agent tool：

- `subagent_type`: `"general-purpose"`
- `prompt`: `references/query.md` 全文 + `\n\n## 本次模式\nMODE=<local|cross>\n\n## 本次查詢\n` + 使用者原始問題

拿到 JSON 後依下方「查詢命中呈現格式」呈現。

## 無 subagent 環境的 fallback

無 Agent 工具的環境（Cursor / Codex / Gemini CLI 等）由主 agent 直接 Read `references/query.md`，依上面判得的模式跑同一流程，query 流程的「唯讀工具契約」照常生效。

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
