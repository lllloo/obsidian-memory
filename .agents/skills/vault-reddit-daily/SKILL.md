---
name: vault-reddit-daily
description: 每天整理 Reddit AI 工程社群動態成一篇 Obsidian briefing，採 broad coverage 策略（目標保留 8-15 則、上限 20），涵蓋工具新版、官方變更、模型行為觀察、熱議與爭議，每則附原文連結。使用時機：使用者要求「Reddit 日報」、「整理今天 Reddit」、「AI Reddit 近況」、「Reddit 動態」、「給我 Reddit 摘要」，或直接呼叫 /vault-reddit-daily。
disable-model-invocation: true
---

# Vault Reddit Daily Report

Reddit 社群動態 briefing。自帶 subreddit 訂閱清單，不讀 `Inbox/Reddit/`，不建立逐篇 Reddit 筆記，只建立或更新每日一篇社群動態 briefing。

> 產出進入 `Inbox/RedditDaily/`，代表「每日社群動態快照」。日報整理當日 Reddit 在 AI 工程相關 sub 的討論熱度、工具新知、官方變更與行為觀察，每則保留原文連結；使用者讀完掌握社群當天的氛圍與焦點，需要深入的內容自行抽到 `Cards/` 或 `Topics/`，日報本身可刪除。
>
> 採 **broad coverage but selective** 策略：單日日報目標保留 **8-15 則**，最多 20 則。重點是「掃過知道今天社群在討論什麼」，**不是「找可重現 bug 或技術文章」**。Reddit 是討論型社群，不是技術文獻來源；保留範圍包含官方新訊息、工具發布、行為觀察、熱議與抱怨潮（集體事件本身就是訊號），跳過範圍限於純 meme、純個人 showcase、純個人客服故障。

## 與 vault-updates-daily 的分工

- `vault-updates-daily`：同步官方 changelog / release notes、GitHub releases、GitHub issues / discussions，建立高信任來源筆記
- `vault-reddit-daily`：讀 `Inbox/RedditDaily/01.index.md` 的訂閱清單，抓當日 top，彙整成一篇 `Inbox/RedditDaily/Reddit日報-YYYY-MM-DD.md`，記錄當日**社群動態、工具新知、行為觀察、熱議爭議**（廣度導向）
- `RedditDaily` 不維護 persisted dedup；同一天重跑覆蓋日報，不影響官方 / GitHub 更新同步流程

## 產出格式

- 日報路徑：`content/Inbox/RedditDaily/Reddit日報-<YYYY-MM-DD>.md`
- 訂閱來源：`content/Inbox/RedditDaily/01.index.md`
- `Inbox/RedditDaily/` 是獨立日報資料夾，不放在 `Inbox/Reddit/` 底下

日報 frontmatter：

```yaml
---
title: Reddit 日報 <YYYY-MM-DD>
created: <今日 YYYY-MM-DD>
updated: <今日 YYYY-MM-DD>
source: https://www.reddit.com/
tags:
  - reddit
  - daily
---
```

日報正文：

```markdown
> 今日 Reddit AI 工程社群動態 briefing。每則附原文連結，供後續判讀與延伸整理。

## 今日重點

> 2-5 條 themed bullets，每條 1-2 句，鎖定「社群當天在關注什麼」而非「有什麼好文」；每條圍繞一個主題（quota / 模型政策 / workflow / 爭議）或一個 subreddit，避免重複條目。

- <主題 1：1-2 句>
- <主題 2：1-2 句>
- <可選：再 1-3 條>

## 工具與模型新知

> 新工具發布、新版本、官方變更、連接器更新、新功能上線。subagent priority=high 多落在這節。

### 1. <貼文標題>

- Subreddit：r/<subreddit>
- 連結：<https://www.reddit.com/r/<subreddit>/comments/<post_id>/>
- 摘要：<繁中 1-2 句，技術名詞保留英文，不補充推測>
- 可參考點：<打開原文時優先看的內容>

## 行為觀察與工作流

> 模型行為變化、Prompt / config 心得、工作流分享、社群普遍觀察到的現象。即使無嚴格 repro 也保留。

### 1. <貼文標題>

（同上格式）

## 熱議與爭議

> 抱怨潮、社群分歧、引發大量留言的觀點、官方政策爭議。集體事件本身就是訊號。

### 1. <貼文標題>

（同上格式）

## 跳過摘要

| Subreddit | 抓取 | 粗篩通過 | 收錄 |
| --------- | ---- | -------- | ---- |
| <name>    | <N>  | <N>      | <N>  |

抓 <總抓取> → 粗篩通過 <總通過> → 收錄 <總收錄>。
```

若當日沒有任何可保留貼文，仍建立日報，正文寫明「今日無高訊號動態」，並附各 subreddit 抓取數與主要跳過原因。三個分節若該節無條目，可省略；不要產出空節。

## 前置作業

```bash
[ -f "content/master-index.md" ] || { echo "ERROR: cwd 不在 repo root"; exit 1; }
```

寫入前依 `content/CLAUDE.md` 的「寫入前 Checklist」自檢。本 skill 高頻踩雷點：tags 固定 `reddit`/`daily`；日報檔名固定 `Reddit日報-YYYY-MM-DD.md`。

