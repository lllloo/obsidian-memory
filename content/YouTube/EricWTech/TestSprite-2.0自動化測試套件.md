---
title: 用 TestSprite 2.0 自動化整個測試套件
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-16
source: https://www.youtube.com/watch?v=nULxyZjDVN8
---

## 什麼是 TestSprite

TestSprite 是一個透過 MCP server 整合進 IDE 的 AI 自動化測試工具，可以分析程式碼、自動生成測試計畫、執行測試，不需手動撰寫測試腳本。

支援的 IDE：
- Visual Studio Code
- Cursor IDE
- Windsurf IDE
- 任何支援 MCP 的工具（如 GitHub Copilot）

## 安裝設定

1. 前往 TestSprite 網站建立帳號
2. 在 Dashboard → Settings 生成 API key
3. IDE 中選擇 "Test locally → Quick install → Add to Cursor"
4. 貼入 API key 完成連線
5. MCP tools 清單中出現 TestSprite 且狀態為綠色即代表連線成功

## 執行第一次測試

1. 確保 app 在本機運行（如 `pnpm dev`）
2. 在 IDE AI chat 中直接輸入「用 TestSprite 測試這個專案」
3. TestSprite 分析 codebase，生成測試計畫（涵蓋導航流程、用戶互動、表單輸入、驗證）
4. 瀏覽器開啟設定頁面確認參數：
   - 測試類型：前端測試
   - 測試模式：codebase（掃描整個專案）
   - 本機 URL：如 `http://localhost:3000`
   - 提供 product specs

## 測試執行與監控

測試開始後自動開啟 progress dashboard，可以：
- 即時看到每個 test case 狀態（執行中 / 通過 / 失敗）
- 點入單一測試查看完整執行錄影，逐步回放互動過程
- 查看測試步驟明細：導航、點擊、輸入、滾動、斷言
- 看錯誤訊息與執行時間
- 歷史執行紀錄永久保存，可隨時重新查閱

## 自訂測試的兩種方式

**方式一：自然語言（最簡單）**
- 直接在 AI chat 描述需求，如「新增空白表單提交的測試」
- TestSprite 更新測試計畫、生成程式碼、自動執行

**方式二：步驟直接編輯**
- 在 results view 開啟測試案例
- 逐步修改：互動方式、輸入值、timeout、目標元素
- 點擊 preview 中的元素自動更新 locator（不需手寫 selector）
- 可選擇只更新當前步驟，或重新生成後續整個流程

## 連接 GitHub 自動觸發

1. commit 生成的測試檔案（包含測試腳本、設定檔、測試計畫）到 repository
2. TestSprite Dashboard → Settings → 連結 GitHub 帳號
3. 授權 TestSprite GitHub App，選擇要監控的 repository
4. 之後每個 PR 自動執行：TestSprite 等待 preview 環境就緒 → 執行完整測試套件 → 結果發布在 PR 上
