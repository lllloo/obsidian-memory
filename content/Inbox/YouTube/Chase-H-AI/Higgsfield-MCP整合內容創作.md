---
title: Higgsfield MCP Server 把 Claude Code 變成內容機器
created: 2026-05-04
updated: 2026-05-04
source: https://www.youtube.com/watch?v=20BDYk-CU_o
published: 2026-04-29
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
---

## 為什麼 Higgsfield MCP Server 重要

兩個原因：

1. **單一通道**接到所有 AI 內容創作工具
   - 過去要手動把 Nano Banana、GPT Image 2、VO3、Cling、Seed Dance 等個別接 Claude，麻煩到沒人做
   - 結果：被綁在自己用慣的一兩個工具上，但**最佳工具每週都在換**
   - Higgsfield MCP 一次提供 17 個 image models、14 個 video models 與其自家專屬模型
2. **可被 Claude Code 自動化**
   - 因為是 MCP server，能把整套內容創作流程腳本化／串進 cron
   - 例：Claude Code 每天掃 GitHub trending → 進 Claude Code 分析 → 產 carousel prompt → 送到 Higgsfield → 自動拿回成品

## 安裝（兩種方式）

### 方式 A：在 claude.ai 設 Connector

1. 進 `claude.ai` → Settings → Connectors → Add Custom Connector
2. 從 Higgsfield MCP page 複製連線資訊貼上 → Add → Connect → 登入授權
3. 即可在 chat 中直接呼叫各模型，圖片會 inline 顯示

範例：「Use the Higgsfield connector and create an image about Claude Code + Higgsfield with GPT Image 2」

inline 圖片支援的選項：

- Recreate（重送 prompt）
- Animate（送進 video editor）
- Edit（彈出新 prompt window，可換到 Nano Banana 2 / GPT Image 2，自動帶 reference image）

### 方式 B：在 Claude Code 內裝

- 自然語言：「set up this MCP server for me」+ 從 Higgsfield MCP 頁面貼 custom connector 資訊
- 重啟 Claude Code → `/mcp` 應看到 Higgsfield 已連線
- 缺點：terminal 看不到圖；好處：能腳本化、自動化

## 自動化範例：GitHub trending → carousel

實作流程：

1. **每日 GitHub 自動腳本**：抓近 7 天新增、依 stars 排序的 top 10 AI repo（含描述），存進 Obsidian
2. **生成 carousel**：
   - 給 Claude Code 一個 cover slide 與幾張 body slide 作 reference image
   - 同時餵 GitHub 摘要
   - 讓 Claude Code 寫 prompt 並呼叫 Higgsfield → GPT Image 2 出 4 個變體（high quality 2K）
3. **MCP 是 fire-and-forget**：要請 Claude Code 每 60-90 秒輪詢一次 Higgsfield 看是否完成
4. **Body slide**：請 Claude Code 自動到 GitHub repo 抓必要素材，加入 MCP request

實測 cover 4 變體約 5 分鐘出齊，風格與 reference image 高度一致。

## 自動化的最終目標

把上述流程整支收進**單一 skill**（例如 `Higgsfield Carousel Skill`）：

- 每日跑 GitHub scan
- 自動產 carousel post
- 輸出 4 變體供人篩選

得到「每天自動更新的 GitHub trending carousel」——是經得起時間的 evergreen 內容類型。

## 混合策略

不一定要全 AI 出圖：

- Cover slide：用 Higgsfield 出 AI 圖，因為視覺風格最重要
- Body slide：改用 HTML / code 渲染，省 token、降成本
- 重點是「現在我們有選擇」

## 結論

- 最大的兩個 unlock：單一通道 + 自動化潛力
- 把 Claude Code 變成行銷機器的關鍵基礎設施
- 推薦透過 Claude Code 而不只是 chat app 接 connector，才能享受腳本化的最大價值
