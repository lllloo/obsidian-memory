---
title: Claude Code 非程式碼應用場景
created: 2026-05-09
updated: 2026-05-09
source: https://www.youtube.com/watch?v=KQDVDtklf34
published: 2026-05-05
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
---

## 第二大腦（Obsidian）

以 Obsidian 作為第二大腦，透過 CLAUDE.md 引導 Claude 操作 Markdown 架構的知識庫。Claude 可搜尋筆記、回答問題、即時更新內容，無需手動翻檔案。圖形視覺化（graph view）有助分析依賴關係，所有資料維持本地儲存。

## 影片製作（Remotion）

用 `npx` 安裝 Remotion skill 後，在 Claude Code 內以 prompt 描述影片的切換時機、動畫細節即可生成產品展示影片。輸出為完全由程式碼驅動的 SVG 動畫序列。注意：50 秒影片可能需要超過 20 分鐘迭代。提供額外素材（圖片、字體）可大幅提升品質。

## 多步驟研究流水線

透過 CLAUDE.md 定義結構化研究工作流，將「搜尋 → 驗證 → 草稿 → 最終文件」拆成獨立 `.md` 步驟檔案，每檔包含輸入、期望輸出、流程與驗收條件。Claude 逐步執行後，自動輸出含引用來源的 PDF/MD 報告，每個論點都有對應參考文獻，避免 LLM 幻覺。

## 影片觀看（Claude Video skill）

透過 `claude video` skill，Claude 可解析本地或遠端影片：
- 萃取影格序列
- 取得 transcript 並對應至影格
- 直接分析視覺內容，不再依賴純文字假設

transcript 後端可選 Whisper 或 Groq（免費額度佳、速度快）。

## Canvas 設計（官方 skill）

安裝 Anthropic 官方 canvas design skill 後，Claude Code 可設計海報、社群貼文、資訊圖表。流程：
1. 生成設計哲學文件（style guide）
2. 用 Python 腳本渲染 SVG
3. 依 prompt 迭代修正字體大小、版面平衡等細節

特別適合文字與 SVG 為主的簡潔動態設計。

## 內容管理系統

整合 Notion MCP 後，Claude Code 可判斷哪些資訊應公開到 Notion，哪些維持本地。配合 NotebookLM CLI，讓 Claude 直接查詢已整合的知識來源，省去跨多檔案彙整的 token 消耗。NotebookLM 額外支援生成影片、投影片、心智圖與 podcast。

## 多角色應用

同一套 Agent 架構可切換至不同專業角色：

| 角色         | 應用方式                                                         |
| ------------ | ---------------------------------------------------------------- |
| 財務顧問     | 讀取 CSV 或 Notion 資料，產出財務方向分析報告                    |
| 教師         | 記錄學習進度與偏好，多角度解釋概念，生成測驗                    |
| 法律顧問     | 對照專案資料夾的條款文件，標記高中低優先度合規問題               |
| 資料分析師   | 彙整多個資料集，生成決策報告                                     |

關鍵：每個角色對應一個含規則與偏好的專案資料夾，讓 Claude 在明確的脈絡下作業。
