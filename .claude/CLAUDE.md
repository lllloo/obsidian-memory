# Claude Code 全域協議

## 優質參考資料來源：Obsidian Vault

使用者維護一個 Obsidian vault 作為優質參考資料，由使用者手動管理（透過 `/ob`、`/vault-check`）。Claude Code 對此 vault 僅做查詢；若需用 shell，也只允許唯讀命令，絕不自動寫入。

- **位置**：查詢時先解析本機 vault 根目錄；常見位置是 `~/code/obsidian-memory/content/`
- **入口**：`content/master-index.md`
- **結構**：`Cards/`（快速筆記）、`Topics/`（MOC）、`YouTube/`（150+ 影片摘要）、`Clippings/`（剪貼）
- **path 格式**：對外回傳一律正規化為 repo-relative 的 `content/...`
- **特色**：繁中整理、含個人註解與踩坑、wikilink 串連

## 查詢協議（Vault + Web 並行）

遇到任何技術/知識性提問，依下列步驟：

### 1. 判斷是否要查資料

- **要查**：Claude Code、Obsidian、RAG、Agent 架構、前端切版、YouTube 已摘要主題、任何使用者可能記過的領域、需要最新資訊的題材
- **不用查**：純語法（如 Python list comprehension）、即時系統狀態、單純閒聊
- 不確定 → 查（寧可多查）

### 2. 並行呼叫兩個來源

單一訊息中同時發兩個 tool call：

- **Vault**：Agent tool 呼叫 `vault-query` subagent，傳入原始問題
- **Web**：WebSearch（需要最新資訊或交叉驗證時）

### 3. 綜合兩邊結果

| 情況 | 作法 |
|------|------|
| Vault 命中 + Web 有料 | 以 vault 打底、web 補最新動態，兩者都引用 |
| 只 Vault 命中 | 以 vault 為主答覆 |
| 只 Web 有料 | 以 web 為主答覆，末尾提示「vault 暫無」 |
| 兩邊矛盾 | 同時呈現，標日期與差異，讓使用者判斷 |

### 4. 引用格式（命中時必加）

答覆末尾加（其中 `<path>` 已含 `content/` 前綴）：

```
來源：

Vault（個人筆記）：
- [[<title>]] — <path>

Web：
- [<頁面標題>](<URL>)
```

### 5. 未命中提示

若 vault 未命中但題目屬「可能有」類，答覆末尾加一行：

```
提示：此題 vault 無相關筆記，可考慮用 /ob 建立。
```

（僅建議，**不自動建檔**。）

## 禁止事項

- 不要不請自來寫 vault；建檔一律由使用者用 `/ob` 觸發
- 不要在非技術性閒聊觸發 vault-query
- 不要把 vault 當唯一真相 — 永遠交叉比對 web

## `/vault` 指令的差異

`/vault <問題>` 是手動模式，**只查 vault 不查 web**。用於想單獨瀏覽 vault 內容、不要 web 雜訊時。與預設並行協議不同。

## 其他全域偏好

- 回應語言：繁體中文（技術名詞保留英文）
- 不主動 commit/push（除非明確要求）
