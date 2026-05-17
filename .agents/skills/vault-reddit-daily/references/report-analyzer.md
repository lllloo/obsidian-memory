# Subagent：Reddit 日報條目分析（社群動態 briefing 版）

> **任務契約**：只分析貼文並回傳日報條目，不建立獨立貼文筆記，不更新 graveyard，不寫檔。主 skill 端負責組裝 `Inbox/RedditDaily/Reddit日報-YYYY-MM-DD.md`。

## 定位提醒

日報是**每日社群動態 briefing**，不是技術文章彙整。Reddit 是討論型社群，內容本質是「社群當天在關注什麼」——含工具新知、行為觀察、熱議與爭議、抱怨潮、爭議言論。

**不要用「技術文章」標準篩選**——若用嚴格 repro / 量化標準，大量真實的社群動態會被誤殺（例如「Opus 今天變笨了」是趨勢訊號、「Anthropic 又限額」是社群事件，雖無 repro 但有意義）。

**價值判斷與 score 無關**，score 只作輔助訊號；comment 數比 score 更能反映「集體討論」的程度。

## 步驟 1：抓取貼文完整內容

呼叫既有 Reddit 貼文抓取腳本：

```bash
if command -v python3 >/dev/null 2>&1; then
  python3 .claude/skills/vault-reddit-daily/scripts/fetch_post.py <subreddit> <post_id>
else
  python  .claude/skills/vault-reddit-daily/scripts/fetch_post.py <subreddit> <post_id>
fi
```

若抓取失敗，回傳 `SKIP`。

## 步驟 2：分類判斷

對每篇貼文先判定**屬於哪一類動態**，再決定 KEEP / SKIP。

### 三大保留類型

**A. 工具與模型新知（priority 多為 high）**

- 新工具 / repo / plugin / skill 發布
- 新版本 / 新功能 / 新 connector / 新 endpoint
- 官方公告（Anthropic / OpenAI / GitHub 等）
- 模型發布 / 下架 / quota 政策變更
- 即使只是 link post 含 demo / 截圖，只要對社群有實際使用影響都保留

**B. 行為觀察與工作流（priority 多為 medium）**

- 模型行為變化的個人觀察（「Opus 4.7 更技術化」、「context 撐不久」、「Codex 找不到 bug 會編造」）—— 不要求嚴格 repro
- Prompt / config / 工作流分享（即使無完整 repo，分享心得本身就是訊號）
- 工具或模型比較（含主觀「feels better」，社群感受本身就是動態）
- 對既有功能的批評但具體（指出設計缺陷、UX 問題）

**C. 熱議與爭議（priority 多為 medium）**

- 引發大量留言的觀點 / 爭議（comments > 30 通常表示有集體共鳴）
- 抱怨潮：多人共鳴的計費、quota、限額抱怨——是社群事件不是純情緒
- 政策爭議（usage reset、pricing change、cybersecurity false positive）
- 社群分歧（「應該禁 X 類貼文嗎」、「Y 比 Z 好」之類引發辯論）

### 跳過範圍（縮減版）

仍跳過的只有：

- **純 meme / image-only / 無文字內容**：純圖片梗無實質討論，且 selftext 為空
- **純個人客服 / 帳號故障**：SMS verification、login fail、單人 billing 問題（沒有集體共鳴 = 不是動態）
- **純 showcase 無社群討論**：「我做了個 X」但內容只貼截圖、無工具名 / 採用情境 / 工作流，且 comments < 5
- **與 AI 工程 / 工具 / 模型完全無關**：旅遊、政治、寵物等
- **fetch 失敗無法判讀**

**邊界判斷原則**：

- comments 多 + 抱怨型 → KEEP（集體事件，C 類）
- comments 少 + 抱怨型 + 純情緒 → SKIP（個人發洩）
- comments 多 + showcase → KEEP（社群有討論，B 或 C 類）
- comments 少 + showcase + 無方法 → SKIP（純自家曬圖）

## 步驟 3：回傳格式

每篇貼文都必須回傳 `KEEP` 或 `SKIP`。

`KEEP`：

```markdown
KEEP <post_id>
title: <貼文標題>
subreddit: <subreddit>
url: https://www.reddit.com/r/<subreddit>/comments/<post_id>/
published: <YYYY-MM-DD>
section: news | observation | debate
summary: <繁中 1-2 句摘要，技術名詞保留英文；不要補充推測；若是 link post，描述外連內容的核心點>
reference: <使用者打開原文時應優先看的點：通常是留言區的共鳴、外連 repo / docs、或主文的 key 段落>
priority: high | medium | low
```

**section 對應日報三節**：

- `news` → 工具與模型新知
- `observation` → 行為觀察與工作流
- `debate` → 熱議與爭議

**priority 判定**：

- `high`：官方新訊息、新工具發布、引發社群熱議的核心話題（comments > 50）、值得 vault 內化的具體做法
- `medium`：行為觀察、工作流分享、工具比較、有共鳴的抱怨潮
- `low`：邊緣相關但仍記錄一筆即可

`SKIP`：

```markdown
SKIP <post_id>
title: <貼文標題>
subreddit: <subreddit>
url: https://www.reddit.com/r/<subreddit>/comments/<post_id>/
reason: <一行跳過原因，使用上面「跳過範圍」的分類詞>
```

## 安全規則

- 敏感資料零容忍：正文或留言若含 `sk-ant-`、`ghp_`、`AKIA` 等 token pattern，不可進入摘要；若貼文核心依賴敏感內容，直接 `SKIP`
- 不大段引用原文；摘要只寫判讀與指路
- `#` 開頭字串若出現在摘要中，必須用反引號包住，避免 Obsidian 當成 tag
