# Subagent：YouTube 影片轉 Obsidian 筆記

> **路徑契約**：任務 prompt 會傳入 `NOTES_DIR`（repo root 相對路徑：`raw/YouTube/<頻道名>/`）。所有讀寫以 `NOTES_DIR` 為 base，cwd 必為 repo root（subagent 繼承父 agent cwd）。腳本路徑一律從 repo root 起算的完整相對路徑（`.agents/skills/vault-youtube-sync/scripts/...`）。
>
> **NOTES_DIR 自檢**：開工前確認 `NOTES_DIR` 已被主 skill 展開。若含字面 `<`、`>` 或仍是占位符，視為傳錯，**立即回報並停止**，不寫入任何檔案。用 `Read CLAUDE.md` 確認 cwd 為 repo root。
>
> **工具取向**：搜尋／讀檔／寫檔一律用 harness-native 工具（`Grep`/`Read`/`Write`），不落 shell。抓取／處理外部內容（defuddle、transcript、影片頁面）走下方 Python 腳本，腳本內部已處理跨平台與編碼。

## 步驟

對每部影片依序執行步驟 0 → 1 →（依結果）2 / 2b → 3。任一步驟若決議「跳過此影片」即直接結束，進入下一部。流程刻意拆成多個 H3 子標題（不用編號清單），避免 markdown formatter 破壞層次。

### 步驟 0：重複偵測（先做）

用 **Grep** 搜尋 `NOTES_DIR` 是否已有對應此 videoId 的筆記：pattern `source: https://www.youtube.com/watch?v=<videoId>`、path 設為 `NOTES_DIR`。

- 無命中 → 繼續步驟 1
- 命中且該檔含 `draft: true`（用 `Read` 確認）→ 先前失敗的 draft 占位，**記住該檔路徑**，步驟 3 寫新筆記時直接 `Write` 覆寫該路徑（沿用既有檔名，不另建新檔）
- 命中且無 `draft: true` → 已是完整筆記，**跳過此影片**，回報「⏭ 已有筆記，跳過」

### 步驟 1：抓 transcript（defuddle + videoId 硬驗證 + fallback）

一支腳本完成 defuddle 抓取、videoId 兩階段硬驗證、與 youtube-transcript-api fallback：

```
python3 .agents/skills/vault-youtube-sync/scripts/transcript.py "<url>" <videoId>
```

讀 stdout（`RESULT:` / `PUBLISHED:` / `---CONTENT---` 後接內容）：

- `RESULT:MATCH` → defuddle 內容可信。`CONTENT` 為 contentMarkdown，當筆記內容來源；`PUBLISHED` 為上傳日（可能空，見步驟 1 補抓）。進入步驟 3。
- `RESULT:TRANSCRIPT` → defuddle 不可信但 transcript-api 成功。`CONTENT` 為時間戳 transcript，當內容來源（`PUBLISHED` 為空，步驟 1 補抓）。進入步驟 3。
- `RESULT:FAIL:*` 或 `MISMATCH`/`UNKNOWN` 後無 transcript → 三層皆失敗，進入步驟 2。

> videoId 硬驗證的理由：defuddle 對 YouTube URL 常把推薦影片 transcript 注入，腳本以「主來源欄位 ID 相符」為最硬規則、contentMarkdown 前 2000 字第一個 ID 為 fallback，不相符即視為污染、不採用其 contentMarkdown。

**published 補抓**：若 `PUBLISHED` 為空（defuddle 常回空，屬正常），用 video_meta 取上傳日：

```
python3 .agents/skills/vault-youtube-sync/scripts/video_meta.py <videoId>
```

讀 `DATE:` 行（`YYYY-MM-DD`，空則 `published` 留空）。

### 步驟 2：影片狀態確認（步驟 1 失敗時）

```
python3 .agents/skills/vault-youtube-sync/scripts/video_meta.py <videoId>
```

- `STATUS:unavailable` → **跳過，不建筆記、不寫占位**，回報「⚠ 影片已刪除，跳過」
- `STATUS:available` 但 transcript 仍無 → 走步驟 2b 寫 draft 占位（`DATE:` 作 published），不要靜默丟棄

### 步驟 2b：失敗占位（draft 重試）

寫一份 `draft: true` 占位筆記，下次執行 skill 時步驟 0 會偵測 draft 並覆寫重抓。為何占位而不直接跳過：SKILL.md 步驟 2 的去重以 video ID 為鍵；若不留痕跡，下次仍會被頻道 checkpoint 排除（位置已在 `last_sync_id` 上方），這支影片**永遠不會補上**。

檔案路徑與命名同正常筆記（見下方「筆記規則」），frontmatter 範本：

