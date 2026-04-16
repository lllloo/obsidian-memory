---
title: 打造下一個十億美元 Agent
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-06-10
source: https://www.youtube.com/watch?v=iq97iSsBsR4
parent: "[[01.index]]"
---

## 垂直 Agent 的機會

AI coding 是第一個真正取得市場驗證的 agent 使用場景，但接下來 24 個月將出現大量垂直型 agent：
- Cursor for 簡報（slides）
- Cursor for 試算表（spreadsheets）
- Cursor for 設計
- Cursor for 影片剪輯

核心洞察：任何深度整合特定知識工作的端對端流程，都是建立垂直 agent 的機會。

## Agent 架構的兩個核心元件

**1. Agent + 工具層**
- Agent 需要存取各種工具才能完成任務
- 以 Cursor 為例：寫程式、建立檔案、執行指令列、git push、搜尋最新文件

**2. Playground / Canvas 層**
- 使用者用來審查、追蹤 agent 進度並協作的工作區
- 以 Cursor 為例：程式碼編輯器是讓使用者看結果並隨時介入修改的空間
- Agent 永遠能取得使用者當前畫面的上下文

## 技術選型：Vercel AI SDK

使用 TypeScript 的開源框架，Perplexity、v0 等均以此為基礎。分兩大部分：

**AI SDK Core**
- 統一語法呼叫不同 LLM 供應商（Anthropic、OpenAI 等），切換 model 不需改底層邏輯
- 提供 `generateText`、`streamText`、`generateObject`（結構化輸出）、工具整合

**AI SDK UI**
- 將 text、JSON、tool call 串流到前端，提供 `useChat` hook

## 建置流程：AI SDK Core 基礎

```bash
pnpm init
pnpm install ai
pnpm install @ai-sdk/anthropic  # 或 @ai-sdk/openai
pnpm install ts-node typescript
```

```typescript
import { anthropic } from '@ai-sdk/anthropic'
import { generateText, streamText, streamObject } from 'ai'
import { z } from 'zod'

const model = anthropic('claude-3-5-sonnet-20241022')

// 串流文字
const result = await streamText({ model, prompt: '...' })
for await (const chunk of result.textStream) { console.log(chunk) }

// 串流結構化輸出
const objResult = await streamObject({
  model,
  schema: z.object({ title: z.string(), author: z.string(), content: z.string() }),
  prompt: '...'
})

// Agent 模式（設 maxSteps 即可）
const agentResult = await generateText({
  model,
  tools: { weather: tool({ description: '...', parameters: z.object({...}), execute: async (args) => {...} }) },
  maxSteps: 10,
  prompt: '...'
})
```

## 建置流程：全端 Agent 應用

使用 Next.js + shadcn 作為前端框架：

```bash
npx shadcn@latest init  # 選 Next.js
```

**API 端點（route.ts）**

```typescript
export async function POST(req: Request) {
  const { messages } = await req.json()
  const result = streamText({
    model,
    system: '...',
    messages,
    tools: { getLocation, getWeather },
  })
  return result.toDataStreamResponse()
}
```

**前端（page.tsx）**

```typescript
'use client'
import { useChat } from 'ai/react'

const { messages, input, setInput, append } = useChat({
  api: '/api/chat',
  maxSteps: 5,
})
```

## 串流 tool call 結果到前端

當 tool 本身也需要呼叫 LLM（如 sub-agent），需用 `createDataStreamResponse` 合併多個串流：

```typescript
return createDataStreamResponse({
  execute: async (dataStreamWriter) => {
    const prdStream = await generatePRD(prompt)
    for await (const chunk of prdStream) {
      if (chunk.type === 'text-delta') {
        dataStreamWriter.writeData({ type: 'prd-content', content: chunk.textDelta })
      }
    }
    result.mergeIntoDataStream(dataStreamWriter)
  }
})
```

前端透過 `useChat` 回傳的 `data` 屬性接收這些自訂資料。

## Playground 架構設計

分拆成三個元件，透過共享 state 連結：
- `ChatPanel`：使用者輸入與 agent 對話
- `ContentPanel`：顯示 agent 生成的產物（如 PRD）
- 共享 state：`[projectData, setProjectData]` 作為短期記憶，搭配資料庫做長期持久化

URL 結構：`/project/[projectId]`，讓每個 project 有獨立的對話與產物。
