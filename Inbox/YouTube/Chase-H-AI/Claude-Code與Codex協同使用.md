---
title: Claude Code 與 Codex 協同使用
created: 2026-05-09
updated: 2026-05-09
source: https://www.youtube.com/watch?v=VdxUKiF8CWI
published: 2026-05-07
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - codex
  - tool-agnostic
---

## 核心觀點：不是二選一，是兩者並用

Claude Code 與 Codex 不是競爭關係，而是互補關係。Venn 圖幾乎是完整的圓形（99% 重疊），學會其中一個就能快速上手另一個。

- Claude Code 在 AI 討論圈主導地位已久，但 Codex 悄悄縮小了差距
- GPT 5.5（含 5.5 Pro）在部分 benchmark 已勝過 Opus 4.7
- OpenAI Pro 方案（$100/月）的用量上限比 Anthropic Max 方案更寬鬆
- 最佳策略：兩者同時使用，互相查漏補缺

## 在 Codex Desktop App 裡跑 Claude Code

只需在 Codex 右上角點「Toggle Terminal」開啟終端機，直接在裡面執行 `claude`。兩者共享同一個專案目錄，可以即時互動。

## Codex Desktop App 概覽

**基本操作**

- 提示視窗支援上傳圖片與檔案
- Plan Mode 是一個切換開關，行為與 Claude Code 的 plan mode 相同
- 權限設定（Permissions）：建議開啟 full access，與 Claude Code 的 bypass/auto 相似
- Intelligence（模型推理強度）與 Model 可獨立選擇
- 工作目錄稱為「Projects」，可選擇本地或雲端

**設定頁重點**

- Work Mode：選 Coding，取得更多技術細節
- Follow-up behavior：Q（queue）vs Steer，建議預設 Q
- Pets：畫面角落的視覺提示小工具，可在 Codex 運作時讓你在其他視窗仍能看到進度
- 全域 Sandbox 設定在 Configuration → Approval Policy
- Workspace Dependencies 預設應開啟
- Memory：預設開啟，可選擇關閉（作者偏好關閉）
- MCP servers、Git environments、Work trees、Browser use、Computer use 等進階功能亦在設定內

**Plugins 與 Skills**

- Plugins 類似預先打包好的 MCP 套件（如 Supabase、Chrome、試算表），一鍵安裝
- Skills 機制與 Claude Code 幾乎一致
- 首次安裝 Codex 時會詢問是否從 Claude Code 或 Open Code 匯入現有 skill，一鍵完成

**Context Window 差異**

- GPT 5.5 Pro：258K context
- Claude Code：1M context
- 258K 迫使使用者更頻繁開新 chat（等同 `/clear`），某種程度反而防止 context 過度累積
- 達到 258K 上限時會自動 compaction

## 雙模型協作工作流

核心流程：讓兩個 AI 互相審查

1. 在 Codex 以 Plan Mode 規劃需求
2. 複製計畫，貼入 Claude Code 詢問盲點或漏洞
3. 將 Claude Code 的反饋再貼回 Codex，讓它更新計畫
4. 執行後，讓 Claude Code 審查 Codex 寫的程式碼（兩者在同一目錄下，Claude Code 可直接讀取）

**Demo 中的實際效果**

Codex 完成第一版後，Claude Code 在同一份程式碼中找出了 20 個潛在 bug，涵蓋 timestamp 問題、competitor self-referencing、功能未正確串接等。前期多花的 token 換取早期發現問題，長遠看來實際節省 token。

**互動方式**

- Codex 支援 `/skill名稱` 呼叫 skill（如 `/front-end-design`）
- `@plugin名稱` 呼叫 plugin（如 `@spreadsheets`）
- 也可以直接用自然語言，行為與 Claude Code 相同
- UI 可直接對 inapp 瀏覽器頁面做標注（highlight → 留 comment → 送出），方便前端審查

## Claude Code 內的 Codex Plugin

Codex 在 Claude Code 內有官方 plugin，其中包含「adversarial review」skill，可讓 Claude Code 以對抗性角度審查 Codex 產生的程式碼。

## 為何要做到 Tool Agnostic

大多數人自以為工具中立，實際上習慣固化後會對特定工具產生近乎球迷的情感依附。

- 模型之間的差距正在收斂，市面上所有主流模型對 99% 的一般任務都已足夠
- 未來五年後更強大的模型出現時，兩者並用的習慣反而是優勢
- Codex 主動支援匯入 Claude Code 的 skill 檔案，工具生態系並沒有刻意築牆
