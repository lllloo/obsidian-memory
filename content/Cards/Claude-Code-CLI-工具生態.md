---
title: Claude Code CLI 工具生態
created: 2026-04-24
updated: 2026-04-24
tags:
  - claude-code
  - cli
---

Claude Code 生態的強共識：**CLI 工具優於 MCP**。本 Card 整理原因、工具分類速查、runtime 可見性方案，以及搭配 CLI 使用的進階技巧。

## 為何 CLI 優於 MCP

- CLI 與 Claude Code 同住 terminal，無額外 overhead
- Token 消耗更低（Playwright CLI 比 Playwright MCP Server 同任務省約 90,000 tokens）
- 功能通常更完整
- 通常配套 skill 一起發佈（一行指令同時裝 CLI + skill 到 `.claude/`）

## 通用安裝方法

```
1. 複製 GitHub repo URL
2. 貼入 Claude Code，說「照這個安裝 <工具名> CLI」
3. Claude Code 自動執行安裝 + 認證
```

## 工具分類速查

| 分類 | 工具 | 用途 |
|---|---|---|
| **部署** | GitHub CLI | commit / push / branch / PR 一句話完成 |
| | Vercel CLI | 配合 GitHub CLI 建 CI/CD pipeline |
| **瀏覽器 / UI** | Playwright CLI | 自動設計並執行 web app 測試；`--headed` 可視化 |
| | Vercel Agent Browser | 用 accessibility tree，比 Chrome extension 壓縮 DOM 至 200-400 tokens |
| **資料庫** | Supabase CLI | 開源、可本地運行；直接建 schema 與認證 |
| **支付** | Stripe CLI | 略過介面，直接處理商品與設定 |
| **多媒體** | FFmpeg | 音訊影片切割、反轉拼接、字幕處理 |
| **Google 套件** | Google Workspace CLI（GWS） | Gmail / Docs / Sheets / Drive；可沙箱化 |
| **本地 LLM** | LLMFit | 判斷本機硬體最適合的 Ollama 模型 |
| **知識工具** | NotebookLM-PY（社群非官方 wrapper） | 終端操控 NotebookLM（丟 URL 做分析、產 podcast / slide / quiz） |
| **Meta** | CLI Anything | 把任何開源專案轉為 CLI |

### 部署流程（GitHub + Vercel）

1. **GitHub**：建 repo → 複製 URL → `commit and push to <URL>`（首次需認證）
2. **Vercel**：用 GitHub 登入 → Import repo → Deploy
3. **自動化**：後續 `commit and push` 會自動觸發 Vercel 重新部署
4. 建議裝 GitHub CLI + Vercel CLI，之後所有操作自然語言完成

## 讓 Agent 看見 client-side runtime

Terminal-only agent 看不到瀏覽器 runtime 問題，三種方案：

| 方案 | 特點 |
|---|---|
| Claude Chrome extension | DOM capture + console log |
| Puppeteer MCP | 隔離瀏覽器，不帶現有 sessions |
| **Vercel Agent Browser（推薦）** | accessibility tree 唯一 element reference，DOM 從數千 token 壓縮到 200-400 token |

在 `CLAUDE.md` 設定「優先使用 agent browser，fallback 才用 MCP」。

## 搭配 CLI 工具的進階技巧

- **TypeScript strict mode**：`tsconfig.json` 設 `strict: true`；compiler 在 build 時抓 null、隱式型別等問題，agent 能依 terminal 錯誤自修
- **User stories 驅動測試**：開發前寫 user stories（含 priority + acceptance criteria），agent 逐一實作，確保符合用戶預期
- **預測性錯誤偵測**：要求 Claude 檢視實作並列出「可能但尚未發生」的問題；透過 pattern matching 已知失敗模式，可抓到多層測試未發現的潛在 bug
- **Context7 MCP**：自動取得指定 library 最新文件，彌補模型知識截止日落差

## 相關主題

- [[Claude-Code-效率技巧與設定]] — Hub MOC，跨主題速查
- [[Claude-Code-Skills]] — CLI 工具通常與 skill 綁在一起發布
- [[Agent-Harness]] — 強化開源專案（AutoResearch / OpenSpace / Claude Peers 等）與 harness 架構
