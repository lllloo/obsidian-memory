---
title: DeepSeek V4 vs Opus 4.7 vs GPT 5.5 實測
created: 2026-04-27
updated: 2026-04-27
source: https://www.youtube.com/watch?v=uT2m7VD99qA
published: 2026-04-24
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - codex
  - deepseek
---

## 三模型背景與成本

- 24 小時內接連發布 GPT 5.5（OpenAI）與 DeepSeek V4 Pro（開源 openweight，1.6T 參數，仍需走 API 因為硬體門檻太高）
- Output token 成本（每 1M tokens）：
  - GPT 5.5：約 $30，目前最貴
  - Opus 4.7：約 $25
  - DeepSeek V4 Pro：約 $3.48（比競品便宜約 8 倍）
- Input token 成本：GPT 5.5 與 Opus 4.7 都是 $5/1M；DeepSeek 約 $1.70/1M
- GPT 5.5 雖比 5.4 貴一倍，但 OpenAI 主張因為更省 token，實際 task 成本只貴約 20%
- 各模型分別綁定一套 harness：GPT 5.5 用 Codex、Opus 4.7 用 Claude Code、DeepSeek V4 Pro 用 Open Code

## Benchmark 比對重點

- 三家共報的 coding benchmark：SWEBench Verified、SWEBench Pro、Terminal Bench 2.0
- SWEBench Verified / Pro：Opus 4.7 第一，但 V4 Pro 落後 Opus 約 5 分卻便宜 8 倍
- Terminal Bench 2.0：GPT 5.5 以 87.2 大幅領先，甚至高於 Anthropic 為 Mythos（未發布的內部模型）所報的數字
- Long context（500K–1M token 區間）retrieval：Opus 4.7 顯著退步，反而比 4.6 差很多，DeepSeek 與 GPT 5.5 表現較好；不過實務上很少人真的會工作在這個區間（context rot 問題依然存在）
- 大方向：5.5 是強力對手；V4 Pro 雖然 benchmark 落後但「打得到」，作為開源便宜選項極具吸引力

## Test 1：3JS 飛行模擬器

Prompt 共通：用 3JS 做可在瀏覽器跑的飛行模擬器，要求飛行手感、視覺、結構自由發揮。三組進 plan mode 後分別問了物理擬真度、地形、相機視角等大同小異的問題。

- **GPT 5.5（Codex）**：第一個完成；計畫含 summary、key changes、實作細節、test plan、assumptions；首次跑 7 分鐘 / 63K tokens；初版起飛失敗，第二次 prompt 後可起飛但仍偏難；第三次 prompt 後正常運作（顯示 vertical speed、altitude、AGL、AoA 指示器），總計約 10–15 分鐘 / 66K tokens，整體最佳
- **Opus 4.7（Claude Code）**：計畫最詳盡（含 stack、flight model、stall buzzer 等細節），Plan 階段就花 5 分鐘；執行 13 分鐘、約 20 分鐘 / 150K tokens；初版立刻被甩進空中且操控極差；經過兩次調整後仍受限於 fog 過重、控制 janky，但有跑道、樹、機體等基本元素到位
- **DeepSeek V4 Pro（Open Code）**：計畫最簡略；耗時約 10 分鐘 / 63K tokens（成本僅 ~$0.44）；第一版視覺幾乎崩潰（人稱「完全不知道在看什麼」），第二次 prompt 後勉強看到飛機但仍無法稱為可玩

結論：Test 1 由 GPT 5.5 明顯勝出（最快、最便宜、最完整）；Opus 4.7 第二；DeepSeek V4 Pro 大敗。

## Test 2：WebGPU Shader 落地頁

Prompt 共通：做一個展示 WebGPU shader 的 awards-style 落地頁（風格參考 Igloo 等 awards 網站），三組都拿到同一份 shader 教學 skill。

- **GPT 5.5（Codex）**：6 分鐘 / 107K tokens；hero 是 GPU 驅動的 living signal field 粒子互動；初版過亮、粒子蓋住主文案；第二次 prompt 修正後較收斂，但整體偏粗糙
- **Opus 4.7（Claude Code）**：~6+ 分鐘 / 175K tokens；風格最克制（25 萬粒子、底下顯示 FPS、film grain 由下往上掃）；不夠 flashy 但設計品味較高，作者偏好這版
- **DeepSeek V4 Pro（Open Code）**：耗時最久 / 130K tokens（成本約 $1.43）；初版接近癲癇警告級的閃爍粒子場，第二次 prompt 後變成詭異 UFO 效果

結論：Test 2 由 Opus 4.7 勝出（taste 取勝），GPT 5.5 第二、DeepSeek 再敗。

## 整體結論

- **GPT 5.5（Codex）**：飛行模擬器這種「明確功能性 + 物理」場景最適合，速度與成本表現極佳
- **Opus 4.7（Claude Code）**：偏 taste / 設計感的任務勝出；但較貴、較慢，long context retrieval 有退步
- **DeepSeek V4 Pro（Open Code）**：兩項測試都明顯落後；只在「task 簡單、token 預算極緊」時才合理，否則性價比並未真正打贏 8 倍價差
- 對 agentic coding 使用者是好消息：Codex 與 Claude Code 兩條路都可走，學的是 AI fundamentals，不存在 vendor lock-in
- 模型競爭加劇對使用者更有利
