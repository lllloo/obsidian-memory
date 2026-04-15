---
title: OpenCode 八大瘋狂應用案例
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-22
source: https://www.youtube.com/watch?v=6KB73J01fGw
---

## 概覽

- OpenCode 是開源 AI Agent，在終端機中運行，可在電腦上執行任何任務，支援所有 AI 模型。
- 本文展示 8 個實際應用案例，每週可節省大量時間。

## 安裝與設定

1. 前往 opencode.ai，複製安裝指令，在終端機執行（已安裝則自動更新）。
2. 輸入 `opencode login`，選擇模型提供商（推薦：OpenAI——可直接使用 ChatGPT 訂閱）。
3. 完成授權後，在任何終端機（全域或 IDE 如 Cursor 內）輸入 `opencode` 啟動。
4. 安裝 **Chrome DevTools MCP Server**（讓 OpenCode 能操控瀏覽器）：
   - 讓 OpenCode 編輯 `~/.opencode/opencode.json`，加入 MCP Server 的 JSON schema。
   - 重新開啟終端機後，應看到「Chrome Dev Tools connected」。

## 案例一：自動尋找高品質潛在客戶

- **Prompt**：「Find high-quality leads for my business of implementing AI automation for local businesses. I live in Warsaw. Find businesses that would be ideal and save them into a clear markdown file.」
- 執行過程：OpenCode 使用 MCP 工具控制瀏覽器、搜尋地區企業、整理資料。
- **結果**：約 90 秒找到 33 家符合條件的企業（含名稱、地址、網站）並儲存為 Markdown 檔案。

## 案例二：整理電腦檔案與資料夾

- **Prompt**：「Find the downloads folder. Analyze it to find the 20 oldest files and 20 largest files. Present them to me. Do not delete anything yet.」
- 確認後執行刪除指令。
- **結果**：下載資料夾從 20 GB 縮減至 4.3 GB，節省 15 GB 空間，全程約 30 秒。

## 案例三：資料分析與視覺化

- **任務**：分析 250+ 個 AI 新創點子的 Markdown 檔案，歸類為不同類別，生成 Obsidian 風格的群組圖表並輸出為 PNG。
- OpenCode 自行寫 400 行 Python 腳本，安裝 matplotlib，建立虛擬環境，生成圖表。
- **結果**：2 分鐘內完成，將 234 個點子分為 21 個類別（AI 基礎設施、生產力工具、HR 招聘等）。

## 案例四：自訂深度研究

- **Prompt**：「Execute deep research on the topic 'how to reduce no-show rates for sales calls'. Use YouTube as the primary source.」
- 執行過程：控制瀏覽器搜尋相關影片、下載逐字稿（使用 YouTube Transcript API）、分析並生成報告。
- **結果**：5 分鐘 15 秒生成近 300 行深度研究報告，涵蓋 13 部影片（75,000+ 觀看次數）的摘要。
- 優勢：比 ChatGPT / Perplexity 更可自訂（指定來源、格式），且可存取本地 Python 函式庫。

## 案例五：診斷電腦效能問題

- **Prompt**：「Find out why my computer has been running slower recently. Check load averages, memory pressure, disk space, swap activity. Give me a report. Do not make any changes yet.」
- **結果**：20 秒生成報告，列出電腦變慢的前五個原因（系統未重啟 11 天、Brave 瀏覽器占用資源、Docker Agent Zero、OBS 錄影等）。
- 確認後可逐項修復。

## 案例六：撰寫 AEO 文章並建立網站

- **任務**：搜尋現有 AI 代碼審查工具，研究 AI Agent 流量最佳化方法，構思 5 篇文章，選最佳主題撰寫，並建立完整 HTML 網站。
- AEO（Answer Engine Optimization）：針對 AI Agent 流量優化的搜尋策略（取代傳統 SEO）。
- **結果**：約 10 分鐘完成——從研究、撰文到建立互動式響應式網站，端到端自動完成（1,000 行 HTML）。

## 案例七：自動產生程式碼文件

- **Prompt**：「Analyze this codebase and identify all areas where documentation is missing, outdated, or incomplete. Create or update readme.md and any relevant doc files. Do not change any code.」
- OpenCode 執行過程：讀取所有原始碼 → 發現問題 → 建立 `/docs` 資料夾 → 撰寫 API 參考、架構說明、元件說明、部署指南等。
- **結果**：8 分鐘內完成，生成數千行文件（每個檔案 280-330 行），並建立 `index.md` 作為文件中心，標示最後更新時間。

## 案例八：建立互動式投資人 Pitch Deck

- **任務**：根據新創點子（一鍵錄製並發布到社群媒體的 App），建立完整的互動式投資人 Pitch Deck。
- Prompt 包含：角色設定、目標、新創點子描述、Pitch Deck 投影片結構要求。
- OpenCode 使用 **Vite** 建立完整前端專案（非單一 HTML 檔案）。
- 執行 TypeScript 型別檢查（`npm run build`）→ 發現錯誤 → 自動修復。
- **結果**：互動式 Pitch Deck 網站，含動畫、問題說明、解決方案、定價、競爭分析、團隊介紹、募資金額（seed $1.5M）等完整投影片。
- 成本：約 $0.8 美元。

## 進階技巧

- **自動 Git 提交**：「Pull latest from GitHub, do a commit and push it.」——OpenCode 自動整理 commit 訊息並推送。
- **個人化 Pitch Deck**：對每位投資人客製化 Pitch Deck——加入該投資人的背景資料，讓 OpenCode 生成專屬版本。
- **遭遇錯誤時**：OpenCode 不會在第一個錯誤時放棄，會持續嘗試不同方法直到完成任務。

## 注意事項

- OpenCode 在本機直接執行，擁有完整系統存取權，請謹慎使用。
- 若需更強的隔離性與安全性，考慮使用 **Agent Zero**（在 Docker 容器中運行）。
- 遇到終端機不熟悉？OpenCode 也有圖形化介面 App，但建議硬撐過前 30-60 分鐘的學習曲線。
