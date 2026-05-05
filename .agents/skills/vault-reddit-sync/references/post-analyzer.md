# Subagent：Reddit 貼文分析與 Obsidian 筆記建立

> **路徑契約**：任務 prompt 會傳入 `NOTES_DIR`（絕對路徑到 `<vault>/Inbox/Reddit/<subreddit>/`）。所有讀寫操作一律以 `NOTES_DIR` 為 base，不可用 cwd-relative 路徑。
>
> **NOTES_DIR 自檢**：開工前確認 `NOTES_DIR` 值已被主 skill 展開。若值包含字面 `<`、`>`、或 `$OBSIDIAN_VAULT_ROOT` 字樣（代表占位符未替換），視為主 skill 傳錯，**立即回報並停止**，不寫入任何檔案。

## 步驟

對每篇貼文，依序執行：

### 步驟 0：重複偵測（先做）

在分析內容前，確認此貼文尚未有對應筆記：

```bash
grep -rl "comments/<post_id>/" "<NOTES_DIR>" 2>/dev/null
```

若有任何輸出，**跳過此貼文**，回報「⏭ 已有筆記，跳過」。

### 步驟 1：抓取貼文完整內容

呼叫 `fetch_post.py`（已處理 UTF-8 / retry / selftext truncate / control char escape，**不要**自行 inline curl + heredoc python，與 SKILL.md 步驟 5 的禁令一致）：

```bash
if command -v python3 >/dev/null 2>&1; then
  python3 .claude/skills/vault-reddit-sync/scripts/fetch_post.py <subreddit> <post_id>
else
  python  .claude/skills/vault-reddit-sync/scripts/fetch_post.py <subreddit> <post_id>
fi
```

輸出格式（每行 `KEY:value`，selftext 用 BEGIN/END 包多行）：

```
TITLE:<標題>
SCORE:<分數>
NUMCOMMENTS:<留言數>
URL:<外部連結，selftext post 為 reddit 連結>
PERMALINK:</r/...>
CREATED:<YYYY-MM-DD>
SELFTEXT_LINES:<行數>
SELFTEXT_TRUNCATED:<true|false>
SELFTEXT_BEGIN
<原文，可多行>
SELFTEXT_END
COMMENT:<score>|||<已 collapse 為單行的留言；上限 500 字>
...（最多 5 條）
```

`SELFTEXT_TRUNCATED:true` 代表原文超過 4000 字已截斷；做筆記時優先抓出方法論／可重現步驟，不要試圖逐行翻譯。失敗會輸出 `ERROR:<msg>` 且 exit 1，此貼文跳過進入下一篇。

### 步驟 2：價值判斷

根據以下規則決定是否建立筆記。價值判斷與 score 無關——**`score` 只是輔助訊號**（高分 + 留言深 → 多看一眼留言區），不是 gate。

**跳過（低價值 / 預設）：**

- 純圖片、meme、showcase、vibecoding 成果展示；若無可重現 workflow / repo 做法 → 跳過
- 純讚美、泛問答、偏好投票、個人使用心得
- pricing / plan / support / suspension / customer service / trust / privacy 類抱怨，若無具體技術做法
- **時效性新聞**（半年後失效類）：
  - Plan / pricing / billing / quota 變動
  - 特定模型發布 / 下架 / 替換亮點
  - 跨模型 benchmark / vs 對比（含具體模型版本與數字）
  - 5-hour limit / token tracker / cost shock 等行情類
  - **例外**：若貼文核心是「在 X 限制下的可遷移**方法論**」（如 routing 策略、降低 token cost 的 prompt 設計、limit-aware workflow），可保留 — 但筆記只記方法論本身，**不抄具體模型名 / plan 名 / 行數價格**（這些半年後會失效）
- Bug 回報但沒有重現步驟、沒有 workaround、沒有明確 context
- 主題與 AI 工程 / 工具 / 模型完全無關（例：純 Reddit drama、政治、生活雜談）
- **價值主要來自留言而非主文** → 跳過；留言只能加強判斷，不能單獨救一篇文

