---
title: TanStack Start 100 秒速覽
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-20
source: https://www.youtube.com/watch?v=1fUBWAETmkk
---

## 是什麼

- 由 Tanner Linsley 開發的全端 React 框架
- 定位：type-safe、server-first、高效能，去除 Next.js 的過度抽象

## 開始使用

```bash
# 建立新專案
npx create-tanstack-start
```

- 預設包含：Vitest（測試）、Tailwind（樣式）、TanStack Router（路由）、TypeScript 端對端型別安全

## 核心功能

### Server Functions
- 只在伺服器執行的邏輯（資料庫連線、檔案系統、環境變數）
- 跨網路維持型別安全

### 檔案系統路由（基於 TanStack Router）
- 在 `routes/` 目錄新增檔案即新增路由
- 路由可定義 **loader** 預先載入資料，確保渲染前資料已就緒

### API Routes
- 使用 `createFileRoute` API 加上 `server` 屬性建立原始 HTTP 請求處理器

## 背景

- Next.js 在 React 自身認同危機後出現安全漏洞、破壞性變更、整體氛圍變差
- TanStack Start 是對這些問題的直接回應，提供更清晰的 server-first 架構
