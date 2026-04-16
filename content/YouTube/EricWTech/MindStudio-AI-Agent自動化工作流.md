---
title: 用 MindStudio 自動化整個工作流程
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-14
source: https://www.youtube.com/watch?v=4zczQAWrG1o
parent: "[[01.index]]"
---

## 核心概念

MindStudio 讓建立 AI agent 變得像複製模板一樣簡單 — 所有 agent 共用同一個基礎結構（觸發器 + AI 步驟），只改 prompt 就能適用不同情境。

## 基本架構

MindStudio agent 的結構：
- Start block（觸發器）
- Generate text block（呼叫 AI 模型）
- End block（輸出結果）

Run mode 設為 **Browser Extension** 後，agent 自動獲取：
- 頁面 URL
- 頁面 metadata
- 完整頁面內容（網站、YouTube transcript、PDF 均自動處理）

## 建立第一個 Agent：內容摘要器

1. Dashboard → Create New Agent
2. Automations tab → 點選 Start block → Run mode 切換為 **Browser Extension**
3. 新增 Generate text block，設定 prompt：`Summarize the content and extract key people and entities`
4. Prompt 中插入變數 `{{page_content}}` 帶入當前頁面內容
5. 命名為「Content Summarizer」→ Publish
6. 開啟三點選單 → Pin to extension，釘選到瀏覽器

效果：在任何文章、YouTube 影片或 PDF 頁面點擊即可取得摘要與關鍵實體。

## 複用模式：複製 Agent 改 Prompt

建好第一個 agent 後，之後幾乎不需要重新建立 — 直接複製修改 prompt：

**X Thread Analyzer（分析 X 貼文串）**
- Duplicate Content Summarizer
- 更新 prompt：識別主推文、對話結構、互動模式
- 可用 MindStudio 的 prompt generator 自動擴展為更詳細格式
- Rename → Publish → Pin

**Financial Document Analyst（財報分析）**
- Duplicate 再一次
- Prompt：分析財務文件的基本面、風險、重點洞察
- 適用 10-Q PDF 等文件，加速初步閱讀

## 核心優勢

三個 agent 結構完全一樣：
- 一個觸發器
- 一個 Generate 步驟
- 不同 prompt

比 n8n 等重型自動化工具更快上手，比自建 pipeline 更整潔，焦點在結果而非接線。
