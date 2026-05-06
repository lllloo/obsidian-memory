---
name: vault-reddit-sync
description: 抓取 Reddit 上 AI 相關的高訊號討論（工程實踐、工具方法論、模型比較、官方變更），分析其技術價值，並將有價值的貼文同步成 Obsidian 筆記。觸發時機：「查 Reddit」、「Reddit 同步」、「Reddit 分析」、「看看 Reddit 上的 AI 討論」、「抓 Reddit 文章」。不應觸發：查詢既有 vault 筆記、YouTube 頻道同步、非 Reddit 來源分析。
---

# Vault Reddit Sync

掃 `content/Inbox/Reddit/` 底下所有頻道資料夾，對每個訂閱 sub 抓一週 top 貼文，內容導向粗篩 + subagent 深入分析後存為 Obsidian 筆記。

> 本 skill 產出進入 `Inbox/Reddit/`，代表「待消化暫存」。使用者讀完後可自行歸檔至 `Cards/` 或 `Topics/`，Inbox 原篇刪除。Skill 只負責抓取與篩選，不負責消化。
>
> 採 **high precision** 策略：寧缺勿濫，不追求 coverage。單次同步目標是全體保留 **3-12 篇** 筆記；邊界模糊直接跳過，不靠留言硬撐成筆記。
>
> **訂閱題材**：訂閱 sub 應為 AI 工程實踐、工具方法論、模型討論、官方變更等高訊號社群（如 r/ClaudeCode、r/LocalLLaMA、r/codex、r/singularity、r/vibecoding 等）；不訂閱廣域非 AI 社群。
>
> **不依賴熱度**：fetch 僅用 `top week` 圈出候選池（過濾長尾雜訊）；篩選與價值判斷一律以「主貼是否含具體技術內容」為準，與 Reddit score 無關。

## 資料夾即訂閱清單

- 筆記存放：`content/Inbox/Reddit/<subreddit>/`
- **資料夾本身即訂閱清單**：skill 不 hardcode 任何 sub 名稱，啟動時掃 `Inbox/Reddit/*/01.index.md` 列出所有訂閱
- 每個 channel 資料夾必含 `01.index.md`（dedup graveyard 來源）與 `02.文章清單.base`（Bases 表格）
- 貼文筆記**不加 `parent:` 欄位**（Reddit 筆記無頻道圖譜需求）
- `Inbox/` 已在 `quartz.config.ts` 的 `ignorePatterns` 中，不會發佈到網站

### 新增/移除頻道（人為觸發）

新增頻道**不需改 skill**，跟主 agent 對話即可：

> 「幫我加 r/Foo」 → 主 agent 應用以下範本建立 `Inbox/Reddit/Foo/`：
>
> 1. `mkdir Inbox/Reddit/Foo/`
> 2. 建 `01.index.md`（見下方 channel index 範本）
> 3. 建 `02.文章清單.base`（見下方 base 範本）

訂閱原則：sub 須為 AI 工程實踐 / 工具方法論 / 模型討論 / 官方變更等高訊號社群。所有訂閱都全收 top week，無模式之分；廣域非 AI 社群（如 r/programming、r/news）不訂閱。

移除頻道：直接刪除整個 `Inbox/Reddit/<subreddit>/` 資料夾，下次同步自然忽略。

### Channel index 範本（`01.index.md`）

```markdown
---
title: Reddit/<subreddit>
created: <今日 YYYY-MM-DD>
updated: <今日 YYYY-MM-DD>
source: https://www.reddit.com/r/<subreddit>/
tags:
  - reddit
  - channel
---

r/<subreddit> AI 高訊號討論精選。

![[02.文章清單.base]]

## 已處理紀錄

> fetch dedup 用，請勿手動編輯。每行格式：`- <post_id> <YYYY-MM-DD>`。超過 14 天的條目由本 skill 自動修剪。
```

### Base 範本（`02.文章清單.base`）

```yaml
filters:
  and:
    - file.inFolder("Inbox/Reddit/<subreddit>")
    - file.ext == "md"
    - file.name != "01.index"
properties:
  published:
    displayName: 發文日期
  source:
    displayName: 連結
  file.name:
    displayName: 筆記
views:
  - type: table
    name: 文章清單
    order:
      - file.name
      - published
      - source
    sort:
      - property: published
        direction: DESC
```

