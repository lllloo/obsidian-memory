---
name: vault-check
description: 對 Obsidian vault 的 content/ 執行稽核與自動修正，分兩段：硬規則由 scripts/vault-check.mjs 自動修（檔名、frontmatter 結構、日期 normalize、敏感資料 high-precision regex）；語意層由 audit references 經 general-purpose subagent 給建議（wikilink 斷鏈、自然語言敏感資料、tag 一致性、缺欄位）。使用時機：使用者要求「稽核 vault」、「檢查 vault」、「跑 vault-check」、「vault 健檢」、「找壞 wikilink」、「修 frontmatter」，或直接呼叫 /vault-check。
---

# /vault-check — Vault 稽核與自動修正

orchestrator：串接 deterministic script（自動修）與語意層 subagent（給建議），把結果合併成一份報告交用戶審核。分兩段是因為兩種問題的可信度不同——格式錯誤可機械判定，語意問題（斷鏈、tag drift、自然語言敏感資料）需要讀內容才能評估。

## 執行流程

### 1. 前置檢查

依序檢查兩件事，任一失敗即中止：

**a. cwd 必須為 repo root**：`test -f content/master-index.md` 失敗即印出「cwd 不在 repo root，請於 repo 根目錄執行 `/vault-check`」並停。語意層 subagent 也會檢查同一條件，但在 orchestrator 早停可避免浪費 subagent context。

**b. 工作區 `content/` 必須乾淨**：執行 `git status --porcelain`，若有任何涉及 `content/` 的變更（含 untracked），印出受影響檔案並停，建議用戶先 commit 或 stash。這是為了讓自動修的 diff 不被既有 in-progress 變更混淆。

### 2. 硬規則自動修（Script）

執行：

```bash
npm run vault:fix
```

等同 `node scripts/vault-check.mjs --fix`。script 處理範圍：

- 檔名空格 → rename
- frontmatter 欄位順序 → 重排
- 白名單外欄位 → 刪
- 選填空值 → 刪
- `updated` 缺失 → 補今日
- 日期格式可推斷 → normalize 為 `YYYY-MM-DD`

**額外硬掃（script 已做，不自動修，命中 → exit code 1）：**

- 敏感資料 high-precision regex（Anthropic / OpenAI / GitHub / Google / AWS / Slack token、private key header、JWT），作為 CI 最後一道防線；語意層敏感資料仍由下一步接手

script exit non-zero **不中止本流程**——硬掃結果與語意層建議都要進最終報告，用戶才能一次看到全貌。讀完 script 輸出後直接進 step 3。

**不在 script 處理範圍**（會由下一步 subagent 接手）：

- frontmatter parse error、缺 `title` / `created` / `tags`、其他 INVALID_VALUE
- wikilink 斷鏈
- 敏感資料語意層（自然語言密碼、個資、內部資訊）
- tag 一致性

### 3. 語意層稽核（subagent）

呼叫 Agent tool：`subagent_type: "general-purpose"`，prompt 為 `references/audit.md` 全文。subagent 唯讀，依 references 的「唯讀工具契約」執行，回 JSON。

無 Agent 工具的環境（Cursor / Codex / Gemini CLI 等）由主 agent 直接 Read `references/audit.md` 跑同一流程，唯讀工具契約照常生效。

### 4. 收尾

**不自動 commit**。所有變更（含 step 2 的自動修）留在工作目錄未 commit，交用戶審核。

印出總結，固定三段：

1. **硬規則自動修（script）**：直接貼 `npm run vault:fix` 輸出的「已修正」摘要與「修正被阻擋」清單
2. **語意層建議（audit JSON）**：依 audit JSON 的非空 key 逐項成段，每段用該 key 的中文名稱（schema_issues / broken_wikilinks / sensitive_data / tag_conflicts → Schema 問題 / Wikilink 斷鏈 / 敏感資料 / Tag 一致性）。空 key 整段省略，不要留空標題。欄位格式以 `references/audit.md` 的 JSON schema 為準
3. **變更摘要與下一步**：`git status --short content/` + `git diff --stat content/`，提示用戶審核 diff、處理語意層建議、滿意後自行 commit

## 規則

- 硬規則變更改 `scripts/vault-schema.mjs` 的 Zod schema，不要在此 skill 或別處另寫
- 語意規則變更改 `.agents/skills/vault-check/references/audit.md`，不要塞進 script
- subagent 給的所有建議都「只 flag 不改檔」，最終是否套用由用戶決定
