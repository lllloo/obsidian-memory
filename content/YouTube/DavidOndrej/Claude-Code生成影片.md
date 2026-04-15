---
title: Claude Code 生成影片教學
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-23
source: https://www.youtube.com/watch?v=fOY0_WCR3eY
---

## 概覽

- Claude Code 現在可以製作影片——用純文字描述需求，就能從零生成專業動畫。
- 本影片本身就是用 Claude Code 製作的，沒有手動操作任何 UI。
- 核心技術：Remotion + Claude Code Agent Skills。

## 什麼是 Remotion

- Remotion 是一個用 Rust 開發的框架，透過程式碼以 React 組件的形式建立影片。
- 運作方式：資料來自 API、資料庫或用戶輸入 → 每一幀截圖 → 用 FFmpeg 合成 MP4。
- **為什麼 AI 喜歡它**：AI 代理擅長寫程式碼，但無法操作 After Effects 或 Premiere 等圖形介面。Remotion 把影片創作轉化為 React 組件，讓 AI 能直接生成。

## Agent Skills 是什麼

- Agent Skills 是教 AI 代理（如 Claude Code、OpenCode）如何使用特定工具的指令檔案。
- 採用**漸進式揭露**（Progressive Disclosure）原則：只在任務需要時載入對應技能，保持 context 精簡。
- Skills 是開放標準，目前支援 Claude Code、Agent Zero、OpenCode 等多個代理。
- Remotion 官方已發布自己的 Agent Skill，可直接整合使用。

## 安裝設定

1. 前往 remotion.dev，複製 `npx create` 指令，選擇空白模板。
2. 加入 Tailwind（可選），選擇加入 Agent Skills（重要）。
3. 使用 Vercel 提供的 skills.sh 頁面，複製安裝指令並執行。
4. 選擇安裝目標代理：Claude Code，選擇安裝範圍（專案或全域）。
5. 在 Claude Code 中執行 `/skill` 即可確認 Remotion 技能已安裝。

## 最佳實踐

- **先寫故事板**：在下提示前，先在文字中描述每個場景。
- **迭代式方法**：不要嘗試一次 one-shot，用 5–10 個提示逐步完善。
- **模組化組件**：把片頭、過場、片尾拆分為可重用的組件。
- **提供高品質素材**：遊戲精靈、產品照片等素材品質越高，成果越好。
- 在提示中明確說明「使用 Remotion skill」。
- 為每個動畫建立獨立子資料夾，保持專案整潔。

## 實作示範一：Pythagorean 定理動畫

- 靈感來源：3Blue1Brown 頻道的數學動畫風格。
- 詳細 400 行提示（用 AI 輔助撰寫），包含顏色、動畫節奏等細節。
- Claude Code 運行約 10 分鐘，生成多個 React 組件：
  - 自動繪線組件
  - 三角形組件
  - 正方形組件
  - 主協調器
- 結果：40 秒、2400 幀的完整動畫，整體流暢，少數順序問題可透過後續提示修正。

## 實作示範二：Claude Code 廣告動畫

- 簡短提示（約 200 行），輸入 Claude Code 的截圖作為素材。
- 2 分鐘內完成，17 秒影片。
- 示範游標移動、點擊、打字等互動動作。
- 後續一句提示「把背景漸層改成 Claude 橘色」，實時更新生效。

## 結語

- 在 2026 年，用 AI 既能建產品，又能行銷產品——現在是創業的最佳時機。
