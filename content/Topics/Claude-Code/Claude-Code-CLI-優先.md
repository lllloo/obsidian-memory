---
title: Claude Code CLI 優先
created: 2026-04-24
updated: 2026-05-04
tags:
  - claude-code
  - cli
---

## CLI 優於 MCP

- CLI 與 Claude Code 同住 terminal，無額外 overhead
- Token 消耗更低（Playwright CLI 比 Playwright MCP Server 同任務省約 90,000 tokens）
- 功能通常更完整
- 通常配套 skill 一起發佈（一行指令同時裝 CLI + skill 到 `.claude/`）
- 安裝方式：複製 GitHub repo URL 貼入 Claude Code，說「照這個安裝 \<工具名\> CLI」，Claude Code 自動執行安裝 + 認證

## 工具速查

| 分類 | 工具 | 用途 |
|---|---|---|
| **部署** | GitHub CLI | commit / push / branch / PR 一句話完成 |
| | Vercel CLI | 配合 GitHub CLI 建 CI/CD pipeline |
| **瀏覽器 / UI** | Playwright CLI | 自動設計並執行 web app 測試；`--headed` 可視化 |
| **資料庫** | Supabase CLI | 開源、可本地運行；直接建 schema 與認證 |
| **支付** | Stripe CLI | 略過介面，直接處理商品與設定 |
| **多媒體** | FFmpeg | 音訊影片切割、反轉拼接、字幕處理 |
| **Google 套件** | Google Workspace CLI（GWS） | Gmail / Docs / Sheets / Drive；可沙箱化 |
| **本地 LLM** | Ollama Benchmark | 評估本機硬體最適合的模型規模 |
| **知識工具** | NotebookLM-PY | 終端操控 NotebookLM（非官方 wrapper，需注意 API 變動風險） |
| **Meta** | CLI Anything | 把任何開源專案轉為 CLI |

## 相關主題

- [[Claude-Code-指令速查]] — session 指令速查（/insights、/btw、/statusline 等）
- [[Claude-Code-多-Agent-協作]] — Subagent / Teams / Fork / worktree
- [[Claude-Code-Skills]] — CLI 工具通常與 skill 綁在一起發布
- [[Agent-Harness]] — 強化開源專案（AutoResearch / OpenSpace / Claude Peers 等）與 harness 架構
