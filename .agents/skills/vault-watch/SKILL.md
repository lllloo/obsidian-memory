---
name: vault-watch
description: 追蹤一批 GitHub issue/PR 的狀態，定期用 gh 抓現況、與快照比對、精選訊號（state 轉換含 PR merged、官方/maintainer 新回應、label 變動）有變才回報。追蹤清單只讀 `feeds/watch/01.index.md` 看板，不硬編碼；路人留言與 reaction 數預設不列為變化，看板列標 `[全留言]` 的項才連社群留言一併採計。使用時機：使用者要求「查一下我追蹤的 issue」「watchlist 有變化嗎」「那幾個 feature request 動了沒」「官方回應了沒」「追蹤 owner/repo#num」，或直接呼叫 /vault-watch。目前僅支援 GitHub issue/PR。
---

# Vault Watch

追蹤一批 GitHub issue/PR，回報「與上次相比動了什麼」。核心問題是「官方/maintainer 回了沒、狀態轉了沒」；重點是 high signal：精選訊號才回報，安靜的一輪零變化不寫檔、只回一句。

## 產出

- 看板（追蹤清單來源）：`feeds/watch/01.index.md`——一列一 issue，含目前狀態（Issue／追蹤重點／狀態三欄），skill 就地更新。
- 變更 digest：`feeds/watch/<YYYY-MM-DD>-watch.md`——**有變化才寫**。
- 快照：skill 目錄 `state.json`（機器資料檔，比對用，非 vault 筆記）。
- 三者皆 browse-only feed，不屬三層系統，不進 raw/wiki、不參與 Ingest/Query/Lint。

## 資源

- `references/watch-runbook.md`：腳本輸出格式、看板更新與 digest 撰寫規則。執行前先讀全文。
- `scripts/watch.py`：讀看板抽 `owner/repo#num` → 用 `gh` 抓現況＋自上輪起的官方留言 → 與 state.json 比對 → 吐機器可讀 deltas 並更新快照。純 stdlib，subprocess 呼 `gh`。

## 主流程

1. 用 harness-native `Read schema/vault-map.md` 確認 cwd 是 vault root；讀不到就停止，請使用者 cd 到 vault root（`~/code/obsidian-memory`；三平台一致，cmd.exe 不認 `~` 改用 `%USERPROFILE%\code\obsidian-memory`）。
2. 讀 `feeds/watch/01.index.md`。不存在或表內無任何 `owner/repo#num` 時停止，請使用者先在看板加追蹤項（格式見該檔說明）。
3. 使用者說「追蹤 owner/repo#num …」時，先在看板表格 append 一列（第一欄放連結 `[owner/repo#num](issue-url)`、第二欄一句追蹤重點）再往下跑。
4. 讀 `references/watch-runbook.md`。
5. 執行抓取：

```
python3 .agents/skills/vault-watch/scripts/watch.py
```

　　自訂看板路徑時加 `--index <path>`。

6. 依 runbook 解讀 stdout：**只更新這輪有 `CHANGE` 的看板列**（狀態欄），`NOCHANGE` 項不動；`changed>0` 時寫／追加當日 digest，`changed=0` 不寫檔、看板與 state.json 皆零 diff。
7. `ERROR` 項照 runbook 保留舊狀態，於收尾回報列出原因。

## 固定回覆

完成後回覆：

- 查核數 / 有變化數（取自 `SUMMARY`）
- 有變化的項各一行摘要（狀態轉換、官方回應、label 變動）；官方回應要點出誰、何時
- **目前追蹤清單（每輪都列，不論有無變化）**：逐項一行 `owner/repo#num` — 追蹤重點 · 現狀。追蹤重點取自看板第二欄（即「為何在追、為解決什麼」），現狀取自該項 `ITEM` 的 state（有 `official` 就加註如 `open · 官方已回應`）。這是給隔很久才回來看的使用者的定位錨——安靜的一輪只回「幾比幾無變化」會讓人忘了自己在 watch 什麼、為什麼追，所以即使零變化也照列全清單。
- 看板路徑；有寫 digest 時附 digest 路徑，無變化時明講「本次無變化、未寫檔」
- `ERROR` 項與原因（若有）
