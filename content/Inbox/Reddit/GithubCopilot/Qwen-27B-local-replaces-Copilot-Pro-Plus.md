---
title: Headsup - I hit my Pro+ weekly limit in 6 prompts and switched to Qwen 27B - it's stunning
created: 2026-05-05
updated: 2026-05-05
source: https://www.reddit.com/r/GithubCopilot/comments/1t3kuvx/headsup_i_hit_my_pro_weekly_limit_in_6_prompts/
published: 2026-05-04
tags:
  - reddit
  - github-copilot
  - local-llm
  - workflow
---

> **繁中摘要**：Pro+ 月度 reset 後 5–6 個 prompt 就用掉 80% weekly premium 額度，作者改用本機 Qwen 27B（5090、Q5 量化、4-bit KV cache、ngram speculative decoding、雙 agent slot），實測 cmake/CUDA debug、C++→PHP refactor、AJAX modal scroll bug 三個情境，主觀體感達 Sonnet 4.5～4.6 等級。

---

## 原文重點

**動機**：Pro+ monthly 額度剛 reset 兩天，premium usage 才 3% 但 weekly limit 已到 80%（約 5–6 個 prompt 用完）。

**本機設定**：

- 模型：Qwen 27B custom 版（接近 vanilla，移除 safety boundaries）
- 硬體：RTX 5090
- 量化：Q5（KV cache 4-bit）
- 推論技巧：ngram speculative decoding、同時跑兩個 agent slot 等於雙倍 context
- 處理 codebase 規模：百萬 token 級

**三個實測情境**：

1. **WSL/Linux cmake CUDA toolkit detection bug**
   - root cause：sub-detection algorithm 用 symlink 位置而非實際 binary 位置
   - 模型一次定位到問題；若放手讓它自動執行 shell 命令會更快
   - 作者主觀評價：難度等同 Sonnet 4.5

2. **把 C++ 自製 scripting language refactor 成 PHP 版**
   - 產出可運作的 PHP 版本
   - **缺陷**：模型沒讀完整個 C++ 檔，部分用「自己發明」的版本取代原邏輯，初看不易發現——這是最大可重現問題

3. **Framework auto-login + admin templating 模組整合**
   - 找到 framework 內 AUTH HASH login 模組，1:1 移植進 admin templating modal
   - 用 curl 測試、卡在 return format
   - 作者提示有 JSON debug version 後，模型自行找到 JSON backend、處理 500KB JSON 而不全載入 context
   - 自動補 README 範例

4. **Opus 4.6 失敗 4 次的 AJAX diagnostic modal bug**
   - 400KB 資料、nested modal、scroll 位置在 grid layout `.cycle-modal-columns` / `.cycle-raw-modal` 上
   - Qwen 一個 prompt 解掉，順手抓出第二個 bug：scroll parent 有多個獨立 scroll location
   - 作者主觀評價：難度等同 Opus / Sonnet 4.6

**已知限制**：refactor 大檔時會「重寫成自己想像的版本」而非忠於原檔，需人工驗證。

## 社群討論亮點

- 4090 user 反映 Qwen 27B 在 LM Studio 下「2 分鐘才處理完 prompt 然後跑很久」——暗示 setup（量化、KV cache、speculative decoding）對速度影響極大，原 po 的 5090 + Q5 + ngram speculative 是關鍵
- 多人在 LM Studio + Cline + VSCode 組合下無法讓 27B 正常運作，提問如何接到 Copilot／OpenCode；社群尚無乾淨可重現的 GitHub Copilot + 本機 LLM 接法
- RTX A5000 24GB / Visual Studio 2026 user 詢問本機 LLM 接 Copilot 路徑——目前似乎只能透過 Ollama 或 fake ollama proxy
