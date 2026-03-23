---
title: Obsidian CLI 整合指南
tags:
  - obsidian
  - claude-code
  - cli
created: 2026-03-17
updated: 2026-03-22
---

透過 [Obsidian CLI](https://obsidian.md/help/cli) 讓 Claude Code 操作 Obsidian vault。

Claude Code 使用 `obsidian:obsidian-cli` skill 呼叫 CLI 指令，直接讀寫 vault 內的筆記。

## 語法

```
obsidian <指令> [參數]
```

- 參數格式：`key="value"`（有空格需引號）
- 布林旗標：`--silent`、`--overwrite`、`--permanent`
- 輸出格式：`format=json|csv|md|yaml|tree|tsv|paths`
- 指定 vault：`vault="Vault Name"`

## 常用指令

### 筆記操作

| 指令 | 說明 |
|------|------|
| `obsidian read file="Note"` | 讀取筆記 |
| `obsidian create name="Title"` | 建立筆記 |
| `obsidian create name="Title" template="Template"` | 從模板建立 |
| `obsidian append file="Note" content="..."` | 追加內容 |
| `obsidian prepend file="Note" content="..."` | 前置內容 |
| `obsidian move file="Note" to=Archive/` | 搬移（自動更新連結） |
| `obsidian delete file="Note"` | 刪除（移至垃圾箱） |

### Daily Notes

| 指令 | 說明 |
|------|------|
| `obsidian daily` | 開啟今日日記 |
| `obsidian daily:read` | 讀取今日日記 |
| `obsidian daily:path` | 取得今日日記路徑 |
| `obsidian daily:append content="..."` | 追加到今日日記 |
| `obsidian daily:open date=YYYY-MM-DD` | 開啟指定日期 |

### 搜尋

| 指令 | 說明 |
|------|------|
| `obsidian search query="keyword"` | 全文搜尋 |
| `obsidian search query="[tag:name]"` | 依標籤搜尋 |
| `obsidian tags` | 列出所有標籤 |
| `obsidian links file="Note"` | 出站連結 |
| `obsidian backlinks file="Note"` | 入站連結 |
| `obsidian orphans` | 孤立筆記 |

### Properties

| 指令 | 說明 |
|------|------|
| `obsidian properties file="Note"` | 查看屬性 |
| `obsidian properties:set file="Note" key=value` | 設定屬性 |
| `obsidian properties:remove file="Note" key=field` | 移除屬性 |

### 開發者

| 指令 | 說明 |
|------|------|
| `obsidian plugin:reload id=my-plugin` | 重載插件 |
| `obsidian eval code="JavaScript"` | 執行 JS |
| `obsidian dev:screenshot path=~/screenshot.png` | 截圖 |
| `obsidian dev:errors` | 查看錯誤 |

## 相關
- [[Obsidian-Skills-總覽]]
- [[daily-append-bug]]