## 前置作業（寫入前必做）

### Cwd 契約

本 skill 是 repo-local，所有讀寫路徑均為 repo root 相對的 `content/...`。呼叫前先確認 cwd 為 repo root：

```bash
[ -f "content/master-index.md" ] || { echo "ERROR: cwd 不在 repo root"; exit 1; }
```

### 寫入前 Checklist

此 skill 是 `content/` 的寫入路徑。寫入前依 `content/CLAUDE.md` 的「寫入前 Checklist」自檢：

- **敏感資料零容忍**：貼文正文（含 code block）若含 token / 私鑰 / API key → 移除該段，不寫入。Reddit selftext 常把 token 貼在 ``` fence 裡，**fence 內也要掃**，subagent 自掃為主、`scripts/vault-check.mjs` 作為兜底（已對 `content/Inbox/**` 啟用 fence 內掃描）
- **Tag 沿用既有**：`reddit` 以外的主題 tag 先 grep 既有 vault tags，避免同義異寫
- **Frontmatter schema**：欄位、順序、白名單以 `scripts/vault-schema.mjs` 為真實來源
- **命名**：檔名不含空格，不含 `?:;"'` 等特殊字元

## 步驟 1：列舉訂閱頻道

掃 `content/Inbox/Reddit/` 底下所有含 `01.index.md` 的子資料夾。實作建議：用 Glob 列出 channel index 路徑，sub 名稱直接取資料夾名（不需 parse frontmatter）：

```
Glob: path="content/Inbox/Reddit", pattern="*/01.index.md"
sub 名 = 該檔的父資料夾名
```

**若 `Inbox/Reddit/` 為空或無任何 `01.index.md`**：輸出「尚未訂閱任何 Reddit 頻道，請先建立 channel index（見『新增/移除頻道』段）」並中止。**不 bootstrap 預設頻道**——資料夾即訂閱清單，零頻道 = 無事可做。

## 步驟 2：抓取 Reddit 貼文清單

把步驟 1 列出的 sub 名直接傳給 fetch script，全收 `top.json?t=week&limit=50`：

```bash
if command -v python3 >/dev/null 2>&1; then
  python3 .claude/skills/vault-reddit-sync/scripts/fetch_reddit.py ClaudeCode LocalLLaMA codex ...
else
  python  .claude/skills/vault-reddit-sync/scripts/fetch_reddit.py ClaudeCode LocalLLaMA codex ...
fi
```

> top week 而非 top day：當日榜偏 meme / 抱怨；一週時窗讓深度技術文有時間冒上來。
>
> 不做 endpoint 層的關鍵詞過濾——訂閱的 sub 本身就應為 AI 高訊號社群，全收即可；題材匹配與品質判斷在後續粗篩與 subagent 分析階段做。

解析輸出：

- `META:<subreddit>|||<post_count>` → 各 subreddit 抓取摘要（供最後統計使用）
- `POST:<post_id>|||<subreddit>|||<score>|||<num_comments>|||<title>` → 每行一篇貼文
- `ERROR:<subreddit>:<message>` → 記錄錯誤並繼續處理其他 subreddit（**不全停**）

> 組成貼文 URL：`https://www.reddit.com/r/<subreddit>/comments/<post_id>/`

## 步驟 3：Graveyard 去重 + 內容導向粗篩

對每個 subreddit 分別執行。

### Graveyard 去重

讀取 `content/Inbox/Reddit/<subreddit>/01.index.md` 的「## 已處理紀錄」段，擷取所有 post_id：

```bash
INDEX="content/Inbox/Reddit/<subreddit>/01.index.md"
[ -f "$INDEX" ] && \
  awk '/^## 已處理紀錄/{flag=1; next} /^## /{flag=0} flag' "$INDEX" \
  | grep -oE '^- [a-z0-9]+ ' | awk '{print $2}'
```

把步驟 2 輸出中已在 graveyard 的 post_id 過濾掉。

- 若 graveyard 為空（首次同步或剛建頻道）：所有候選都算新
- 過濾後若無新候選：輸出「無新貼文」並跳過該 subreddit

