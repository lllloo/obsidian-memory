---
title: Advisor 顧問策略
created: 2026-05-27
updated: 2026-05-28
source: https://www.youtube.com/watch?v=hGYfsvlQ5Ok
published: 2026-04-09
tags:
  - claude-code
  - advisor
  - context-engineering
---

Anthropic 的 **Advisor Strategy**：Opus 當顧問（只規劃、指導，不執行任何工具呼叫），Sonnet/Haiku 當執行者（負責所有工具呼叫並保有完整共享 context）。Opus **只在執行者卡住時才介入**——填補 Sonnet ↔ Opus 之間沒有中間模型的空缺。效能介於兩者，成本卻比純 Sonnet 還低（多數工作由 Sonnet 跑，Opus 偶爾諮詢）。

## 兩種落地面

| 層 | 啟用 | 對象 |
|---|---|---|
| **API 層** | 呼叫帶 `type: "advisor"` + `max_uses`（Opus 被諮詢次數上限） | 直接呼叫 Anthropic API 的 app，不需 Claude Code |
| **Claude Code CLI 層** | `--advisor` flag 指定 Opus 為顧問模型 | Claude Code 使用者 |

## 與 Plan Mode 的差異

- **Plan Mode**：一次性單向——Opus 規劃 → Sonnet 執行，規劃只發生一次。
- **Advisor**：持續性雙向——執行者遇到無法自解的決策時隨時回頭諮詢 Opus，這個顧問↔執行者關係貫穿整個任務，Opus 始終保有執行者的完整 context。

## 何時用、何時別用

**適合**：在 token 限制內工作、任務以直接實作為主但偶爾需要深度推理的中小型應用。

**不適合（直接用 Opus）**：複雜 app、多個相互依賴元件、多個潛在失敗點。原因——Sonnet 即使遵循 Advisor 建議，仍可能選錯實作路徑，因為它**無法同時評估多種方案的下游影響**；Opus 當主 agent 不只更準，還能識別可平行執行的任務而更快。

**已知問題**：

- 執行者不總能正確判斷任務複雜度，可能該諮詢卻跳過。
- 常需**手動提示「使用 Advisor」**才能觸發正確行為。
- 複雜 app 的來回修正，總時間可能比一開始就用 Opus 還久（執行者循序處理而非平行）。

## 實測印證

- **同步 bug**：純 Sonnet 多次修不好；開 Advisor 後 Sonnet 主動諮詢，Opus 直指同步邏輯斷點位置，一次套用修復。
- **大規模 UI 改版**：Opus 發現新舊元件庫版本衝突、要求先解依賴；但 Sonnet 循序執行，整體偏慢。
- **新功能失誤**：Sonnet 自判常規任務沒諮詢、結果出錯（變更外溢到鄰近元件）；手動要求 Advisor 後 Opus 識別根因（錯誤元件選擇），修正生效。

## 相關

- [[Claude-Code-多-Agent-協作]] — 模型 / agent 協作的其他拓撲
- [[Claude-Code-記憶系統選型]] — context engineering 視角的模型分層
