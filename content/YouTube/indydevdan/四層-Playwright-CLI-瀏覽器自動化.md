---
title: 四層 Claude Code Playwright CLI 瀏覽器自動化架構
tags:
  - youtube
  - claude-code
  - playwright
  - browser-automation
  - ui-testing
created: 2026-04-13
updated: 2026-04-13
published: 2026-02-16
source: https://www.youtube.com/watch?v=efctPj6bjCY
---

## 核心理念

用 agent 自動化兩大類工作：**Browser Automation**（代替人操作網頁）和 **UI Testing**（自動驗證 UI 使用者流程）。

框架名稱：**Bowser** — 一個可移植到任何 codebase 的四層架構模板。

關鍵原則：**用 CLI 而非 MCP server**
- MCP server 大量消耗 tokens，且固定在別人設計的介面
- CLI 讓你完全掌控，可在其上建構自己的 opinionated 系統

## 四層架構

### Layer 1：Skills（能力層）

兩個核心 skill：

**`playwright-browser` skill**
- 直接調用 Playwright CLI
- 預設 headless 模式
- 支援平行 sessions（`--parallel`）
- Named sessions 可持久化 login 狀態

**`claude-browser` skill**
- 使用 `--chrome` flag 啟動 Claude，注入 Chrome 控制工具
- 限制：**不能並行執行**（一次只能一個 browser instance）
- 適合單一複雜的瀏覽器任務

### Layer 2：Agents（擴展層）

在 skill 上建構專門的 sub-agent：

**`playwright-browser-agent`**
- 簡單 sub-agent，可被重複 prompt 執行任意瀏覽器工作
- frontmatter 啟用 skill，然後在 workflow 裡再次提及

**`browser-qa-agent`**
- UI 驗證專用，處理 user stories
- Workflow：解析 user story → 建立目錄 → 執行步驟 → 截圖 → 回報 pass/fail → 關閉瀏覽器
- 每步驟截圖，提供完整的成功/失敗軌跡

User story 格式（YAML）：
```yaml
name: View Top Post Comments
url: https://news.ycombinator.com
workflow:
  - 前往首頁
  - 點擊第一篇文章的 comments
  - 確認 comments 頁面載入
```

### Layer 3：Commands（編排層）

自訂 `/` 指令作為 orchestration layer：

**`/ui-review`**
- 自動發現所有 user stories
- 建立 agent team，每個 story 指派一個 sub-agent 並行執行
- 每個 agent 完成後透過 task list 回報結果
- 收集所有結果，產生 UI Summary

執行示範：
```bash
# 觸發完整 UI 測試
j ui-review

# 觸發瀏覽器自動化
j automate-amazon
```

**Higher Order Prompt（HOP）**技術：
- `automate` 指令接收另一個 prompt 作為參數
- 固定部分（儲存 workflow、設定環境）放在 HOP
- 變動部分（具體步驟）放在傳入的子 prompt
- 可儲存多個 automation workflow 供重複使用

### Layer 4：Just File（可重用性層）

使用 `just` 作為任務執行器（alias `j`）：

```bash
# 查看所有可用指令
just

# 執行 Chrome 瀏覽器 agent
j chrome-browser

# 執行 Playwright 測試
j playwright-browser

# 帶參數執行
j automate workflow=amazon-add-to-cart
```

`just` 的優勢：
- 集中管理所有 agent 入口
- 支援變數覆寫
- 讓 agent 本身也能發現並使用這些指令
- 整個 team 共用一致的執行方式

## Agentic UI Testing vs 傳統 Testing

| 面向 | Agentic Testing | Jest/Vitest |
|------|-----------------|-------------|
| 設定成本 | 幾乎零 | 需要大量配置 |
| User Story 新增 | 描述性文字即可 | 需寫程式碼 |
| 並行執行 | 多 agent 天然並行 | 需要額外配置 |
| 截圖軌跡 | 自動 | 需要設定 |
| 非確定性 | 是 | 否 |

作者觀點：兩者都需要，但要適度偏向 agentic 方案。

## 完整執行範例

```bash
# 啟動 Amazon 購物自動化（14 分鐘，走到下單前停止）
j automate-amazon

# 同時啟動 UI 測試（3 個並行 browser agents）
j ui-review

# 每個 agent 自動截圖儲存至 screenshots/ 目錄
ls screenshots/
```

## 核心結論

> 「Code 完全商品化了。你的優勢在於你對特定問題的專屬解法，這一路延伸到你怎麼寫 skill。」

不要外包學習：能自己從 library 構建 skill → 疊加 sub-agent → 用 command 編排，才能建構真正有競爭力的 agentic 系統。
