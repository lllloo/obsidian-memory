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
- `CHANGE|<ref>|official|<login>|<date>|<snippet>` — 官方/maintainer（OWNER/MEMBER/COLLABORATOR）自上輪起的新回應。
- `NOCHANGE|<ref>` — 無精選訊號變化。
- `ERROR|<ref>|<訊息>` — 該項抓取失敗。
- `SUMMARY|checked=N|changed=M|date=YYYY-MM-DD` — 收尾統計。

一般路人留言與 reaction 數**不**進 CHANGE（設計上刻意濾掉，避免熱門 issue 洗版）。

## 依輸出更新看板

對每個 `ITEM`：在 `feeds/watch/01.index.md` 表格找到對應列（第一欄含該 `owner/repo#num`），用 Edit 更新：

- 「狀態」欄 = 現 state；若該項有 `official` 變化或你已知官方回應狀態，可加註（如 `open · 官方無回應` / `open · 官方已回應`）。
- 「最後查核」欄 = SUMMARY 的 date。

`ERROR` 項不動其看板列的狀態，但把「最後查核」留舊值、於收尾回報中列出失敗原因。

## digest 撰寫規則

- **只有 changed>0（有任何 `CHANGE`）才寫 digest**；`changed=0` 不寫檔，只在收尾回報「本次無變化」。
- 路徑 `feeds/watch/<YYYY-MM-DD>-watch.md`（date 取 SUMMARY）。同日再跑且又有新變化時，**追加**到當日檔尾、不覆蓋。
- frontmatter：`title: "<YYYY-MM-DD> Watch"`、`created`、`updated`、`tags: [watch]`。
- 正文按項分點，每點：issue 連結（markdown 超連結）＋這輪變了什麼。`official` 變化要點出是誰（login）、日期、留言摘要——這是這個 skill 最有價值的訊號，別淹沒。
- digest 是 browse-only feed，不 wikilink 回 index，不進 raw/wiki。

## 快照 state.json

- 位置：skill 目錄 `state.json`（機器資料檔，非 vault 筆記，不進 Quartz、不需 wikilink）。
- 腳本每輪覆寫；看板列被刪的項，其快照殘留無害，不必手動清。
- 想強制「重當基準」某項：從 state.json 刪該 key（或整檔），下輪該項會以 `new` 重新登錄。
