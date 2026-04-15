---
title: 用 Python MCP Server 在 Claude Desktop 自動化任何任務
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-10-31
source: https://www.youtube.com/watch?v=l6Pw7G9URTY
---

## 核心概念

用自訂 Python MCP Server 搭配 Claude Desktop 或 Claude Code 作為介面，取代傳統的 cron job、UI 與部署流程。只需建立 Python function，就能讓 Claude 以自然語言呼叫任意自動化任務。

## 專案結構與建置

- 用 `uv init` 建立專案，再用 `uv venv` 建立虛擬環境
- 安裝依賴：`uv add python-dotenv "mcp[cli]" youtube-transcript-api`
- 目錄結構：
  ```
  project/
  ├── server.py       # MCP server 入口
  ├── src/
  │   ├── service.py  # 功能邏輯（如 YouTubeTranscriptService）
  │   └── utils/      # 工具函式（如 extract_video_id）
  └── tests/
      └── test.py
  ```
- UV 特色：在 Python 檔案頂端以特定語法宣告 dependencies，UV 執行時會自動建立環境並安裝，免去手動管理虛擬環境

## 本地測試

用 MCP Inspector 驗證 server：

```bash
mcp dev server.py
```

- 首次執行會提示安裝 MCP Inspector
- 連線後可列出工具、輸入參數、執行並查看輸出

## 連接 Claude Desktop

編輯 Claude Desktop 的 `claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "youtube": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/project", "run", "server.py"]
    }
  }
}
```

- 儲存後重啟 Claude Desktop，至 Settings → Developer 確認 server 狀態為 running
- 新對話中點選工具圖示可看到 MCP server 已連線

## 連接 Claude Code

```bash
claude mcp add youtube --command "uv" --args "--directory" "/absolute/path" "run" "server.py"
claude mcp list  # 確認已加入
```

啟動 Claude Code 後可直接以自然語言呼叫 MCP 工具，並立即在本地建立檔案。

## 商業應用潛力

- B2B 機會：許多企業員工已在使用 ChatGPT/Claude 但遇到整合限制，開發者可整合 off-the-shelf MCP server 與客製 server，為企業建立自動化工作流
- 優勢：無需複雜部署、員工使用熟悉的 AI 介面操作
