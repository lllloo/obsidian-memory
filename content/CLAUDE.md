# Obsidian Memory Vault — 吸收型卡片盒

**本檔涵蓋**：Vault 內容規則——卡片盒哲學、Inbox/Cards/Topics 工作流、寫入前 Checklist、frontmatter schema、tag/命名、敏感資料。
**不涵蓋**：Quartz 部署、agent/command/skill 架構、symlink 配置 → 見 repo 根目錄 [`CLAUDE.md`](../CLAUDE.md)。

## 三條原則

此 vault 採用「吸收型卡片盒」，核心如下：

1. **吸收並內化** — 筆記是「我理解的版本」，不是別人說法的保存
2. **不留原料，留參考資料** — Inbox 抄錄整篇消化完刪除（多主題筆記允許保留未消化段落，加 `extracted_to` 標記指回 MOC）；Card 保留參考資料（來源網址等），用於回查原文，不作為證據
3. **正確 + 不斷更新** — Card 可覆寫、永不定稿（持續修改）

**一句話：Vault 是腦的延伸，不是倉庫。**

## Vault 結構（三層成熟度）

| 資料夾           | 角色                                | 成熟度 | 生命週期                                  |
| ---------------- | ----------------------------------- | ------ | ----------------------------------------- |
| `Inbox/`         | AI 抄錄的外部原料                   | 未消化 | 暫存，消化完刪除                          |
| `Cards/`         | 未歸屬的完整概念 Card               | 待歸類 | 累積同主題或裂變後批次搬進 Topics/<主題>/ |
| `Topics/<主題>/` | 已歸檔的完整概念 Cards + 主題入口頁 | 已歸檔 | 長期，可持續覆寫                          |

## 三層工作流

### Inbox → Cards（消化）

三條清空路徑：

- A. 寫新 Card（放 `Cards/`） — 真有新啟發（少數）
- B. 強化既有 Card / Topic 內容 — 呼應舊想法（多數）
- C. 直接刪除 — 沒學到新東西、品質差（多數）

三條都以「刪除 Inbox/ 原篇」作結。Inbox 空 = 無積欠。

路徑 A、B 寫 Card 時，按既有慣例附上來源連結（回查用）。

**多主題例外**：若 Inbox 筆記同時涵蓋多個主題、本次整理只內化其中一個切角，允許從原筆記移除已內化段落、保留剩餘段落，並在 frontmatter 加 `extracted_to: "[[<MOC 名>]]"` 指回 MOC。半消化筆記仍是 Inbox 的「待消化」狀態，鼓勵下次同主題整理時再消化剩餘。

### Cards → Topics/<主題>/（歸檔）

**Card = 完整概念**（獨立可讀，不需搭配其他筆記或原文就能理解），不是零碎斷句。兩種批次觸發：

- **A. 同主題累積**：多張同主題 Cards 一起搬
- **B. Card 裂變**：單張長大後拆成多張，同時搬

動作：

1. 找到或建立 `Topics/<主題>/` 資料夾（含 `index.md` 作為主題入口頁）
2. **一次 `git mv` 整組 Cards** 搬入 `Topics/<主題>/`（內容不動）
3. 在 `index.md` 補上 wikilink 清單

跨主題靠 `tags` 串連：`Topics/` 第一層不做跨主題巢套（不建「AI-工具/Claude-Code/」這種群組）；單一主題內 Cards 過多時，可在 `Topics/<主題>/` 底下再分子資料夾。

### 防爆量

- Inbox 靠「消化完刪除」
- Cards 靠「成批搬走」
- Topics 靠「第一層不跨主題聚合 + 主題數有限」

不靠紀律，靠流動。

## 寫入前 Checklist（所有 agent 寫入 content/ 前必做）

此 vault 透過 Quartz 發佈到公開網站（ob.bugloop.com），寫入前必須自檢。這是 vault 健康的第一道防線——任何修改 `content/` 的流程（vault-writer、skills、手動編輯）在寫入前逐項檢查。`/vault-check` 只兜底跨檔案 emergent 問題（斷鏈、tag drift、非 writer 來源漏網），**不依賴它抓本清單能預防的錯**。

### 1. 敏感資料（零容忍）

寫入前掃正文與 frontmatter，確認不含：

- **Token / Key**：`sk-`、`sk-ant-`、`ghp_`、`gho_`、`AKIA`、`AIza`、`xox[baprs]-`、`eyJ`（JWT）
- **Private key header**：`-----BEGIN ... PRIVATE KEY-----`
- **自然語言密碼**：「密碼是 …」、「password: …」後接明文
- **客戶 / 公司內部資訊、個資**：身分證、私人電話、地址、內部 IP / 網址

命中 → 移除或告知使用者中止，不寫入。若發現既有筆記含有敏感資料，立即移除並通知用戶。

### 2. Frontmatter schema（寫入當下即合法）

必含 `title` / `created` / `updated` / `tags`；欄位順序、白名單、型別以 [`scripts/vault-schema.mjs`](../scripts/vault-schema.mjs) 為準。**不要產出需要 auditor 事後補 title 或修 YAML 的筆記**——YAML 引號、縮排、wikilink 包雙引號（`parent: "[[01.index]]"`）等在寫入前就確保正確。

細節見下文「Frontmatter Schema（固定）」。

### 3. Tag 沿用既有

