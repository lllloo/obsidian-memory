---
name: vault-topic-moc
description: Consolidates multiple related notes in an Obsidian vault into a single topic MOC (Map of Content). Identifies overlapping notes, extracts consensus and differences, verifies facts against official sources, and iterates via reviewer/fixer subagents until the MOC is finalized. Use when the user asks to synthesize notes, merge overlapping notes into a topic, create a topic index, organize notes by theme, or mentions "整理成一個主題", "合併筆記", "MOC", "主題整合", "topic synthesis". Also triggers when the user asks for topic recommendations across the vault — phrases like "給我主題", "給我新主題", "推薦主題", "有什麼主題可以整合", "有什麼建議的主題", "有什麼可以做" — invoke the skill's "推薦主題模式" which scans for cohesive note clusters and proposes candidates. Do not use for single-note edits, daily journal additions, or channel-level YouTube sync (that is handled by vault-youtube-sync).
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

| 來源 → 產出               | 預設目的地                      | 由誰決定                 |
| ------------------------- | ------------------------------- | ------------------------ |
| Inbox/\* 整理 → MOC       | `Cards/<主題>.md`               | 本 skill                 |
| Cards/\* 同主題整合 → MOC | `Cards/<主題>.md`（覆寫或新建） | 本 skill                 |
| Cards/ → Topics/ 升級     | `Topics/<類別>/<主題>.md`       | **使用者** 人工 `git mv` |

本 skill 預設**不寫 `Topics/`、不更新 `Topics/<類別>/index.md`**。若使用者明確指示寫 Topics/（罕見），才走 `Topics/<類別>/<主題>.md` 並補 index.md wikilink。

### 術語對照（升 Topics/ 才需要）

下列名詞僅在使用者明確指示寫 Topics/ 時用得到。`Topics/` 實際結構：

| 層級          | content/CLAUDE.md 稱呼 | 本文件稱呼   | 範例                                  |
| ------------- | ---------------------- | ------------ | ------------------------------------- |
| 第一層資料夾  | 「主題」               | **類別**     | `Topics/Claude-Code/`                 |
| 第二層 MOC 檔 | —（視為 cards 之一）   | **主題 MOC** | `Topics/Claude-Code/Agent-Harness.md` |

content/CLAUDE.md「Topics/ 第一層不跨主題巢套」指的是不要建 `Topics/AI-工具/Claude-Code/`（兩層類別）；單層類別 `Topics/<類別>/<主題>.md` 不違反此規則。

### 寫入前 Checklist（與 vault 通用規則的差異）

寫入前依 content/CLAUDE.md 的寫入前 Checklist 自檢（敏感資料、frontmatter schema、命名、tags 沿用）。本 skill 額外注意：

- **`moc` tag 處理**：用 Grep（`pattern="^tags:"`, `path="$OBSIDIAN_VAULT_ROOT"`, `-A 5`）看既有同主題 MOC 習慣——都加 `moc` 就跟上、都沒加就先不加，避免單篇開新風格
- **WebFetch 內容過濾**：事實校正從官方來源抓的內容若帶 token / API key / 私人資訊，移除再寫入

`/vault-check` 只兜底跨檔案 emergent 問題，不負責抓本清單能預防的錯。

## 核心流程（7 步）

### 1. 盤點與確認候選範圍

#### 1a. 蒐集候選

先讀 `$OBSIDIAN_VAULT_ROOT/master-index.md` 了解 vault 結構，再用 Glob / Grep tool 找出候選筆記（pattern / path 為獨立參數，非單一 shell 字串）：

- 檔名含關鍵字：**Glob** `pattern="**/*<keyword>*.md"`, `path="$OBSIDIAN_VAULT_ROOT"`
- 內容含關鍵字：**Grep** `pattern="<keyword>"`, `path="$OBSIDIAN_VAULT_ROOT"`
- Frontmatter tags 或 source URL 過濾：同上，`pattern` 改為 `^tags:` 或 URL regex

