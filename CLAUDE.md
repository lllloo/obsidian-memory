# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概覽

Obsidian 個人知識庫，以 [Quartz 4](https://quartz.jzhao.xyz/) 發佈至 `ob.bugloop.com`。Vault 內容放在 `content/`，Quartz 框架程式碼在 `quartz/`。

## 常用指令

```bash
npx quartz build --serve   # 本地預覽（localhost:8080）
npm run check              # TypeScript 型別檢查 + Prettier 格式驗證
npm run format             # 自動格式化
npm run test               # 執行測試
```

## 架構

- `content/` — Obsidian vault（筆記、日記、模板），Quartz 從此目錄讀取 Markdown 建站
- `quartz/` — Quartz 框架原始碼（不需修改）
- `quartz.config.ts` — 站台設定（外觀、plugins、ignorePatterns）
- `quartz.layout.ts` — 版面配置
- `.github/workflows/deploy.yml` — push 到 `main` 自動建置並部署至 GitHub Pages

## Quartz 重要行為

- `ignorePatterns` 包含 `Templates`、`CLAUDE.md`、`private`、`.obsidian`，這些不會發佈
- frontmatter 加 `draft: true` 的筆記會被 `RemoveDrafts` plugin 過濾，不發佈
- 日期優先順序：frontmatter → git → filesystem（`CreatedModifiedDate` plugin）

## Obsidian Vault 規則

筆記結構、命名規則、tag 格式、安全規範等詳見 [`content/CLAUDE.md`](content/CLAUDE.md)。

**核心規範 (Core Mandates)：**
- **Obsidian 寫入規範優先級**：在進行任何 `content/` 目錄下的讀取、建立或修改操作前，**必須**先完整讀取並嚴格遵循 `content/CLAUDE.md` 中的命名規則、Frontmatter 格式與安全規範。此文件內容具有最高指令效力。

## Claude Code Agent 與指令

此 repo 統一管理 Obsidian 相關的 Claude Code 設定，透過 symlink 掛載至全域，讓這些設定在任何專案目錄都能生效。

| 檔案 | 全域路徑 | 用途 |
|------|---------|------|
| `.claude/agents/obsidian.md` | `~/.claude/agents/obsidian.md` | Obsidian 筆記操作 agent |
| `.claude/commands/ob.md` | `~/.claude/commands/ob.md` | `/ob` 指令定義 |

**建立 symlink（Windows，需開啟 Developer Mode 或以管理員執行）：**

```powershell
# 在 repo 根目錄執行
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\agents\obsidian.md" -Target "$PWD\.claude\agents\obsidian.md"
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\commands\ob.md" -Target "$PWD\.claude\commands\ob.md"
```

觸發方式：對話中提到「ob」、「日記」、「daily」、「記一下」、「建立筆記」、「新增筆記」、「找筆記」時自動啟用。
