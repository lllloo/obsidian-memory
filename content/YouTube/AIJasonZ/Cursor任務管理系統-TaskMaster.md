---
title: Cursor 任務管理系統：TaskMaster
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-04-08
source: https://www.youtube.com/watch?v=1L509JK8p1I
---

## 核心概念：任務管理系統

給 AI coding agent 一個任務管理系統，讓它：
1. 理解整體實作計畫
2. 控制每個步驟的上下文量
3. 避免實作某功能時破壞其他部分

## 三種實作方式

### 方式一：手動 task.md（最簡單）

在 cursor rules 中加入規則，要求 Cursor 維護 `task.md`：
- 新任務前先列出所有子任務
- 完成每個 task 後標記為 done

### 方式二：Roo Code + Boomerang Tasks

Roo Code 是免費的 open-source Cursor（VS Code 擴充），可建立自訂 agent mode：

- **Architect mode**：拆解 PRD，分析依賴，產出完整任務清單
- **Code mode**：依序執行任務，支援自動執行 + 瀏覽器測試
- 每個子任務在獨立 context 執行，避免干擾

### 方式三：Claude TaskMaster AI（最強）

```bash
npm install -g taskmaster-ai
taskmaster init         # 初始化專案
taskmaster parse-prd scripts/prd.txt   # 從 PRD 產生任務清單
taskmaster list         # 查看所有任務（含依賴關係）
taskmaster analyze-complexity          # 分析每個任務的複雜度
taskmaster complexity-report          # 查看複雜度報告
taskmaster expand --id=<id>           # 展開高複雜度任務成子任務
taskmaster update --id=<id> --prompt="..."  # 更新任務計畫
taskmaster next                       # 取得下一個待執行任務
```

**需要設定 `.env`：**
- `ANTHROPIC_API_KEY`：用 Claude 拆解任務
- `PERPLEXITY_API_KEY`：研究最新套件文件

**TaskMaster 的關鍵優點：**
- 依賴順序排列任務，不會出現「先實作依賴未就緒的功能」
- `analyze-complexity` 用 Claude + Perplexity 評估每個任務的難度分數
- 高複雜度任務可進一步 `expand` 拆解
- 任務更新時會重新計算整個計畫

## 最佳實作工作流

1. 撰寫或產生 `prd.txt`（可用工具如 10xcoder.dev）
2. `taskmaster parse-prd scripts/prd.txt` 產生任務
3. `taskmaster analyze-complexity` 分析複雜度
4. 對高分任務執行 `taskmaster expand` 拆解
5. 讓 Cursor 在 Yolo mode 執行：`check next task using taskmaster`
6. Cursor 完成一個任務後自動呼叫 `taskmaster next` 繼續

**搭配 Gemini 2.5 Pro Max 可跳過 25 次對話限制。**

實測結果：20 分鐘內從 PRD 生成出多人連線繪圖遊戲（含 lobby、認證、畫布、GPT-4 評分機制），幾乎一次到位。