**保留（高價值），需符合下列高信號條件之一：**

- 可重現 bug + root cause / workaround / fix（任何 AI 工具皆可）
- 技術工作流、prompting 技巧、AI 工具使用方式（Claude / Codex / Copilot / Cursor / 本地 LLM 等），且含具體步驟、檔案、指令、設定或 repo 結構
- 官方變更 / connector / model policy change（任何 AI 廠商），且會直接影響實際使用
- 工具或模型比較，且含明確測試設定、數據或可驗證結果

**若是 link/demo post：**

- 只有在連出去的 repo / docs / article 本身提供可重用做法時才保留
- 只有「作品很酷」但沒有方法論 → 跳過

**判斷模糊時，傾向跳過**而非強行建立低品質筆記。

跳過時回報：「⏭ [原因] 跳過：<標題>」（如「⏭ 純讚美，無技術細節，跳過」）。

### 步驟 3：建立筆記

通過價值判斷後建立筆記。

**檔名規則：**

- 以英文標題為主，技術名詞保留英文；標題為中文則保留中文
- 不含空格（空格改 `-`），不含 `?:;"'` 等特殊字元
- 不超過 40 字元，截斷時保留關鍵詞
- 範例：`Claude-Code-parallel-subagents-tip.md`、`LocalLLaMA-quantization-bench.md`、`Codex-CLI-config-walkthrough.md`

**Frontmatter（嚴格遵守 `scripts/vault-schema.mjs` 欄位順序，無 `parent:` 欄位）：**

```yaml
---
title: <貼文標題，英文原文保留，中文為主則保留中文>
created: <今日 YYYY-MM-DD>
updated: <今日 YYYY-MM-DD>
source: https://www.reddit.com<permalink>
published: <created_utc 轉換的 YYYY-MM-DD>
tags:
  - reddit
  - <subreddit-tag>
---
```

subreddit tag 從資料夾名 normalize 取得：CamelCase 轉 kebab-case，全小寫。範例：

- `ClaudeCode` → `claude-code`
- `GithubCopilot` → `github-copilot`
- `vibecoding` → `vibecoding`
- `codex` → `codex`

依貼文主題可額外加：`workflow`、`ai-tools`、`bug`、`best-practices`、`mcp`、`subagent`、`hook` 等（先 grep 既有 vault tags 確認用法一致）。

**正文結構：**

```markdown
> **繁中摘要**：<一到兩句說明本貼文核心價值，技術名詞保留英文>

---

## 原文重點

<依貼文實際內容整理，條列或短段落；不補充推測；具體指令/設定/數值用 code block>

## 社群討論亮點

<從 top comments 中選有技術資訊的 1-3 點條列；純聊天或純讚美的留言跳過>
```

若 selftext 為空（link post 或純圖）：

```markdown
> **繁中摘要**：<一到兩句>

---

## 連結

<URL>

## 社群討論亮點

<同上>
```

### 步驟 4：確認檔案存在 + 回報格式

每個 save 的筆記建立後 `ls "<NOTES_DIR>/<檔名>.md"` 確認檔案存在。

**全部完成後，每篇貼文回報一行**，供主 skill 端整理 graveyard：

```
<post_id> save <一行原因>
<post_id> skip <一行原因>
```

範例：

```
1svdm1w save HERMES.md billing routing bug，含可重現步驟與官方確認
1sv6m1o skip 純偏好投票討論，無技術細節
1sv7k80 save knowledge graph for Claude，含 repo 結構與實作細節
```

不論 save 或 skip 都要回報——主 skill 端會把每個 post_id 寫入 graveyard，避免下次重複處理。

## 筆記規則補充

- `#` 開頭字串（hex 色碼等）在 Obsidian 會被當 tag，**必須用反引號包住**
- 敏感資料零容忍：正文若含 `sk-ant-`、`ghp_`、`AKIA` 等 token pattern → 移除該段
- 不使用 `# ` heading（Quartz 從 frontmatter title 自動產生）
- `tags` 必須 YAML list（`- tag`），不用 inline array
