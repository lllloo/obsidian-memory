---
title: "I've been in game dev for over 20 years and just tried vibecoding a production-quality competitive multiplayer .io game in 30 days. Here's the honest breakdown."
created: 2026-05-04
updated: 2026-05-04
source: https://www.reddit.com/r/vibecoding/comments/1t10tmu/ive_been_in_game_dev_for_over_20_years_and_just/
published: 2026-05-01
tags:
  - reddit
  - vibecoding
  - workflow
  - ai-tools
  - best-practices
---

> **繁中摘要**：20 年資歷遊戲開發者用 30 天 + Claude 做出 production 級多人 .io 遊戲（nodecontrol.gg）的真實流程。重點是「PRD/DESIGN 鎖定 + 14 階段拆解 + 持久 memory file + 人工判斷何時偏離計畫」，並坦白 AI 在「手感、production bug、debug 鎖死、scope creep」上仍需人類接管。

---

## 原文重點

### 專案

- nodecontrol.gg：神經網路主題的多人領土爭奪 .io 遊戲，Free / 瀏覽器 / 不需安裝。
- 30 天，solo + Claude，已上 production：4 區域 anycast、行動裝置、telemetry、in-game help、FTUE。

### Stack

- **Client**：Three.js (WebGL)、純 JS、單一 HTML entry，所有視覺 procedural（無 model / texture / sprite）
- **Server**：Node.js + `ws` (WebSocket)，server-authoritative game state，60Hz tick
- **Audio**：所有音效用 Web Audio API procedural 合成；BGM 是外部 `.ogg` 串流
- **Deploy**：Cloudflare Pages（client，免費無限頻寬）+ Fly.io 4 區域 anycast（game server，約 `$8/mo`）
- **AI**：Claude 全程，比例約 1% Sonnet、80% Opus 4.6、19% Opus 4.7

### Process

1. **動工前手寫 PRD + DESIGN 文件**（gameplay、network protocol、視覺語言），然後「鎖定」這些文件——但實作中很多決策會被推翻，**判斷何時該偏離原計畫是人類專家的核心價值**：AI 太死守原文件 → 一直走錯路；完全忽略 → 每次 session 重新討論一輪。
2. **拆成 14 個編號階段**：rendering → movement → 基本玩法 → 多人 → bots → UI → mobile → audio → polish → FTUE → deploy → analytics → 最終 polish → 提交。
3. 每個階段一個結構化 implementation pass。AI 寫大部分 code，作者 review 每個 diff、實際跑、判斷、做小幅 polish（即使另有 polish 階段）。
4. **Persistent memory files** 跨 session 維持 AI 方向：學到的規則、專案狀態、code 位置索引。

### AI 做得好

- Three.js boilerplate（instanced geometry、shader uniform、scene setup）
- Game logic 在 client prediction 與 server-authoritative state 之間翻譯
- 從自然語言描述合成音效
- 從 key-list spec 實作 FTUE / 提示系統
- Settings UI、telemetry pipeline、region picker、行動裝置觸控

### 仍需要人

- **手感（Feel）**：AI 可實作 RTT 量測與 lag compensation，但只有人類能實際玩 30 分鐘後說「這 boost 在 production 比 localhost 感覺差」、「玩久了會頭痛」。主觀評估不可化約為自動化。
- **Production bug**：上線後留下一個 bandwidth leak——每個 idle client 每 5 秒發 12 個 HTTPS region probe，每月每 idle client 約 4.4 GB。AI 之前的 code review 從未 flag，作者是 deploy 後好奇看 network panel 才發現。
- **一般 debug**：AI 擅長實作明確變更，但會鎖在錯誤推測上越鑽越深。需人工介入：「你假設 X，但我們還沒驗證 X，先測這個」。
- **擋 scope creep**：AI 永遠樂意加新功能，需要人決定何時停。

## 社群討論亮點

- 多數留言為讚美 / 自我宣傳，技術討論偏少。
- 一名玩家回饋：視覺過亮、過晃、顏色變化太多（每次重生顏色不同），玩起來會 physically sick——間接呼應原作者「手感只能靠人」的論點，視覺也是。
