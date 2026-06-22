---
title: 10 倍強化 Hermes Agent 的隱藏設定
description: Hermes 內建但多數人沒用滿的設定，從 context/output 上限、subagent 並行數、成本控制到 workflow 功能，調 config.yaml 把 agent 效能拉滿。
created: 2026-06-22
updated: 2026-06-22
source: https://www.youtube.com/watch?v=nN6DZi_fiSo
published: 2026-06-20
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
  - automation
---

影片核心：不必再外掛工具，Hermes 本身就藏了一堆沒被用滿的設定，全部集中在 `.hermes` 資料夾的 `config.yaml`（多 profile 時各自一份），調好就能大幅改善 workflow。設定分成四大類。

## Context 與 Output 上限

- **max bytes**：預設 50,000，代表單次只把工具輸出的前 50,000 字元拉進 context window，其餘截斷。監控長測試輸出時會看不到完整問題，需調高。可直接改 `config.yaml` 或用 `hermes config` 指令；用指令改的會寫進當前 active profile 的設定檔，要確認選對 profile。
- **單檔讀取行數上限**：agent 讀大檔（例如 2,000 行以上的政策文件）時按 chunk 拆讀會漏細節，可調到 5,000 讓它一次讀更多。
- **單行字元上限**：預設 2,000；長段落存成單一長行且超過 2,000 字元時不會被完整讀取，用 `hermes config` 調高。
- **compression threshold（壓縮門檻）**：預設 0.5（50% context 填滿就壓縮）。Codex、Claude Code 多設在 0.75 左右。小模型搭 200K context 時 0.5 會太早壓縮影響長任務，建議改 0.75。註：Opus 或百萬 token 的 Gemini 模型壓縮發生在 500K tokens，影響較小；200K context 模型在 100K tokens 就壓。
- **target ratio（保留比例）**：預設 0.2。壓縮時不壓整段對話，保留 20% 不壓並接上摘要作為新對話的 tail，讓 agent 接得上前文。實際保留量隨 context window 大小變動（1M context 保留約 100K tokens、200K context 保留約 20K tokens）。建議範圍 10%–80%，越高保留越多但可用空間越少。
- **memory.md / user.md 字元上限**：超過後 Hermes 會自動丟棄它認為不再需要的資訊。可在 `config.yaml` 或 Hermes 桌面 app 的 settings 調整（多數上述設定也可在桌面 app 改）。

## Subagents

- **max concurrent children**：預設 3，即最多同時跑 3 個 subagent。專案大時會卡瓶頸，影片改成 5。注意這很吃 token，subagent 多時要留意成本。
- **max spawn depth**：預設 1，禁止 subagent 再生 subagent。設大於 1 後，subagent 可再開自己的 subagent（適合在大型巢狀 repo 中分支探索）。
- **auto approve**：預設 false，subagent 只繼承 parent 權限、仍可能被權限提示卡住。設 true 後 subagent 可自動核准、不被 permission prompt 擋。
- **subagent 模型**：web search 之類簡單任務不需主模型，可把 subagent 換成較小模型省 token。若小模型來自其他 provider，用 `hermes auth` 指令把該 provider 的模型加進來。

## 成本設定

- **auxiliary models（輔助模型）**：較便宜、較快、給背景子任務用的模型，避免主模型浪費在小任務上。留空時 Hermes fallback 到 config 內成本最低的模型（影片用 OpenRouter 時是 Gemini Flash）。可手動設定便宜模型處理 web search、壓縮等任務；主模型若是 Opus 更不該浪費在瑣事上。
- **effort level（思考強度）**：越高輸出越好但耗 token 越多。可設 low 或 minimum，或完全關掉 thinking。

## Workflow 功能

- **quick commands**：類似 Claude Code 的 slash command，但 Hermes 不走 prompt 指令方式，分兩種：
  - **exec**：執行終端指令並把輸出塞進 context window，適合把一連串指令（如 Git 操作）包成單一指令。
  - **alias**：替既有指令改名（例：把 `compress` 設成單一字母快速執行）。沒有直接設定入口，要在 `config.yaml` 手動改，或叫 Claude Code / Hermes 代改。
- **checkpointing**：某時間點的檔案存檔，實驗弄壞時可回滾。預設關閉，需設 true，之後用 rollback 指令回到前一個 checkpoint。
- **background process notifications**：設 all 會收到所有背景動作通知，不想要可調整。
- **HERMES_EPHEMERAL_SYSTEM_PROMPT**：環境變數，值會成為 agent system prompt 的一部分。只對該終端開啟的 session 生效、不長期保留，適合一次性用途。
- **Yolo 模式**：等同 Claude 的 dangerously skip permissions，agent 不再等你逐項核准。用 `yolo` 指令或啟動時帶 yolo flag 開啟。
- **ignore user config 模式**：剝除 `.hermes` 內所有 config、隔離執行，用來判斷錯誤是來自 Hermes 本身還是自己的設定。
- **personality 指令**：切換內建的多種人格與語音風格。
