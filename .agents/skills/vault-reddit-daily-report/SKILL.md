---
name: vault-reddit-daily-report
description: 每天整理 Reddit 上 AI 相關高訊號討論成一篇 Obsidian 日報，提供每則原文連結供使用者參考。觸發時機：「Reddit 日報」、「每日 Reddit」、「今天 Reddit 有什麼」、「整理 Reddit 日報」、「AI Reddit 日報」、「給我 Reddit 每日摘要」。不應觸發：逐篇同步 Reddit 筆記（用 vault-reddit-sync）、查詢既有 vault 筆記、YouTube 同步、非 Reddit 來源分析。
---

# Vault Reddit Daily Report

參考 `vault-reddit-sync` 的篩選策略，但這是**獨立功能**：自帶 subreddit 訂閱清單，不讀 `Inbox/Reddit/`，不建立逐篇 Reddit 筆記，只建立或更新每日一篇日報。

> 產出進入 `Inbox/RedditDaily/`，代表「拋棄式待消化參考」。日報只做摘要、判斷與指路，每則都保留 Reddit 原文連結；使用者讀完後自行把有價值內容抽到 `Cards/` 或 `Topics/`，日報本身可刪除。
>
> 採 **high precision** 策略：寧缺勿濫，不追求 coverage。單日日報目標保留 **5-12 則**，最多 15 則；邊界模糊直接跳過。

## 與 vault-reddit-sync 的分工

- `vault-reddit-sync`：抓一週 top，分析後把高價值貼文各自存成 Obsidian 筆記
- `vault-reddit-daily-report`：讀 `Inbox/RedditDaily/01.index.md` 的訂閱清單，抓當日 top，分析後彙整成一篇 `Inbox/RedditDaily/Reddit日報-YYYY-MM-DD.md`
- `RedditDaily` 不維護 persisted dedup；同一天重跑覆蓋日報，不影響逐篇同步流程

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
> 今日 Reddit AI 工程討論摘要。每則附原文連結，供後續判讀與延伸整理。

## 今日重點

- <1-3 句總結今日共同趨勢或操作影響>

## 精選討論

### 1. <貼文標題>

- Subreddit：r/<subreddit>
- 連結：<https://www.reddit.com/r/<subreddit>/comments/<post_id>/>
- 訊號：<為什麼值得看>
- 摘要：<繁中 2-4 句，技術名詞保留英文，不補充推測>
- 可參考點：<打開原文時優先看的內容>

## 跳過摘要

| Subreddit | 抓取 | 粗篩通過 | 收錄 |
| --------- | ---- | -------- | ---- |
| <name>    | <N>  | <N>      | <N>  |

- 主貼粗篩跳過：<數量>（<主要原因分布，例：純抱怨 X / showcase Y / meme Z>）
- 分析後跳過：<數量>
  - <post_id>：<一行原因>
  - ...
```

若當日沒有任何可保留貼文，仍建立日報，正文寫明「今日無高訊號貼文」，並附各 subreddit 抓取數與主要跳過原因。

## 前置作業

### Cwd 契約

本 skill 是 repo-local，所有讀寫路徑均為 repo root 相對的 `content/...`。呼叫前先確認 cwd 為 repo root：

```bash
[ -f "content/master-index.md" ] || { echo "ERROR: cwd 不在 repo root"; exit 1; }
```

### 寫入前 Checklist

此 skill 是 `content/` 的寫入路徑。寫入前依 `content/CLAUDE.md` 的「寫入前 Checklist」自檢：

- **敏感資料零容忍**：貼文正文與留言若含 token / 私鑰 / API key，不寫入日報；若貼文核心依賴敏感內容，直接跳過
- **Frontmatter schema**：欄位、順序、白名單以 `scripts/vault-schema.mjs` 為真實來源
- **Tag**：日報固定使用 `reddit`、`daily`
- **命名**：日報檔名固定 `Reddit日報-YYYY-MM-DD.md`

## 步驟 1：讀取 RedditDaily 訂閱頻道

讀取 `content/Inbox/RedditDaily/01.index.md` 的「## 訂閱頻道」段，擷取每行 `- <subreddit>`。

若 `Inbox/RedditDaily/01.index.md` 不存在，先建立含空訂閱清單的 index，再輸出「尚未訂閱任何 RedditDaily 頻道，請先在 `Inbox/RedditDaily/01.index.md` 的『訂閱頻道』段新增 subreddit」並中止。不 bootstrap 預設頻道。

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
if command -v python3 >/dev/null 2>&1; then
  python3 .claude/skills/vault-reddit-daily-report/scripts/fetch_reddit_daily.py ClaudeCode LocalLLaMA codex ...
else
  python  .claude/skills/vault-reddit-daily-report/scripts/fetch_reddit_daily.py ClaudeCode LocalLLaMA codex ...
fi
```

