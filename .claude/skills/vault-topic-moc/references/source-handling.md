# 原筆記處置策略

MOC 建好後，原筆記有三種處置選項。**執行前必須先問用戶**，不要自動刪除。

## 選項 A：保留

- 原筆記不動
- MOC 文內用 `[[筆記檔名]]` wikilink 連結

**優點**：
- 雙向可追溯
- Obsidian graph view 有明確連結
- 原筆記細節不丟失

**缺點**：
- vault 冗餘（資訊分散在 MOC 與原筆記）
- 原筆記可能與 MOC 逐漸分歧（誰才是真相）

**適用**：原筆記有獨特細節、MOC 是摘要入口。

## 選項 B：刪除（MOC 自足）— YouTube 來源的預設

**Roy 的慣例**：當原筆記來源是 `content/Inbox/YouTube/` 下的影片摘要，整理完成後預設選此選項。仍必須在 `git rm` 前列出檔案清單給用戶過目。

**流程**：
1. MOC 文內移除指向原筆記的 wikilink，改為外部 URL（YouTube、GitHub、官方 docs 等）
2. MOC 末尾的「來源」章節列原始外部 URL
3. `git rm <原筆記路徑>`（保留 git 歷史）
4. 若 `Topics/<類別>/` 有 `index.md`（類別入口頁），新增一條指向本 MOC 的 wikilink；若被刪除的原筆記本身也出現在 index.md 清單（僅適用 Cards 歸檔後再整併的情境；Inbox/YouTube 來源通常不會被 index.md 列出），一併移除

**優點**：
- MOC 自足，vault 精簡
- 單一真相來源

**缺點**：
- 失去原筆記的個別段落細節
- 若原筆記是 YouTube 影片筆記，下次同步頻道時可能被視為新影片重抓（checkpoint 失效時）

**YouTube 影片筆記的特殊情境**：
- `vault-youtube-sync` skill 用 `01.index.md` 的 `last_sync_id` 做 checkpoint
- 若刪除的影片都比 checkpoint 舊，下次同步不會重抓
- 若 checkpoint 失效（距上次同步超過 30 支），刪除的影片會被視為新的 → 可考慮在 MOC 或獨立 gitignored 檔案記錄「已整理移除」的 video ID 清單

**適用**：原筆記只是轉述、MOC 已完整覆蓋核心內容。

## 選項 C：加 draft（折衷）

- 原筆記 frontmatter 加 `draft: true`
- Obsidian 仍看得到
- Quartz 發佈時會被 `RemoveDrafts` plugin 過濾，不上網站

**優點**：
- 可回頭
- 公開網站乾淨
- vault 內還能查細節

**缺點**：
- vault 仍有冗餘

**適用**：不確定要不要刪、想先觀察 MOC 夠不夠用。

## 決策建議表

| 情境 | 建議選項 |
|------|---------|
| **來源是 `content/Inbox/YouTube/` 影片筆記**（Roy 慣例） | **B 刪除** |
| 原筆記有獨特細節、MOC 是摘要 | A 保留 |
| 原筆記只是轉述，MOC 已完整覆蓋 | B 刪除 |
| 不確定、想先觀察 | C draft |
| 原筆記屬於發佈網站但想精簡對外 | C draft |
| vault 太亂、想徹底整理 | B 刪除 |

## 執行前 checklist

**選 B 刪除**前必須確認：

- [ ] 用戶明確同意刪除
- [ ] MOC 已定稿（Generator/Reviewer 迴圈完成）
- [ ] MOC 末尾已保留外部 URL 清單
- [ ] 列出要刪的檔案給用戶過目
- [ ] 用 `git rm`（非 `rm`）保留歷史

## 常見錯誤

- 自動幫用戶決定選項（必問）
- 用 `rm` 而不是 `git rm`（失去歷史）
- wikilink 沒先移除就刪原筆記（造成 dead link）
- 沒確認 MOC 定稿就開始刪（發現 MOC 有漏需要回填時，原筆記已消失）
