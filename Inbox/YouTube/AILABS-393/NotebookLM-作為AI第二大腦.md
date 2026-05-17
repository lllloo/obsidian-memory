---
title: NotebookLM 作為 AI 第二大腦
created: 2026-04-15
updated: 2026-04-15
source: https://www.youtube.com/watch?v=eFCHwtufjJc
published: 2026-02-13
parent: "[[01.index]]"
tags:
  - youtube
---

## NotebookLM CLI 工具

安裝與使用（token-efficient，適合長期任務）：

```bash
# 安裝
# 一個指令完成

# 驗證（開啟 Chrome 視窗登入 Google 帳號）
nlm auth

# 常用操作：建立 notebook、新增 source、查詢
```

## 作為 Codebase 的 Single Source of Truth

在 `CLAUDE.md` 中指定：所有架構決策與文件存入 notebook。工作流程：

1. 功能開發前：用 plan mode 規劃
2. Build 通過後：更新 notebook（記錄實作決策）
3. 未來查詢：Claude 透過 notebook 的 RAG 能力取得精確答案，不搜尋大量檔案

優點：Claude 獲得 Gemini 合成的答案，而非原始文件 dump。可分享 notebook 給非技術成員。

## 研究任務分工

Claude 負責找資料來源，NotebookLM 負責管理與查詢：

1. Claude 找到相關來源並上傳到新 notebook
2. 清除 context
3. Claude 透過 CLI 向 notebook 提問取得 key findings

好處：來源永久保存在 notebook，未來不需重複搜尋。

## Codebase 理解工具

使用 repomix 將 codebase 轉為 AI 友善格式：

```bash
npm install -g repomix
repomix  # 生成 token-efficient 文件
```

再用 notebookLM CLI 建立 notebook 並上傳。NotebookLM 可生成：

- Codebase atlas（key workings 導覽）
- 各功能的 mind map（可個別對話）
- Infographic 視覺化
- CSV/JSON 格式的結構化資料供 agent 使用

## Debug 知識庫

建立 notebook 存放除錯資源：

- 官方文件
- GitHub issues
- Community forums
- 相關部落格

在 `CLAUDE.md` 告知 Claude 遇到 bug 時先查 notebook，再上網搜尋。效果：直接查詢 notebook 取得結構化答案，不需 fetch 整個文件。

## 文件知識庫

PRD、架構文件等上傳到 notebook，供所有工具（Claude Code、Cursor、Gemini CLI）查詢，確保 context 準確性。

## 安全知識庫

建立安全 handbook notebook（可達 61 個 sources）：

- OWASP cheat sheets
- Tech stack 的安全 GitHub repos
- CVE databases

Claude 執行安全稽核時，以此 notebook 為依據，可發現程式化難以偵測的問題（如交易中的浮點誤差）。

## Agent 導向的視覺化

為 agent 建立導航用的視覺化資料：

- Mind map（JSON 格式）：Claude 查看各功能流程時使用
- 完整 slide deck
- Markdown 表格

Agent 遇到問題時查詢對應 mind map，而非在 file system 中爬尋。
