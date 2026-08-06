# vault-watch Runbook

`watch.py` 只負責抓取與比對，吐機器可讀行到 stdout；**看板更新、digest 撰寫、git 一律不由腳本做**，由主 agent 依本檔用 harness 工具（Read/Edit/Write）處理。正文一律繁體中文，技術名詞／品牌名保留英文。

## 前置

需要 `gh`（GitHub CLI）已安裝並 `gh auth login`。讀公開 repo 的 issue/PR 不強制授權，但授權可提高 rate limit。腳本遇 `gh` 缺失或 API 失敗時對該項印 `ERROR|<ref>|<訊息>` 並續跑其餘項，不整批中斷。

## 腳本輸出格式

每項一或多行，`|` 分隔：

- `ITEM|<ref>|<type>|<state>|<title>` — 該項現況。type=`issue`/`pr`；state=`open`/`closed`/`merged`/`closed-unmerged`。
- `CHANGE|<ref>|new|<type> <state>` — 首次見到（快照裡沒有）。
- `CHANGE|<ref>|state|<old>-><new>` — 狀態轉換。
- `CHANGE|<ref>|label+|<name>` / `label-|<name>` — label 增／刪。
- `CHANGE|<ref>|official|<login>|<assoc>|<date>|<snippet>` — 自上輪起的新回應。`<assoc>` 是 GitHub 的 `author_association`：`OWNER`／`MEMBER`／`COLLABORATOR` 才是官方/maintainer，其餘（`CONTRIBUTOR`／`NONE` 等）是社群。**寫看板與 digest 一律照 `<assoc>` 表述**，別把社群留言寫成「官方已回應」。
- `NOCHANGE|<ref>` — 無精選訊號變化。
- `ERROR|<ref>|<訊息>` — 該項抓取失敗。
- `SUMMARY|checked=N|changed=M|date=YYYY-MM-DD` — 收尾統計。

reaction 數**不**進 CHANGE。留言的採計範圍**逐項可調**：看板列預設只採官方/maintainer（刻意濾掉路人留言，避免熱門 issue 洗版），該列標了 `[全留言]` 才連社群留言一併採計——給留言量小、關鍵訊號常來自非 maintainer 的冷門項用。標記變更**不回填**快照之前的舊留言，只影響往後的新留言。

## 依輸出更新看板

**只更新這輪有 `CHANGE` 的項**——quiet round（該項只出現 `NOCHANGE`）一律不動看板列，讓沒有訊號的一輪在 repo 留零 diff（與下方 state.json 凍結時間戳同一原則）。

對每個帶 `CHANGE` 的 `ITEM`：在 `feeds/watch/01.index.md` 表格找到對應列（第一欄含該 `owner/repo#num`），用 Edit 更新：

- 「狀態」欄 = 現 state；有 `official` 變化時依 `<assoc>` 加註（OWNER／MEMBER／COLLABORATOR → `open · 官方已回應`；其餘 → `open · 社群有新回應`）。看板只有 Issue／追蹤重點／狀態三欄，不記查核日期——使用者只關心「現在好了沒」，即狀態欄本身。**「追蹤重點」欄是使用者的，除了本節指定的狀態欄更新外不要改動它**（`[全留言]` 標記就住在該欄，改寫會把設定弄丟）。
- 有任何看板列被改時，一併把 frontmatter `updated` 設為 SUMMARY date；整輪零變化則連 frontmatter 都不動。

`NOCHANGE` 項與 `ERROR` 項都不動看板列；`ERROR` 於收尾回報中列出失敗原因。

## digest 撰寫規則

- **只有 changed>0（有任何 `CHANGE`）才寫 digest**；`changed=0` 不寫檔，只在收尾回報「本次無變化」。
- 路徑 `feeds/watch/<YYYY-MM-DD>-watch.md`（date 取 SUMMARY）。同日再跑且又有新變化時，**追加**到當日檔尾、不覆蓋。
- frontmatter：`title: "<YYYY-MM-DD> Watch"`、`created`、`updated`、`tags: [watch]`。
- 正文按項分點，每點：issue 連結（markdown 超連結）＋這輪變了什麼。`official` 變化要點出是誰（login）、是官方還是社群（依 `<assoc>`）、日期、留言摘要——這是這個 skill 最有價值的訊號，別淹沒。
- digest 是 browse-only feed，不 wikilink 回 index，不進 raw/wiki。

## 快照 state.json

- 位置：skill 目錄 `state.json`（機器資料檔，非 vault 筆記，不進 Quartz、不需 wikilink）；tracked 進 repo 以維持跨機／跨工具可攜。
- 腳本每輪重寫，但**無實質變化的一輪產出 byte-identical**：`checked_ts`（抓新留言的 `since` 游標）只在該項有 `CHANGE` 時才推進到現在，quiet round 沿用舊值，且不寫任何純裝飾的日期欄。因此沒有訊號的一輪 state.json 零 diff、無需 commit。
- 看板列被刪的項，其快照殘留無害，不必手動清。
- 想強制「重當基準」某項：從 state.json 刪該 key（或整檔），下輪該項會以 `new` 重新登錄。
