---
title: Claude Code + Playwright CLI：用更少 Token 自動化 QA
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-08
source: https://www.youtube.com/watch?v=nN5R9DFYsXY
parent: "[[01.index]]"
---

## Playwright 三種使用方式

1. **標準測試程式碼**：開發者手寫自動化測試腳本（傳統方式）
2. **Playwright MCP**：讓 AI 透過 MCP server 控制瀏覽器
3. **Playwright CLI**：透過 shell commands 控制瀏覽器（Microsoft 推薦的新方式）

## 為什麼 CLI 優於 MCP

### MCP 的問題：Token 消耗過高

MCP 的運作方式：每次 AI 導航到新頁面，就把整個頁面的 accessibility tree 塞進 context window。每執行一個 action 後，再次塞入整頁資料。

結果：context window 被頁面資料填滿 → AI 用於思考程式碼邏輯的空間減少 → 準確度下降（隨 context 增長，準確度曲線下滑）。

### CLI 的解決方法：Lazy Loading 頁面資料

CLI 不是把頁面資料塞進 context，而是：
1. 把頁面截圖和結構存入 YAML 檔案（disk）
2. 只給 AI 一個「sticky note」摘要
3. AI 需要了解頁面細節時，才讀取 YAML 檔案

YAML 格式的頁面結構（vs 完整 HTML）只有幾百行，每個 element 有一個 reference code 供點擊使用。

```
# 頁面 YAML 範例結構
page: /dashboard
elements:
  nav-transactions: [reference code]
  btn-view-receipt: [reference code]
  dialog-receipt: [reference code]
```

### 效能比較

| 特性 | Playwright MCP | Playwright CLI |
|------|----------------|----------------|
| 每頁面 token 消耗 | 完整 accessibility tree | 僅摘要（需要時讀完整資料）|
| 功能數量 | 基礎 | 3x 更多功能 |
| 最適情境 | 未知 codebase、需要完整視野 | 已知預期行為、驗證 bug 修復 |
| Token 效率 | 低 | 高 |

## MCP vs CLI 準確度取捨

| 場景 | 較好的選擇 |
|------|-----------|
| 登入頁面（已知結構）| CLI |
| 驗證 bug 是否修復 | MCP（需要看完整流程）|
| 導航到未知頁面 | MCP |
| Claude 知道預期行為 | CLI |

**核心原則**：Claude 已知預期結果 → CLI 更好；探索未知 codebase → MCP 更好。

## Playwright CLI Skill 六個核心步驟

1. **Setup**：依資料庫設定，啟動 server
2. **Provision**：建立測試用戶（透過 Supabase MCP）
3. **Login**：登入應用程式
4. **Test**：執行測試，每步截圖，儲存到 `playwright-qa-screenshots/` 資料夾
5. **Cleanup**：清理測試用戶
6. **Report**：生成測試報告，包含：問題狀態（已修復 / 部分修復 / 未修復）+ 重現步驟 + 截圖 + 建議

## Skill 建立方式

作者使用 **Skill Creator** 建立：
1. 傳入 Microsoft Playwright CLI 官方文件
2. Skill Creator 讀取文件 + 加入最佳實踐的 CLI patterns
3. 生成可重用的 skill

依賴項：Jira MCP、Supabase MCP、Playwright CLI（全域安裝）

## 實際 Demo

使用 Jira ticket（bug：點擊「View」後跳轉頁面而非開啟 dialog）：

```
/playwright-qa-cli
  mode: verify
  ticket: CAN-191
```

執行流程：
- 從 Jira MCP 讀取 ticket 詳情
- Supabase MCP 確認/建立測試用戶
- 登入應用程式
- 導航到交易頁面，上傳測試收據
- 點擊「View」按鈕
- 截圖記錄每個步驟
- 生成報告：bug 狀態為「部分修復」（某欄位仍有問題）

## 嵌入更大工作流程

Playwright CLI skill 可以嵌入完整開發自動化流程：

```
Jira ticket → 研究 → 規劃 → 實作 → QA check(1) → code review → QA check(2) → 部署
                                        ↑                              ↑
                              用 CLI 確認 bug 存在              用 CLI 驗證已修復
```
