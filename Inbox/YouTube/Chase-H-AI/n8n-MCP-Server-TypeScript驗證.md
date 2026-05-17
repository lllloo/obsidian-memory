---
title: n8n 官方 MCP Server 用 TypeScript 改變 Claude Code 自動化
created: 2026-05-04
updated: 2026-05-04
source: https://www.youtube.com/watch?v=Gq0l4IYRIIU
published: 2026-05-01
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - n8n
---

## 為什麼這個 MCP Server 重要

- n8n 在 Claude Code、Codex 出現後地位下滑，但本週剛推出的官方 MCP Server 重新給了它存在價值
- 過去第三方 MCP（如 Lonkowski 版）都是 hack：把整堆文件塞進 context，或寫超長 skill 文件強迫 Claude Code 寫出能用的 JSON
- 共同問題：**LLM 在猜 JSON 結構，沒有 guardrail**

## 關鍵差異：用 TypeScript 表達工作流

不是直接讓 LLM 產生 raw JSON，而是：

1. Claude Code 解析使用者意圖（例如「每早報天氣的自動化」）
2. 呼叫 MCP server 取 node types
3. 用 **TypeScript** 撰寫 workflow
4. TypeScript 送回 MCP server 做 type-check 與編譯驗證
5. 通過後轉 JSON
6. 自動寫入 n8n instance

n8n 團隊在 LinkedIn 的說法：「TypeScript 給你 type checking 與 compilation，模型必須產出能編譯的東西，過濾掉大量錯誤」——這就是 guardrail 的來源。

## n8n 在 2026 的角色

- 不再是「主力自動化工具」
- 仍有獨特 niche：
  - AI agency 場景：交付給非技術 client 看得懂的視覺化 workflow
  - 簡單流程，又要 client 能自己手動微調
- 複雜邏輯仍建議直接寫 code（在 Claude Code 內）
- 但「簡單但需要 hand-off」的場景，現在又重新值得用了

## 安裝步驟

1. 確保 n8n instance 升級到最新
2. 進 Settings → Instance Level MCP → 設為 enabled
3. （選用）若要對既有 workflow 操作，需個別啟用該 workflow
4. 點 Connection Details → 拿 access token（生產環境請用環境變數，不要直接貼進 chat）
5. 把 server URL、access token、JSON config 餵給 Claude Code，請它幫忙設定 MCP
6. 重啟 Claude Code，輸入 `/mcp` 應看到 n8n MCP 已連線

## 使用範例 1：簡單天氣自動化

prompt：「Use the n8n MCP to build me a workflow that fires daily at 9 a.m., fetches Toronto weather, and emails me the forecast.」

行為：

- 抓 SDK 與 node list
- 寫好 workflow 並驗證
- 呼叫 n8n MCP 直接寫進 instance
- 完成後在 n8n 中可見 `Toronto Daily Weather Email`，**節點全部已串好對應欄位**
- 點 execute 即可寄出

## 使用範例 2：每日 AI 新聞 newsletter

prompt：每早 10:00 抓多個 AI RSS、用 GPT-5 摘要、寄信給我（讓 Claude Code 自選 RSS 源）。

產出：

- Trigger → 三個 RSS feed → merge → 過濾 24 小時內 → aggregate → GPT-5 系統 prompt → email
- 第一次跑出錯（GPT-5 不支援 `temperature` 參數）→ 把錯誤訊息貼回 Claude Code → 自動修好
- 全程約 5 分鐘含 troubleshooting

## 結論

- 對仍把 n8n 放在 stack 裡的人，這是目前最順的整合方式
- 要建立**過於複雜的自動化**——直接寫 code 仍是最佳解
- 簡單、需 visual、需 client hand-off 的 niche——這個 MCP Server 顯著降低門檻
