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

- 主貼粗篩跳過：<數量>（<主要原因分布>）
- 分析後跳過：<數量>（<主要原因分布>）
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

主流程此時只有 `fetch_reddit_daily.py` 回傳的標題、score、comment 數，**不要使用 selftext 條件做 gate**。selftext / comments 的完整判斷交給步驟 4 的 subagent 透過 `fetch_post.py` 處理。

**送 subagent 的 title-level 預篩條件**：

- 標題含技術關鍵詞：`workflow` / `workaround` / `bug` / `fix` / `MCP` / `hook` / `skill` / `subagent` / `config` / `prompt` / `cache` / `context` / `model` / `API` / `rate limit` / `token` / `memory` / `worktree` / `agent`
- 標題暗示具體工具、repo、設定或方法：`AGENTS.md`、`Claude.md`、`rules`、`CI`、`Docker`、`VS Code`、`Copilot`、`Codex`、`Claude Code`
- comment 數高且標題與 AI 工程 / 工具使用相關，值得讓 subagent 抓全文確認
- score 低但標題明確指向 bug、workflow、成本控制、context 管理、parallel agents 等高訊號題材

**直接跳過**：

- 標題明顯是純抱怨、pricing / billing / support / suspension，且沒有 bug / workflow / workaround / config 等技術訊號
- 純時效新聞、模型發布、額度變動、行情類 benchmark，且標題沒有可遷移方法論訊號
- meme / image-only / showcase / 偏好投票 / 泛問答
- 主題與 AI 工程 / 工具 / 模型完全無關

通過預篩的貼文由 subagent 抓全文後做最終 `KEEP` / `SKIP` 判斷。直接跳過與 subagent skip 都不寫入 vault；下次重跑可重新評估當日列表。

## 步驟 4：分批平行分析貼文

將通過粗篩的貼文合併，按每批 5-6 篇，用 Agent tool 平行啟動 subagents。

若候選過多，依以下優先級只送最值得分析的一批：

1. 可重現 bug / workaround
2. 具體 workflow / commands / files / prompt / config
3. 官方變更且有 operational impact
4. 有量化結果的工具 / 模型比較

每個 subagent prompt：

```text
任務：分析 Reddit 貼文的技術價值，回傳可放入每日 Reddit 日報的精簡條目；不要建立獨立貼文筆記。
詳細指示請先 Read `.claude/skills/vault-reddit-daily-report/references/report-analyzer.md`。

今日日期：<YYYY-MM-DD>

貼文清單：
1. [score:<分數> comments:<留言數>] <標題>
   ID: <post_id>
   Subreddit: <subreddit>
   URL: https://www.reddit.com/r/<subreddit>/comments/<post_id>/
```

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
