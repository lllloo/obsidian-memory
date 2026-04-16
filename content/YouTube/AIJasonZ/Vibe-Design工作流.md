---
title: Vibe Design 工作流：Figma MCP + Shadcn MCP
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-09-06
source: https://www.youtube.com/watch?v=4j51FMU-SUQ
parent: "[[01.index]]"
---

## 核心工具組合

- **Framelink Figma MCP**：讀取 Figma 設計稿，下載圖片與 SVG 資源，幾乎像素完美實作
- **Shadcn MCP**：連接各種 Shadcn-based UI component library，自動搜尋、下載、引入元件

## Figma MCP 流程

1. Figma 中複製 frame 的 link to selection
2. 貼入 cursor/Claude Code，提示「implement this UI 100% pixel perfect」
3. Figma MCP 自動下載圖片與 SVG 資產
4. 通常兩個提示內可達到接近 100% 像素完美

### 安裝 Figma MCP

- 需要 Figma Personal Access Token（Settings → Security → Generate Token）
- Token 需要 files read 權限

## Shadcn MCP 流程

### 設定

```bash
npx shadcn@latest mcp init --client cursor  # 或 claude-code / vscode
```

- 需 per-project 安裝（因為要讀取各專案的 `components.json`）
- 設定完後會新增 `agents.md` 說明 agent 使用方式

### 加入 UI Library Registry

在 `components.json` 的 `registries` 中加入第三方 library：
```json
{
  "registries": [
    "https://ui.library.com/r"
  ]
}
```

### 可用的第三方 Shadcn Registry 範例

- **Fancy Components**：各種動畫效果元件
- **Animate UI**：動畫元件
- **Chat UI**：modal、selector、聊天介面元件
- **Magic UI**：豐富動畫效果
- **Plate UI**：專業文字編輯器元件（rich text editor）

## 結合兩個 MCP 的最佳效果

當 Figma 設計稿使用 Shadcn-based 元件（且 layer 名稱對應 component 名稱）時：
- Figma MCP 識別設計稿中的元件
- Shadcn MCP 從 registry 搜尋並安裝對應元件
- 一次提示即可達到 100% 像素完美

## 自建 Registry

可以建立自己的 UI component library，host 並加入 registry，在不同專案中複用。
