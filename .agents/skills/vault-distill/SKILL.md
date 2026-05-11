---
name: vault-distill
description: 將 Obsidian vault 中多篇相關筆記整合為單一主題 MOC（Map of Content）：辨識重疊、萃取共識與差異、對照官方來源校正事實，透過 reviewer/fixer subagent 迭代直到定稿。也支援推薦適合整合的候選主題（vault 中已累積到內聚門檻的群組）。使用時機：使用者要求「整合筆記」、「合併同主題筆記」、「建立 MOC」、「主題整合」、「topic synthesis」、「有什麼主題可整合」、「推薦主題」，或直接呼叫 /vault-distill。
---

# Synthesizing Notes to MOC

**每次呼叫做一件事**，用 vault 狀態 + 使用者意圖決定當前步驟，不在單次呼叫內執行迴圈。重複呼叫才推進到下一步。

## 狀態偵測（每次呼叫最先執行）

```bash
[ -f "content/master-index.md" ] || { echo "ERROR: cwd 不在 repo root"; exit 1; }
```

**Step 0：先確認 F 觸發條件**
若使用者訊息含「建議主題」/「推薦主題」/「有什麼可以做」/「有什麼主題可以整合」→ **立刻跳步驟 F**，不繼續以下狀態偵測。

**Step 1：動詞快捷路由**
若使用者訊息含動詞快捷（`review`/`fix`/`校正`/`verify`/`dispose` + 主題名稱），直接路由對應步驟（B/C/D/E），跳過下方詢問環節。

**Step 2：掃描現有 MOC**
先嘗試讀取 `.vault-distill/state.json`（gitignored，不存在時靜默略過）取出 `mocs` 鍵清單，再分兩處掃描合併結果：

- `rg -l "^\s*- moc" content/Cards --include="*.md" --glob='!**/index.md'`
- `rg -l "^\s*- moc" content/Topics --include="*.md" --glob='!**/index.md'`

state.json 的 `round` 與 `candidates` 欄位直接傳給後續步驟（省去跨 session 輪數推算）。詳細 schema 見 `references/state-schema.md`。

額外偵測半成品：

- 含 `draft: true` 的 MOC → 標記為「進行中」

依 MOC 數量路由：

**推薦模式（使用者說「有什麼建議的主題」）→ F**（已在 Step 0 提前攔截）

**沒有任何 MOC（含半成品）**
→ 問：「要整合哪個主題？」
→ 用戶回答主題名稱後進 **A**

**有 1 個 MOC（`Cards/<主題>.md` 或 `Topics/.../<主題>.md`）**
→ 問：「<主題> MOC 已存在，要做什麼？」，選項：review / fix / 校正 / 處理原筆記
→ 依回答進 B / C / D / E

**有多個 MOC**
→ 列出清單（標注所在位置 Cards/ 或 Topics/），問：「要繼續哪一個？」
→ 確認主題後再問同上選項，路由到 B / C / D / E

---

## 步驟 A：生成 v0

**觸發**：`Cards/<主題>.md` 不存在。

### A1. 蒐集候選

先讀 `content/master-index.md` 了解 vault 結構，再用 Glob / Grep 找候選（pattern / path 為獨立參數）：

- 檔名含關鍵字：Glob `pattern="**/*<keyword>*.md"`, `path="content"`
- 內容含關鍵字：Grep `pattern="<keyword>"`, `path="content"`
- Frontmatter tags 或 source URL：同上，`pattern` 改為 `^tags:` 或 URL regex

搜尋結果排除 frontmatter 含 `moc` tag 的檔案（已是 MOC，不應作為整合來源）。

搜尋完畢後額外執行：

- 掃 `content/Cards/` 是否有含「## 來源」章節但無 `moc` tag 的 .md 檔（疑似未補 tag 的 MOC）→ 若有，警示用戶確認再繼續
- 列出所有現有 MOC（moc tag），確認候選主題名稱無同義詞衝突（如「Claude Code Skills」vs「Claude Skills」）→ 若有疑似重複，告知用戶是否合併

### A2. 內聚度檢驗

對每篇候選讀 frontmatter + 前 30 行，提煉**核心問題**（一句話：「在解什麼問題」）。

- **強內聚**（所有篇回答同一問題）→ 靜默通過，不打斷，直接進 A3
- **弱內聚**（≥ 2 個獨立核心問題）→ 打斷，給縮範圍建議，等用戶確認後才繼續
- **候選 < 3 篇** → 告知，建議改用 wikilink 手動串連，等用戶確認是否仍要繼續

用戶確認縮範圍後，以用戶指定的子關鍵字**重跑 A1 搜尋**，取得新的候選清單，再進 A2 重新檢驗。

