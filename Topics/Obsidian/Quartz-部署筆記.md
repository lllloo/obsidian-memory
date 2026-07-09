---
title: Quartz 部署筆記
created: 2026-03-22
updated: 2026-07-09
source: https://github.com/lllloo/obsidian-deploy
tags:
  - quartz
  - obsidian
  - deploy
---

把 Obsidian vault 透過 [Quartz 4](https://quartz.jzhao.xyz) 發佈成靜態網站的紀錄。發佈層與筆記本體**分屬兩個 repo**，本 vault 不含任何 Quartz 設定。

## 架構（分離雙 repo）

- **筆記本體**：本 repo `obsidian-memory`，含 `raw/`、`wiki/`、`schema/`、`Cards/`、`Topics/` 與 skills，無 Quartz 設定檔。
- **發佈層**：獨立 repo [obsidian-deploy](https://github.com/lllloo/obsidian-deploy)，存放 `quartz.config.ts`、`quartz.layout.ts`、CI 與稽核腳本。
- **串接方式**：發佈 repo 的 CI 用 `actions/checkout` 把 `obsidian-memory` 整個 clone 進 `content/`（**獨立 checkout，非 submodule**），Quartz 把 `content/` 當 vault 根目錄讀取。
- **發佈範圍**：`ignorePatterns`（定義在發佈 repo 的 `quartz.config.ts`）排除 `.obsidian` 與私有層整個資料夾（`raw/`、`wiki/`、`schema/`）、根目錄治理檔（`CLAUDE.md`、`AGENTS.md`、`README.md`）；實際只發佈 `Cards/`、`Topics/` 與根 `index.md`。完整清單以發佈 repo 的 `quartz.config.ts` 為準，vault 新增私有資料夾時記得同步加入。
- **部署網址**：[bugloop.com](https://bugloop.com)（GitHub Pages + 自訂網域）。

## 部署流程

部署由**發佈 repo（obsidian-deploy）** 的 `main` 觸發，不是本 vault：

1. **自動觸發**：push 到 obsidian-deploy `main` 且異動到 Quartz 層檔案（`quartz/**`、`quartz.config.ts`、`quartz.layout.ts`、`package.json` / `package-lock.json`、`deploy.yml`）。
2. **本 vault 筆記變動「不會」自動觸發**：改了 `obsidian-memory` 的筆記後，要到 obsidian-deploy 手動 `workflow_dispatch` 才會重新抓最新內容重建。
3. CI（`deploy.yml`）依序：checkout 兩 repo（deploy 自身 + vault 進 `content/`）→ Node 22 `npm ci` → `npx quartz build` 產出 `public/` → `upload-pages-artifact` → `deploy-pages` 部署到 GitHub Pages。
4. 完成後發 Discord 成功／失敗通知（webhook 走 `secrets.DISCORD_WEBHOOK`）。

## 重點設定

`quartz.config.ts`（在發佈 repo）關鍵值：

```ts
pageTitle: "Memory Pieces"
baseUrl: "bugloop.com"
locale: "zh-TW"
enableSPA: true
defaultDateType: "created"   // 用 created 當顯示日期
// ignorePatterns 見上方「發佈範圍」，以發佈 repo 原始檔為準
```

## 筆記格式

- 用 frontmatter `title` 當標題，不用 `# heading`
- `draft: true` 可隱藏未完成的筆記
- Wikilinks 連筆記，Markdown link 連 tag 頁面和外部連結
