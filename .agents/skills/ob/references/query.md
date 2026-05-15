# Vault 查詢流程

執行使用者 Obsidian vault 的唯讀搜尋任務：先解析本機 vault 根目錄，再從其中的 `content/` 找出與問題最相關的筆記，以結構化 JSON 回傳。

## 唯讀工具契約（強制）

此流程**禁止任何寫入**。違反即停止輸出，回報「query 流程不得寫入」。

- **允許工具**：`Read` / `Glob` / `Grep`
- **允許 Bash 命令**（僅唯讀）：`pwd`、`test`、`ls`、`find`、`rg`、`cat`、`Get-Content`、`realpath`、`git status`、`git diff --stat`
- **禁止工具**：`Write` / `Edit` / `NotebookEdit`
- **禁止 Bash 命令**：`mkdir`、`mv`、`cp`、`Move-Item`、`Copy-Item`、`Set-Content`、`Add-Content`、`Out-File`、`Remove-Item`、`rm`、`sed -i`、`tee`、shell redirect（`>`、`>>`）、任何 `npm run` 含 `:fix` / `:write` / `:build` 的 script（特別是 `npm run vault:fix`）、`obsidian create` / `obsidian append` / `obsidian property:set` 等任何寫入子命令
- **無法確認某命令是否唯讀**：停止並回報「無法確認 `<命令>` 唯讀，已中止」

其他絕對規則：

- **輸出必為 JSON**：不加解釋、不加 markdown wrapper，純 JSON 物件
- **不再呼叫其他 subagent**（避免遞迴）
- **不做 WebSearch**：只負責 vault；web 由主 agent 並行處理
- **path 一律正規化**：詳見下方「輸出格式」段的 `path` 規則

## Vault 路徑解析（必先執行）

```
VAULT_ROOT = $OBSIDIAN_VAULT_ROOT
```

`$OBSIDIAN_VAULT_ROOT` 必須指向 repo 的 `content/` 目錄（也就是底下直接有 `master-index.md`、`Cards/`、`Topics/`）。env 未設或該路徑底下找不到 `master-index.md`，直接輸出未命中 JSON：`hits` 為空，`miss_reason` 寫「`$OBSIDIAN_VAULT_ROOT` 未設或無效，設定方式見 README」。

## Vault 佈局

- 入口：`<VAULT_ROOT>/master-index.md` — 資料夾索引與 Tag 查詢指南都在裡面，**實際資料夾清單與 tag 字典以 master-index 為準**，下列只是粗結構
- 資料夾粗結構：
  - `Cards/` — 未歸屬的完整概念 Cards（工作區）
  - `Topics/<主題>/` — 已歸檔主題，第一層子目錄一個主題一個
  - `Inbox/YouTube/<頻道>/` — 影片摘要，每個頻道一個子目錄
  - `Inbox/Clippings/` — 網頁剪貼
- **搜尋時排除**：`.obsidian/`

## 三層搜尋策略

### L1：讀 master-index（必先執行）

1. Read `<VAULT_ROOT>/master-index.md`
2. 對照「資料夾索引」描述與「Tag 查詢指南」表格，抽出 **候選資料夾** 與 **候選 tag 清單**
3. 若 master-index 描述直接指出精確檔案（如頻道名稱、主題筆記名），可跳到 L3 直接 Read 該檔

### L2：Tag 與路徑篩選

- 對 `<VAULT_ROOT>` 下的候選資料夾 Glob 列出 `.md` 檔
- 對檔案集合**並行兩種篩選**，結果**聯集**進 L3：
  - Grep frontmatter tags（例：`^\s*-\s+(claude-code|rag|memory)$`）
  - Grep frontmatter title（例：`^title:.*\b(Discord|webhook)\b`，關鍵字含中英變形）
  - title 是高密度信號——能救「tag 沒打對但 title 含關鍵字」的筆記
- 排除匹配：`.obsidian/`

### L3：正文 Grep 與驗證

1. 對 L2 篩出的檔案 Grep 關鍵字正文（取 `-C 2` 看上下文）
2. **L2 空集合 fallback**：若 L2 兩種篩選聯集後仍為 0 筆，L3 改對 `<VAULT_ROOT>/Cards/**/*.md` + `<VAULT_ROOT>/Topics/**/*.md` 全範圍 Grep（**排除 `Inbox/YouTube/`、`Inbox/Clippings/` 避免雜訊**）
3. 對 Grep 命中的檔案 Read 首 50 行，判斷是否真正回答問題（不只字面出現）
4. 挑最相關 1~5 筆組成 `hits`

## 關鍵字抽取

- 中文問題：抽名詞與技術術語
  - 例「Claude Code 的 dream 是什麼」→ `dream`、`Claude Code`、`記憶`
- 英文問題：直接用英文術語 + 可能的中文翻譯
  - 例「RAG seven levels」→ `RAG`、`七層次`、`七個層次`、`seven levels`
- vault 中英混用，必要時中英互譯搜

## 效能守則

- Read 檔案數 ≤ 15（候選太多靠 frontmatter `title` 篩）
- Grep 指定 `<VAULT_ROOT>/**/*.md` 或候選資料夾以加速
- 不要對 `Inbox/YouTube/` 影片摘要做全域正文 Grep；先靠 L1 縮範圍

## 輸出格式

**命中**：

```json
{
  "query": "<使用者原始問題>",
  "hits": [
    {
      "path": "content/Inbox/YouTube/Chase-H-AI/Claude-Code-RAG七層次.md",
      "title": "Claude Code 與 RAG 的七個層次",
      "summary": "將 Claude Code 記憶架構分為 7 層，從 AutoMemory 到 Agentic RAG",
      "relevance": "high"
    }
  ],
  "miss_reason": null
}
```

**未命中**：

```json
{
  "query": "<使用者原始問題>",
  "hits": [],
  "miss_reason": "已檢查：Topics/Claude-Code/、Inbox/YouTube/Chase-H-AI/；嘗試關鍵字：dream, 記憶；皆無相關內容"
}
```

`relevance` 三值：

- `high` — 筆記主題直接對應問題
- `medium` — 筆記主題相關但非焦點
- `low` — 僅字面提到、需配合其他筆記才能答題

`path` 規則：

- 一律回 `content/...`，不要回 `<VAULT_ROOT>` 絕對路徑
- 因 `$OBSIDIAN_VAULT_ROOT` 指向 `content/`，輸出時需把 `<VAULT_ROOT>` 下的相對路徑前綴補成 `content/`；例如 `<VAULT_ROOT>/Cards/foo.md` → `content/Cards/foo.md`
- 例如實際檔案是 `~/code/obsidian-memory/content/Cards/foo.md`，輸出仍要寫成 `content/Cards/foo.md`
- **一律使用 forward slash（`/`）**，不論作業系統。Windows Glob 回 `content\Cards\foo.md` 時，輸出前需 replace `\` 為 `/`

## 與其他流程的分工

- **此流程（query）**：純讀、回 JSON。呼叫來源有三：
  1. `/ob <查詢關鍵字>` skill 直接分派
  2. 主 agent 自動並行協議（與 WebSearch 一起跑）
  3. 其他流程需要唯讀搜尋時
- **write 流程**：寫入專用（建檔、append、改 frontmatter），不再處理查詢
- 若查詢後使用者想建筆記，由 orchestrator 再呼叫 write 流程，本流程不跨界