解析輸出：

- `META:<subreddit>|||<post_count>` → 各 subreddit 抓取摘要
- `POST:<post_id>|||<subreddit>|||<score>|||<num_comments>|||<title>` → 每行一篇貼文
- `ERROR:<subreddit>:<message>` → 記錄錯誤並繼續處理其他 subreddit

貼文 URL：`https://www.reddit.com/r/<subreddit>/comments/<post_id>/`

## 步驟 3：本次執行內去重 + 標題預篩

`RedditDaily` 不寫入 persisted dedup。只在本次執行的記憶體中用 post_id 去重，避免同一次抓取中重複分析同一貼文。

主流程此時只有 `fetch_reddit_daily.py` 回傳的標題、score、comment 數，**不要使用 selftext 條件做 gate**。selftext / comments 的完整判斷一律交給步驟 4 的 subagent 透過 `fetch_post.py` 處理。

**分工原則**：步驟 3 只負責「光看標題就能 100% 確定可刷掉」的硬篩；任何模糊邊界（含可疑技術訊號、可疑數字、無法從標題斷定主題）一律放行給 subagent。subagent 才做完整價值判斷。**這份清單與 `references/report-analyzer.md` 不重疊**——前者只看標題、後者看全文。

**直接跳過（標題即可斷定）**：

- meme / image-only / 截圖梗圖（標題明顯如「look at this」「lol」「😭」「lmao」）
- 純讚美 / 純抱怨單句，且無任何工具名 / 工具行為描述（如「X is garbage」「WTF」「anyone else」）
- pricing / billing / suspension / SMS verification / 帳號登入問題（標題只談計費或客服）
- 純粹的「我做了個 X」showcase，且標題未提到方法、設定、規格或可重現做法
- 主題與 AI 工程 / 工具 / 模型完全無關（旅遊、政治、寵物等）

**其餘一律放行**——包含但不限於：含技術關鍵詞、提及具體工具或 repo、score 低但題材具體、comment 數高暗示有實質討論。寧可多送幾篇給 subagent 篩，也不要在標題層誤刷。

直接跳過與 subagent skip 都不寫入 vault；下次重跑可重新評估當日列表。

## 步驟 4：分批平行分析貼文

**Batching 上限**：每批 5-6 篇，**最多 3 批、總候選上限 18 篇**。若粗篩通過數超過 18，依以下優先級二次淘汰至 18 篇以內：

1. 可重現 bug / workaround
2. 具體 workflow / commands / files / prompt / config
3. 官方變更且有 operational impact
4. 有量化結果的工具 / 模型比較

二次淘汰時優先保留標題明確指向上述四類的貼文；同類內按 comment 數排序（comment 多通常代表有實質討論）。

用 Agent tool（`subagent_type: "general-purpose"`）平行啟動 subagents，一次發出多個 Agent 呼叫於同一訊息中以實際並行。

**Subagent prompt 結構**（依 `~/.claude/rules/skill-writing.md`：references 全文嵌入，不叫 subagent 自己 Read）：

```text
任務：分析 Reddit 貼文的技術價值，回傳可放入每日 Reddit 日報的精簡條目；不要建立獨立貼文筆記，不寫任何檔。
詳細指示如下（references/report-analyzer.md 全文）：

---
<在此貼上 .claude/skills/vault-reddit-daily-report/references/report-analyzer.md 全文>
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
- 若 `KEEP` 超過 15 則，主 skill 端依步驟 4 優先級二次淘汰

## 步驟 6：總結

不更新任何 dedup index。若同一天重跑，步驟 5 會覆蓋當天日報。

最後輸出：

- 日報路徑
- 各 subreddit 抓取數 / 通過粗篩數 / 日報收錄數
- 跳過原因分布
- 本次 top 3 最高價值貼文（含原文連結）
