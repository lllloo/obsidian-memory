---
title: 建立付費 MCP 服務
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-05-20
source: https://www.youtube.com/watch?v=VKAq_PA_21U
---

## 核心概念

Stripe 推出了 Agent Toolkit，讓你能為 MCP server 加上付費機制，並結合 Cloudflare MCP Agent class 和 mcp-remote 套件，實現完整的 MCP 商業化流程：使用者直接在 Cursor 中觸發付款、訂閱、按使用量計費。

## 技術架構

三個關鍵套件：
- **Stripe Agent Toolkit**：為 MCP tool 加上付款邏輯
- **Cloudflare MCP Agent class**：將任意函式轉成 MCP tool，並處理 OAuth
- **mcp-remote**：讓使用者在 Cursor 加入 MCP 時自動觸發登入 / 付款流程

## 建立 MCP Server 基礎（Cloudflare）

```bash
npx create-cloudflare my-mcp-server --template=cloudflare-ai-demo-remote-mcp-oauth
```

在 `src/index.ts` 中繼承 `McpAgent` 並定義工具：

```typescript
class MyMCP extends McpAgent {
  server = new McpServer({ name: 'My MCP', version: '1.0.0' })

  async init() {
    this.server.tool('add', { a: z.number(), b: z.number() }, async ({ a, b }) => ({
      content: [{ type: 'text', text: String(a + b) }]
    }))
  }
}
```

MCP URL 格式：`https://your-worker.workers.dev/mcp`

## 整合 Stripe 付款

改用 `PaidMcpAgent`（Stripe Agent Toolkit 提供，繼承自 Cloudflare 的 `McpAgent`）：

```typescript
// 付費工具需額外傳入 priceId 和 paymentReason
this.server.tool('generateEmoji', 
  { priceId: 'price_xxx', paymentReason: '每次生成 emoji 計費' },
  { prompt: z.string() },
  async ({ prompt }) => { /* 實際邏輯 */ }
)
```

使用者未付款時，agent 會自動收到付款連結並顯示原因。

## 三種付款模式

**一次性付款**
- Stripe 建立 Product → 定價選 One-off → 複製 Price ID
- mode: `payment`

**訂閱制**
- 定價選 Recurring，設定月費
- mode: `subscription`

**按使用量計費（最適合 MCP）**
- Stripe 建立 Meter（設定計量事件名稱）
- 建立 Usage-based 定價，定義分級方案，例如：
  - 前 5 次免費（單價 $0）
  - $1 = 30 credits
  - $10 = 500 credits，超額按 $0.001/次計算
- Meter 自動追蹤用量並動態計算帳單

## OAuth 認證層

Cloudflare 提供 `OAuthProvider` class，自動處理 OAuth 流程（發送 code、等待授權、產生 access token）。只需實作 `/authorize` 端點的實際登入邏輯：

```typescript
// app.ts - 替換 mock 登入，加入真實驗證
app.get('/authorize', async (c) => {
  // 若未登入 → 顯示登入/註冊頁面
  // 若已登入 → 直接進行 OAuth 授權確認
})
```

mcp-remote 套件讓 Cursor 加入 MCP 時自動觸發此流程：開啟瀏覽器 → 登入 → 完成後 Cursor 自動連上已授權的 MCP。