**典型陷阱**：候選群表面都涉及同一 umbrella term（「給 LLM 知識」），實際上每篇解的是獨立問題（CAG vs RAG vs NotebookLM vs Skill 設計）。強迫自己用一句話說出「這 N 篇共同在解的那個問題」——說不出來或說得很空泛就是弱內聚，不要做。

### A3. 讀取內容

Read 全部候選筆記，記錄：觀點、關鍵數字、獨特資訊、可能偏誤（創作者主觀 vs 官方事實）、筆記間重複與差異。

### A4. 產出 v0

先 Read `.agents/skills/vault-distill/references/moc-structure.md` 確認骨架與「常見錯誤」checklist，再寫入 `content/Cards/<主題>.md`。

寫入前，確認 A1 的同義詞衝突掃描已通過，或用戶已確認不合併。

寫入前依 `content/CLAUDE.md` 的「寫入前 Checklist」自檢，額外注意：

- **`moc` tag**：Grep 既有同主題 MOC 習慣，沿用不另創
- **WebFetch 內容過濾**：事實校正若帶 token / 個資，移除再寫入

若 `Cards/<主題>.md` 已存在：問用戶要擴充、重寫、還是另建子主題，確認後才繼續。

### A 結束

輸出：

- 檔案路徑、行數、候選筆記清單（N 篇）
- 自檢摘要：前言列出的面向 vs 實際章節對應（有無孤兒）、wikilink 數量、frontmatter 是否符合 schema

提示：「再次呼叫執行 review；加 fix 執行修正；加 dispose 處理原筆記；加校正執行事實校正」

---

## 步驟 B：Review

**觸發**：`Cards/<主題>.md` 存在，使用者選 review 選項。

用 Agent tool（`subagent_type: "general-purpose"`）啟動 reviewer subagent，prompt = `references/review-loop.md` 的 **Reviewer Subagent Prompt** 段全文，填入以下 placeholder：

- `<MOC 絕對路徑>` → 實際路徑（e.g., `/Users/.../content/Cards/主題.md`）
- `<官方 docs URL 1/2>` → 若未跑步驟 D，填 `N/A`；若已跑步驟 D，從對話中的校正摘要取出官方 docs URL 帶入（reviewer 才會驗收校正效果）
- `第 N 輪` → 優先讀 `.vault-distill/state.json` 的 `round` 欄位；state.json 不存在或無此 MOC 鍵時才預設 `第 1 輪`（告知用戶）

不必告訴 subagent 去 Read references/review-loop.md——直接貼段落全文。

Reviewer 回報**三類問題**（必改 / 應改 / 可選），每項含具體位置與建議。

### B 結束

完整呈現 reviewer 問題清單。若無問題則說「MOC 品質已達標，可定稿」。

提示：「加 fix 再次呼叫套用修正；加 dispose 處理原筆記」

---

## 步驟 C：Fix

**觸發**：`Cards/<主題>.md` 存在，使用者含 fix / 套用 / 修。

**兩次獨立 Agent tool 呼叫，依序執行**（第一次完成後才啟動第二次）：

1. **優先使用對話中最近一次 B review 清單**（省一次 subagent 呼叫）。若對話中沒有本主題的 B 結果（如直接輸入 fix 跳過 B），才啟動 reviewer subagent（prompt 同步驟 B）補抓漂移。
2. 等 reviewer 結果確認後，啟動 fixer subagent，prompt = `references/review-loop.md` 的 **Fixer Subagent Prompt** 段全文，替換所有 placeholder：
   - `<MOC 絕對路徑>` → 實際路徑（e.g., `/Users/.../content/Cards/主題.md`）
   - `N 項` → reviewer 回報的問題數量
   - `<貼上 reviewer 回報的完整清單，按必改/應改/可選分組>` → reviewer 回傳的必改與應改清單
   - `<今日日期 YYYY-MM-DD>` → 今日日期（e.g., `2026-05-10`）

### C 結束

輸出修改摘要（哪些問題已處理、哪些可選項跳過）。

提示：「再次呼叫繼續 review；加 dispose 處理原筆記」

---

## 步驟 D：事實校正

**觸發**：`Cards/<主題>.md` 存在，使用者含 校正 / verify。

適用主題：技術概念（工具、API、框架），影片創作者常有二手轉述或過度簡化。

- WebSearch 找官方 docs、Engineering blog、GitHub repo
- WebFetch 抓原文比對 MOC 中的「事實性描述」：數字、規則、語法、API 介面
- 不確定的社群數據加註「（社群實測）」
- 官方明確規則（token 上限、字元限制、保留字）必須準確

校正後過「內容風格濾鏡」（見下節），不直接照搬版本數字或 benchmark。

### D 結束