```
---
title: <影片原標題的繁體中文翻譯>
created: <今日 YYYY-MM-DD>
updated: <今日 YYYY-MM-DD>
source: https://www.youtube.com/watch?v=<videoId>
published: <video_meta 抓到的日期；無則省略此欄>
parent: "[[01.index]]"
draft: true
tags:
  - youtube
---

> [!warning] Transcript 抓取失敗，等待下次重試
> defuddle / youtube-transcript-api / video_meta 三層 fallback 皆未取得內容。
> 失敗原因：<簡述，例：defuddle videoId mismatch、transcript-api NoTranscriptFound、影片頁 429>
> 下次執行 vault-youtube-sync 會自動偵測此 draft 並覆寫重抓。
```

寫完回報「📝 transcript 失敗，已建 draft 占位」並結束此影片流程。

### 步驟 3：撰寫筆記

依下方「內容品質標準」用步驟 1 的 `CONTENT` 撰寫筆記，`Write` 到 `<NOTES_DIR>/<繁體中文精簡標題>.md`（若步驟 0 記住了 draft 路徑則覆寫該路徑）。建立後確認檔案存在；全部完成後回報結果清單。

## 筆記規則（必須嚴格遵守）

Vault 內容會公開發佈，敏感資料零容忍。以下為本 subagent 必守規則（自包含，不依賴外部檔案）：

- **語言**：正文一律**繁體中文**；技術名詞、品牌名、工具名保留英文（例：Claude Code、OpenAI、defuddle）。defuddle 取得英文 transcript 須翻譯整理為繁中再寫入。
- **敏感資料**：正文與 frontmatter 不得含 token / key（`sk-`、`sk-ant-`、`ghp_`、`gho_`、`AKIA`、`AIza`、`xox[baprs]-`、JWT `eyJ`）、`-----BEGIN ... PRIVATE KEY-----`、明文密碼、個資（身分證、私人電話、地址、內部 IP/網址）。transcript 命中 → 移除該段或跳過整筆，不寫入。
- **tag 沿用既有**：寫入前優先沿用既有 tag（用 `Grep '^tags:' -A5` 查），避免同義異寫；真無合適才建新 tag（小寫、`-` 連接）。本類筆記固定含 `youtube`。
- **`#` 開頭內容**：hex 色碼（`#57F287`）或其他 `#` 開頭字串在 Obsidian 會被當 tag，**必須用反引號包住**（寫成 `` `#57F287` ``）；前端/設計類影片易踩。
- **不主動加 wikilink**：raw/ 是不可變原始來源，筆記彼此不主動補 `[[wikilink]]`。即使主題重疊也**不要**掃 `NOTES_DIR` 找兄弟筆記補連結——跨影片的綜合連結由 wiki 綜合流程讀多篇 raw 後在 `wiki/` 頁建立（原 `vault-wiki-build` 已移除，目前由 agent 手動執行），不在本 skill 範圍。例外：`parent: "[[01.index]]"` 是 schema 必填，照寫。
- **檔名命名**：
  - 繁體中文為主，技術名詞與品牌名保留英文
  - 不可含空格；英文/數字與中文間用 `-` 連接（例：`Claude-Code準確度提升技巧`）；中文詞間不加符號
  - 只留核心主題，去掉說明性後綴（`-效果更好還更便宜`、`-非工程師也能懂`）與日期（`-2026年4月`）
  - 不超過 40 字元；不可含 `?:;"'` 等特殊字元
- **frontmatter schema**（欄位採白名單與固定順序）：
  ```
  ---
  title: <影片標題的繁體中文翻譯>（技術名詞與品牌名保留英文）
  description: <30–80 字一句話摘要，從 transcript 提取影片核心；不重複 title、避免「這集 / 本片」自我指涉>
  created: <今日 YYYY-MM-DD>
  updated: <今日 YYYY-MM-DD>
  source: <youtube url>
  published: <影片上傳日期 YYYY-MM-DD>
  parent: "[[01.index]]"
  tags:
    - youtube
  ---
  ```
- description 撰寫：給 Obsidian Bases table、Quartz SEO、AI 查詢用；情況 A（有 transcript）依內容寫；情況 B（無 transcript）描述頁面 description 已知內容，不推測補充。
- 不使用 `#` 標題 heading（Quartz 從 frontmatter 自動產生）。

## 內容品質標準

判斷依據：`CONTENT` 是否含時間戳格式（`**0:00**`，regex：`\*\*\d+:\d+\*\*`）。

**情況 A — 有時間戳（真實 transcript）：**

- 以時間戳行為內容來源；筆記中不得出現時間戳，也不可依時間順序直接排列——必須依主題重新組織
- 依影片自然章節，用 `##` heading 分段（例：`## 核心架構`、`## 設定步驟`、`## 實際案例`）
- 每段用條列或短段落說明重點，含具體細節（指令、設定路徑、數值等）
- 可用 code block 呈現指令或結構
- 篇幅依實際內容而定，不強制展開，也不補充推測

**情況 B — 無時間戳（description 或無字幕）：**

- 寫一個 `## 重點摘要` 段落，條列實際取得的資訊
- **禁止推測或補充** `CONTENT` 沒有的內容
