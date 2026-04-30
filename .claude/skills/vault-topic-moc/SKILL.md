---
name: vault-topic-moc
description: Consolidates multiple related notes in an Obsidian vault into a single topic MOC (Map of Content). Identifies overlapping notes, extracts consensus and differences, verifies facts against official sources, and iterates via reviewer/fixer subagents until the MOC is finalized. Use when the user asks to synthesize notes, merge overlapping notes into a topic, create a topic index, organize notes by theme, or mentions "整理成一個主題", "合併筆記", "MOC", "主題整合", "topic synthesis". Also triggers when the user asks for topic recommendations across the vault — phrases like "給我主題", "給我新主題", "推薦主題", "有什麼主題可以整合", "有什麼建議的主題", "有什麼可以做" — invoke the skill's "推薦主題模式" (1d) which scans for cohesive note clusters and proposes candidates. Do not use for single-note edits, daily journal additions, or channel-level YouTube sync (that is handled by vault-youtube-sync).
---

# Synthesizing Notes to MOC

把 Obsidian vault 中多篇相關筆記（典型情境：YouTube 影片筆記、Cards 的同主題筆記）整合為單一主題 MOC，並與用戶確認原筆記的處置方式。

## 前置作業（寫入前必做）

### Vault 路徑解析

所有讀寫與 Grep/Glob 路徑以 `$OBSIDIAN_VAULT_ROOT` 為 base，避免從非 repo cwd 呼叫時讀寫到錯地方。

```
VAULT_ROOT = $OBSIDIAN_VAULT_ROOT
```

env 未設或該路徑底下找不到 `master-index.md` → 告知用戶並停止，不要猜測 fallback。開工前先跑一次可執行 guard：

```bash
[ -z "$OBSIDIAN_VAULT_ROOT" ] && { echo "ERROR: OBSIDIAN_VAULT_ROOT 未設"; exit 1; }
[ -f "$OBSIDIAN_VAULT_ROOT/master-index.md" ] || { echo "ERROR: $OBSIDIAN_VAULT_ROOT 底下找不到 master-index.md"; exit 1; }
```

設定方式見 README 的「Vault 路徑設定（跨機器）」。

### 產出位置（卡片盒三層工作流）

依 `content/CLAUDE.md`，AI 整理 Inbox/ 或合併既有筆記的產出**一律先進 `Cards/`**，由使用者主觀判斷成熟度後再批次 `git mv` 進 `Topics/<類別>/`。

| 來源 → 產出 | 預設目的地 | 由誰決定 |
|---|---|---|
| Inbox/* 整理 → MOC | `Cards/<主題>.md` | 本 skill |
| Cards/* 同主題整合 → MOC | `Cards/<主題>.md`（覆寫或新建） | 本 skill |
| Cards/ → Topics/ 升級 | `Topics/<類別>/<主題>.md` | **使用者** 人工 `git mv` |

本 skill 預設**不寫 `Topics/`、不更新 `Topics/<類別>/index.md`**。若使用者明確指示寫 Topics/（罕見），才走 `Topics/<類別>/<主題>.md` 並補 index.md wikilink。

### 術語對照（升 Topics/ 才需要）

下列名詞僅在使用者明確指示寫 Topics/ 時用得到。`Topics/` 實際結構：

| 層級 | content/CLAUDE.md 稱呼 | 本文件稱呼 | 範例 |
|---|---|---|---|
| 第一層資料夾 | 「主題」 | **類別** | `Topics/Claude-Code/` |
| 第二層 MOC 檔 | —（視為 cards 之一） | **主題 MOC** | `Topics/Claude-Code/Agent-Harness.md` |

content/CLAUDE.md「Topics/ 第一層不跨主題巢套」指的是不要建 `Topics/AI-工具/Claude-Code/`（兩層類別）；單層類別 `Topics/<類別>/<主題>.md` 不違反此規則。

### 寫入前 Checklist

此 skill 是 `content/` 的寫入路徑（寫 MOC、改 index.md、刪原筆記）。寫入前依 `$OBSIDIAN_VAULT_ROOT/CLAUDE.md` 的「寫入前 Checklist」自檢：

- **敏感資料零容忍**：事實校正從 WebFetch 抓的官方內容若帶 token / API key / 私人資訊，移除再寫入
- **Tag 沿用既有**：寫入前用 Grep tool（`pattern="^tags:"`, `path="$OBSIDIAN_VAULT_ROOT"`, `-A 5`）查既有同主題 tags 再決定，避免 `claude-code` vs `claudeCode` drift；`moc` tag 視同主題既有 MOC 習慣決定是否加（既有都沒加就先不加，既有都加就跟上）
- **Frontmatter schema**：欄位、順序、白名單以 `scripts/vault-schema.mjs` 為真實來源；寫入當下即合法，schema 以外欄位不允許
- **命名**：檔名不含空格，中英文間用 `-`，不含 `?:;"'`

`/vault-check` 只兜底跨檔案 emergent 問題，不負責抓本清單能預防的錯。

## 核心流程（7 步）

### 1. 盤點相關筆記

#### 1a. 蒐集候選

先讀 `$OBSIDIAN_VAULT_ROOT/master-index.md` 了解 vault 結構，再用 Glob / Grep tool 找出候選筆記（pattern / path 為獨立參數，非單一 shell 字串）：

- 檔名含關鍵字：**Glob** `pattern="**/*<keyword>*.md"`, `path="$OBSIDIAN_VAULT_ROOT"`
- 內容含關鍵字：**Grep** `pattern="<keyword>"`, `path="$OBSIDIAN_VAULT_ROOT"`
- Frontmatter tags 或 source URL 過濾：同上，`pattern` 改為 `^tags:` 或 URL regex