輸出校正摘要（哪些事實修正、哪些無法確認）。

提示：「再次呼叫執行 review；加 fix 套用修正」

---

## 步驟 E：Disposal（原筆記處置）

**觸發**：使用者含 處理原筆記 / 刪 / dispose。

**原筆記清單來源**（按優先順序）：

1. 對話中已有 **本主題** Step A 候選清單 → 直接使用（使用前先確認主題與當前 MOC 一致，多 MOC 場景尤需注意）
2. 否則重跑 A1 搜尋，使用 MOC 的 **frontmatter tags**（而非標題文字）作為關鍵字，再用 MOC 現有 wikilink 做交叉補充
3. 或掃描 MOC 現有 wikilink，把 `[[...]]` 指向 `content/Cards/` 或 `content/Inbox/` 的檔案視為候選

三個來源結果不一致時（相差 ≥ 3 篇），列出差異，讓用戶確認正確清單，再繼續。

**執行前必做**：用 Glob 驗證清單中每個路徑仍存在，移除已消失的路徑並告知用戶。

列出清單，讓用戶選：

- **A. 保留** — 在 MOC 加 wikilink
- **B. 整篇刪除** — YouTube 影片摘要預設
- **B-partial. 部分內化** — 保留剩餘段落 + frontmatter 加 `extracted_to`
- **C. 加 draft** — 保留但不發佈

詳細說明見 `references/source-handling.md`。**執行前給用戶看清單確認，確認後才動檔。**

---

## 步驟 F：推薦主題模式

**觸發**：使用者問「有什麼建議的主題」/ 「推薦主題」等。不寫任何檔案。

1. 先讀 `content/master-index.md` 了解 vault 整體結構與已有主題（包括 Topics/ 下已整合的主題，稍後排除）
2. 用 `rg` 讀所有 `content/Cards/**/*.md` + `content/Inbox/**/*.md` 的 frontmatter，按 tags 分群（排除 frontmatter 含 `moc` tag 的檔案）
3. **只對 tag 相同筆記數 ≥ 3 的群**，才讀每篇前 30 行做核心問題提煉（其他群直接跳過，不浪費 IO）
4. 對每個候選群跑內聚度檢驗（同步驟 A2）：能一句話說出「這群共同解的問題」才算強內聚
5. **排除與 Topics/ 已歸檔主題高度重疊的候選群**（避免重複整合）
6. 只推薦強內聚群；弱內聚群也列出，明確標記並說明哪些核心問題相互獨立
7. 每個推薦群附上：
   - 「對話張力」（正反對立 / 互補實作 / 世代演進等）
   - **預估整合工作量**（候選篇數、是否需事實校正、預期 review 輪數）

---

## 產出位置

依 `content/CLAUDE.md` 卡片盒工作流，AI 整理的產出**一律先進 `Cards/`**：

| 來源 → 產出               | 預設目的地                | 由誰決定                 |
| ------------------------- | ------------------------- | ------------------------ |
| Inbox/\* 整理 → MOC       | `Cards/<主題>.md`         | 本 skill                 |
| Cards/\* 同主題整合 → MOC | `Cards/<主題>.md`         | 本 skill                 |
| Cards/ → Topics/ 升級     | `Topics/<類別>/<主題>.md` | **使用者** 人工 `git mv` |

本 skill 預設**不寫 `Topics/`**。使用者明確指示時才例外（同時補 `Topics/<類別>/index.md` 的 wikilink）。

---

## 內容風格

MOC 聚焦**概念與大方向**，經得起時間、跨模型世代重讀仍有效。

**應該放**：問題本質、架構策略、操作準則、速查表、相對關係（「Opus 成本約 Sonnet 3 倍」）、世代演進趨勢。

**不要放**：特定模型版本 benchmark 分數、模型發布日期、plan 可用矩陣、跨模型分數對照表。

**Why**：這類資料隨模型迭代快速過時，不是 MOC 的價值所在。

**How to apply**：事實校正若官方來源主要是版本數字，改寫成抽象準則（「每 100K tokens 約損失 2% 效能」）。具體資訊放「外部來源」章節連結，不寫進正文。

---

## 硬性規則

- 預設寫 `Cards/<主題>.md`（唯一例外：使用者明確指示寫 Topics/）
- wikilink 必須指向實際存在的檔案，否則改用外部 URL
- 繁體中文為主，技術名詞保留英文
- 不自動 commit

## Fallback（無 Agent 工具時）

若環境不支援 `Agent` tool（Cursor、Codex、Gemini CLI 等），主 agent 直接 Read `references/review-loop.md` 全文，自行扮演 reviewer 或 fixer 角色執行同流程，結果直接輸出或寫入，無需 subagent。
