---
title: Claude Code Agent Packages
created: 2026-03-22
updated: 2026-03-29
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
- **說明**：完整的 Claude Code 工作流 agent 套件，包含架構規劃、程式碼審查、重構、安全審查、TDD、E2E 測試、文件更新等開發流程各階段的專用 agent

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

已安裝：

- architect — 系統架構、可擴展性與技術決策
- build-error-resolver — 建置/TypeScript 錯誤快速修復
- code-reviewer — 程式碼品質、安全與可維護性審查
- doc-updater — Codemap 與文件同步更新
- e2e-runner — E2E 測試（Vercel Agent Browser / Playwright）
- loop-operator — 自動迴圈執行、監控與介入
- planner — 複雜功能與重構的規劃
- refactor-cleaner — 死碼清理（knip/depcheck/ts-prune）
- security-reviewer — 安全漏洞檢測（SSRF/注入/OWASP Top 10）
- tdd-guide — 測試驅動開發（80%+ 覆蓋率）

未安裝：

- docs-lookup — 透過 Context7 MCP 即時查詢函式庫/API 文件
- chief-of-staff — Email/Slack/LINE/Messenger 訊息分級與草稿回覆
- harness-optimizer — Agent harness 設定的可靠性、成本與吞吐量優化
- python-reviewer — Python 程式碼審查
- database-reviewer — 資料庫/Supabase 審查
- typescript-reviewer — TypeScript/JavaScript 程式碼審查
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
- performance-optimizer — 效能瓶頸分析、記憶體洩漏偵測與 bundle 優化

### 自訂

- obsidian — 自建的 vault 操作助手