## 步驟 1：讀取 RedditDaily 訂閱頻道

讀取 `content/Inbox/RedditDaily/01.index.md` 的「## 訂閱頻道」段，擷取每行 `- <subreddit>`。

若 `content/Inbox/RedditDaily/01.index.md` 不存在，先建立含空訂閱清單的 index，再輸出「尚未訂閱任何 RedditDaily 頻道，請先在 `content/Inbox/RedditDaily/01.index.md` 的『訂閱頻道』段新增 subreddit」並中止。不 bootstrap 預設頻道。

Index 範本：

```markdown
---
title: Reddit Daily
created: <今日 YYYY-MM-DD>
updated: <今日 YYYY-MM-DD>
source: https://www.reddit.com/
tags:
  - reddit
  - daily
  - index
---

Reddit 每日日報訂閱 index。

## 訂閱頻道

- ClaudeCode
- codex
- GithubCopilot
- vibecoding
```

## 步驟 2：抓取當日 Reddit 貼文清單

把步驟 1 列出的 sub 名傳給本 skill 的 fetch script，全收 `top.json?t=day&limit=50`：

```bash
SCRIPT=$(find .agents/skills/vault-reddit-daily .claude/skills/vault-reddit-daily -name "fetch_reddit_daily.py" 2>/dev/null | head -1)
[ -z "$SCRIPT" ] && { echo "ERROR: fetch_reddit_daily.py not found"; exit 1; }
PY=$(command -v python3 || command -v python)
$PY "$SCRIPT" ClaudeCode LocalLLaMA codex ...
```

解析輸出：

- `META:<subreddit>|||<post_count>` → 各 subreddit 抓取摘要
- `POST:<post_id>|||<subreddit>|||<score>|||<num_comments>|||<is_self>|||<post_hint>|||<domain>|||<link_flair_text>|||<upvote_ratio>|||<title>` → 每行一篇貼文
- `ERROR:<subreddit>:<message>` → 記錄錯誤並繼續處理其他 subreddit

欄位語意：

- `is_self`：`true` = text post，`false` = link/image/video post
- `post_hint`：`image` / `hosted:video` / `rich:video` / `link` / `self` / 空（API 未回傳）
- `domain`：外連 domain（`i.redd.it` / `github.com` 等）或 `self.<sub>`
- `link_flair_text`：sub 自訂 flair（`Bug Report` / `Showcase` 等）；無則為空
- `upvote_ratio`：0.00–1.00，越接近 1 共識度越高；< 0.7 通常代表爭議或抱怨

貼文 URL：`https://www.reddit.com/r/<subreddit>/comments/<post_id>/`

## 步驟 3：本次執行內去重 + 預篩

`RedditDaily` 不寫入 persisted dedup。只在本次執行的記憶體中用 post_id 去重，避免同一次抓取中重複分析同一貼文。

主流程此時只有 `fetch_reddit_daily.py` 回傳的 metadata（標題 + 9 個欄位），**不要使用 selftext / 留言條件做 gate**。selftext / comments 的完整判斷一律交給步驟 4 的 subagent 透過 `fetch_post.py` 處理。

**分工原則**：步驟 3 只做「光看 metadata 就能 100% 確定可刷掉」的硬篩；任何模糊邊界（含可疑技術訊號、可疑數字、無法從 metadata 斷定主題）一律放行給 subagent。subagent 才做完整價值判斷。**這份清單與 `references/report-analyzer.md` 不重疊**——前者只看 metadata、後者看全文。

**新定位提醒**：日報抓「社群動態」不是「技術文章」。抱怨潮、行為觀察、爭議都是有效訊號（集體事件本身就有意義），只要不是純個人 / 純無內容雜訊，**寬鬆放行**。

### A. metadata 硬刷（事實型，命中即直刷）

- `post_hint == image` 或 `post_hint == hosted:video` 或 `post_hint == rich:video`（純圖片 / 影片貼文無文字討論）
- `domain` 屬媒體類：`i.redd.it`、`v.redd.it`、`imgur.com`、`i.imgur.com`、`youtube.com`、`youtu.be`、`streamable.com`
- `link_flair_text` 屬雜訊類（per-sub denylist，動態 briefing 縮減版）：
  - 通用：`Humor`、`Meme`、`Praise`（純讚美無內容）、`Showcase`（純自家成果）
  - r/vibecoding：`My Project`
  - r/GithubCopilot：`Help`（多為個人故障申訴，非集體事件）
- `upvote_ratio < 0.5`（多數人按噓，且 num_comments < 20）—— 純爭議無實質討論

**注意保留的 flair**：`Vent`、`Complaint`、`Limits`、`Bug Report` 不再 denylist——這些是社群情緒指標，當有共鳴（comments 多）時就是動態訊號。

note：`post_hint` 在 text post 為空，**不可單獨用「post_hint 為空」判斷**——要先看 `is_self`。

### B. 標題硬刷（語意型，metadata 沒命中再看標題）

