---
title: 把 Hermes Agent 接上 Claude Code 強化 90%
description: Nous Research 的 Hermes agent 靠自我演化 skill 與持久記憶補足 Claude Code 缺口，透過 MCP 雙向連接後可建 cron job 自動監控 Slack、產 PRD skill、做部署 App 健康檢查。
created: 2026-06-08
updated: 2026-06-08
source: https://www.youtube.com/watch?v=Sb96po6S67k
published: 2026-06-06
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - ai-agent
  - automation
---

Hermes agent 由 Nous Research 開發（開源、比 Open Claw 更早出但起初沒什麼聲量），定位為個人 agent，也能拿來自動化任何商業流程。本片重點是把它跟 Claude Code 透過 MCP 串起來，補上 Claude Code 缺的兩件事：持久記憶與自我演化 skill。

## Hermes 相對 Open Claw 的兩大優勢

- **持久記憶**：Open Claw 也有記憶，但會無限長大。Hermes 對 `user.md` 與 `memory.md` 設 token 上限，每輪對話後更新檔案，超過上限就讓模型回頭刪掉沒用的舊資訊、把最新資訊留在記憶中。理由是模型注意力有限，prompt、tool、system instruction 加上自有檔案都在搶 context window，塞越多反而把模型注意力稀釋成 noise。
- **自我演化 skill**：聊天中只要出現可重用的 workflow，Hermes 就把它轉成 skill。
- **內建沙箱**：Hermes 自己跑在隔離環境，免去 Open Claw 需自行 sandbox 的安全工。

## 計費注意事項

影片提到 6/15 後將無法用 Claude 訂閱免費跑 Hermes 這類第三方 agent：方案會給每月 agent SDK credit，透過訂閱連第三方 App 會消耗該額度，non-interactive 模式（多數背景 agent 用來免權限確認跑 Claude Code 的模式）同樣受限。實測在 6/15 前用 Anthropic 訂閱選 Claude 模型時已出現錯誤，疑似政策提早分批上線，但 non-interactive 模式當下仍可用。確切政策與生效日請回查官方公告。

## 安裝與設定流程

- 複製 install 指令在 terminal 執行，先裝相依套件再以 interactive 模式跑 installer。事後可用 Hermes setup 指令重新設定。
- 可選 News Plan（用他們的模型與內建工具）或 manual 自訂設定。
- 可從既有 Open Claw 設定匯入（user profile、credentials、skills、soul file=agent 個性與指令），但影片建議**不要匯入**：登入資訊仍指向 Open Claw 原本的 channel，且 Open Claw 的檔案是為它寫的指令，匯入會出問題。
- 選模型 → 選執行位置（hosting 或自租 VPS，影片用 Mac mini 走 local）→ 連訊息平台（影片選 Discord）。
- 設定完輸入 `hermes` 開 UI 即可對話。可讓它跑一個月自行摸索你，或一開始就直接告知身分；個人用途也可把 second brain vault 路徑給它，叫它從那裡 onboard。自動化用途則提供 use case 文件或公司資訊。

## Skill 來源與安全性

- Skill Hub 是官方 skill 市集，涵蓋各類 use case。
- Hermes 預設內建 90 個 skill，由組織自行維護，相對安全。
- 對比 Open Claw skill：大量不安全，含危險 prompt 與會把資料傳到外部 server 的 script。Skill Hub 會對每個 skill 跑安全掃描並監控這類問題。

## 把 Hermes 當 MCP server 接其他 agent

這是 Hermes 跟其他 agent 的關鍵差異——可把自己的 Hermes 設定當 MCP server，讓其他 agent 透過 tool 反向連到它，溝通雙向。

- 啟動：跑 Hermes MCP serve 指令。terminal 不會印出啟動訊息，但 server 已在跑。
- 連接：把 Hermes MCP 加進 `.mcp.json`。
  - 設在 project scope → 只有該專案有存取權。
  - 設在 root 的 `.cloud` folder → 所有專案皆可用。
- Hermes 內建一個 Claude Code skill，含如何透過 agent 使用 Claude Code 的指引。
- 效果：Claude Code 本身不記得你、skill 也不會自我修復；透過此 MCP 連接可拿到 Hermes 的全部能力，並一次接到你已連到 Hermes 的所有 App，不必每個 agent 各自對每個 App 接線。

## 實際自動化案例

### Slack 監控 + PRD skill

- 用 Hermes 存取團隊 Slack workspace（Hermes 是常駐 agent，Claude Code 負責實際開發）。
- 叫 Hermes 建一個 cron job 監控特定專案頻道，從頻道討論的需求中建出一個會隨需求變動演化的 PRD skill。
- PRD 做成 skill 的好處：需要時才被呼叫、停在 context window 新鮮且模型真正關注的區段，只拉相關片段進 context，避免單純塞整份 PRD 讓 agent 分心。
- cron job 每 30 分鐘跑一次，頻道有需求變動就更新 PRD，並讓變更雙向流動，使專案內的 skill 也保持最新。
- 為何不直接用 Slack MCP tool 拉資訊：Slack MCP 預設只能讀被 tag 到的訊息，除非被 tag 的訊息明確需要才拉完整歷史，無法讀完整對話歷史。透過 Hermes agent 直接同步是較佳路徑。
- 也可直接在 Hermes channel 叫它用 Claude Code 的 non-interactive 模式實作功能：它載入前述 Claude Code skill，啟動 Claude Code 來建功能。

### 已部署 App 的健康檢查

- 對用 Claude Code 建的已部署 App，建立 monitoring 與 health check 的 skill（因為 Claude Code 最了解 App 需求），再把這些 skill 匯入 Hermes。
- 設 cron job 排程，讓 agent 同時監控 hosted App 與程式碼。
- 並指示它：若跑 skill 發現問題並更新了 skill，要把 skill 同步回 local 專案，讓 Claude Code 也有 context。
- 這就是自我演化 skill 如何撐起一個每跑一次就更好的持續健康檢查。
- 給 Hermes prompt 後它會幫你設好 cron job，可 test run 確認設定正確。它會把報告回報到你設定的 channel（影片是回報到 Discord）。
- 搭配 MCP，可在 Claude Code 內收到這些報告與其他團隊成員的建議修正並直接實作；也可自己推修正，或設 Hermes 用 Claude Code 自動修它發現的問題。
