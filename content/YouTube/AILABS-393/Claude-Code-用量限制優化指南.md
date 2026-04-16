---
title: Claude Code 用量限制問題的完整優化指南
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-07
source: https://www.youtube.com/watch?v=YsdQE6juGXY
parent: "[[01.index]]"
---

## Claude 計畫與限制機制說明

- 所有付費方案均採 **5 小時滾動視窗**，視窗從第一則訊息開始計算
- 視窗期間無論是否閒置都持續倒數，多裝置共用同一計數
- 訊息配額依方案不同：Pro ≈ 45、Max ≈ 225、Max 20x ≈ 900
- 使用 Opus 比 Sonnet 消耗約 3 倍 token，因此實際訊息數會更少
- 高峰時段 Anthropic 會額外加速限制到期

## Session 層級優化技巧

**清空 context：**
- `/clear`：完成一個任務後直接重置，下個任務從乾淨 context 開始
- `/compact`：保留必要資訊並壓縮 context（適合想延續部分脈絡時）

**避免主視窗膨脹：**
- 用 `/btw`（by the way）問旁支問題，回應不會帶入主 context

**恢復錯誤輸出：**
- `/rewind`：回到 Claude 沒按照指示做的那一條訊息之前，修改 prompt 重試
- 或按兩下 Escape 鍵達到同樣效果
- 好處：錯誤輸出不會進入 context，減少 token 浪費

**規劃不要跳過：**
- 前期花 token 規劃，遠比後期花更多 token 修正來得划算

## 專案結構層級優化

**CLAUDE.md 精簡原則：**
- 建議控制在 **300 行以內**，越短越好
- 不要放 Claude 本來就知道的事（如 dev server 啟動指令、專案結構解說）
- 只放：不該做的事、開發慣例、Claude 預設不知道的規範

**文件拆分策略：**
- 特定區域（如 DB schema、API 規範）拆成獨立文件，在 CLAUDE.md 連結
- 讓 Claude 用到才載入，不是每次都全部注入 context

**Path-specific rules：**
- 為不同路徑設置規則，Claude 只載入當前任務相關的規則

**Skills 的效益：**
- 重複工作流程封裝成 skill，搭配腳本執行確定性任務
- 避免把確定性任務（可用程式解決）的 token 浪費在 Claude 上

## 設定層級優化

**模型選擇：**
- 簡單任務 → Haiku
- 中等任務 → Sonnet
- 複雜任務 → Opus（但消耗最多）

**Effort 設定：**
- 預設 `auto`，Claude 自行決定推理深度
- 非複雜任務可手動設為 `low`

**停用思考模式（disable thinking）：**
- 與 effort 不同：effort 控制推理深度，disable thinking 完全關閉內部推理步驟
- 不需深度推理的任務直接關閉，節省大量 token

**MCP 管理：**
- 停用目前不需要的 MCP，避免不必要資訊注入 context

**Hooks 過濾輸出：**
- 設置 hook，讓測試結果只將**失敗的測試**注入 context，略過通過的測試
- 可針對各種輸出設置類似過濾

**`.claude` 資料夾設定：**
```
disablePromptCaching: false   # 啟用快取，減少重複 prefix 的費用
autoMemory: false             # 停用背景記憶分析，避免額外 token 消耗
disableBackgroundTask: true   # 停用背景任務（dream、memory refactor、indexing）
```

**append system prompt flag：**
- 一次性指令用 `--append-system-prompt` 帶入，而不是寫進 CLAUDE.md
- 這類指令不會永久佔用 context，session 結束後消失

**max output tokens：**
- 沒有預設值，可手動設定上限
- 不需要長輸出的任務設低一點，積極省 token

## Claude Code 原始碼已知問題

從洩漏的原始碼中發現的隱性 token 浪費：
- 截斷的回應（如 rate limit 錯誤）會保留在 context 繼續累積
- Skills 清單在啟動時自動注入，即使不需要也佔用空間
