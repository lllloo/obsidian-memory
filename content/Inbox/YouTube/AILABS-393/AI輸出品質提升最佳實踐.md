---
title: AI 輸出品質提升最佳實踐
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-03
source: https://www.youtube.com/watch?v=cop_G65D7PA
parent: "[[01.index]]"
---

## manifest.md 作為資料夾導航基礎

每個工作資料夾建立 `manifest.md`（等同 Claude Code 的 `CLAUDE.md`），三層結構：

- Tier 1：永遠載入的核心文件（source of truth）
- Tier 2：按需載入的文件
- Tier 3：Archive 資料（設為 ignore，除非明確要求）

效果：Claude 優先讀取 manifest，快速找到正確文件，避免 context bloat 與錯誤引用。

## 個人化 context 文件

在 Documents/Claude context 資料夾建立三個文件：

- `about_me.md`：個人背景
- `brand_voice.md`：溝通風格
- `working_style.md`：工作習慣與偏好

在 global instructions 引用，讓所有 session 自動套用。需要持續迭代更新。

## Global Instructions 設定重點

Global instructions 在 prompt 載入前就先生效，建議加入：

- 指定 manifest.md 是第一個要讀取的文件
- 要求 Claude 在行動前先提問釐清
- 要求先呈現計畫再執行
- 禁止填充詞，不 pad 輸出
- 低信心時詢問而非猜測

## 定義結束狀態而非過程

不要描述「怎麼做」，而是描述「做完後應該長什麼樣」，提供：

- 範例輸出或測試案例
- 每個資料夾的最終狀態描述
- 明確指定不應碰觸的部分
- Edge case 的處理方式

## 任務批次化策略

- 相互依賴的任務（前者輸出是後者輸入）合為單一 session
- 獨立任務利用 parallel agents 同時執行
- Sub agents 適合大量任務，但消耗 token 多，謹慎使用
- 不相關的任務不要強行批次，會浪費 token 且影響品質

## 排程自動化

Co-work 的 schedule skill 可自動化每日重複任務（需電腦開機且 Claw Desktop 執行中）。例如：定期分析會議記錄 → 生成摘要報告 → 放置指定資料夾。可再透過 connector 連接 Gmail、Google Drive 進一步整合。

## Plugin 擴充能力

每個 plugin 包含一組 skills、指令、sub agent 整合，針對特定領域客製化。內建 plugin 製作 plugin 的功能，可直接在 chat 介面請 Claude 建立新 plugin，透過問答確認需求後自動生成。

## Co-work 安全邊界

- 敏感資料放獨立資料夾，只暴露必要內容
- 加入「不要刪除任何東西」等明確限制指令
- 注意 prompt injection 風險（文件或網站可能含有惡意指令）
- Co-work 資源消耗比一般 chat 高，避免過度使用
