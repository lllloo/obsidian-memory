# Obsidian Memory Vault

## Vault 結構

| 資料夾 | 用途 | 路徑規則 |
|--------|------|----------|
| `Cards/` | 筆記 | `Cards/<標題>.md` |
| `Topics/` | MOC 與主題資料夾 | `Topics/<主題>.md` 或 `Topics/<主題>/` |
| `Templates/` | 模板 | — |

### 筆記組織策略（混合式）

1. **新筆記一律放 `Cards/`**
2. 當某個主題累積足夠筆記，在 `Topics/` 建立 **MOC** 筆記（如 `Topics/Obsidian.md`），用 wikilinks 串連相關筆記
3. 當 MOC 下的筆記多到需要獨立管理時，將 MOC 轉為 `Topics/<主題>/index.md`，相關筆記搬入該資料夾
4. **不要主動拆資料夾**，由用戶決定何時拆分

## 模板

- 筆記：`Templates/card.md`

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

### 自動更新 updated

**每次修改任何 `.md` 檔案內容時，必須同步將 frontmatter 的 `updated` 欄位更新為今日日期（`YYYY-MM-DD`）。** 無論是追加內容、修改欄位、還是程式化批次更新，都適用此規則。

### Frontmatter 屬性

**card.md 標準屬性：**
- `title`、`created`、`updated`、`source`、`tags`

**特殊屬性：**
- `draft: true` — 草稿，Quartz 不發佈；完成後移除
- `source` 無來源時可省略
- `tags` 固定放最後，且使用 YAML 清單格式

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
- YouTube 篇數（`YouTube/ — N 篇影片摘要`）
- 若有新頻道，加入頻道清單與描述

## YouTube 筆記語言規範

所有 YouTube 影片筆記正文內容一律以**繁體中文**撰寫。
- 技術名詞、品牌名、工具名保留英文（例：Claude Code、OpenAI、defuddle）
- 若 defuddle 取得英文 transcript，需翻譯整理為繁體中文後再寫入筆記

## 查詢規則

查詢相關知識時：
1. 先讀 `master-index.md` 確認資料位置
2. 主題筆記 → 對應 `Topics/` 子目錄
3. 影片摘要 → 依主題選對應 `YouTube/<頻道>/`
4. 跨主題 → Grep 搜尋 tag（frontmatter 中的 tags 欄位）

### 回應格式

- 筆記：「已建立筆記《標題》✓」+ 路徑
- 搜尋：列出結果，最多 5 筆
