---
name: vault-topic-moc
description: Consolidates multiple related notes in an Obsidian vault into a single topic MOC (Map of Content). Identifies overlapping notes, extracts consensus and differences, verifies facts against official sources, and iterates via reviewer/fixer subagents until the MOC is finalized. Use when the user asks to synthesize notes, merge overlapping notes into a topic, create a topic index, organize notes by theme, or mentions "整理成一個主題", "合併筆記", "MOC", "主題整合", "topic synthesis". Do not use for single-note edits, daily journal additions, or channel-level YouTube sync (that is handled by vault-youtube-sync).
---

# Synthesizing Notes to MOC

把 Obsidian vault 中多篇相關筆記（典型情境：YouTube 影片筆記、Cards 的同主題筆記）整合為單一主題 MOC，並與用戶確認原筆記的處置方式。

## 核心流程（7 步）

### 1. 盤點相關筆記

先讀 `content/master-index.md` 了解 vault 結構，再用 Grep / Glob 找出候選筆記：
- 檔名含關鍵字：`Glob "content/**/*<keyword>*.md"`
- 內容含關鍵字：`Grep "<keyword>" content/`
- Frontmatter tags 或 source URL 過濾

輸出表格供用戶確認：路徑 + 標題 + 發布/建立日期 + 每篇一句主旨。

**建議門檻**：至少 3 篇以上才值得做 MOC，少於 3 篇建議用 wikilink 手動串連即可。

不明主題時，問用戶要包含哪些筆記再開工。

### 2. 讀取全部內容

Read 全部候選筆記。記錄：
- 每篇的觀點、關鍵數字、獨特資訊
- 可能的偏誤（影片創作者的主觀解讀 vs 官方事實）
- 筆記間的重複與差異

### 3. 產出 MOC v0

寫進 `content/Topics/<類別>/<主題>.md`。骨架範本見 [references/moc-structure.md](references/moc-structure.md)。

若該主題 MOC 已存在，先問用戶：擴充既有的？重寫？還是建新的子主題？

### 4. 事實校正（若有官方來源）

若主題是技術概念（工具、API、框架），影片創作者常有二手轉述或過度簡化。應：
- WebSearch 找官方 docs、Engineering blog、GitHub repo
- WebFetch 抓原文比對 MOC 中的「事實性描述」：數字、規則、語法、API 介面
- 不確定的社群數據加註「（社群實測）」等來源標記
- 官方明確規則（如 token 上限、字元限制、保留字）必須準確

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

**與 `vault-evaluator` / `vault-fixer` 的差別**：那兩個 agent 是對整個 vault 做規則稽核（見 `/vault-check` 指令），本 skill 的 reviewer/fixer 是對單篇 MOC 做深度 review + 事實校正，不共用。

### 7. 原筆記處置（與用戶確認）

**不要自動刪除原筆記**。先問用戶選 A/B/C：

- **A. 保留**：原筆記不動，MOC 用 `[[筆記檔名]]` wikilink
- **B. 刪除**（**YouTube 來源筆記的預設**）：MOC 末尾保留外部 URL 清單，`git rm` 原筆記，更新 master-index
- **C. 加 draft**：原筆記加 `draft: true`，Obsidian 可見、不發佈

**Roy 的慣例**：當原筆記來源是 `content/YouTube/` 下的影片摘要，整理完成後預設會選 **B 刪除**（MOC 自足、vault 精簡）。仍必須在刪除前給清單讓用戶過目，不要跳過確認。

執行細節見 [references/source-handling.md](references/source-handling.md)。

## 硬性規則

- MOC 寫在 `content/Topics/<類別>/<主題>.md`（**不要**寫 `Cards/` 或 `YouTube/`）
- frontmatter 遵守 `content/CLAUDE.md` 的 card.md 標準（title/created/updated/tags）
- `updated` 欄位盡量同步為今日日期（不強制）
- wikilink 檔名需確實存在，否則改用外部 URL
- 選項 B 執行前再次確認用戶是否真的要刪
- 繁體中文為主，技術名詞保留英文

## 觸發範例

- 「把 YouTube/Chase-H-AI 裡 Claude Code 的影片整理成一個主題」
- 「幫我把 RAG 相關筆記合併成一篇 MOC」
- 「用這次的方法整理 Agent Harness」
- 「把 `Cards/` 裡跟 Hooks 有關的筆記整合成一個主題頁」

## Workflow Checklist（複製到回應中追蹤進度）

```
- [ ] 1. 盤點候選筆記，用戶確認範圍
- [ ] 2. Read 全部筆記內容
- [ ] 3. 產出 MOC v0
- [ ] 4. 事實校正（若適用）
- [ ] 5. 用戶 Checkpoint：看 v0，決定是否迭代 / 手動改 / 直接停
- [ ] 6. Reviewer/Fixer 迴圈（每輪 review 都給用戶過目）
- [ ] 7. 與用戶確認原筆記處置方式（A/B/C）
- [ ] 8. 若選 B，更新 master-index
```
