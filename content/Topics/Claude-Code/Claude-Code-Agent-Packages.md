---
title: Claude Code Agent Packages
created: 2026-03-22
updated: 2026-04-08
tags:
  - claude-code
  - ai-tools
---

目前使用的網路 agent packages：

## awesome-claude-code-subagents

- **來源**：[VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- **說明**：社群精選的 Claude Code subagent 集合，涵蓋前後端開發、UI 設計、Docker、框架專家等角色，可直接安裝使用

## everything-claude-code

- **來源**：[affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)
- **說明**：完整的 Claude Code 工作流 agent 套件，涵蓋規劃/架構、程式碼審查、重構、安全/效能、TDD、E2E 測試、文件更新，以及 GAN Harness（Planner/Generator/Evaluator 三件組）等開發流程各階段的專用 agent

## 目前已安裝的 Agent

### awesome-claude-code-subagents

已安裝：

**Core Development**
- backend-developer — 後端 API、微服務與可擴展架構
- frontend-developer — 前端跨框架開發（React/Vue/Angular）
- fullstack-developer — 全端功能開發（DB + API + 前端）
- ui-designer — 視覺介面設計、Design System 與無障礙

**Language Specialists**
- javascript-pro — JavaScript ES2023+、非同步與效能優化
- laravel-specialist — Laravel 10+ Eloquent、Queue 與 API 效能
- typescript-pro — TypeScript 進階泛型與全端型別安全
- vue-expert — Vue 3 Composition API、Nuxt 3 與效能優化

**Infrastructure**
- docker-expert — Docker 容器映像建置、優化與安全

Core Development 未安裝：

- api-designer — REST/GraphQL API 設計、版本管理與文件
- electron-pro — Electron 跨平台桌面應用、自動更新與系統整合
- graphql-architect — GraphQL schema 設計、federation 與 subscription
- microservices-architect — 微服務拆分、服務間通訊與分散式交易
- mobile-developer — iOS/Android 跨平台開發（React Native/Flutter）
- websocket-engineer — WebSocket 即時雙向通訊、大規模連線管理

另有 Quality/Security、Data/AI、DevExp 等 10 大類，按需安裝。

### everything-claude-code

已安裝（共 23 個）：

**規劃與架構**
- planner — 複雜功能與重構的整體規劃
- architect — 系統架構、可擴展性與技術決策
- code-architect — 分析現有 codebase 慣例，產出功能架構藍圖（檔案、介面、資料流、建置順序）
- code-explorer — 深入分析現有功能：追蹤執行路徑、繪製架構層次與相依關係

**程式碼品質與審查**
- code-reviewer — 程式碼品質、安全與可維護性審查（寫/改後即用）
- code-simplifier — 簡化與精煉程式碼，保留行為
- typescript-reviewer — TypeScript/JavaScript 審查（型別安全、非同步正確性、慣用模式）
- silent-failure-hunter — 審查被吞掉的錯誤、錯誤 fallback、缺失的錯誤傳播
- type-design-analyzer — 型別設計的封裝性、不變量與約束強制
- security-reviewer — 安全漏洞檢測（SSRF/注入/OWASP Top 10）
- performance-optimizer — 效能瓶頸、記憶體洩漏、bundle 優化

**建置與重構**
- build-error-resolver — 建置/TypeScript 錯誤快速修復（最小 diff）
- refactor-cleaner — 死碼清理（knip/depcheck/ts-prune）

**測試**
- tdd-guide — 測試驅動開發（80%+ 覆蓋率）
- e2e-runner — E2E 測試（Vercel Agent Browser / Playwright fallback）

**文件與工作流**
- doc-updater — Codemap 與文件同步更新
- docs-lookup — 透過 Context7 MCP 即時查詢函式庫/API 文件
- loop-operator — 自動迴圈執行、監控與介入
- harness-optimizer — Agent harness 設定的可靠性、成本與吞吐量優化

**GAN Harness**（配合 `gan-style-harness` skill 使用）
- gan-planner — 將一句提示展開為完整產品規格（功能、Sprint、評估標準、設計方向）
- gan-generator — 實作功能、讀取 Evaluator 回饋，迭代至品質門檻
- gan-evaluator — 透過 Playwright 測試運行中的應用，評分並提供可行動回饋

**溝通**
- chief-of-staff — Email/Slack/LINE/Messenger 訊息分級與草稿回覆

未安裝：

- python-reviewer — Python 程式碼審查
- database-reviewer — 資料庫/Supabase 審查
- cpp-reviewer — C++ 程式碼審查
- cpp-build-resolver — C++ 建置錯誤修復
- go-reviewer — Go 程式碼審查
- go-build-resolver — Go 建置錯誤修復
- java-reviewer — Java/Spring Boot 程式碼審查
- java-build-resolver — Java/Maven/Gradle 建置錯誤修復
- kotlin-reviewer — Kotlin/Android/KMP 程式碼審查
- kotlin-build-resolver — Kotlin/Gradle 建置錯誤修復
- rust-reviewer — Rust 程式碼審查
- rust-build-resolver — Rust 建置錯誤修復
- pytorch-build-resolver — PyTorch/CUDA 訓練建置錯誤修復
- flutter-reviewer — Flutter/Dart 審查（widget、狀態管理、效能、無障礙）
- healthcare-reviewer — 醫療應用審查（臨床安全、PHI 合規、EMR/EHR）

### 自訂

- obsidian — 自建的 vault 操作助手