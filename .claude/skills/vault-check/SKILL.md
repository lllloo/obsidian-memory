---
name: vault-check
description: 對 Obsidian vault 的 content/ 執行稽核與自動修正，分兩段：硬規則由 scripts/vault-check.mjs 自動修（檔名、frontmatter 結構、日期 normalize、敏感資料 high-precision regex）；語意層由 vault-auditor subagent 給建議（wikilink 斷鏈、自然語言敏感資料、tag 一致性、缺欄位）。觸發詞：「vault check」、「/vault-check」、「稽核 vault」、「檢查 vault」、「跑 vault-check」、「vault 健檢」。不應觸發：單篇筆記建檔/查詢（用 /ob）、跨筆記主題整合（用 vault-topic-moc）、批次同步（用 vault-youtube-sync / vault-reddit-sync）。
---

# /vault-check — Vault 稽核與自動修正

對 `content/` 執行 vault 稽核與自動修正，分兩段：硬規則由 `scripts/vault-check.mjs` 自動修；語意層由 `vault-auditor` subagent 給建議。

## 執行流程

### 1. 前置檢查

執行 `git status --porcelain`。若有任何涉及 `content/` 的變更（含 untracked），**直接中止**並印出：

```
偵測到 content/ 變更，已中止以避免 diff 混雜：
<git status --porcelain 內 content/ 相關行>

請先 commit 或 stash 後再跑 /vault-check。
```

工作區乾淨（無 `content/` 變更）才進入下一步。

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

**額外硬掃（script 已做，不自動修，命中 → exit non-zero）：**
- 敏感資料 high-precision regex（Anthropic / OpenAI / GitHub / Google / AWS / Slack token、private key header、JWT），作為 CI 最後一道防線；語意層敏感資料仍由 subagent 接手

**不在 script 處理範圍**（會由下一步 subagent 接手）：
- frontmatter parse error、缺 `title` / `created` / `tags`、其他 INVALID_VALUE
- wikilink 斷鏈
- 敏感資料語意層（自然語言密碼、個資、內部資訊）
- tag 一致性

### 3. 語意層稽核（Subagent）

呼叫 `vault-auditor` subagent，請它對 `content/` 執行語意稽核並回 JSON。subagent 唯讀，只 flag 不改檔。

### 4. 收尾

**不自動 commit**。所有變更（含 step 2 的自動修）留在工作目錄未 commit，交用戶審核。

印出總結：

```
## Vault Check 完成（變更未 commit，請審核）

### 硬規則自動修（script）
<script 輸出的「已修正」摘要>
<script 輸出的「修正被阻擋」清單，若有>

### 語意層建議（vault-auditor，需手動處理）

#### Schema 問題
<schema_issues：缺 title / created / tags、parse error，含 LLM 建議值>

#### Wikilink 斷鏈
<broken_wikilinks：含 LLM 推測的目標>

#### 敏感資料
<sensitive_data：含嚴重度與位置>

#### Tag 一致性
<tag_conflicts：含建議標準化值>

### 變更摘要
<git status --short content/>
<git diff --stat content/>

### 下一步
- 審核 diff：`git diff content/`
- 處理語意層建議（subagent 不會自動改檔，需自行決定）
- 滿意後自行 commit（建議訊息：`vault-check: 自動修正 frontmatter`）
- 若前置做了 auto-stash：審核完畢後記得 `git stash pop`
```

若某類別無建議，該段落可省略。

## 規則

- 只能修 `content/` 底下（script 已限制範圍）
- 不 push、不 merge（除非用戶明確要求）
- 全程繁體中文、禁用 `$()`
- **硬規則變更請改 `scripts/vault-schema.mjs` 的 Zod schema**，不要在此 skill 或別處另寫
- **語意規則變更請改 `.claude/agents/vault-auditor.md`**，不要塞進 script
- subagent 給的所有建議都「只 flag 不改檔」，最終是否套用由用戶決定
