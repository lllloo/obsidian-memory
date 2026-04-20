對 `content/` 執行 vault 稽核與自動修正迴圈。依 `content/CLAUDE.md` 規則掃描違規、內容錯誤，並在獨立 git branch 上自動修正，最後讓用戶審核。

$ARGUMENTS

## 執行流程

請嚴格依以下步驟執行：

### 1. 前置檢查

**a. 工作區變更檢查**

執行 `git status --porcelain` 並分類：

- `^ M` / `^M ` / `^MM` / `^A ` / `^AM` / `^D ` → **已追蹤變更**（modified/staged/deleted）
- `^\?\?` → **未追蹤**（untracked）

依分類決策：

1. **全空** → 直接往下
2. **只有 untracked，且 untracked 不涉及 `content/`**（例：`.DS_Store`、repo 根的暫存檔）→ 列出後提示「將忽略以下 untracked 繼續」並往下
3. **有已追蹤變更，或 untracked 涉及 `content/`** → 列出完整變更清單後詢問用戶：

```
偵測到工作區變更：
<列出 git status --porcelain 的輸出>

這會影響 /vault-check 的 diff 可讀性。要如何處理？
  1. 自動 git stash（含 untracked），完成後 pop 回來
  2. 繼續（變更會跟稽核修正混在一起，不建議）
  3. 中止（自行處理後再重跑）
```

- 選 **1** → `git stash push -u -m "vault-check auto-stash <timestamp>"`，並記住結束時要 `git stash pop`
- 選 **2** → 繼續（警告 user diff 會混雜）
- 選 **3** → 中止

**b. 分支確認**

執行 `git branch --show-current` 確認目前在 main（或用戶的主分支）。若不在，警告但繼續。

**c. 建立 branch**

分兩步取得時間戳（遵守禁用 `$()` 的規則）：
1. Bash 執行 `date +%y%m%d-%H%M` 取得字面值，例如 `260408-1530`
2. 用該值組出 branch 名稱 `vault-check/260408-1530`

建立並切換到該 branch：`git checkout -b vault-check/<timestamp>`

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

- 可自動修：`code` 為 R1, R2, R3, R4, A, B, D, E, F
- 僅報告：`code` 為 R5, R6, R7, C, G, H，或 `fix_hint == "REPORT_ONLY"`

> C（跨筆記矛盾）、G（TODO/未完成）、H（重複筆記）皆需用戶判斷取捨，不交給 fixer 自動處理，避免誤改。

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

### 3. 收尾

若前置檢查選了「1. 自動 stash」：
- 執行 `git stash pop`
- 若 pop 出現 conflict（vault-check 修正的檔案與 stash 的變更重疊）→ **不要自動解決**，保留 conflict 狀態並告知用戶手動處理，附上 `git stash list` 輸出

### 4. 結果輸出

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