> Graveyard 是**唯一** dedup 來源（不再 grep source URL）。前提：所有 Reddit 筆記都透過此 skill 建立。若曾手動建 Reddit 筆記，需手動把 post_id 加進 graveyard。

### 內容導向粗篩

**保留（送 subagent）需符合下列任一**：

- selftext 含 code block（`三反引號`）
- selftext 含具體路徑、flag 或指令樣本（`/`、`.md`、`--`、`~/`、`npm `、`git `、`claude `、`pip `、`docker ` 等）
- 標題或 selftext 含技術關鍵詞：`workflow` / `workaround` / `bug` / `fix` / `MCP` / `hook` / `skill` / `subagent` / `config` / `prompt` / `cache` / `context` / `model` / `API` / `rate limit` / `token`
- selftext 長度 ≥ 200 字（純文字長文較可能含方法論）

**直接跳過（不看分數）**：

- selftext < 50 字且無 code block（單行感嘆 / 求援 / showcase）
- 標題明顯抱怨 / 焦慮類：`suspended` / `banned` / `pricing` / `billing` / `refund` / `support` / `customer service`（除非含具體技術現象 + 重現步驟）
- **時效性新聞 / 行情變動**：標題主軸是「半年後失效」的內容，除非 selftext 已命中上方「保留」清單第 1 條（含 code block）或第 2 條（含具體路徑 / 指令）。常見模式：
  - Plan / pricing / billing 變動：`plan change`、`new multiplier`、`(usage|tier|billing) (change|update)`、`pricing (cut|nerf|raise)`、`(\d+)x plan`
  - 模型發布 / 下架 / 替換：`(release|launch|drops?|out now|announce|unveil) (gpt|claude|gemini|qwen|deepseek|llama|gemma|opus|sonnet|haiku)`、`(deprecat|removed|sunset|discontinu)`、`replac.*model`
  - 跨模型 benchmark / vs 對比：`\bvs\b`、`benchmark`、`comparison`、`outperform`（涉及具體模型名）
  - 額度 / 限制 / cost shock：`(\d+-?(hour|day|week)) limit`、`cost shock`、`(rate|usage) limit (raised|cut|changed)`、`shrink.*limit`、`token tracker`
- meme / image-only post（標題含 `[image]` / `[meme]`，或 selftext 為空且無外部 URL）
- 純展示 / showcase / vibecoding 成果，無方法論
- 個人使用心得 / 偏好投票 / 泛問答
- 主要價值來自留言、而非主文本身
- 主題與 AI 工程 / 工具 / 模型完全無關（即使在 AI sub 偶爾出現）

> Reddit `score` 與 `num_comments` 可作為輔助訊號（高分 + 留言深 → subagent 多看一眼留言區），**但不是 gate**。score 0-50 的好技術文多得是。

**直接跳過的貼文** → 加入步驟 5 graveyard pending list，標 `skip:粗篩-<原因>`。下次 fetch 時不重複粗篩。

## 步驟 4：分批平行處理貼文

將**通過主貼粗篩**的貼文合併，按每批 5-6 篇，在**同一個 response** 中用 Agent tool 平行啟動所有 subagents。跨 subreddit 的 subagents 可直接平行（無相依性）。

若候選仍過多，先按以下優先級排序，只送最值得分析的一批：

1. 可重現 bug / workaround
2. 具體 workflow / commands / files / prompt / config
3. 官方變更且有 operational impact
4. 有量化結果的工具 / 模型比較

**目標上限：每個 subreddit 最多保留 4 篇，全體最多保留 12 篇。**

每個 subagent 的任務 prompt 格式如下。**所有 `<...>` 占位符，主 skill 端必須在送出前全部替換為實際值**（subreddit 帶入、subreddit-tag 從資料夾名 normalize 取得、日期填上），不要把未替換的 `<…>` 傳給 subagent。subagent cwd 必為 repo root，所有路徑為 repo root 相對：

