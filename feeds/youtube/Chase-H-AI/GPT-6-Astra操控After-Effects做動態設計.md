---
title: GPT-6 Astra 解鎖 motion design 與 After Effects
description: 透過免費開源的 Higgsfield motion designer plugin 讓 GPT-6 Astra 在 Codex 內操控 After Effects，以分鏡、詳細 prompt、迭代修改三步驟產出動態圖像
created: 2026-09-15
updated: 2026-09-15
source: https://www.youtube.com/watch?v=C8dWdic-oK4
published: 2026-09-14
parent: "[[01.index]]"
tags:
  - youtube
  - motion-design
  - codex
  - workflow
---

## 核心概念

- GPT-6 Astra 可在 Codex 內直接控制 After Effects，講者完全沒用過 After Effects，所有成品都沒手動點過任何按鈕
- 關鍵是 **Higgsfield motion designer plugin**：免費、開源、不消耗 Higgsfield credits；同樣適用於 Blender 等工具
- plugin 不只是 GPT-6 與 After Effects 之間的橋接，還內含多個 skill，教模型如何最好地使用 After Effects；Astra 透過腳本加 computer use 的組合操控軟體

## 事前準備

需要三樣東西：

1. GPT-6 Astra
2. 已安裝的 After Effects
3. Motion Designer plugin（說明欄附連結）

安裝後在 Codex 內用 `higgsfield/use after effects` 呼叫，或直接以自然語言說「我要用 Higgsfield After Effects plugin skill 來做」即可。

## 步驟一：先做分鏡（storyboard）

- 不要直接丟 prompt 期待 Astra 一次產出滿意成品，而是先讓它產出分鏡圖，視覺化確認雙方想法一致
- 講者的範例最初分鏡為 18 秒，最後剪到 10 秒；對著分鏡溝通遠比成品出來後再改容易
- After Effects 產出很耗時：15～20 秒的動態圖像常需 10～20 分鐘，前期對齊越充分越能避免陷入反覆 prompt 的迴圈
- Astra 內建圖像生成工具，很適合做分鏡；若在 Claude Code 內做，則需要接 Higgsfield MCP 之類的圖像生成來源
- 講者的 GitHub repo 附上影片中所有成品與 prompt，並提供分鏡、建構、修改三種模板
- **參考影片**：可把喜歡的動態效果影片丟給 Astra，它會看影片、擷取合適截圖作為自己創作的指引。範例中的白板動畫即參考 Higgsfield 首席設計師在 Twitter 上發的影片，結果不是一比一複製，但能帶往正確方向

## 步驟二：寫詳細 prompt 並建構

- 實際做法是讓 Codex 自己產生 prompt，但 prompt 需相當詳細。白板影片的 prompt 包含：
  - 明確指示：「用已安裝的 Higgsfield After Effects integration，在 Adobe After Effects 做一支 12 秒白板動畫」
  - 指向參考檔案
  - 拆解 **beats**（動畫中的各個場景），內容應取自分鏡
  - 描述動態效果要長什麼樣子
- 不是動態設計師、不知道怎麼描述動態時的解法：
  - 把參考影片丟給 Codex，請它納入 prompt
  - clone 講者的 GitHub repo，讓 Codex 參考其中 prompt 與模板，依你的分鏡填寫
  - 請 Codex 上網查 After Effects 最佳實務，建立一份「有哪些動態效果可用」的效果庫——非設計師最大的障礙是不知道自己不知道什麼
- 建構耗時範例：15 秒影片花了 22 分 56 秒，且不耗 Higgsfield credits
- plugin 會讓 Codex 自動對照分鏡檢查成果、自行開始 render、檢查最終 render，再於 Codex 內呈現影片並附上專案與所有素材連結，全程不需人手介入

## 步驟三：以 prompt 修改

- 懂 After Effects 可直接在軟體內改；不懂的話同樣靠 prompt 修改，範圍包含畫面、音效設計與背景音樂
- 講者的各個成品通常 2～3 輪迭代就到位
- 觀察到的問題：若不緊盯各 beat 之間的轉場與速度，Astra 傾向每個場景停留 2.5～3 秒，節奏拖沓；要主動要求更俐落的切換
- 修改 prompt 的重點是**明確指出何時、改什麼**（repo 也附修改模板）
- 除非很有經驗，否則避免為這類影片建立自動迴圈——每輪耗時長；創作類工作應保持 human in the loop，不要以為有了分鏡就能讓 Codex 與 Astra 每輪自行對照迭代

## 結語

- 以往已有 Remotion、HyperFrames 等方案，但能直接操控 After Effects 不同：過去需要大量專業與時間，現在非設計背景的人也能涉足動態設計，且只會越來越好
