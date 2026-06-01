---
name: vault-lint
description: Vault 健檢：掃描孤立頁面、死連結、Inbox 積壓、tag 同義異寫、frontmatter 缺欄位、Topics 缺 index.md、vault-map 未收錄、extracted_to 遺留等問題。列出報告後互動確認，等用戶拍板再修。使用時機：使用者說「健檢」、「lint」、「vault 健康檢查」、「掃問題」、「vault 狀態」，或直接呼叫 /vault-lint。
---

# /vault-lint — Vault 健檢

掃描 → 列分類報告 → 等用戶拍板 → 修。

## 前置條件

用 `Read vault-map.md` 確認 cwd 為 vault root（harness-native，不經 shell）。讀不到就停止，告知用戶 cd 到 vault root。

## 掃描

所有掃描邏輯收在 `scripts/lint.py`（純 Python stdlib，跨平台，無外部依賴）。cwd 為 vault root，用完整相對路徑執行：

```
python .agents/skills/vault-lint/scripts/lint.py
```

`python3` 無效時改 `python`。腳本輸出單一 JSON 物件到 stdout，**不修改任何檔案**；判讀與修補由本流程依下方規則處理。

JSON 欄位對應的問題與嚴重度：

| JSON 欄位 | 意義 | 報告分類 |
|---|---|---|
| `inbox_backlog` | Inbox 篇數（排除 `Inbox/Updates/`） | > 50 🔴；> 20 🟡；≤ 20 不報 |
| `dead_links` | wikilink 目標不存在（已排除 `[[<佔位符>]]`、帶路徑、`.base`） | 🔴 |
| `missing_title` | Cards/Topics 缺 `title` | 🔴 |
| `missing_description` | 規範必填 `description` 缺失（Topics `index.md`、`Inbox/Clippings/*`、YouTube 影片筆記） | 🔴 |
| `topics_missing_index` | Topics 資料夾無 `index.md` | 🔴 |
| `missing_tags` | Cards/Topics 缺 `tags`（已排除 `index.md`） | 🟡 |
| `orphans_topics` | 升級主題卻無入站 wikilink（異常） | 🟡 |
| `topics_not_in_vaultmap` | Topics 未收錄進 `vault-map.md` | 🟡 |
| `missing_required_dirs` | 規範常設資料夾遺漏（git 不追蹤空目錄） | 🟡 |
| `frontmatter_order` | frontmatter 白名單欄位順序錯亂 | 🟡 |
| `frontmatter_rogue` | 出現白名單外游離欄位（`[路徑, [欄位…]]`） | 🟡 |
| `extracted_to` | 半消化 Inbox 筆記（仍有剩餘段落） | 🟡 |
| `orphans_cards` | 孤立 Cards | 🔵（吸收型卡片盒，孤立可接受；摺疊成數量，不逐張列） |
| `missing_updated` | Cards/Topics 缺 `updated` | 🔵 |
| `tag_counts` | 純英數 tag 使用次數 top 60 | 🔵（肉眼辨識同義異寫，如 `claude-code` vs `claudeCode`） |

> frontmatter 白名單與固定順序（`frontmatter_order`/`rogue` 的判準，與 `CLAUDE.md` schema 同步）：`title` > `description` > `created` > `updated` > `source` > `published` > `parent` > `last_sync_id` > `draft` > `extracted_to` > `tags`。

## 報告格式

讀完 JSON 後**統一輸出**分類報告：

```
## Vault 健檢報告（YYYY-MM-DD）

### 🔴 嚴重（N 項）
- 死連結：[[xxx]]、[[yyy]]
- 缺 title：Cards/foo.md
- 缺 description：Inbox/Clippings/foo.md
- Topics/bar/ 無 index.md

### 🟡 警告（N 項）
- Inbox 積壓：42 篇（> 20）
- 孤立 Topics：Topics/foo/bar.md（升級主題卻無入站連結）
- vault-map 未收錄：SomeTopic
- 規範資料夾遺漏：Inbox/Clippings
- frontmatter 欄位順序 / 白名單外欄位：ORDER Cards/foo.md、ROGUE Cards/bar.md: author
- extracted_to 遺留：Inbox/abc.md

### 🔵 資訊（N 項）
- 孤立 Cards：7 張（吸收型卡片盒，孤立可接受；摺疊成數量，不逐張列）
- 缺 updated：N 篇
- tag 同義異寫候選：（列出疑似重複的 tag 對）
```

## 互動確認

報告後**逐類**列出「可自動修補」vs「需人工判斷」：

**可自動修補（問用戶是否執行）：**
- 補 Topics 缺失的 index.md（建含基本 frontmatter 的空白檔）
- 在 vault-map 補收錄缺漏的 Topics
- 補缺失的 `updated` 欄位（設為今日日期）
- 補回規範資料夾遺漏（建立資料夾並放 `.gitkeep` 佔位，讓 git 追蹤）

**需人工判斷（只列出，不自動動）：**
- 孤立頁面 — **Topics 孤立**才需處置（補連結／檢查升級是否成立）；Cards 孤立預設保留，除非用戶主動要連。
- 死連結 — 改外部 URL？刪 wikilink？補建目標頁？
- tag 同義異寫 — 哪個是正典？
- frontmatter 欄位順序 / 白名單外欄位 — ORDER 手動調整欄位順序；ROGUE 判斷該補進白名單還是刪除
- extracted_to 遺留 — 何時消化剩餘段落？
- Inbox 積壓 — 批次清理時機由用戶自選
- description 缺失 — 需手動寫 30–80 字摘要，不自動產生

**執行前給用戶看確認，確認後才動檔。一次修一個類別。** 修補一律用 harness-native 工具（`Write`/`Edit`），不落 shell。