- meme / 截圖梗圖（標題明顯如「look at this」「lol」「😭」「lmao」「nailed it」）
- 純粹的「我做了個 X」showcase，且標題未提到工具名 / 採用情境 / 適用工作流（純自家專案曬圖、無社群討論價值）
- 個人客服 / 帳號故障（標題明確指向：SMS verification、verification code、suspension、login、`I don't receive...`）—— 這是個人問題不是社群動態
- 主題與 AI 工程 / 工具 / 模型完全無關（旅遊、政治、寵物等）

**不在硬刷之列**（保留給 subagent 看內容判斷）：

- 抱怨型標題（`X is garbage`、`unusable`、`nerfed`）—— 若有共鳴是動態訊號，純個人發洩 subagent 會 SKIP
- 計費 / 限額話題（`limit`、`pricing`、`reset`）—— 官方政策變更或集體抱怨潮都屬動態
- 模型行為觀察（`X feels dumber`、`Y context fills quick`）—— 趨勢訊號

### C. 其餘一律放行

包含但不限於：含技術關鍵詞、提及具體工具或 repo、score 低但題材具體、comment 數高暗示集體事件、`link_flair_text` 是 `Discussion` / `Bug Report` / `Tutorial` / `Comparison` / `Limits` 等動態訊號。寧可多送幾篇給 subagent 篩，也不要在 metadata 層誤刷。

直接跳過與 subagent skip 都不寫入 vault；下次重跑可重新評估當日列表。

### 報告統計

跳過摘要表格內部用三個計數：抓取（fetch_reddit_daily 回傳數）、粗篩通過（A + B 未命中數）、收錄（最終 KEEP 數）。直接刷與步驟 4 上限二次淘汰的細節不入日報，僅內部追蹤。

## 步驟 4：分批平行分析貼文

**Batching 上限**：每批 5-6 篇，**最多 4 批、總候選上限 20 篇**。若粗篩通過數超過 20，依以下優先級二次淘汰至 20 篇以內：

1. **官方變更 / 新工具 / 新版本發布**（時效性新訊息，動態 briefing 的核心）
2. **集體事件**（comments 多 + score 高，反映社群當天關注焦點，含抱怨潮、爭議、共鳴型行為觀察）
3. **行為觀察 / 工作流分享**（個人觀察但題材具體，可作為趨勢訊號）
4. **具體 spec / config / plugin 架構分享**（深度內容仍保留）
5. **工具或模型比較**（含主觀比較，不再要求量化）
6. **可重現 bug / workaround**（不再排第一，但仍保留）

二次淘汰時：

- 優先保留 1-3 類（動態訊號）
- 同類內按 `score × num_comments` 大致排序（雙高代表討論熱度高）
- 跨 sub 適度分配，避免單一 sub 壟斷收錄

用 Agent tool（`subagent_type: "general-purpose"`）平行啟動 subagents，一次發出多個 Agent 呼叫於同一訊息中以實際並行。

**Subagent prompt 結構**（依 `~/.claude/rules/skill-writing.md`：references 全文嵌入，不叫 subagent 自己 Read）：

```text
任務：分析 Reddit 貼文的動態訊號（工具新知 / 行為觀察 / 熱議爭議），回傳可放入每日 Reddit 社群動態 briefing 的精簡條目；不要建立獨立貼文筆記，不寫任何檔。
詳細指示如下（references/report-analyzer.md 全文）：

---
<在此貼上 .claude/skills/vault-reddit-daily/references/report-analyzer.md 全文>
---

今日日期：<YYYY-MM-DD>

cwd：<repo root 絕對路徑>（已驗證）

貼文清單（本批 N 篇）：
1. [score:<分數> comments:<留言數>] <標題>
   ID: <post_id>
   Subreddit: <subreddit>
   URL: https://www.reddit.com/r/<subreddit>/comments/<post_id>/
...

請對每篇逐一執行 fetch_post.py、判斷、回傳 KEEP/SKIP 條目。最後合併所有條目以純文字輸出（每篇之間空一行），不要寫入任何檔案。
```

**Fallback（無 Agent tool 環境）**：主 agent 直接 Read `references/report-analyzer.md` 後，逐批序列執行同流程，產出相同 KEEP/SKIP 條目格式。

## 步驟 5：建立或更新每日報告

建立資料夾：`content/Inbox/RedditDaily/`

日報檔案：`Reddit日報-<YYYY-MM-DD>.md`

- 若檔案不存在：建立新日報
- 若檔案已存在：覆蓋整篇內容為本次最新結果，不附加重複條目
- 每則 `KEEP` 必須包含原文連結
- 若 `KEEP` 超過 20 則，主 skill 端依步驟 4 優先級二次淘汰；理想保留 8-15 則
- 三節（工具與模型新知 / 行為觀察與工作流 / 熱議與爭議）若該節無條目，省略整節，不要產出空 heading

## 步驟 6：總結

不更新任何 dedup index。若同一天重跑，步驟 5 會覆蓋當天日報。

最後輸出：

- 日報路徑
- 各 subreddit 抓取數 / 通過粗篩數 / 日報收錄數
- 跳過原因分布
- 本次 top 3 最高價值貼文（含原文連結）