#### 1b. 內聚度檢驗 + 給用戶確認（**必做**）

關鍵字命中只是表面相似，**不等於**主題內聚。先做內部驗證再向用戶呈現範圍——避免讓用戶替弱內聚候選背書。

**內部驗證步驟**：

1. 對每篇候選 Read 其 frontmatter + 前 1-2 個章節（或前 30 行），提煉**這篇的核心問題**（一句話：「在解什麼問題」），不要被檔名與關鍵字騙
2. 比對所有候選核心問題：
   - **強內聚**：所有候選解同一個問題（不同角度可，例：推薦觀點 vs 反方觀點）→ 直接做 MOC
   - **弱內聚**：候選分屬 2 個以上獨立的核心問題 → **拒絕拼湊**，主動建議縮範圍（挑真正同問題的子集）或換主題（補更多同類筆記），不把決策推給用戶

**典型陷阱（必看）**：

> 候選群「RAG / CAG / NotebookLM / 書本 Skill 主副檔」表面都涉及「給 LLM 知識」這個 umbrella term，實際每篇的核心問題是：
>
> - CAG 篇：「context window 變大後是否還需要 RAG」
> - Web 搜尋篇：「Agent 怎麼編排多個工具決定查哪邊」
> - NotebookLM 篇：「怎麼用 NotebookLM CLI 把外部記憶接進工作流」
> - Skill 主副檔篇：「Claude Code Skill 怎麼設計按需載入」
>
> 這四個是**獨立問題**。共同 umbrella 不算內聚——MOC 寫出來會是四個獨立章節湊一起，缺乏交互呼應。應改為各自做（或加更多同類）。

**判準**：強迫自己用一句話說出「這 N 篇共同在解的那個問題是什麼」。如果這句話寫不出來、或寫得很空泛（「都跟 X 有關」），就是弱內聚——不要做。

**對用戶呈現**（驗證完才確認範圍）：表格列路徑 + 標題 + 發布/建立日期 + 每篇一句**核心問題**（不是「主旨」）。額外必須附上：

- 共同核心問題（一句話）
- 內聚度自評（強 / 中 / 弱）+ 為什麼
- 弱內聚時主動給縮範圍或換主題的具體建議

**建議門檻**：至少 3 篇以上才值得做 MOC，少於 3 篇建議用 wikilink 手動串連即可。

不明主題時，問用戶要包含哪些筆記再開工。

#### 1c. 推薦主題模式（用戶問「有什麼建議的主題」時）

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

### 4. 用戶 Checkpoint（看 v0 決定下一步）

**v0 寫完後必須停下來讓用戶看再繼續**。事實校正會花 WebFetch 與 token，方向走偏才做白工；reviewer/fixer 迴圈會產生大量修改來回，太早進去用戶難追蹤、也無法在方向走偏時及早喊停。

停點要做的事：

1. 簡述 v0 寫了什麼（章節列表 + 字數或行數）
2. 給 MOC 絕對路徑讓用戶自行打開看
3. 明確詢問下一步，提示可能的選項：
   - **要事實校正**：跳 Step 5（主題是技術概念且有官方來源時）
   - **不需校正、直接迭代品質**：跳 Step 6 reviewer/fixer
   - **停（就到這）**：跳 Step 7（原筆記處置）
   - **給修改方向**：用戶指出結構/取捨問題，手動改完再回本 checkpoint

不自動進入下一步。用戶說 OK 或指定方向後才走下一站。

### 5. 事實校正（用戶選擇做、且有官方來源時）

若主題是技術概念（工具、API、框架），影片創作者常有二手轉述或過度簡化。應：

- WebSearch 找官方 docs、Engineering blog、GitHub repo
- WebFetch 抓原文比對 MOC 中的「事實性描述」：數字、規則、語法、API 介面
- 不確定的社群數據加註「（社群實測）」等來源標記
- 官方明確規則（如 token 上限、字元限制、保留字）必須準確

