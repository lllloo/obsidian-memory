# Obsidian Memory Vault — 吸收型卡片盒

## 三條原則

此 vault 採用「吸收型卡片盒」，核心如下：

1. **吸收並內化** — 筆記是「我理解的版本」，不是別人說法的保存
2. **不留原料，留參考資料** — Inbox 抄錄整篇消化完刪除；Card 保留參考資料（來源網址等），用於回查原文，不作為證據
3. **正確 + 不斷更新** — Card 可覆寫、永不定稿（持續修改）

**一句話：Vault 是腦的延伸，不是倉庫。**

## Vault 結構（三層成熟度）

| 資料夾 | 角色 | 成熟度 | 生命週期 |
|--------|------|-------|---------|
| `Inbox/` | AI 抄錄的外部原料 | 未消化 | 暫存，消化完刪除 |
| `Cards/` | 未歸屬的完整概念 Card | 待歸類 | 累積同主題或裂變後批次搬進 Topics/<主題>/ |
| `Topics/<主題>/` | 已歸檔的完整概念 Cards + 主題入口頁 | 已歸檔 | 長期，可持續覆寫 |

## 三層工作流

### Inbox → Cards（消化）

三條清空路徑：
- A. 寫新 Card（放 `Cards/`） — 真有新啟發（少數）
- B. 強化既有 Card / Topic 內容 — 呼應舊想法（多數）
- C. 直接刪除 — 沒學到新東西、品質差（多數）

三條都以「刪除 Inbox/ 原篇」作結。Inbox 空 = 無積欠。

路徑 A、B 寫 Card 時，按既有慣例附上來源連結（回查用）。

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

## 已知問題

Obsidian CLI 在 Git Bash 環境下部分指令會回傳 exit code 127（shell 差異造成）。

**Windows (Git Bash)**：用 PowerShell 包一層：
```bash
powershell.exe -Command "obsidian <指令>"
```

**macOS/Linux**：若遇到同類問題，改用等效的兩步驟拆解（先取得路徑再 `append`）。

## 安全規則

此 vault 的內容會透過 Quartz 發佈到公開網站（ob.bugloop.com）。**所有寫入或修改的內容在 commit 前必須檢查，確保不包含以下敏感資料：**

- API key、secret、token
- 密碼、帳號憑證
- 私人 IP、內部網址
- 個人隱私資訊（身分證、電話、地址等）
- 任何不適合公開的內容

若發現既有筆記含有敏感資料，應立即移除並通知用戶。

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

### 筆記命名

- **檔案名稱不可含空格**，空格一律改為 `-`（例：`Obsidian-CLI-整合指南.md`）
- Wikilink 需對應實際檔名（含 `-`）：`[[Obsidian-CLI-整合指南]]`

### `updated` 欄位（盡力而為）

修改 `.md` 內容時**盡量**同步 frontmatter 的 `updated` 為今日日期（`YYYY-MM-DD`），但不強制 — 偶爾漂移可接受，不需為此中斷流程或裝 hook。

### Frontmatter Schema（固定）

所有筆記統一使用以下 schema。欄位**必須依此順序**，缺漏選填欄位可直接省略，但不可自行新增未列出的欄位。

```yaml
---
# ── 核心（必填，所有筆記） ──
title: <筆記標題>
created: YYYY-MM-DD
updated: YYYY-MM-DD

# ── 選填（依筆記類型出現） ──
source: <URL>                  # 外部來源
published: YYYY-MM-DD          # 外部來源發佈日（YouTube 影片日、文章發表日）
parent: "[[01.index]]"         # 歸屬 index（圖譜用）
last_sync_id: <video-id>       # 僅 YouTube 頻道 01.index.md
draft: true                    # Quartz 不發佈（opt-out）

# ── 必填，固定放最後 ──
tags:
  - tag-1
---
```

**欄位順序（硬規則）：**

```
title → created → updated → source → published → parent → last_sync_id → draft → tags
```

**欄位說明：**

| 欄位 | 必填 | 出現於 | 作用 |
|------|------|-------|------|
| `title` | ✓ | 全部 | Quartz 頁面標題來源（正文不用 `# Heading`） |
| `created` | ✓ | 全部 | 建立日 `YYYY-MM-DD` |
| `updated` | ✓ | 全部 | 最後修改日（盡力而為，見下節） |
| `source` | 條件 | 有外部來源時 | 外部資料必填，跨階段保留（Inbox → Cards → Topics 都不刪，供回查原文）；純原創 Card 可省略 |
| `published` | — | 有外部來源發佈日時 | 原文／影片發佈日 `YYYY-MM-DD`（YouTube 影片由 `vault-youtube-sync` 帶入、Clipping 由 Web Clipper 帶入）；無法取得可省略 |
| `parent` | — | Inbox/YouTube 影片 | `[[01.index]]`，讓筆記出現在頻道圖譜 |
| `last_sync_id` | — | YouTube 頻道 `01.index.md` | `vault-youtube-sync` skill 的同步書籤 |
| `draft` | — | 草稿 | `true` = 不發佈到 ob.bugloop.com；完成後移除 |
| `tags` | ✓ | 全部 | YAML list 格式，**固定放最後** |

**格式細節：**

- 日期一律 `YYYY-MM-DD`（不含時分秒）
- `tags` 必須 YAML list（不用 inline array `[a, b]`）
- Wikilink 值用雙引號包：`parent: "[[01.index]]"`
- URL 不需引號，除非含特殊字元

**白名單制**：未列於上表的欄位一律移除。

- Obsidian Web Clipper 若帶入 `author` / `description` / `cover` / `image` / `banner` 等未列欄位，一律清掉
- `/vault-check` 會自動稽核（R8）並由 `vault-fixer` 刪除
- 新增欄位前需先在本 schema 擴充，不可直接寫入未列欄位

### 筆記

- `title:` 用用戶說的主題，不加日期前綴
- 不使用 `# 標題` heading，Quartz 會從 frontmatter `title` 自動產生
- 若筆記尚未完成，可加 `draft: true` 防止發佈到網站
- Tags：優先沿用現有 tags，沒有才建新的（小寫、`-` 連接）
- Tag 格式一律用 YAML 清單：
  ```yaml
  tags:
    - obsidian
    - claude-code
  ```
- 建立後加 `open` 讓 Obsidian 自動開啟

## 更新規則

每次新增或批次更新筆記後，必須同步更新 `master-index.md`：
- YouTube 篇數（`Inbox/YouTube/ — N 篇影片摘要`）
- 若有新頻道，加入頻道清單與描述

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

### 回應格式

- 筆記：「已建立筆記《標題》✓」+ 路徑
- 搜尋：列出結果，最多 5 筆
