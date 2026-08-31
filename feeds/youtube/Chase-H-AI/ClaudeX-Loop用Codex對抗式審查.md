---
title: ClaudeX Loop 用 Codex 對抗式審查補上 Claude 的最大缺陷
description: AI 無法客觀評自己的產出；此 skill 用四階段流程讓 Codex 在計畫與建置兩處把關，Calendly 重製實測揭露 27 項計畫缺陷與 23 項建置發現
created: 2026-08-31
updated: 2026-08-31
source: https://www.youtube.com/watch?v=rZQDZWayzNo
published: 2026-08-24
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - codex
  - evaluation
  - loop-engineering
---

前提：**不能讓 Claude 自己評自己的作品**。每個模型看自己的產出都過度寬容——問 Claude 它剛寫的計畫好不好，答案永遠是「很棒」。ClaudeX Loop 這個 skill 的做法是把 Codex 拉進來，對 Claude 的計畫與執行結果給出「行／不行、為什麼、該改什麼」。

## 四階段流程

使用時機是要新增某個功能之前，或開一個全新的 greenfield 專案。核心原則：第一個模型提出的計畫或執行結果，都要等第二個模型看過點頭才往下走大動作。

1. **Phase 0 — Reconnaissance**：Claude 上網探勘答案是否已經存在。可選擇一般 web search（派幾個 sub agent），或呼叫內建的 deep research dynamic workflow 做更深的挖掘。
2. **Interrogation**：增強版 plan mode 的提問集，在 Claude 產出第一版計畫前先跟使用者對齊。
3. **Review（引入第二個模型）**：Claude Code 依前面的討論與研究寫出標準的 `plan.md`；Codex 在**唯讀 sandbox** 內審查，回覆「approved」或「需修訂 X、Y、Z」。Claude Code 收到修訂意見後表態同意或不同意，再回送自己的改動。此迴圈最多 5 輪。
4. **Build**：雙方達成共識後才建置。可以 Claude 建、也可以 Codex 建；不論誰建，**另一個模型都會再看一次成果**才往下走。

## 可調參數

- Review 階段上限預設 5 輪；作者表示自己從沒真的跑滿 5 輪而未達成共識，設上限是為了避免陷入無盡迴圈燒 token，提供一道明確硬牆。
- Build 階段由 Codex 覆核的迴圈，作者調降為 2 輪；實務上沒遇過需要往上加的情況。
- 可以把 Codex 換成本地模型。

### 與前一版 Grill Me Codex 的差異

- **interrogation 模式強化**：提問更深入。
- **執行階段更深度整合 Codex**：讓它也看實際產出的程式碼，而不只看計畫。

## 實測：重製 Calendly

作者用 `/claudexloop` 加一段意識流描述（做自己的 Calendly、用 Google Meet 取代 Zoom、要跟自己的行事曆連動）啟動。

- **研究階段**：skill 詢問要 web search 還是 deep research。作者的 skill 把 deep research **釘在 Opus**——若在 Fable 上直接跑 `/deepresearch` 會叫出 Fable sub agent，用量會爆掉。系統推薦 web，作者選 deep 試試；接著會顯示提案的 deep research prompt 與想釐清的問題（Google Calendar、Meet、排程領域的坑、技術堆疊），可直接核准或編輯。
- **Assumptions ledger**：研究完成後列出它假設你想要的一切，可整批確認或逐項改。
- **Load-bearing 問題**：真正影響架構的問題逐題提出，每題附建議答案。作者強烈建議：看不懂建議選項時，別當「accept monkey」一路按推薦，改用旁邊的欄位要求 Claude 繼續解釋到你懂為止，這才是真的學會建東西的方式。
- **Cosmetic 決策**：不影響基礎功能的部分整批列出，可一次接受或指定修改，用來加速流程。

### 對抗迴圈的實際數字

計畫送給 Codex（使用 GPT-5.6 Sol）審查後：

- 第 1 輪提出 **27 項問題**，逐輪遞減；跑滿 5 輪仍未達成共識，剩幾項小問題。
- 此時 skill 給出選項：就此打住維持現狀、接受僵局、或**再延長 2 輪**。作者選延長，**第 7 輪達成共識**。

Codex 在計畫階段抓到的問題例如：

- double booking 約束無法編譯。
- OAuth connect flow 有問題。
- 併發問題：同一筆預約的兩次改期可能同時成功。

大多是 edge case 類型。

### 建置與覆核

達成共識後 skill 詢問由誰建置：Claude 建 Codex 看，或反過來；某些情境（例如需要素材生成、要拉進 GPT Image 之類）還會提供**協同建置**選項。此次由 Claude 建置。

成品是可運作的排程頁：有 intro call 與 working session 兩種會議，時段與作者的 Gmail 行事曆同步；填名字與 email 後確認預約，收到含 join link 的 email，行事曆上也出現該筆。

建置後啟動**全新的 Codex session**——記憶全空、context window 全新、沒讀過計畫——直接拿程式碼對照 spec 檢查「做出來的」與「計畫的」是否一致：

- 回報 **23 項發現，19 項被接受並修復，4 項被否決**。
- 例子：每場會議之後時間格線會漂移、management token 以明文存放、全日事件擋掉錯誤的時段。

作者評估：若 Codex 全程不在場，結果會是功能壞掉、預約只存在資料庫而其他地方沒有等狀況；純靠 Claude 或許最終也能迭代到能動，但差別在於**這些問題在計畫階段就被抓出來**，不必先燒一輪 token 做出來、再燒一輪修，整體省時間也省錢。