#### 1b. 內聚度檢驗（**必做**，不要跳過）

關鍵字命中只是表面相似，**不等於**主題內聚。寫 MOC 前必須驗證候選們是否真的在解同一個核心問題。

**步驟：**

1. 對每篇候選 Read 其 frontmatter + 前 1-2 個章節（或前 30 行），提煉出**這篇的核心問題**（一句話：「在解什麼問題」），不要被檔名與關鍵字騙
2. 把所有候選的核心問題列出來並比對：
   - **強內聚**：所有候選解同一個問題（不同角度可，例：推薦觀點 vs 反方觀點）→ 直接做 MOC
   - **弱內聚**：候選分屬 2 個以上獨立的核心問題 → **拒絕拼湊**，改為兩個解：
     - (a) 縮範圍：挑出真正同問題的子集做 MOC
     - (b) 重找：候選不夠 cohesive，改換主題或補更多筆記

**典型陷阱（必看）**：

> 候選群「RAG / CAG / NotebookLM / 書本 Skill 主副檔」表面都涉及「給 LLM 知識」這個 umbrella term，實際每篇的核心問題是：
> - CAG 篇：「context window 變大後是否還需要 RAG」
> - Web 搜尋篇：「Agent 怎麼編排多個工具決定查哪邊」
> - NotebookLM 篇：「怎麼用 NotebookLM CLI 把外部記憶接進工作流」
> - Skill 主副檔篇：「Claude Code Skill 怎麼設計按需載入」
>
> 這四個是**獨立問題**。共同 umbrella 不算內聚——MOC 寫出來會是四個獨立章節湊一起，缺乏交互呼應。應改為各自做（或加更多同類）。

**判準**：強迫自己用一句話說出「這 N 篇共同在解的那個問題是什麼」。如果這句話寫不出來、或寫得很空泛（「都跟 X 有關」），就是弱內聚——不要做。

#### 1c. 給用戶確認範圍

通過 1b 後，輸出表格供用戶確認：路徑 + 標題 + 發布/建立日期 + 每篇一句**核心問題**（不是「主旨」）。

額外**必須**附上：
- 共同核心問題（一句話）
- 內聚度自評（強 / 中 / 弱）+ 為什麼這樣評
- 弱內聚時要主動建議縮範圍或換主題，不要把決策推給用戶

**建議門檻**：至少 3 篇以上才值得做 MOC，少於 3 篇建議用 wikilink 手動串連即可。

不明主題時，問用戶要包含哪些筆記再開工。

#### 1d. 推薦主題模式（用戶問「有什麼建議的主題」時）

不要按「資料夾」或「關鍵字頻率」推薦——表面命中很容易產生弱內聚候選群。應該：

