---
title: Claude Designer 打造精美 UI 工作流
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-03-19
source: https://www.youtube.com/watch?v=PLbwB5_HIdc
---

## 核心工作流：兩步驟產出高品質 UI

Claude 3.7 在 UI 實作上能力大幅提升，可以生成高品質自訂 UI（不依賴 shadcn 等元件庫）。核心工作流分兩步驟：

### 步驟一：用 Claude 設計靜態 UI

在 Cursor 中使用這個 prompt 框架：

```
You are a senior front-end developer. [詳細設計風格描述]

Technical specifications:
- Each page: [尺寸]
- Icons: use online vector icon library
- Images: sourced from open-source websites
- Style: [描述]

App: [你的 app 描述]

Role-play as a product manager. Design functional and information architecture.
Follow the design style and technical specifications to generate a complete UI design plan,
and create ui.html with all pages displayed in horizontal layout.
Generate the first 2 pages first.
```

**關鍵技巧：**
- 可附上截圖作為設計參考，讓 Claude 模仿樣式
- 單頁修正：截圖出問題的部分，明確描述問題（例：「1250 calories left 文字沒有垂直置中」）
- 先生成 2 頁確認品質，再繼續「keep the same quality and continue creating more pages」
- 加互動動畫：「don't change UI, just add hover interaction animations」

### 步驟二：將靜態 UI 轉換為 Next.js 應用

不要直接叫 Cursor 建立整個 app，先規劃：

1. 詢問「要建哪些 UI 元件？只列清單，先不要產生檔案」
2. 將元件清單存入 `plan.md`
3. 用 shadcn 初始化 Next.js 專案：
   ```bash
   npx shadcn@latest init  # 選 Next.js + Tailwind
   ```
4. 告訴 Cursor：「已把計畫存到 plan.md，請依序建立元件，每完成一個在 plan.md 打勾」

**逐元件實作的好處：**每個元件的 context 更聚焦，複製靜態 UI 的成功率大幅提升。

## 為什麼這個方法比 v0 更強

- 不受限於 shadcn 元件庫，可以建立任意風格的自訂元件
- Claude 3.7 的 HTML/CSS 生成品質已可比擬 v0
- 靜態 HTML → 元件規劃 → Next.js 的分解過程，讓 AI 每步更成功
- 最終產出是可直接開發的 Next.js 程式碼，不需從 v0 匯出再整合
