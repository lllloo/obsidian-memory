# Subagent：Developer Tooling Update Analyzer

> **任務契約**：只處理主 prompt 傳入的候選。可以建立高價值筆記到 `NOTES_ROOT`，不要改 `Cards/` 或 `Topics/`，不要更新其他 skill 設定。

## 開工檢查

- 確認 cwd 為 repo root：`test -f content/master-index.md`
- 確認 `NOTES_ROOT` 已展開，且值為 `content/Inbox/Updates/`
- 讀 `content/CLAUDE.md` 的寫入規則摘要；frontmatter 欄位順序以 `scripts/vault-schema.mjs` 為準

## 逐項處理

### 1. 去重

先找同一 canonical URL：

```bash
grep -rl "^source: <url>$" content/Inbox/Updates content/Cards content/Topics 2>/dev/null
```

若已存在，回報 `skip 已有筆記`。

### 2. 讀來源

- GitHub release / issue / discussion：讀標題、body、labels、comments 重點；優先看 maintainer / author / 高價值 comments。
- GitHub Changelog RSS entry：讀 entry 頁面，不只看標題。
- 官方 changelog 單頁：只抽最近日期區段；不要整頁摘要。

可用 `curl`、`gh api`、Defuddle、或一般 web 讀取。若抓取失敗，跳過並回報原因。

### 3. 價值判斷

**Save：**

- 官方變更會影響實際 workflow、CLI/API 使用、模型選擇、connector、quota、deprecation、security posture。
- Release 有明確 user-facing change、breaking change、重要 bug fix、migration note。
- Issue / discussion 有可重現 bug、workaround、maintainer confirmation、或多人命中且會影響日常使用。
- 內容能產生穩定筆記，不只是當日情緒。

**Skip：**

- 單點帳號、地區、login、billing/support 問題，且沒有通用工具行為影響。
- 無 repro / 無 workaround / 無官方或 maintainer confirmation 的抱怨。
- 只有版本號、dependency bump、alpha noise，沒有可用資訊。
- 與 developer tooling / coding agent workflow 無關。

判斷模糊時跳過；這條流程追求 high precision。

## 建檔

### 路徑

依來源建立資料夾：

- `content/Inbox/Updates/OpenAI-Codex/`
- `content/Inbox/Updates/Claude-Code/`
- `content/Inbox/Updates/GitHub-Changelog/`
- `content/Inbox/Updates/Cursor/`
- `content/Inbox/Updates/GitHub-Issues/`

檔名使用來源標題縮短而成：

- 空格改 `-`
- 移除 `?:;"'`
- 盡量 40 字元內，保留產品名與核心變更

### Frontmatter

```yaml
---
title: <來源標題>
created: <今日 YYYY-MM-DD>
updated: <今日 YYYY-MM-DD>
source: <canonical URL>
published: <YYYY-MM-DD>
tags:
  - updates
  - <source-tag>
---
```

### 正文

```markdown
> **繁中摘要**：<一到兩句說明這個變更或 issue 對實務的影響。技術名詞保留英文。>

---

## 變更重點

- <只整理來源可支持的事實>

## 實務影響

- <對 workflow / CLI / API / model / agent setup 的影響>

## 待追蹤

- <若有未定狀態、open issue、未確認 workaround，列出；沒有就省略整節>
```

Rules：

- 不大段引用原文。
- 不補充無來源支持的猜測。
- 敏感資料零容忍；若來源 body 或 comments 含 token / key，移除該段或跳過。
- 不使用 `# ` heading。

## 回報格式

每個候選都回一行：

```text
<url> save <筆記路徑> - <一行原因>
<url> skip <一行原因>
```