**校正後輸出到 MOC 前先過「內容風格濾鏡」**（見下節「內容風格」），不要直接把官方的模型版號 / benchmark / plan 可用矩陣照搬進 MOC。

校正完成後再給用戶看一次 v0.5（或直接進 Step 6）。

### 6. Reviewer / Fixer 迴圈

用戶同意繼續後，用 subagent 迴圈把品質推到定稿：

1. 啟動 **reviewer** subagent 盤點問題（必改 / 應改 / 可選）
2. **把 reviewer 回報完整呈現給用戶**，由用戶決定是否進 fixer（可要求跳過某些項目、或直接定稿）
3. 啟動 **fixer** subagent 照用戶確認的清單修改
4. 回 1，直到 reviewer 回報「無問題，MOC 可以定稿」
5. 連續 2 輪若只剩純風格微調，讓用戶決定是否停
6. 超過 5 輪未收斂，停下讓用戶介入

每輪 reviewer 結束都讓用戶看過再按 fixer，避免 subagent 自由修改失控。

**subagent 呼叫方式**：用 `Agent` tool，`subagent_type: "general-purpose"`，prompt 從 [references/review-loop.md](references/review-loop.md) 取用並填入該輪的 MOC 絕對路徑、官方來源 URL、review 輪次編號。**若 Step 5 跳過（沒做事實校正）**，官方來源欄位填 `N/A`，reviewer 會跳過事實準確性檢查。

**與 `/vault-check` 的分工**：`/vault-check` 是 repo-wide 兩段稽核（`scripts/vault-check.mjs` 硬規則自動修 + audit reference 經 general-purpose subagent 跑語意層），對象是整個 vault、判準是 schema 與跨檔一致性；本 skill 的 reviewer/fixer 是對單篇 MOC 做深度 review + 事實校正，判準是主題內部一致與官方事實對齊。兩邊不共用流程。

### 7. 原筆記處置（與用戶確認）

**不要自動刪除原筆記**。先問用戶選 A/B/B-partial/C：

- **A. 保留** wikilink 連回
- **B. 整篇刪除**（YouTube 影片摘要預設）
- **B-partial. 部分內化**（多主題影片：保留剩餘段落 + frontmatter 加 `extracted_to`）
- **C. 加 draft**

**Roy 的慣例**：YouTube 影片摘要預設選 B；若原筆記涵蓋多主題、本次 MOC 只覆蓋一個切角，改選 B-partial。執行前必須給檔案/段落清單讓用戶過目。

四選項詳細流程、優缺點、checklist 與決策建議表見 [references/source-handling.md](references/source-handling.md)。

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

- 預設寫 `Cards/<主題>.md`（產出位置段已說明，唯一例外：使用者明確指示寫 Topics/）
- wikilink 檔名需確實存在，否則改用外部 URL
- `updated` 盡量同步為今日日期（不強制）
- 繁體中文為主，技術名詞保留英文

## 觸發範例

- 「把 YouTube/Chase-H-AI 裡 Claude Code 的影片整理成一個主題」
- 「幫我把 RAG 相關筆記合併成一篇 MOC」
- 「用這次的方法整理 Agent Harness」
- 「把 `Cards/` 裡跟 Hooks 有關的筆記整合成一個主題頁」

## Workflow Checklist（複製到回應中追蹤進度）

```
- [ ] 0. 前置作業：env guard + 寫入前 Checklist 自檢
- [ ] 1a. 蒐集候選筆記
- [ ] 1b. 內聚度檢驗 + 給用戶確認範圍（含核心問題 + 內聚度自評）
- [ ] 2. Read 全部筆記內容
- [ ] 3. 產出 MOC v0
- [ ] 4. 用戶 Checkpoint：看 v0 決定下一步（事實校正 / reviewer / 停 / 改方向）
- [ ] 5. 事實校正（用戶選擇且有官方來源時）
- [ ] 6. Reviewer/Fixer 迴圈（每輪 review 都給用戶過目）
- [ ] 7. 與用戶確認原筆記處置方式（A/B/B-partial/C）
```
