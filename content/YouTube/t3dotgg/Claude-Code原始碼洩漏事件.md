---
title: Claude Code 原始碼洩漏事件
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: 2026-03-31
source: https://www.youtube.com/watch?v=Wvj1mTqyzsQ
---

## 事件經過

2026 年 3 月 31 日（Theo 生日當天），Claude Code 的完整 TypeScript 原始碼透過 npm 套件中意外包含的 **source map** 洩漏。

- Anthropic 為取得更好的 production log（為了排查 rate limit 問題），疑似在 build 時意外啟用了 source map
- Source map 的用途：讓混淆後的 JavaScript（13MB 的 cli.js）可以對應回原始 TypeScript 程式碼
- Anthropic 發布的 npm 套件直接包含了 source map folder，等於把原始碼一起發布了
- Anthropic 隨後將 npm 版本下架，並送出大量 DMCA 請求，但程式碼已廣泛傳播（>57k forks）

## Source Map 是什麼

- 瀏覽器只能執行 JavaScript，不能執行 TypeScript
- Build 步驟會把 TypeScript 轉換、壓縮、混淆成難以閱讀的 JS
- Source map 負責把混淆後的 code 對應回原始 source，供 debug 使用
- 若 source map 包在套件中公開發布，等於把原始碼一起交出去

## 陰謀論破解

| 陰謀論 | 事實 |
|--------|------|
| 刻意洩漏 | 否，DMCA 狂送、npm 版本下架，顯然不想外洩 |
| Bun 的 bug 造成 | 否，Bun serve bug 只影響 web hosting，Claude Code 不用 Bun serve |
| 競爭對手會用來改進自家工具 | Claude Code 是最差的 harness（terminal bench 排名倒數），根本不值得抄 |

Anthropic 聲明：「這是人為錯誤造成的 release packaging 問題，非安全漏洞。」

## 從原始碼發現的未發布功能

- **Buddy**：4/1～4/7 期間在 Claude Code 內孵化的虛擬寵物（已因洩漏取消）
- **Dream Mode**：背景 agent 自動整理過往 session 的記憶，改善後續行為
- **Coordinator Mode**：一個 Claude Code 派生出多個 worker agent 平行執行，共用 prompt cache 降低成本
- **Ultra Plan / Ultra Review**：遠端 agent 執行複雜規劃或程式碼審查，含計費控制
- **Teleport**：跨裝置轉移 session（CLI → 手機 / 網頁版）
- **Auto Mode**：用戶不在電腦旁時主動執行任務
- **Chyros**：常駐背景 agent，定期心跳詢問「現在有什麼值得做的事？」，可自動 push PR、回覆 review
- **Undercover Flag**：Anthropic 工程師用 Claude Code 貢獻外部開源專案時隱藏身分，內含「不要暴露你的身分」的嚴格指令

## 技術細節

- **CLAUDE.md 插入時機**：不只在 session 開頭，每次「turn 切換」（用戶送出新訊息）都會重新插入
- **Sub-agent 共享 prompt cache**：多個 sub-agent 共用相同的 context 前半段，大幅降低 input token 費用
- **反 distillation 機制**：在 tool call history 中注入假資料，污染對手嘗試用 Claude 輸出訓練自家模型的資料
- **五層 permission cascade**：policy → flags → local → project → user
- **五種 compaction 策略**：嘗試解決 context 用盡後失去任務連貫性的問題
- **Feature flag 工具**：從 Statsig 改用 GrowthBook（疑因 OpenAI 收購 Statsig）

## 程式碼品質（Claude 自評 7/10）

- 型別安全：500+ 個檔案中只有 38 個 `any`
- 無 callback hell，async pattern 正常
- 使用 Biome 作為 linting 工具
- 缺點：有多個 5000+ 行的 god file、feature flag 散落 250 個檔案、env var sprawl 嚴重、無測試檔案（source map 不含測試）
- 程式碼約 390,000 行（不含 npm 套件）

## Theo 的建議給 Anthropic

1. **直接開源**：門已經被炸開了，秘密醬料的理由不再成立；給個時程表即可
2. **搶先一步**：Anthropic 員工主動聊那些洩漏的功能，而非讓外人用 AI 分析錯誤詮釋
3. **停止亂送 DMCA**：對沒有侵權的人送 DMCA 只會讓你看起來是律師在管公司
4. **用人的方式回應**：學 OpenAI 工程師的風格，幽默、真實、直接，而非法務聲明
