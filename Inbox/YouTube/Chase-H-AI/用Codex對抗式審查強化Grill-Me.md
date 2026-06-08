---
title: 用 Codex 對抗式審查強化 Grill Me
description: 在 Matt Pocock 的 Grill Me 計畫對齊之上，bolt 一層 Codex 迭代式對抗審查——Claude Code 與 Codex 多輪來回，補上單一模型無法自評的盲點，讓非工程師也能信任計畫。
created: 2026-06-08
updated: 2026-06-08
source: https://www.youtube.com/watch?v=ENCRw5-uJBA
published: 2026-06-04
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - codex
  - workflow
---

## 要解決的根本問題

Plan mode 不夠。Grill Me、GSD、Superpowers 等 skill 都在解同一件事：把腦中模糊的想法變成 Claude Code 能實作的東西。但無論走哪條路，都撞上同一個問題——你依賴單一模型同時負責規劃、實作，還要它替自己的成果打分。

當你問 Claude「這是不是最佳路徑」，它幾乎一律說「很棒」。對非技術背景的人這很危險：你根本無法判斷 Claude 寫的到底合不合理；而 Claude Code 自己也不能信任去評自己的程式碼（Anthropic 本身講過 Claude 很會「替自己寫的程式碼說好話」，不是可靠的敘述者與評估者）。

存在兩段 gap：

- **你 ↔ Claude Code**：你有想法卻articulate 不出來——Grill Me 這類 skill 處理這段。
- **Claude Code ↔ 最佳程式碼**：就算你和 Claude Code 對齊了，也不代表這就是該被實作的最佳版本。多數人不是資深工程師，無法判斷；Claude Code 也不能可靠自評。這段 gap 正是本 skill 要補的。

## 提供的兩個 skill

建立在 Matt Pocock GitHub 的 Grill Me 與 Grill with Docs 之上，作者做出對應的 **Grill Me Codex** 與 **Grill with Docs Codex**。

- **Grill Me / Grill with Docs（基底）**：plan mode 強化版，問更深的問題，逼出你真正想要的東西。articulate 不清楚就會留下一堆假設，產出平庸成果。
- **加上的第二階段**：你和 Claude Code 對齊後，Codex 進場說「這合理、那不對、修這個」，然後 Claude Code 與 Codex 來回。

## 對抗審查怎麼運作

第一半與原版 Grill Me 完全相同：來回問答把計畫定下來。計畫定稿後 Codex 進場審視 Claude Code 的成果，指出好壞，Claude Code 回應並修正再請 Codex 複看，循環最多五輪（可自行調整）。與標準 Codex plugin 的 adversarial review 不同之處在於它是迭代的——來回夠多次後，理想上在五輪內雙方都點頭 push forward。

雖然 headless，但全程給 Codex session ID，所以第 1、2、3 輪不是空白起點，Codex 一直保有與 Claude Code 整段來回的記憶。

產出兩個 markdown 檔：

- **plan.md**：最終交付物、唯一真實來源，一切以此為基礎實作。
- **plan-review-log.md**：Claude Code 與 Codex 對幹、實際「做香腸」的地方，記錄各輪來回。

## Demo：email gate 範例

需求：在現有網站加一個 email 擷取 gate，輸入 email 才能解鎖（cosmetic blur 遮罩）某個 skill 下載，email 寫進既有資料庫。指令 `run grillme codex` 加上需求與 context。

- 先走 Grill Me 段（與 Matt Pocock 原版相同），總共問了 10 個問題；每題都附帶推薦選項與理由，類似 plan mode 但更深。
- 轉入 Codex 段後產出 plan.md 與 plan-review-log.md。
- **第一輪**：Codex 找出 11 個它認為的問題，Claude Code 更新 plan.md（只採納它認可的）。
- **第二輪**：再找出 4 個 finding（從 11 降到 4），計畫再更新。
- **第三輪**：verdict 為 approved，雙方對齊；Codex 仍標了幾個 low-level note，但屬非阻斷。

抓到的真實安全與正確性漏洞包括：unbounded client skill slug、case-sensitive DDoS 繞過、relative email link、raw bombing vector、table-scanning rate limit。第二輪還抓到「假修正」：聲稱做了 double opt-in 卻沒接線、Supabase JS 無法 target 的 expression index dedup、把 await 移到 response 之後但仍阻斷 unlock。

只三輪就比直接執行第一版計畫再除錯省下大量時間。

## 需求與彈性

需要 OpenAI 帳號與安裝 Codex；$20/月的 OpenAI 方案就能用得很充分。整套設計也容易抽換成本地或更便宜的模型（如 DeepSeek）——把 skill 帶進 Claude Code，叫它把 Codex 換成想用的模型即可，bones 都在，很有彈性。

核心價值：給不自認是專家工程師的人一個能快速、有效率地判斷「Claude Code 做的合不合理」的工具，而這本來就不必是每個人的 wheelhouse。
