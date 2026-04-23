對 `content/` 執行 vault 稽核與自動修正。跑 `scripts/vault-check.mjs` 用 Zod schema 驗證 frontmatter 與檔名，對可自動修項目直接修正，最後讓用戶審核。

$ARGUMENTS

## 執行流程

### 1. 前置檢查

執行 `git status --porcelain`。若有任何涉及 `content/` 的變更（含 untracked），**直接中止**並印出：

```
偵測到 content/ 變更，已中止以避免 diff 混雜：
<git status --porcelain 內 content/ 相關行>

請先 commit 或 stash 後再跑 /vault-check。
```

工作區乾淨（無 `content/` 變更）才進入下一步。

### 2. 稽核與修正

執行：

```bash
npm run vault:fix
```

等同 `node scripts/vault-check.mjs --fix`。script 會：

- 掃描 `content/**/*.md`（排除 `.obsidian/`、`CLAUDE.md`、`index.md`、`master-index.md`）
- 用 Zod schema 驗證 frontmatter（欄位、順序、必填、白名單、空值）
- 檢查檔名空格
- 掃 wikilink 斷鏈（正文與 `parent`）與敏感資料（API key / token / private key，code fence 內忽略）
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
- `BROKEN_WIKILINK`（wikilink 斷鏈）、`SENSITIVE_DATA`（敏感資料）**會偵測但不會自動修**，命中時印在「無法自動修」區塊需手動處理
- `MISPLACED_NOTE`（新筆記位置錯誤）**尚未實作**
