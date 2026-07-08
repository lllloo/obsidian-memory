---
name: vault-lint
description: Vault 健檢：掃描 raw/wiki 的孤立 wiki 頁、死連結、raw 積壓、tag 同義異寫、frontmatter 缺欄位等問題。列出報告後互動確認，等用戶拍板再修。使用時機：使用者說「健檢」、「lint」、「vault 健康檢查」、「掃問題」、「vault 狀態」，或直接呼叫 /vault-lint。
---

# /vault-lint — Vault 健檢

掃描 → 列分類報告 → 等用戶拍板 → 修。

## 前置條件

用 `Read vault-map.md` 確認 cwd 為 vault root（harness-native，不經 shell）。讀不到就停止，告知用戶 cd 到 vault root。

## 掃描

所有掃描邏輯收在 `scripts/lint.py`（純 Python stdlib，跨平台，無外部依賴）。掃描範圍只有 `raw/` + `wiki/`（加上根層治理 .md 用於 dead_links 的連結來源與目標索引）；`Cards/`、`Topics/` 是使用者私人區，一律不掃。cwd 為 vault root，用完整相對路徑執行：

```
python3 .agents/skills/vault-lint/scripts/lint.py
```

腳本輸出單一 JSON 物件到 stdout，**不修改任何檔案**；判讀與修補由本流程依下方規則處理。

JSON 欄位對應的問題與嚴重度：

| JSON 欄位 | 意義 | 報告分類 |
|---|---|---|
| `dead_links` | wikilink 目標不存在（已排除 `[[<佔位符>]]`、帶路徑、`.base`） | 🔴 |
| `missing_title` | `raw/`、`wiki/` 筆記缺 `title` | 🔴 |
| `missing_description` | 規範必填 `description` 缺失（wiki 頁、`raw/Clippings/*`、`raw/YouTube` 影片筆記；各自 `01.index.md` 為目錄頁不算） | 🔴 |
| `schema_drift` | `lint.py` 的 `WHITELIST` 與 `CLAUDE.md` schema 表格不一致（`null` = 一致） | 🔴 |
| `inbox_backlog` | raw root 未歸檔散項數（各 raw 子夾 Clippings/Archive/Updates/YouTube 不計） | > 20 🔴；> 5 🟡；≤ 5 不報 |
| `orphans_wiki` | wiki 頁（排除 `01.index.md`）無任何入站 wikilink | 🟡 |
| `missing_tags` | `raw/`、`wiki/` 筆記缺 `tags` | 🟡 |
| `missing_required_dirs` | 規範常設資料夾遺漏（`raw/`、`wiki/` 及其固定子夾；git 不追蹤空目錄） | 🟡 |
| `frontmatter_order` | frontmatter 白名單欄位順序錯亂 | 🟡 |
| `frontmatter_rogue` | 出現白名單外游離欄位（`[路徑, [欄位…]]`） | 🟡 |
| `missing_updated` | `raw/`、`wiki/` 筆記缺 `updated` | 🔵 |
| `tag_counts` | 純英數 tag 使用次數 top 60 | 🔵（肉眼辨識同義異寫，如 `claude-code` vs `claudeCode`） |

> `frontmatter_order`/`rogue` 的判準依 `lint.py` 的 `WHITELIST` 常數，它是 `CLAUDE.md` frontmatter schema 的機器執行副本。兩者格式不可互通、無法合成一份；`schema_drift` 項即用來校驗兩者一字不差，漂移時報 🔴。判準不在此重抄，避免成為第三份會漂的副本。

## 報告格式

讀完 JSON 後**統一輸出**分類報告：

```
## Vault 健檢報告（YYYY-MM-DD）

### 🔴 嚴重（N 項）
- 死連結：[[xxx]]、[[yyy]]
- 缺 title：wiki/foo.md
- 缺 description：raw/Clippings/foo.md
- schema 漂移：lint.py WHITELIST 與 CLAUDE.md schema 不一致（列出兩邊欄位差異）

### 🟡 警告（N 項）
- raw 散項：8 篇未歸檔（> 5）
- 孤立 wiki 頁：wiki/foo.md（無入站連結，需補交叉引用）
- 規範資料夾遺漏：raw/Clippings
- frontmatter 欄位順序 / 白名單外欄位：ORDER wiki/foo.md、ROGUE raw/bar.md: author

### 🔵 資訊（N 項）
- 缺 updated：N 篇
- tag 同義異寫候選：（列出疑似重複的 tag 對）
```

## 互動確認

報告後**逐類**列出「可自動修補」vs「需人工判斷」：

**可自動修補（問用戶是否執行）：**
- 補缺失的 `updated` 欄位（設為今日日期）
- 補回規範資料夾遺漏（建立資料夾並放 `.gitkeep` 佔位，讓 git 追蹤）

**需人工判斷（只列出，不自動動）：**
- 孤立 wiki 頁 — 補交叉引用，或判斷這頁是否真的該存在（wiki 交叉引用是核心紀律，不留孤立頁）
- 死連結 — 改外部 URL？刪 wikilink？補建目標頁？
- tag 同義異寫 — 哪個是正典？
- frontmatter 欄位順序 / 白名單外欄位 — ORDER 手動調整欄位順序；ROGUE 判斷該補進白名單還是刪除
- raw 散項 — 未歸進 raw 子夾的散項，歸檔時機由用戶自選（raw 子夾永久留存，不計積壓）
- description 缺失 — 需手動寫 30–80 字摘要，不自動產生
- schema 漂移 — 判斷 `CLAUDE.md` schema 與 `lint.py` 的 `WHITELIST` 哪邊才是正確意圖，再同步另一邊（規範變更通常以 `CLAUDE.md` 為準）

**執行前給用戶看確認，確認後才動檔。一次修一個類別。** 修補一律用 harness-native 工具（`Write`/`Edit`），不落 shell。