1. 跨資料夾掃描，找出**講同一個核心問題的小群**（不分頻道、不分來源）
2. 對每個候選群跑 1b 內聚度檢驗
3. 只推薦**通過內聚度檢驗**的群（強內聚），其他即使數量多也明確標記「弱內聚不推薦」並說明原因
4. 推薦時順便指出每群的「對話張力」（例：正反觀點對立、互補實作、世代演進等），這是 MOC 寫起來會有趣的訊號

### 2. 讀取全部內容

Read 全部候選筆記。記錄：
- 每篇的觀點、關鍵數字、獨特資訊
- 可能的偏誤（影片創作者的主觀解讀 vs 官方事實）
- 筆記間的重複與差異

### 3. 產出 MOC v0

寫進 `$OBSIDIAN_VAULT_ROOT/Cards/<主題>.md`（依「產出位置」段預設規則）。骨架範本見 [references/moc-structure.md](references/moc-structure.md)。

若 `Cards/<主題>.md` 已存在，先問用戶：擴充既有的？重寫？還是另建子主題（如 `<主題>-進階.md`）？

若該主題在 `Topics/<類別>/` 已有 MOC（表示之前已升 Topics），同樣先問用戶要動 Cards/ 新版還是覆寫 Topics/ 既有版——後者需用戶明確同意。

### 4. 事實校正（若有官方來源）

若主題是技術概念（工具、API、框架），影片創作者常有二手轉述或過度簡化。應：
- WebSearch 找官方 docs、Engineering blog、GitHub repo
- WebFetch 抓原文比對 MOC 中的「事實性描述」：數字、規則、語法、API 介面
- 不確定的社群數據加註「（社群實測）」等來源標記
- 官方明確規則（如 token 上限、字元限制、保留字）必須準確

**校正後輸出到 MOC 前先過「內容風格濾鏡」**（見下節「內容風格」），不要直接把官方的模型版號 / benchmark / plan 可用矩陣照搬進 MOC。

### 5. 用戶 Checkpoint（第一版停點）

**事實校正完成後，必須停下來讓用戶看 v0 再繼續**。太早進 reviewer/fixer 迴圈會產生大量修改來回，用戶難追蹤、也無法在方向走偏時及早喊停。

停點要做的事：
1. 簡述 v0 寫了什麼（章節列表 + 字數或行數）
2. 給 MOC 絕對路徑讓用戶自行打開看
3. 明確詢問：「要繼續 reviewer/fixer 迭代嗎？」並提示可能的選項：
   - **Y（繼續迭代）**：啟動 Round 1 reviewer
   - **停（就到這）**：跳到 Step 7（原筆記處置）
   - **給修改方向**：用戶指出結構/取捨問題，手動改完再回本 checkpoint

不要自動開 Round 1。用戶說 OK 或指定方向後才進下一步。

### 6. Reviewer / Fixer 迴圈

用戶同意繼續後，用 subagent 迴圈把品質推到定稿：

1. 啟動 **reviewer** subagent 盤點問題（必改 / 應改 / 可選）
2. **把 reviewer 回報完整呈現給用戶**，由用戶決定是否進 fixer（可要求跳過某些項目、或直接定稿）
3. 啟動 **fixer** subagent 照用戶確認的清單修改
4. 回 1，直到 reviewer 回報「無問題，MOC 可以定稿」
5. 連續 2 輪若只剩純風格微調，讓用戶決定是否停
6. 超過 5 輪未收斂，停下讓用戶介入

每輪 reviewer 結束都讓用戶看過再按 fixer，避免 subagent 自由修改失控。

**subagent 呼叫方式**：用 `Agent` tool，`subagent_type: "general-purpose"`，prompt 從 [references/review-loop.md](references/review-loop.md) 取用並填入該輪的 MOC 絕對路徑、官方來源 URL、review 輪次編號。

**與 `/vault-check` 的分工**：`/vault-check` 是 repo-wide 兩段稽核（`scripts/vault-check.mjs` 硬規則自動修 + `vault-auditor` subagent 語意層），對象是整個 vault、判準是 schema 與跨檔一致性；本 skill 的 reviewer/fixer 是對單篇 MOC 做深度 review + 事實校正，判準是主題內部一致與官方事實對齊。兩邊不共用流程。

