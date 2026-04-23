---
title: Anthropic 修復 1M Context Window 的問題
tags:
  - youtube
created: 2026-04-23
updated: 2026-04-23
published: 2026-04-22
source: https://www.youtube.com/watch?v=O1XLCh-uA_E
parent: "[[01.index]]"
---

## 核心觀念

- Opus 4.5 之後 Claude Code 模型皆配 1M context window（先前為 200K），但這是一把雙面刃。
- **Context rot**：context 填越滿，模型要分心關注的資訊越多，推理越容易偏掉。
- Claude Code 開發者 Tariq 指出：context rot 從 **300K–400K tokens（約 40% 使用量）** 就開始出現，而不是撐到接近 1M 才惡化。
- 多數人預設的「自動 compact」反而常讓事情更糟，需要主動管理 context。

## 四種 Agent 失敗模式

context 沒管好時，長任務 agent 會出現以下四種失敗：

1. **Context pollution（污染）**：context 太雜，干擾模型推理。
2. **Goal drift（目標漂移）**：agent 忘記原本的目標，UI 要求被反覆提醒還是做不到。
3. **Memory corruption（記憶損毀）**：agent 內部狀態或事實被寫錯、仍照錯誤狀態繼續動作。常見情境：主 agent 建了檔，sub-agent 後來改了檔，主 agent 仍依自己舊記憶操作。
4. **Decision inaccuracy（決策不一致）**：近乎相同的情境下給出矛盾決策，例如同一份程式兩處用不同的 error handling pattern。

## Claude 任務結束後的五種下一步

每次 Claude 完成一段工作，下一步大致有五個選項：繼續、compact、clear、clear + compaction（handoff）、rewind。關鍵是「依意圖選擇」，不要無腦繼續。

### 1. Compact（壓縮）

- 把既有對話摘要成更短的新 context。
- **問題**：summary 是 lossy 的，你以為重要、但 Claude 判斷不重要的細節會被丟掉。
- 自動 compact 最不可靠：觸發時 Claude 被剝掉 system prompt 等輔助 context，全靠自己猜什麼重要；又有 recency bias，偏好保留最近內容，較早但仍關鍵的資訊被忽略。
- **實務建議**：
  - 在 300K–400K token 區間主動觸發 compact，不要等 autocompact。
  - 明確告訴 Claude 要保留哪些決策、限制、已知 issue — 有指令時它會更小心。
  - 只在「想把上一段 context 帶進新視窗」時用 compact，想要乾淨重開就別用。

### 2. Clear（清空）

- 直接清掉全部 context，用空白視窗重新開始。
- 和 compact 不同：什麼都不帶過去，只留你重新丟進去的東西。
- **適用時機**：切換到無關的新任務時。例：剛叫 agent 寫完 test case，接著要 debug 應用程式 — 不想讓剛才寫 test 的脈絡影響 debug 過程，就該 clear。

### 3. Clear + Compaction（JSON Handoff）

- 結合兩者：主動指定要保留什麼，其餘全丟。
- 作法：
  1. 做一個 custom command，以結構化 JSON 捕捉需保留的資訊（完整任務、目前狀態、限制、已知 issue 等）。
  2. 讓 Claude 分析整段對話與專案狀態，依 schema 把資訊寫到檔案。
  3. 用 `/clear` 清掉 context。
  4. 新 session 開起來、讓 Claude 先讀那份檔再繼續。
- **為何比 prose summary 好**：schema 比散文嚴格，Claude 依固定結構填值時表達更一致、更準確。

### 4. 週期性 Recap

- 在長任務中途暫停，請 agent 回顧做過什麼、限制是什麼、重要因素有哪些。
- 這會把原始目標和關鍵細節「推回 context 較新的位置」，對抗 goal drift 與 decision inconsistency。
- 在 compact 或時間稀釋掉它們之前，先讓它們重新「靠近現在」。

### 5. Sub-agents（隔離 context）

- 每個 sub-agent 是獨立實例，有自己的 context window、工具、權限，只把最終輸出回傳給主 agent。
- 所有中間的 tool call、讀檔、web search、推理過程都留在 sub-agent 內，不污染主 context。
- **最典型的用途**：research 任務 — 要逛很多網頁與來源，把整個過程丟進主 context 會爆。
- **判準**：問自己「之後還需要看中間步驟嗎？還是只在意最終結果？」只在意結果就該用 sub-agent。
- Claude Code 會自動派 sub-agent，但有時需在 prompt 明確指示 delegate。
- 常見適用：research、refactor、summarization、document generation。

### 6. Rewind（倒帶）比 re-prompt 更好

- Claude 出錯時，多數人直覺是再下一個 prompt 修正它，但這樣錯的那段仍留在 context 裡。
- **更好的作法**：用 `/rewind` 指令，或連按兩次 `Esc`，把錯誤那段從 context 剔除；然後以新 prompt 給正確方向。
- 也可以從 rewind 點再做一次 summary，保留對的部分當 context。
- **好處**：
  - 清掉出錯段，compaction 時摘要更乾淨，只保留正確實作。
  - 就算有 pin 重要資訊，也能避免把偏題的段落帶到後面。
  - sub-agent 拿到的上游 context 更乾淨；handoff 指令也會捕捉到正確狀態而非被污染的版本。
- 養成「rewind 而非繼續往前修」的習慣。

## 一句話收斂

1M context window 不是問題消失，是 context rot 的起點往後延。真正的護城河是主動管 context：在 300K–400K 之前主動 compact、切任務就 clear、重要狀態走 JSON handoff、長任務中途 recap、研究類工作丟 sub-agent、出錯就 rewind 不要硬修。
