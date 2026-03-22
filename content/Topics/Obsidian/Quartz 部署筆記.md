---
title: Quartz 部署筆記
tags:
  - quartz
  - obsidian
  - deploy
created: 2026-03-22
updated: 2026-03-22
---

把 Obsidian vault 透過 [Quartz 4](https://quartz.jzhao.xyz) 發佈成靜態網站的紀錄。

## 架構

- Quartz 直接整合在 vault 的 repo 中
- `content/` 用 symlink 連結 `Cards/`、`Inbox/`、`Topics/`，Quartz 透過這些 symlink 讀取 vault 內容
- `ignorePatterns` 排除 Templates、.obsidian、.claude、CLAUDE.md
- 部署網址：[ob.bugloop.com](https://ob.bugloop.com)

## 部署流程

1. 推送到 GitHub `main` 分支
2. GitHub Actions 自動執行 `npx quartz build`
3. 產出 `public/` 靜態檔案，部署到 GitHub Pages
4. 自訂網域 `ob.bugloop.com` 指向 GitHub Pages

## 重點設定

```ts
// quartz.config.ts
pageTitle: "Memory Pieces"
baseUrl: "ob.bugloop.com"
locale: "zh-TW"
defaultDateType: "created"
ignorePatterns: ["private", "Templates", ".obsidian", ".claude", "CLAUDE.md", "node_modules"]
```

## 筆記格式

- 用 frontmatter `title` 當標題，不用 `# heading`
- `draft: true` 可隱藏未完成的筆記
- Wikilinks 連筆記，Markdown link 連 tag 頁面和外部連結

## 本地開發

```bash
npx quartz build --serve
# http://localhost:8080
```

## 相關
- [[Obsidian]]