### 7. 原筆記處置（與用戶確認）

**不要自動刪除原筆記**。先問用戶選 A/B/B-partial/C：

- **A. 保留**：原筆記不動，MOC 用 `[[筆記檔名]]` wikilink
- **B. 整篇刪除**（**單主題 YouTube 來源的預設**）：MOC 末尾保留外部 URL 清單，`git rm` 原筆記
- **B-partial. 部分內化**（**多主題影片專用**）：列「已進 MOC 章節」對照表，per 段落決定刪/留，剩餘段落留 Inbox + frontmatter 加 `extracted_to: "[[<MOC 名>]]"`
- **C. 加 draft**：原筆記加 `draft: true`，Obsidian 可見、不發佈

**Roy 的慣例**：YouTube 影片摘要預設選 **B 整篇刪除**（MOC 自足、vault 精簡）。若整理時發現原筆記涵蓋多個主題、本次 MOC 只覆蓋其中一個切角，改選 **B-partial** 保留剩餘段落。兩者都必須在執行前給清單讓用戶過目，不要跳過確認。

執行細節見 [references/source-handling.md](references/source-handling.md)。

## 內容風格

MOC 聚焦**概念與大方向**，經得起時間、可在不同模型世代重讀仍有效。

**應該放**：
- 問題本質、架構策略、操作準則、速查表
- 相對關係（例：「Opus 成本約 Sonnet 3 倍」）
- 世代演進趨勢（例：「context rot 從斷崖到緩降」）

**不要放**：
- 特定模型版本的 benchmark 分數（例：「Opus 4.6 MRCR v2 76%」）
- 模型發布日期（例：「Opus 4.6 2026-02-05 發布」）
- plan 可用矩陣（例：「Max / Team / Enterprise 才支援 1M」）
- 跨模型分數對照表

**Why:** 這類資料會隨模型迭代快速過時，且不是 MOC 的價值所在。

**How to apply:** 事實校正階段若官方來源主要是模型版本數字，改寫成抽象準則或經驗法則（例：「每 100K tokens 約損失 2% 效能」）。若一定要放具體資訊，放在「外部來源」章節的連結裡，不要寫進正文章節。

## 硬性規則

- MOC 預設寫在 `$OBSIDIAN_VAULT_ROOT/Cards/<主題>.md`（**不要**主動寫 `Topics/<類別>/`，**也不主動更新任何 `Topics/<類別>/index.md` 的 wikilink 清單**——升 Topics 與 index 維護由使用者決定）
- 唯一例外：使用者**明確指示**「直接寫 Topics/<類別>/」時才走 Topics/ 路徑並補 index.md wikilink
- frontmatter 遵守前置作業段「寫入前 Checklist」與 `scripts/vault-schema.mjs`（schema 真實來源）
- `updated` 欄位盡量同步為今日日期（不強制）
- wikilink 檔名需確實存在，否則改用外部 URL
- 選項 B 與 B-partial 執行前都要列檔案／段落清單給用戶過目並確認
- 繁體中文為主，技術名詞保留英文

## 觸發範例

- 「把 YouTube/Chase-H-AI 裡 Claude Code 的影片整理成一個主題」
- 「幫我把 RAG 相關筆記合併成一篇 MOC」
- 「用這次的方法整理 Agent Harness」
- 「把 `Cards/` 裡跟 Hooks 有關的筆記整合成一個主題頁」

## Workflow Checklist（複製到回應中追蹤進度）

```
- [ ] 0. 前置作業：env guard + 術語對照 + 寫入前 Checklist 四項自檢
- [ ] 1a. 蒐集候選筆記
- [ ] 1b. 內聚度檢驗（強/中/弱），弱內聚就縮範圍或換主題
- [ ] 1c. 給用戶確認範圍（含共同核心問題 + 內聚度自評）
- [ ] 2. Read 全部筆記內容
- [ ] 3. 產出 MOC v0
- [ ] 4. 事實校正（若適用）
- [ ] 5. 用戶 Checkpoint：看 v0，決定是否迭代 / 手動改 / 直接停
- [ ] 6. Reviewer/Fixer 迴圈（每輪 review 都給用戶過目）
- [ ] 7. 與用戶確認原筆記處置方式（A/B/C）
```