```
任務：分析 Reddit 貼文的技術價值，並在 Obsidian vault 建立有價值貼文的筆記。
詳細指示請先 Read `.claude/skills/vault-reddit-sync/references/post-analyzer.md`。

NOTES_DIR：content/Inbox/Reddit/<subreddit>/
今日日期：<YYYY-MM-DD>
Subreddit：<subreddit>

**貼文清單（處理第 N-M 篇）：**
N. [score:<分數> comments:<留言數>] <標題>
   ID: <post_id>
   URL: https://www.reddit.com/r/<subreddit>/comments/<post_id>/
...

**回傳格式**：每篇一行 `<post_id> save|skip <一行原因>`，供主 skill 端整理 graveyard。
```

## 步驟 5：彙整結果 + 更新 Graveyard

輸出彙整表格：

| #   | Subreddit    | 貼文標題 | 筆記路徑                      | 狀態                      |
| --- | ------------ | -------- | ----------------------------- | ------------------------- |
| 1   | <subreddit>  | ...      | Inbox/Reddit/<subreddit>/...  | ✓ 已存                    |
| 2   | <subreddit>  | ...      | —                             | ⏭ 主貼粗篩跳過（純抱怨） |

### 更新 Graveyard

對每個 subreddit 把本次處理的所有 post_id 寫入 `01.index.md` 的「## 已處理紀錄」段，**無論 save、subagent skip、主貼粗篩 skip 都記**。

- 條目格式：`- <post_id> <YYYY-MM-DD>`（日期 = 處理日，今日）
- 寫入「## 已處理紀錄」段下方
- 同 post_id 重複時覆蓋日期（取最新）
- **修剪**：刪除超過 14 天的條目（`today - entry_date > 14`）

實作建議：用 Read + Edit 工具直接處理 `01.index.md`（不要用 bash heredoc + inline Python，shell 逃逸風險高）。流程：

1. Read `01.index.md`
2. 解析「## 已處理紀錄」段現有條目
3. 加入本次新條目（save / skip 全部），同 ID 取新日期
4. 過濾掉超過 14 天的條目
5. 依日期 desc 排序
6. Edit 替換整段（標題 + blockquote 說明保留）
7. 同步把 frontmatter `updated` 改成今日

對每個訂閱 subreddit 各執行一次。

### 總結報告

- 各 subreddit 抓取數 / 通過粗篩數 / 存入數
- 跳過原因分布（主貼粗篩 / subagent 評估後）
- 本次 top 3 最高價值貼文（含一行摘要）

若 subagents 回傳 `saved` 超過上限，主 skill 端需依步驟 4 的優先級**二次淘汰**，多出的筆記立即刪除，不保留「也許之後有用」的低信號篇。**被淘汰的 post_id 仍要寫入 graveyard（標 skip），避免下次重複處理。**

## 注意事項

- **Reddit API rate limit**：一次請求 limit=50，fetch 失敗時最多重試 2 次（間隔 3s），不要短時間大量重試
- **跨工具視角全收**：訂閱 sub 涵蓋多種 AI 工具（Claude、Codex、Copilot、本地 LLM 等），不偏袒任何一家——只要主貼有可遷移的工程方法論、bug 重現、或量化比較，就算 save，工具無關
- **tags**：一律加 `reddit`，加 subreddit 對應 tag（從資料夾名 normalize：CamelCase 轉 kebab-case，如 `ClaudeCode`→`claude-code`、`LocalLLaMA`→`local-llama`、`codex`→`codex`、`vibecoding`→`vibecoding`）；依貼文主題可額外加（先 grep 既有 vault tags 確認用法）
- **published 欄位**：來自 `data.created_utc`（Unix timestamp），subagent 用 `datetime.fromtimestamp(ts, tz=datetime.timezone.utc)` 轉換（避免 Python 3.12+ deprecation）
- **檔名長度**：超過 40 字元適當縮短，保留關鍵詞
- **不發佈**：`content/Inbox/Reddit/` 已在 ignorePatterns，無需加 `draft: true`
- **Graveyard 是唯一 dedup 來源**：不再 grep source URL；所有 Reddit 筆記應透過此 skill 建立。若曾手動建 Reddit 筆記，需手動把對應 post_id 加進 graveyard
- **Graveyard 14 天時窗**：top.json `t=week` 不會回傳超過 7 天的文，14 天緩衝足夠覆蓋一輪；超過自動修剪避免無限增長
- **本次無新貼文**：若某 subreddit graveyard 過濾後為空，輸出「無新貼文」並跳過，不影響其他 subreddit