寫入前先查現有 tags（`obsidian tags`，或 `rg -A5 '^tags:' content -g '*.md'`），優先沿用，避免製造同義異寫（`claude-code` vs `claudeCode` vs `claude_code`）。真無合適才建新 tag，小寫、`-` 連接。

### 4. 命名

檔名不含空格，空格一律改為 `-`（例：`Obsidian-CLI-整合指南.md`）；wikilink 對應實際檔名（含 `-`）。`title:` 用主題名，不加日期前綴。

## 規則

### Obsidian Bases（.base 檔案）

- wikilink 必須加副檔名：`[[02.影片清單.base]]`，不加會找不到檔案
- embed 同理：`![[02.影片清單.base]]`
- `.base` 檔案的內容**不會在圖譜產生連結**，這是 Obsidian 已知限制
- 要讓筆記出現在圖譜中，需在筆記 frontmatter 加 `parent` property 指向 index：
  ```yaml
  parent: "[[01.index]]"
  ```

### 色碼與特殊符號

- `#` 開頭的內容（如 hex 色碼 `#57F287`）在 Obsidian 會被解讀為 tag，**必須用反引號包住**：`` `#57F287` ``

### `updated` 欄位（盡力而為）

修改 `.md` 內容時**盡量**同步 frontmatter 的 `updated` 為今日日期（`YYYY-MM-DD`），但不強制 — 偶爾漂移可接受，不需為此中斷流程或裝 hook。

### Frontmatter Schema（固定）

機器驗證真實來源：[`scripts/vault-schema.mjs`](../scripts/vault-schema.mjs)（欄位清單、順序、必填、型別、strict 白名單皆在那）。本節只記**人類語意**（欄位作用、出現情境）與 Obsidian 特有坑。

```yaml
---
# ── 核心（必填，所有筆記） ──
title: <筆記標題>
created: YYYY-MM-DD
updated: YYYY-MM-DD

# ── 選填（依筆記類型出現） ──
source: <URL> # 外部來源
published: YYYY-MM-DD # 外部來源發佈日
parent: "[[01.index]]" # 歸屬 index（圖譜用）
extracted_to: "[[<MOC 名>]]" # 半消化筆記：部分內容已被整合到 MOC
last_sync_id: <video-id> # 僅 YouTube 頻道 01.index.md
draft: true # Quartz 不發佈（opt-out）

# ── 必填，固定放最後 ──
tags:
  - tag-1
---
```

**欄位說明：**

| 欄位           | 必填 | 出現於                     | 作用                                                                                                       |
| -------------- | ---- | -------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `title`        | ✓    | 全部                       | Quartz 頁面標題來源（正文不用 `# Heading`）                                                                |
| `created`      | ✓    | 全部                       | 建立日                                                                                                     |
| `updated`      | ✓    | 全部                       | 最後修改日（盡力而為，見下節）                                                                             |
| `source`       | 條件 | 有外部來源時               | 外部資料必填，跨階段保留（Inbox → Cards → Topics 都不刪，供回查原文）；純原創 Card 可省略                  |
| `published`    | —    | 有外部來源發佈日時         | 原文／影片發佈日（YouTube 影片由 `vault-youtube-sync` 帶入、Clipping 由 Web Clipper 帶入）；無法取得可省略 |
| `parent`       | —    | Inbox/YouTube 影片         | `[[01.index]]`，讓筆記出現在頻道圖譜                                                                       |
| `extracted_to` | —    | 半消化 Inbox 筆記          | `[[<MOC 名>]]`，指回部分內容已被整合到的 MOC，避免遺忘                                                     |
| `last_sync_id` | —    | YouTube 頻道 `01.index.md` | `vault-youtube-sync` skill 的同步書籤                                                                      |
| `draft`        | —    | 草稿                       | `true` = 不發佈到 ob.bugloop.com；完成後移除                                                               |
| `tags`         | ✓    | 全部                       | 固定放最後                                                                                                 |

**Obsidian 特有注意：**

- `tags` 必須 YAML list（`- tag`），不用 inline array `[a, b]` — Obsidian UI 偶爾會誤寫成 inline
- Wikilink 值必須用雙引號包：`parent: "[[01.index]]"`（YAML parser 會把 `[[...]]` 當 flow sequence 吃掉）

**白名單制**：schema 以外的欄位一律移除。

- Obsidian Web Clipper 若帶入 `author` / `description` / `cover` / `image` / `banner` 等未列欄位，一律清掉
- `/vault-check` 會自動稽核（`UNKNOWN_FIELD`）並由 `scripts/vault-check.mjs` 刪除
- 新增欄位前需先在 `scripts/vault-schema.mjs` 擴充，不可直接寫入未列欄位

## YouTube 筆記語言規範

所有 YouTube 影片筆記正文內容一律以**繁體中文**撰寫。

- 技術名詞、品牌名、工具名保留英文（例：Claude Code、OpenAI、defuddle）
- 若 defuddle 取得英文 transcript，需翻譯整理為繁體中文後再寫入筆記

## 查詢規則

查詢相關知識時：

1. 先讀 `master-index.md` 確認資料位置
2. 主題筆記 → 對應 `Topics/` 子目錄
3. 影片摘要 → 依主題選對應 `Inbox/YouTube/<頻道>/`
4. 跨主題 → Grep 搜尋 tag（frontmatter 中的 tags 欄位）
