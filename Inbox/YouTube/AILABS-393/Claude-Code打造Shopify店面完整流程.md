---
title: Claude Code 打造 Shopify 店面完整流程
created: 2026-05-20
updated: 2026-05-20
source: https://www.youtube.com/watch?v=x2pRavsHdls
published: 2026-05-15
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - shopify
  - mcp
  - ai-coding
---

> [!info] 影片定位
> 用 Claude Code 從零搭一個 Shopify 店面的 end-to-end 流程：Shopify Partner / CLI / AI Toolkit MCP / plugin → CLAUDE.md / 自製 skill / hooks → 用 prototype skill 設計 → Gemini CLI 並行生成圖片 → 同步上線 → 接 admin API → 加商品 → 設付款。重點不是把 agent 接上 Shopify 就好，而是「組合」哪幾塊配件能避開「每家店長一樣」的 generic 模板。

## 前置：Shopify Partner 帳號

- 註冊 Shopify Partner，取得 development store 沙箱。
- 沙箱提供 fake payments、test users，方便上線前驗證。
- 之後切到 merchant 帳號、加上付款設定，development app 可以直接搬過去開賣。

## 安裝 Shopify CLI

- 從 CLI docs 複製 install 指令到 terminal 跑。
- 選 React app（非 extension app），語言選 TypeScript（type safety）。
- 依賴安裝完成後就有 basic template，跑起來看得到雛形。

## 安裝 AI Toolkit：MCP + plugin

- **Shopify MCP**：docs 提供 Claude Code 對應的 install 指令；MCP 暴露的工具裡含 Shopify API 文件與驗證能力。
- **單獨 MCP 不夠**：MCP 沒有推送變更到雲端 store 的能力，只能提供知識與驗證；要靠 CLI 當「local 與 Shopify app 之間的橋」。
- **Plugin**：把多個 agents 與 skills 打包進來，install 完跑 reload plugins 即可使用。

## 專案準備：CLAUDE.md + 自製 skills + hooks

### CLAUDE.md
- 寫好 best practice 指引給 agent，沿用 AILABS 既有的 Claude.md 範本。

### Gemini image generation skill（自製）
- 解決 Claude 預設用 SVG placeholder 當網站視覺、無法當實品圖的問題。
- Skill 內容是「如何呼叫 Gemini CLI 生成圖片、生完存哪」。
- 因為 Gemini CLI 自帶 image generation，**不需要額外 API key**，靠 Gemini CLI 自身的 auth 即可。

### Prototype skill（自製）
- 工作流分兩階段：
  1. 改設計時先寫一份 HTML 預覽檔，等使用者過目
  2. 過目通過後再把該設計套進 app 本體
- 為何重要：直接套到 app 既慢又花 token，HTML 預覽快、便宜，可以多輪迭代設計。

### Hooks 當護欄
- 放在 `.claude/settings.json`。
- 例：`PreToolUse` 攔截 Claude 在未經核可前直接推 store 的動作。
- 數量自訂，視團隊風險容忍而定。

## 建站流程

### 1. 生成 landing page
- Prompt 描述要做的 landing page 風格。
- Prototype skill 接管：先寫 HTML，預覽完成才動 app。
- 第一版視覺乾淨但留 placeholder 圖；要明確指示 agent「載入 image generation skill 並補圖」。

### 2. Gemini CLI 並行生圖
- Claude 用 bash tool 啟動多個 Gemini CLI（yolo mode 跳過 permission prompt），多 terminal 同時生圖。
- 生圖較慢，但用 Claude 控 prompt 能讓圖風格與 UI 一致。

### 3. HTML 設計轉 development app
- 確認沒有要改後請 Claude proceed，會問是否要同步 live store 等選項。
- Agent 把 HTML 轉到 development app（不是直接主 app），1:1 還原設計。

### 4. 同步到 live store
- 此時設計還只在 local + theme preview（draft）。
- 一句「sync to live」→ Claude 用 Shopify CLI + MCP 把 design 推到 store URL。
- 其他頁面同理：prototype → development app → sync。

## 進階：產品與付款

### Shopify Admin API
- 加產品、改 about page 等管理操作需要 admin API。
- 用 Shopify CLI 跑 auth 指令、瀏覽器完成登入。
- 之後 Claude 可同時用 Shopify MCP 與 CLI 更新其他頁面。

### 權限分階段提權
- 一開始只授 content 權限即可改設計。
- 加產品要更高權限：write products、read/write publications。
- 重跑 auth 指令、加上新的 scope，Claude 才能執行 add products。
- 加完後 product details、cart features 都會自動長出來。

### 付款 + 解鎖瀏覽
- 沒設定付款 plan 之前，訪客連看店都要輸密碼。
- 設好付款方案才算真正能銷售。

## 核心啟示

- 「Claude Code + Shopify MCP」本身只是知識層；真正能動的鏈條是 **MCP（知識）+ CLI（執行）+ plugin（agent/skill 套件）+ 自製 skill（補生圖與 prototype 缺口）+ hooks（護欄）**。
- Prototype skill（HTML 預覽再套用）是避免 token / 時間爆掉的關鍵 pattern：先在便宜層收斂設計，再進入昂貴層套用。
- 影片提到完整 setup 與 skills 收錄在 AI Labs Pro。
