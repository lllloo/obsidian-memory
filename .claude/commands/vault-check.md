對 `content/` 執行 vault 稽核與自動修正。跑 `scripts/vault-check.mjs` 用 Zod schema 驗證 frontmatter 與檔名，對可自動修項目直接修正，最後讓用戶審核。

$ARGUMENTS

## 執行流程

### 1. 前置檢查

執行 `git status --porcelain`。若有任何涉及 `content/` 的變更（含 untracked），詢問用戶：

```
偵測到 content/ 變更：
<git status --porcelain 輸出>

  1. 自動 git stash（含 untracked），結束後提示手動 pop
  2. 繼續（diff 會混雜，不建議）
  3. 中止
```

選 1 → `git stash push -u -m "vault-check auto-stash"`，結束後**不自動 pop**（避免與未審核修正衝突），在總結提示用戶手動 `git stash pop`。

### 2. 稽核與修正

執行：

```bash
npm run vault:fix
```

等同 `node scripts/vault-check.mjs --fix`。script 會：

- 掃描 `content/**/*.md`（排除 `.obsidian/`、`CLAUDE.md`、`index.md`、`master-index.md`）
- 用 Zod schema 驗證 frontmatter（欄位、順序、必填、白名單、空值）
- 檢查檔名空格
- 對可自動修項目直接修正（rename、補 `updated`、重排欄位、刪白名單外欄位、刪選填空值）
- 無法自動修的印在 "無法自動修" 區塊

### 3. 收尾

**不自動 commit**。變更保留在 worktree，交用戶審核。

印出總結：

```
## Vault Check 完成（變更未 commit，請審核）

### 修正統計
<script 輸出的「已修正」摘要>

### 變更摘要
<git status --short content/>
<git diff --stat content/>

### 需手動處理
<script 輸出的「無法自動修」清單>

### 下一步
- 審核 diff：`git diff content/`
- 滿意後自行 commit（建議訊息：`vault-check: 自動修正 frontmatter`）
- 若前置做了 auto-stash：審核完畢後記得 `git stash pop`
```

## 規則

- 只能修 `content/` 底下（script 已限制範圍）
- 不 push、不 merge（除非用戶明確要求）
- 全程繁體中文、禁用 `$()`
- **規則變更請改 `scripts/vault-schema.mjs` 的 Zod schema**，不要在此 command 或別處另寫規則
- **`BROKEN_WIKILINK`（wikilink 斷鏈）、`SENSITIVE_DATA`（敏感資料）目前未實作**。若 `content/` 有此類問題，需手動處理或擴充 `scripts/vault-check.mjs`
