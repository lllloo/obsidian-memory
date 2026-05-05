# Subagent：Reddit 日報條目分析

> **任務契約**：只分析貼文並回傳日報條目，不建立獨立貼文筆記，不更新 graveyard，不寫檔。主 skill 端負責組裝 `Inbox/RedditDaily/Reddit日報-YYYY-MM-DD.md`。

## 步驟 1：抓取貼文完整內容

呼叫既有 Reddit 貼文抓取腳本：

```bash
if command -v python3 >/dev/null 2>&1; then
  python3 .claude/skills/vault-reddit-sync/scripts/fetch_post.py <subreddit> <post_id>
else
  python  .claude/skills/vault-reddit-sync/scripts/fetch_post.py <subreddit> <post_id>
fi
```

若抓取失敗，回傳 `SKIP`。

## 步驟 2：價值判斷

價值判斷與 score 無關，score 只作輔助訊號。

**跳過（預設）：**

- 純圖片、meme、showcase、成果展示，且無可重現做法
- 純讚美、泛問答、偏好投票、個人心得
- pricing / plan / support / suspension / customer service 類抱怨，且無具體技術做法
- 時效性新聞：plan、pricing、quota、特定模型發布 / 下架、token tracker、cost shock 等
- Bug 回報但沒有重現步驟、workaround、明確 context
- 主題與 AI 工程 / 工具 / 模型無關
- 價值主要來自留言而非主文

**保留：**

- 可重現 bug + root cause / workaround / fix
- 技術 workflow、prompting 技巧、AI 工具使用方式，且含具體步驟、檔案、指令、設定或 repo 結構
- 官方變更 / connector / model policy change，且會直接影響實際使用
- 工具或模型比較，且含明確測試設定、數據或可驗證結果
- link/demo post 的外部 repo / docs / article 本身提供可重用做法

判斷模糊時跳過。

## 步驟 3：回傳格式

每篇貼文都必須回傳 `KEEP` 或 `SKIP`。

`KEEP`：

```markdown
KEEP <post_id>
title: <貼文標題>
subreddit: <subreddit>
url: https://www.reddit.com/r/<subreddit>/comments/<post_id>/
published: <YYYY-MM-DD>
signal: <一行說明為什麼值得看>
summary: <繁中 2-4 句摘要，技術名詞保留英文；不要補充推測>
reference: <使用者打開原文時應優先看的點>
priority: high|medium|low
```

`SKIP`：

```markdown
SKIP <post_id>
title: <貼文標題>
subreddit: <subreddit>
url: https://www.reddit.com/r/<subreddit>/comments/<post_id>/
reason: <一行跳過原因>
```

## 安全規則

- 敏感資料零容忍：正文或留言若含 `sk-ant-`、`ghp_`、`AKIA` 等 token pattern，不可進入摘要；若貼文核心依賴敏感內容，直接 `SKIP`
- 不大段引用原文；摘要只寫判斷與指路
- `#` 開頭字串若出現在摘要中，必須用反引號包住，避免 Obsidian 當成 tag
