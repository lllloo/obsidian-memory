---
name: ob-note
description: |
  在 Obsidian vault 中捕捉、記錄或搜尋內容。當用戶想把任何東西記到 Obsidian 時，或說「ob」、「筆記」、「日記」時，一定要使用此 skill。

  觸發情境（只要符合其中一個就觸發）：
  - 日記/今日記錄：「記一下今天」、「日記」、「daily」、「今天做了什麼」、「幫我記錄」
  - 建立筆記：「新增筆記」、「建立一則關於 X 的筆記」、「記錄這個想法」、「我想記下來」
  - 搜尋 vault：「找一下有沒有關於 X 的筆記」、「搜尋 vault」、「查一下我有沒有寫過 X」

  即使用戶只說「幫我記一下 X」而沒有指定位置，也應觸發此 skill 並判斷最合適的模式。
---

# Obsidian 捕捉 Skill

先讀取 vault 規則：

```bash
obsidian read path="CLAUDE.md"
```

依 CLAUDE.md 的規則執行。

## 模式判斷

| 用戶提到 | 使用模式 |
|----------|----------|
| 「今天」、「日記」、「daily」、「今天做了」 | 追加到今日日記 |
| 主題、概念、想法（非今日）、「建立」、「新增」 | 建立新筆記 |
| 「找」、「搜尋」、「有沒有」、「查」 | 搜尋 vault |

不確定時問：「你是想加到今天的日記，還是建立一則新筆記？」

---

## 追加到今日日記

直接追加，並更新 `updated` 屬性（Git Bash 需透過 PowerShell 執行）：

```bash
powershell.exe -Command "obsidian daily:append content='<內容>'"
obsidian daily:path
powershell.exe -Command "obsidian property:set path='<daily:path 回傳的路徑>' name='updated' value='<今日日期>'"
```

## 建立新筆記

```bash
obsidian tags
obsidian create path="Cards/<標題>.md" template=card open
```

若需自訂內容或 template 不支援，改用真實換行產生完整 content：

```bash
obsidian create path="Cards/<標題>.md" content="<依模板產生>" open
```

建立後補設屬性（`tags` 也要 set，否則不會寫入）：

```bash
powershell.exe -Command "obsidian property:set path='Cards/<標題>.md' name='created' value='<今日日期>'"
powershell.exe -Command "obsidian property:set path='Cards/<標題>.md' name='updated' value='<今日日期>'"
powershell.exe -Command "obsidian property:set path='Cards/<標題>.md' name='tags' value='<選好的 tags>'"
```

- `tags`：YAML list 格式，從 `tags` 結果挑選，優先沿用現有 tag
- `# 標題`：用戶說的主題

## 搜尋 vault

```bash
obsidian search:context query="<關鍵字>" format=json
```

若失敗改用：

```bash
obsidian search query="<關鍵字>"
```
