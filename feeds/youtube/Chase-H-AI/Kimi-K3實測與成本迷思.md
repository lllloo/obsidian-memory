---
title: Kimi K3 的熱度是真的嗎——benchmark 拆解與前端實測
description: 拆解 Kimi K3 的 benchmark 與定價，並用 3D 地球儀網站與 Fable 5、GPT 5.6 對打，指出低單價被 token 效率與速度吃掉
created: 2026-07-21
updated: 2026-07-21
source: https://www.youtube.com/watch?v=MeYdaNnXuHI
published: 2026-07-17
parent: "[[01.index]]"
tags:
  - youtube
  - multi-model
  - llm-pricing
  - evaluation
  - web-design
---

## Kimi K3 是什麼

- 2.8 兆參數的 open-weight 模型，由 Moonshot Lab（Kimi）發表。
- open weight 不等於能在自家電腦跑：實際部署需要數百萬美元等級的硬體。真正的好處是參數調校方式可被檢視，不像 Fable 5 或 GPT 5.6 完全不透明。

## Benchmark 怎麼讀

官方圖表顯示 K3 在主要程式 benchmark 上與 Fable 5、GPT 5.6 並駕齊驅。另一張被大量轉發的圖來自 arena.ai，量的是前端程式碼：

- 機制類似 Pepsi challenge——請它產一個 landing page，回傳兩個匿名模型的結果讓使用者票選，長期累積勝率。
- K3 目前在該榜勝過所有其他模型，但這種投票結果**高度主觀**，不宜當硬指標。

## 定價與真實成本的落差

紙面單價（每百萬 token）確實便宜：

| 模型 | 輸入 | 相對成本 |
|---|---|---|
| Kimi K3 | $3 | 基準 |
| GPT 5.6 | $5 | K3 約為其 60% |
| Fable 5 | $10 | K3 約為其 30% |

輸出端 K3 約為 GPT 5.6 的一半、Fable 5 的 30%。但單價不是成本：

- **token 效率才是關鍵**。中國開源模型普遍是 token hog，GPT 5.6 系列則極度精簡。
- 用 artificial analysis 的「完成同一組 intelligence index 任務要花多少錢」來看：K3 約 $9.5、GPT 5.6 Sol 約 $14、Fable 5 約 $2.75（原始敘述如此，與單價方向相反，屬該指標的任務組合結果）。GPT 5.6 家族中的 Terra／max 檔在某些情況只要 K3 的一半價錢。
- 結論是「比 Fable 5 省」成立，「比 GPT 5.6 大幅便宜」則被誇大，差距常在 10% 以內。

## 速度與幻覺

- **速度**：中國開源模型歷來偏慢。K3 相對前代 K2.6 已大幅改善（該圖表約 6 分鐘），但仍落後 Fable 5（5 分鐘）與 GPT 5.6（4.7 分鐘）。
- **omniscience index（幻覺量測）**：出高難度題目，答對 +1、答錯 -1、回答「我不知道」得 0，滿分 100。Fable 5 得 40 分居首，GPT 5.6 為 22，K3 僅 18。需要大量 nuance、灰色地帶多的 agent 場景，這項特別重要。

## 前端實測：3D 地球儀儀表板

同一個 prompt 分別餵給 Claude Code 內的 Fable 5、Claude Code 內的 Kimi K3，以及 Codex。要求做出「像科幻電影場景、不只是網站」的 3D 地球儀旅遊儀表板，並刻意加上「至少給我一個沒看過的點子」讓三者自由發散。

- **Kimi K3**：地球可縮放旋轉，但精緻度普通；點城市多半無反應，左側 active route 可跳轉，右側顯示經緯度、天氣、最佳旅遊窗口與當下價格，日夜分界有做出來。整體算不錯。
- **Fable 5**：畫面明顯更乾淨銳利，有燈光效果，日夜切換做成可拖曳的滑桿；縮放範圍較小但城市密度與精細度較高。調整時間時右側票價會跟著更新，是三者中完成度最高的。
- **GPT 5.6（Codex）**：地球本身明顯退一階，走比較純的科幻風；點城市的彈窗會壓到地球、字太小難讀；底部雖有日夜掃描但夜間看不見大陸輪廓。排第三。

排名：Fable 5 > Kimi K3 > GPT 5.6。

## 三者的 token、時間與花費

| | Kimi K3 | Fable 5 | Codex |
|---|---|---|---|
| tokens | 21.5M | 3.5M | 5.6M |
| 時間 | 1 小時 33 分 | 17 分鐘 | 25 分鐘 |
| 花費（Open Router） | $8.66 | $11.64 | $5.66 |

token 數與花費不會與公告單價完全對齊，因為三者都有大量 caching 在作用。

K3 吃掉 21.5M token、跑了一個半小時——多做幾個範例就要耗上二十小時，實務上難以接受。花費最高的是 Fable 5，最便宜的是 Codex。

## 結論

- open-weight 模型能與 Fable 5／GPT 5.6 正面競爭，這件事本身值得肯定。
- 但「超便宜」是被誇大的敘事：token 效率低把單價優勢吃掉，某些情境甚至更貴。
- 速度慢是對很多人來說的 dealbreaker；能接受等待的話則不成問題。
- 真正在 benchmark 圖表裡看不見的成本，是 token 與時間這兩種貨幣。
