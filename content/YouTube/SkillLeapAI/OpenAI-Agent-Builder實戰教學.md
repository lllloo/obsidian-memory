---
title: 用OpenAI Agent Builder打造自己的AI Agent
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-12-03
source: https://www.youtube.com/watch?v=ZkYxLIsqJoo
---

## 什麼是 AI Agent

- **一般 chatbot**（如 ChatGPT）：被動回應，你問它答
- **AI Agent**：主動執行，給它目標，它自己決定步驟、呼叫工具、處理多步驟任務並產出結果
- 通常含有記憶、可存取外部工具

## OpenAI Agent Builder 概覽

- 入口：platform.openai.com → 左側「Agents」→「Build agents」
- 視覺化工作台，不需寫程式，拖放節點（Node）即可建立工作流程
- 目前仍處於 Beta，連接工具時可能遇到問題

## 核心元件（Nodes）

- **Start Node**：觸發入口（通常是聊天輸入）
- **Agent Node**：Agent 的大腦，包含：指令（System Prompt）、模型選擇、工具存取、記憶（Chat History）、輸出格式
- **Condition Node**：根據條件分流（如：這是退款問題→轉退款 agent）
- **File Search Node**：讓 Agent 搜尋可查詢的文件庫
- **Guard Rail Node**：安全檢查，防止不當輸入/輸出或 jailbreak
- **MCP Node**：連接外部服務（Gmail、Zapier 等）
- **Notes**：供開發者記錄說明用，不影響功能

## 建立三階段 Lead Generation Agent

### 目標工作流程

1. **Lead Finder Agent**：用網路搜尋找特定類型的潛在客戶
2. **Data Entry Agent**：將資料填入 Google Sheets
3. **Outreach Agent**：依據資料在 Gmail 草擬個人化開發信

### 準備工作

- 在 Google Sheets 建立欄位：名稱、商業類型、地址、電話、Email、描述、是否已發信

### Agent 1：Lead Finder

- 指令：你是潛在客戶開發 agent，搜尋指定地點與類型的公司，並將資訊傳遞給下一個 agent
- 工具：啟用 Web Search
- 上下文大小設定為 High（搜尋更多資訊）

### Agent 2：Data Entry（需設定 MCP + Zapier）

由於 Agent Builder 目前不支援直接寫入 Google Sheets，需透過 Zapier MCP：

1. 前往 mcp.zapier.com，登入帳號
2. 建立新 MCP Server（選擇 OpenAI Agent Builder 作為 client）
3. 指定工具：Google Sheets → 「建立新列」
4. 選定特定試算表（避免 Agent 存取錯誤檔案）
5. 複製 API 金鑰，貼入 Agent Builder 中的 MCP 連接欄位
6. 關閉預設勾選的「Allow adding more tools」

- 指令：取得前一個 agent 的資料，依照試算表欄位逐一填入

### Agent 3：Outreach（需設定 Gmail + Google Sheets MCP）

在同一 Zapier MCP Server 加入三個工具：
- Gmail：「建立草稿」（設定 Body Type 為 HTML）
- Google Sheets：「查詢特定列」
- Google Sheets：「更新特定列」（用來標記「已發信」）

- 指令：從試算表讀取潛在客戶資料 → 根據描述個人化撰寫開發信 → 在 Gmail 建立草稿 → 將該列「已發信」欄位更新為 Yes

### 執行測試

- 在聊天框輸入：「幫我找芝加哥 5 間影片製作公司」
- Agent 1 搜尋並找到公司
- Agent 2 將資料填入 Google Sheets（含 Email 與描述）
- Agent 3 為每間公司在 Gmail 建立個人化草稿（主旨與郵件內容均不同）

## 注意事項

- 建議設定 MCP 的 Approval：由於已限制工具範圍，可選「Never require approval」
- 此平台仍處於 Beta，有時需多試幾次才能成功連接
- 若要將 Agent 嵌入自有網站，需要更進階的技術（作者仍偏好 Chatbase 做網站嵌入）

## 其他 Agent 建置平台比較

- **Make、Zapier、N8N**：更容易上手，直接支援多種工具連接
- **Google 新 Agent 平台**（Opal 等）：功能也在快速演進
- **Chatbase**：最適合建立可嵌入網站的客服 Agent
