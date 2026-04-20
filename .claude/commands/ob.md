依使用者需求判斷模式後分派：

- **建檔**（「建立筆記」、「新增」、「記一下」、「寫一篇」、「筆記關於…」）
  → Agent tool，`subagent_type: obsidian`，傳入原始需求
- **查詢**（「找」、「搜尋」、「有沒有」、「查」）
  → Agent tool，`subagent_type: vault-query`，傳入原始問題；拿到 JSON 後依下方格式呈現

模式不明確時，向使用者確認。不做 WebSearch（全域協議會在其他場景自動並行）。

$ARGUMENTS

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
