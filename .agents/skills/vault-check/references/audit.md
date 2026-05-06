# Vault 語意層稽核流程

對 Obsidian vault 的 `content/` 執行語意層稽核，回傳結構化 JSON。定位為「兜底層」：寫入路徑（write 流程等）依 `content/CLAUDE.md` 的寫入前 Checklist 自檢預防；deterministic 規則由 `scripts/vault-check.mjs` 處理；本流程抓漏網——Web Clipper / 手動編輯帶入的敏感資料與 schema 缺漏、跨筆記 emergent 問題（broken wikilinks、tag drift）。大多數時候結果應為空；非空代表寫入路徑或外部來源需要補強。

**不負責的範圍**：筆記位置（Inbox/Cards/Topics）屬於使用者主觀判斷，不在稽核清單，禁止產生此類建議。

## 唯讀工具契約（強制）

此流程**禁止任何寫入**。違反即停止輸出，回報「audit 流程不得寫入」。

- **允許工具**：`Read` / `Glob` / `Grep`
- **允許 Bash 命令**（僅唯讀）：`pwd`、`test`、`ls`、`find`、`rg`、`cat`、`Get-Content`、`realpath`、`git status`、`git diff --stat`
- **禁止工具**：`Write` / `Edit` / `NotebookEdit`
- **禁止 Bash 命令**：`mkdir`、`mv`、`cp`、`Move-Item`、`Copy-Item`、`Set-Content`、`Add-Content`、`Out-File`、`Remove-Item`、`rm`、`sed -i`、`tee`、shell redirect（`>`、`>>`）、任何 `npm run` 含 `:fix` / `:write` / `:build` 的 script（特別是 `npm run vault:fix`）、`obsidian create` / `obsidian append` / `obsidian property:set` 等任何寫入子命令
- **無法確認某命令是否唯讀**：停止並回報「無法確認 `<命令>` 唯讀，已中止」

其他絕對規則：

- **輸出必為 JSON**：純 JSON 物件，不加 markdown wrapper、不加解釋
- **不再呼叫其他 subagent**
- **path 一律正規化**：`content/...`，不要絕對路徑

## Cwd 契約（必先執行）

本流程是 repo-local，cwd 必為 repo root。先驗證：

```bash
test -f content/master-index.md
```

失敗即直接輸出空結果，`error` 欄寫「cwd 不在 repo root，無法執行 audit」。orchestrator 通常會在 step 1 早停，這條是兜底，避免 subagent 被孤立呼叫時誤掃。

## 掃描範圍

- 全部 `content/**/*.md`
- **排除**：`.obsidian/`、`content/index.md`、`content/master-index.md`、`content/CLAUDE.md`

開工前先 `Read content/CLAUDE.md` 取得當前的「寫入前 Checklist」內容（敏感資料定義、frontmatter schema、tag 一致性判準、命名規則）作為稽核依據。Checklist 更新時本流程自動跟上，不需改 reference。

## 四類稽核

### 1. schema_issues — 缺必填或 parse 失敗

- frontmatter 缺 `title` / `created` / `tags`（這三個 script 故意不修）
- YAML 完全解析不了（引號、縮排錯）
- 對缺 `title` 的，看正文第一段建議合理 title
- 對缺 `created` 的，建議用 git log 第一次 commit 日期（若難取得就建議今日）
- 對缺 `tags` 的，根據內容建議 1-3 個 tag（優先沿用既有 tag）

### 2. broken_wikilinks — wikilink 斷鏈

- 掃正文與 frontmatter `parent` 的 `[[...]]`
- target 對照 `content/**/*.{md,base}` 的檔名（Quartz `shortest` 語義，比 basename）
- 排除 code fence 內的 `[[...]]`
- 對每個斷鏈，找最相似的現有檔名做 suggestion；找不到就 `suggestion: null`

### 3. sensitive_data — 敏感資料

**清單以 `content/CLAUDE.md` 的「寫入前 Checklist §1」為準**（regex 白名單 + 自然語言密碼 + 個資 / 公司內部資訊）。開工前已 Read 該檔，依當下清單掃描，CLAUDE.md 更新時本流程自動跟上。

稽核側專屬規則（不屬於清單本身）：

- 排除 code fence 內的範例
- 嚴重度分三級：`high`（確定的 secret，regex 命中）/ `medium`（疑似但需人工確認，語意命中）/ `low`（一般敏感詞）
- `match` 欄位只取前 12 字 + `…` 避免日誌洩漏

### 4. tag_conflicts — tag 一致性

- 蒐集全 vault frontmatter tags
- 找出疑似同義但寫法不同的 group：`claude-code` vs `claudeCode` vs `claude_code`、`ai` vs `AI` vs `人工智慧`、單複數差異等
- 給 `suggestion`（建議標準化到哪個，優先選最常出現的）
- 列出每組受影響的檔案路徑

## 輸出格式

```json
{
  "scanned_files": 123,
  "schema_issues": [
    {
      "file": "content/Cards/foo.md",
      "code": "MISSING_TITLE",
      "message": "缺 title 欄位",
      "suggestion": "Claude Code 記憶系統設計"
    },
    {
      "file": "content/Inbox/bar.md",
      "code": "PARSE_ERROR",
      "message": "frontmatter YAML 解析失敗：第 3 行引號未配對",
      "suggestion": null
    }
  ],
  "broken_wikilinks": [
    {
      "file": "content/Topics/Claude-Code/index.md",
      "line": 42,
      "target": "Memory-Architecture",
      "suggestion": "Claude-Code-記憶架構"
    }
  ],
  "sensitive_data": [
    {
      "file": "content/Inbox/test.md",
      "line": 10,
      "kind": "OpenAI API key",
      "match": "sk-proj-abcd…",
      "severity": "high"
    }
  ],
  "tag_conflicts": [
    {
      "variants": ["claude-code", "claudeCode"],
      "suggestion": "claude-code",
      "files": ["content/Cards/a.md", "content/Topics/X/b.md"]
    }
  ],
  "error": null
}
```

未命中的類別給空陣列。掃描失敗（cwd 不對等）`error` 寫原因。

## 效能守則

- 不要把 `Inbox/YouTube/` 全部 Read（量大），這部分主要做 sensitive_data 與 schema_issues 即可
- broken_wikilinks 與 tag_conflicts 用 Grep 蒐集後再 Read 必要的檔案
- Read 檔案總數估算：< 60 是合理區間，超過要思考是否該抽樣或分批

## 與 vault-check.mjs 的分工

判斷原則：能 deterministic 修的歸 script，需要讀內容才能決定的歸本流程。詳細範圍劃分見 `.agents/skills/vault-check/SKILL.md` 的「執行流程」段（orchestrator 視角最完整）。
