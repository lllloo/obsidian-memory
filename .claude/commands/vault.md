使用 Agent tool 委派給 `vault-query` agent 查詢使用者 Obsidian vault（**只查 vault，不做 WebSearch**）。

查詢主題：

$ARGUMENTS

## 執行步驟

1. 呼叫 Agent tool：
   - subagent_type: `vault-query`
   - prompt: `$ARGUMENTS`
2. 接收回傳的 JSON
3. 依以下格式輸出給使用者

## 輸出格式

### 命中

```
Vault 命中 N 筆：

1. [[<title>]] — <path>
   <summary>

2. [[<title>]] — <path>
   <summary>
```

（relevance 標註：`★` high、`·` medium、`-` low，列於 summary 前）

### 未命中

```
Vault 無相關筆記。
原因：<miss_reason>

若此主題有長期價值，可用 /ob 建立筆記。
```

## 注意

- `path` 為 repo-relative 路徑，固定以 `content/` 開頭
- 本指令**不觸發 WebSearch**（與全域 Search-First 協議不同）
- 若使用者想同時查 web，請直接問問題讓全域協議處理
