---
name: vault-check
description: 對 Obsidian vault 執行語意層稽核，由 audit references 經 general-purpose subagent 給建議（wikilink 斷鏈、自然語言敏感資料、tag 一致性、缺欄位、frontmatter schema 問題）。使用時機：使用者要求「稽核 vault」、「檢查 vault」、「跑 vault-check」、「vault 健檢」、「找壞 wikilink」、「修 frontmatter」，或直接呼叫 /vault-check。
---

# /vault-check — Vault 稽核

語意層 subagent 稽核，給建議交用戶決定是否手動修正。

## 執行流程

### 1. 前置檢查

**cwd 必須為 repo root**：`test -f master-index.md` 失敗即印出「cwd 不在 vault root，請於 obsidian-memory 根目錄執行 `/vault-check`」並停。

### 2. 語意層稽核（subagent）

呼叫 Agent tool：`subagent_type: "general-purpose"`，prompt 為 `references/audit.md` 全文。subagent 唯讀，依 references 的「唯讀工具契約」執行，回 JSON。

無 Agent 工具的環境（Cursor / Codex / Gemini CLI 等）由主 agent 直接 Read `references/audit.md` 跑同一流程，唯讀工具契約照常生效。

### 3. 收尾

印出語意層建議，依 audit JSON 的非空 key 逐項成段，每段用該 key 的中文名稱（schema_issues / broken_wikilinks / sensitive_data / tag_conflicts → Schema 問題 / Wikilink 斷鏈 / 敏感資料 / Tag 一致性）。空 key 整段省略。欄位格式以 `references/audit.md` 的 JSON schema 為準。

所有建議「只 flag 不改檔」，最終是否套用由用戶決定。

## 規則

- 語意規則變更改 `.agents/skills/vault-check/references/audit.md`，不要塞進別處
- subagent 給的所有建議都「只 flag 不改檔」，最終是否套用由用戶決定
