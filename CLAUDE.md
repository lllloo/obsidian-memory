# Obsidian Memory Vault

## Vault 結構

| 資料夾 | 用途 | 路徑規則 |
|--------|------|----------|
| `Inbox/` | 日記 | `Inbox/YYYY-MM-DD.md` |
| `Cards/` | 筆記 | `Cards/<標題>.md` |
| `Templates/` | 模板 | — |

## 模板

- 日記：`Templates/daily.md`
- 筆記：`Templates/card.md`

操作前先讀取對應模板以了解結構。

## 已知問題

Obsidian CLI 在 Git Bash 環境下部分指令會回傳 exit code 127（shell 差異造成）。

**Windows (Git Bash)**：用 PowerShell 包一層：
```bash
powershell.exe -Command "obsidian <指令>"
```

**macOS/Linux**：若遇到同類問題，改用等效的兩步驟拆解。例如 `daily:append` 失敗時：
1. `obsidian daily:path` 取得今日路徑
2. `obsidian append path="<date>.md" content="內容"`

## 安全規則

此 vault 的內容會透過 Quartz 發佈到公開網站（ob.bugloop.com）。**所有寫入或修改的內容在 commit 前必須檢查，確保不包含以下敏感資料：**

- API key、secret、token
- 密碼、帳號憑證
- 私人 IP、內部網址
- 個人隱私資訊（身分證、電話、地址等）
- 任何不適合公開的內容

若發現既有筆記含有敏感資料，應立即移除並通知用戶。

## 規則

### 日記

- 若有未填佔位符，先 `create overwrite` 填入再追加：
  - `created:` / `updated:` → 今日日期
  - `# 標題` → 今日日期（如 `2026-03-19`）
- 追加內容保持簡潔，不加多餘標題或結構

### 筆記

- 標題用用戶說的主題，不加日期前綴
- Tags：優先沿用現有 tags，沒有才建新的（小寫、`-` 連接）
- Tag 格式一律用 YAML 清單：
  ```yaml
  tags:
    - obsidian
    - claude-code
  ```
- 建立後加 `open` 讓 Obsidian 自動開啟

### 回應格式

- 日記：「已追加到今日日記 ✓」+ 簡短顯示內容
- 筆記：「已建立筆記《標題》✓」+ 路徑
- 搜尋：列出結果，最多 5 筆
