對 `content/` 執行 vault 稽核與自動修正迴圈。依 `content/CLAUDE.md` 規則掃描違規、內容錯誤，並在獨立 git branch 上自動修正，最後讓用戶審核。

$ARGUMENTS

## 執行流程

請嚴格依以下步驟執行：

### 1. 前置檢查

- 執行 `git status --porcelain`，若輸出非空 → 中止並告知用戶：「工作區有未 commit 變更，請先 commit 或 stash 再執行 /vault-check」
- 執行 `git branch --show-current` 確認目前在 main（或用戶的主分支）。若不在，警告但繼續
- 分兩步取得時間戳（遵守禁用 `$()` 的規則）：
  1. Bash 執行 `date +%y%m%d-%H%M` 取得字面值，例如 `260408-1530`
  2. 用該值組出 branch 名稱 `vault-check/260408-1530`
- 建立並切換到該 branch：`git checkout -b vault-check/<timestamp>`

### 2. 迴圈（最多 3 輪）

設定 `round = 1`，最大 3 輪。每輪執行：

**a. 呼叫 vault-evaluator**

用 Agent tool：
```
subagent_type: vault-evaluator
description: "Vault 稽核第 N 輪"
prompt: "掃描 content/ 下所有 .md 檔案，依 agent 定義的規則與類別找出違規，輸出 JSON。"
```

解析回傳的 JSON。若 `total_issues == 0` → 跳出迴圈。

**b. 分類 issues**

- 可自動修：`code` 為 R1, R2, R3, R4, A, B, C, D, E, F, G
- 僅報告：`code` 為 R5, R6, R7, H，或 `fix_hint == "REPORT_ONLY"`

將「僅報告」項目暫存到 orchestrator 記憶（最後要印出）。

**c. 若無可自動修項目** → 跳出迴圈

**d. 呼叫 vault-fixer**

用 Agent tool：
```
subagent_type: vault-fixer
description: "Vault 修正第 N 輪"
prompt: "依 agent 定義處理以下 issues 清單並輸出修正報告 JSON：<貼入可自動修的 JSON 陣列>"
```

**e. Commit 本輪修正**

- 執行 `git status --porcelain content/` 確認有變更
- 若無變更 → 跳出迴圈（fixer 全部失敗或跳過）
- 若有變更：
  - `git add content/`
  - Commit message 範本（類別列表從 fixer 回報的 `categories_touched` 取得）：
    ```
    vault-check: 第 N 輪修正

    類別：R1, R3, A, B
    應用：12 項 / 跳過：3 項 / 失敗：0 項
    ```
  - 用 HEREDOC 傳入 commit message

**f. `round += 1`**，回到 a

### 3. 結果輸出

迴圈結束後，印出總結給用戶：

```
## Vault Check 完成

Branch: vault-check/<timestamp>
共 N 輪，修正 X 個檔案

### 修正統計
- R1 檔名空格：2
- R3 缺 frontmatter：1
- A 錯字：5
- B Markdown 語法：3
（依實際統計）

### 變更摘要
<git diff main...HEAD --stat 的輸出>

### 僅報告項目（需手動處理）
- [R6] content/Cards/API-test.md:8 — 疑似 API key，請手動檢查
- [H] content/Cards/xxx.md ↔ content/Cards/yyy.md — 疑似重複，建議合併
（依實際情況列出所有 REPORT_ONLY）

### 下一步
查看完整 diff：
  git diff main...HEAD

接受修正：
  git checkout main && git merge vault-check/<timestamp>

丟棄修正：
  git checkout main && git branch -D vault-check/<timestamp>
```

## 規則

- 只能在 `content/` 底下修改檔案
- 絕對不執行 `git push`
- 絕對不自動 merge 回 main
- 絕對不執行 `git branch -D` 除非用戶明確要求
- 全程遵守全域規則：繁體中文、禁用 `$()`、不主動打包
