---
title: Loop Engineering 任務迴圈化的四步驟流程（兼談 Prompt Engineering 未死）
description: Loop engineering 本質仍是堆疊的 prompt，從手動驗證、做成 skill、自動化到加入成功標準與狀態紀錄，逐步把任務升級成可自我改進的迴圈。
created: 2026-06-24
updated: 2026-06-24
source: https://www.youtube.com/watch?v=JirDfgJcJFU
published: 2026-06-23
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - loop-engineering
  - prompt-engineering
  - automation
  - workflow
---

## Loop engineering 的本質

「Prompt engineering 已死、只該做 loop engineering」這個說法是錯且本末倒置的。迴圈（loop）的核心仍然是 prompt——只是把同一個 prompt 加上額外的鷹架（scaffolding）反覆執行而已。所以說 prompt engineering 死了是誤稱，因為迴圈本身就是一層層堆疊的 prompt。

迴圈和 prompt 一樣只是工具。發現了扳手不代表要丟掉螺絲起子，各有適用場合。不是每個任務都需要做成迴圈，這也反駁了「一招打天下」的迷思。

Loop engineering 的定義：不是給 agent（Claude Code、Codex 等）一個 prompt 叫它做完就好，而是設計成它會反覆、迭代地嘗試，直到達成某個明確的成功標準（success criteria）為止。重點在於把這個迴圈設計得有效率、有效果且合理。

## 迴圈的四個階段

每個迴圈都有四個階段，再加上一個停止條件：

- **觸發（Trigger）**：怎麼把迴圈啟動。可用 Claude Code 的排程任務／routines、cron job、webhook 等，理想上要能自動啟動。
- **執行（Execution）**：AI 實際動手做事的階段，通常是某種 coding 形式。最好做成 skill，因為 skill 適合叫 Claude Code 用特定方式做特定的事、產出特定的輸出。
- **驗證（Verification）**：核心是成功標準。怎麼判斷任務真的完成了。
- **狀態（State）**：輸出與記憶。Loop engineering 真正的賣點是它能每一輪自我改進——但前提是要有文件或資料庫記錄上一輪的結果、嘗試過什麼、什麼有效、什麼無效，下一輪的執行階段才能讀取並據此改進。這呼應了 Ralph loop 的概念。
- **停止條件（Stop criteria）**：嚴格說不算階段，但很重要。何時不再迴圈。可能是達標即停，但因為 AI 不是免費的，通常要設硬性停止（例如進展不再明顯、或固定跑 8 輪就收手）。

## 成功標準是關鍵

如果這支影片只能記住一件事，那就是**成功標準**。它同時決定了「這個任務到底適不適合做成迴圈」。

- **明確／客觀的標準**（最好是數字）：迴圈非常適合。例：要讓 Python 程式跑更快，成功標準就是 runtime，可以一輪輪嘗試降低執行時間。
- **模糊的標準**：例如「寫出更好的 LinkedIn 文章」——什麼叫更好？是互動數嗎？互動數真的等於文章品質嗎？很模糊。模糊的成功標準會降低迴圈的有效性。沒有明確目標與成功標準時，整件事就是空轉、白燒 token。

驗證大致可分五個層級（tier）：

- 前三層是理想區：確定性的 yes/no、某種規則或約束（如 Python 跑更快就屬於規則／約束型）、或可量化的數字（如 likes／engagement）。
- 第三到第五層偏模糊，這時要開始思考「怎麼判斷成功」。

## 與 auto research、`/goal` 的差異

- **Auto research（Karpathy 提出的概念）**：很多 loop engineering 做的事它能自動完成，但它**必須**有明確定義的成功標準，無法處理模糊任務。Python 跑更快是完美用例；模糊目標則不行。Loop engineering 在 Claude Code 裡反而能處理稍微模糊的成功標準。
- **`/goal`（Claude Code 內建，Codex 亦類似）**：本質就是 loop engineering 的縮影——叫 agent 反覆迭代直到達成某條件。差別在於 `/goal` 是**單一 session 內**完成一件事就結束；loop engineering 則是無限時間軸（infinite horizon），帶有自我改進性質，像是「不斷地循環執行 `/goal`」。例如「現在替我寫一篇 LinkedIn 文章」可用 `/goal`，但「每週持續產出更好的文章」就要靠 loop engineering。

## 升級任務的四步驟（英雄旅程）

想把一個任務 loop engineer 化，要循序漸進，不能一步到位：

- **步驟一：純手動驗證**。先打開 Claude Code 手動操作（例如「研究 AI 相關內容、幫我寫一篇 LinkedIn 文章」）。這一步是為了確認這件事 AI 真的做得到、可行。很多人不幸永遠卡在這一步。
- **步驟二：做成 skill**。確認可行且值得未來持續改進後，把流程編碼（codify）成 skill，避免每次都重述 A、B、C 步驟。
- **步驟三：自動化**。在 Claude Code 的 routines 裡建一個自動化（例如命名為「LinkedIn article」），指示就是「跑 LinkedIn article skill」，再排定觸發時機（例如每天早上 9:00）。到這裡其實已經順手把**觸發**和部分**執行**做完了。
- **步驟四：真正的 loop engineering**。在 skill 上補齊後半段——自我改進、成功標準與狀態紀錄。

關鍵提醒：到步驟三之後要問自己「真的需要步驟四嗎」。只要能用某種方式定義成功（即使有點模糊），又有辦法記錄狀態，通常就夠用了。

## 狀態紀錄與 LLM 評審的取捨

要做到自我改進，必須能把輸出與成效記錄下來。以 LinkedIn 文章為例，若以「likes」定義成功，就需要某種 scraper 去抓互動數據，存進資料庫，之後才能分析「哪個 hook 有效、哪個 CTA 有效」並回饋到下一輪執行。

判斷模糊品質時的兩種評審路線，都要小心：

- **用 LLM 當評審（LLM as judge）**：若 Claude Code 是寫文章的人，通常**不該**讓它自己評自己的文章——AI 系統普遍偏愛自己的產出。可以引入 Codex 之類的另一個模型來審查 Claude 的輸出。
- **把人放進迴圈（human in the loop）**：最強但最不自動。這時要反問「這還需要做成迴圈嗎」。有些場景確實需要人介入，例如一篇文章互動數很高，可能只是時機與題材剛好，與文章品質無關，未必該把它當成往後的黃金標準。

這些取捨沒有完美解，全是個案判斷，需要自己實驗才能定案。

## 完整迴圈範例與現實中的複雜度

把 LinkedIn 例子組起來：觸發在每天 9:00、執行靠 skill、目標定為「拿到最多 likes」、用 scraper 驗證、把文章與 likes 寫進資料庫。每天 9:00 觸發後，skill 不只抓 AI 新聞，還會讀取過往文章與 likes 的資料庫做分析（最近什麼在 trending、試過哪些 hook、CTA 如何），把這些一起帶進執行——這就是自我改進的部分。

現實中模糊目標會增加複雜度：

- 從「寫文章」到「拿到 likes」之間有延遲，所以不會只有一個迴圈。通常還要有**第二個迴圈**在外面跑（例如每 24 小時 scrape 一次 likes）來持續更新數據，這需要時間累積出真實的資料。
- 相較之下，明確目標（如「Python app 跑更快」）就單純得多：例如每 10 分鐘觸發、跑 app、檢查時間，用一份 handoff 文件記錄各次的時間與對應 code 改動（diff），反覆改 code 看哪個 diff 能降低時間。

結論：成功標準越明確，loop engineering 就越容易。
