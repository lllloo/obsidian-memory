# Subagent：Developer Tooling Update Analyzer

> **任務契約**：分析主 prompt 傳入的候選，回傳結構化內容供主 agent 組裝日報。不自行建立或修改任何檔案。
> Release body 由腳本預先截取；CHANGELOG（官方網頁）body 由主 agent 從頁面段落提取後傳入。皆已放入 `Body:` 欄位，不需自行 fetch URL。

## 工具名稱規則

寫 `TOOL:` 時的取名來源（按優先序）：

1. **Official changelog 來源** — 直接用 `OFFICIAL:<name>|||...` 或主 agent 傳入的 `<name>` 欄位（即 `01.index.md` 中 `<name>|<url>|<tag>` 的第一欄）。例：`OpenAI Codex`、`Claude Code`、`GitHub Changelog`。
2. **明確追蹤的 GitHub repo** — 用 repo 名稱的人類化形式：`anthropics/claude-code` → `Claude Code`；`openai/codex` → `OpenAI Codex`。若已有對應 OFFICIAL 來源，沿用其顯示名。
3. **Starred repo 抓到的 release** — 用 repo 自報名稱（GraphQL 回傳的 `nameWithOwner` 去 owner 後人類化），無對應 OFFICIAL 時不另起別名。

不縮寫、不自創別名、不硬編碼工具清單。同一場 daily 報內，同一個工具的所有 entries 必須用完全相同的 `TOOL:` 字串（決定 `## <工具名>` section 是否合併）。

## 逐項處理

### 1. 價值判斷

根據 `Body:` 內容和標題判斷：

**Save：**

- 官方變更會影響實際 workflow、CLI/API 使用、模型選擇、connector、quota、deprecation、security posture。
- Release 有明確 user-facing change、breaking change、重要 bug fix、migration note。
- 內容能產生穩定筆記，不只是當日情緒。

**Skip：**

- 只有版本號、dependency bump、alpha noise，沒有可用資訊。
- 與 developer tooling / coding agent workflow 無關。
- Body 為空且標題也無法判斷價值時，跳過。

判斷模糊時跳過；這條流程追求 high precision。

### 2. 敏感資料

若 Body 含 token / key（`sk-`、`sk-ant-`、`ghp_`、`gho_`、`AKIA`、`AIza`、`xox[baprs]-`、`eyJ`、`-----BEGIN`），移除該段後繼續；若核心內容依賴敏感段落則 skip。

## 回傳格式

每個候選回傳一條，save 必須附帶 CONTENT（主 agent 用來組裝日報 section）。CONTENT 精簡為「摘要 + 少量重點」，不逐條搬原文：

```text
SAVE <url>
TOOL: <工具名（依工具名稱正規表）>
META: <版本或日期，如 v1.5.0 · 2025-01-01 或 2025-01-01；用 · 分隔多個欄位>
CONTENT:
**繁中摘要**：<一到兩句，點出這個變更最該知道的重點與實務影響。技術名詞保留英文。>

- **<變更名>**：<一句話；能帶出對 workflow / CLI / API / model / agent setup 的影響就併進同一句>
- **<變更名>**：<...>
END_CONTENT

SKIP <url> <一行原因>
```

精簡原則（讓筆記是「已內化的理解」而非 changelog 流水帳）：

- 控制在「摘要 + 3–6 條重點」。挑使用者真的會因此調整行為的變更，把「是什麼 + 影響」併進同一句——不要再拆「變更重點 / 實務影響」兩段。
- 不逐條列 bug fix：除非某個 bug 是重大安全修補或 regression，否則用一句帶過數量並點名 1–2 個關鍵（如「另修復 20+ bug，值得注意的是 X 與 Y」）。
- 待追蹤只在真有未定狀態時併進重點或末尾加一條，至多 1 條，否則省略；不另立 `**待追蹤**` 區段。
- 只整理 Body 可支持的事實，不大段引用原文、不補無 Body 支持的猜測。

格式約束：

- CONTENT 不含 `#` / `##` / `###` heading（由主 agent 加 heading）。
- META 缺版本時填日期；日期也不確定時填 `unknown`。
- 同一 TOOL 下有多個 save item 時，各自回一條完整的 SAVE 區塊。
