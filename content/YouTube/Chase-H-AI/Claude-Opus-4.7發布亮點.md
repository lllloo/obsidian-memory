---
title: Claude 推出 Opus 4.7 差距拉開
tags:
  - youtube
created: 2026-04-17
updated: 2026-04-17
published: 2026-04-16
source: https://www.youtube.com/watch?v=gc297hx4F7o
parent: "[[01.index]]"
---

## 整體評價

Opus 4.7 相較 4.6 是一次扎實的升級，尤其在 coding、視覺推理與文件推理三大面向提升明顯。Mythos 雖然出現在比較表右側暗示未來登場，但實際可用的是 4.7 對 4.6，這也是評估新模型時真正該看的基準。

## Coding Benchmark 提升

三大主力 coding 測試皆有顯著成長：

| 測試 | 4.6 | 4.7 |
|------|-----|-----|
| SWE-bench Pro | 53 | 64 |
| SWE-bench Verified | 80 | 87 |
| Terminal Bench 2.0 | 65 | 69 |

唯一沒有領先的是 agentic search，GPT 5.4 以 89.3 勝過 Opus 4.7 的 86.7，且這項分數反而比 4.6 還低。當官方放出倒退的 benchmark 時，有時候像是在強調「數據是真的、我們沒有造假」，但也提醒使用者此版本在 agentic search 與研究所等級推理上仍落後 GPT 5.4。

## 視覺與文件能力大幅躍進

- **視覺推理**：69 → 82
- **文件推理**：57.1 → 80.6
- **圖片解析度**：Opus 4.7 處理輸入圖片的解析度提升 **3 倍**，對於含圖表、細小文字的文件特別有用
- 對於長期將文件餵給模型的 office/co-work 使用場景，這是最明顯的生產力紅利

## 長 Context 表現

Long context reasoning 從 71 提升到 75。作者強調**不要因為這個小幅提升就放鬆 session management**，Context Rot 問題依然存在：

- 建議仍維持在 context window 用到 20%~25% 時就 `/clear`
- 頻繁清空 session 是 Claude Code 使用上的長期紀律，不因版本升級而改變

## Multimodal Coding

涵蓋「coding 任務中丟入圖片等多模態內容」的綜合 benchmark 也有提升，與圖片解析度提高直接相關。

## Effort Control 新增 X-High

- 以前只有 high / max，現在在中間插入 **X-high**（明顯是參考 OpenAI 的分層設計）
- **Claude Code 預設升級到 X-high**
- 此變動可能是對 Opus 4.6「被偷偷降級」爭議的回應——Cloud Code 作者 Boris Churnney 曾說明，他們把預設 effort 調到 medium，引發抱怨
- 推出 X-high 可以讓體驗變「更努力」，但又不直接推到 max（推到 max 用量會爆掉，又會引發另一波抱怨）
- 切換指令：`/effort <level>`

## Token 使用量增加（注意額度）

官方明確提醒 Opus 4.7 會比 4.6 吃更多 token，原因有二：

1. **Tokenizer 更新**：輸入 token 數量大約放大 **1x ~ 1.35x**，依內容類型而定
2. **高 effort 下思考更多**：預設從 medium 直接跳到 X-high

若過去已在 4.6 medium 下頻繁撞到 usage limit，升級後更要提早警覺，考慮維持較低的 effort level 或加嚴 session 管理。

## 其他更新

- **API 支援更高解析度圖片輸入**
- 新指令 `/ultra-review`：進入獨立 review session 做深度審查
- **Auto mode 延伸**：等同於 `--dangerously-skip-permissions` 的替代方案，延長使用時間
- **移除 extended thinking**：官方文件有完整 migration 說明

## 小結

- 對 coding 與文件/視覺任務的使用者，升級收益顯著
- 對已逼近額度上限的重度使用者，要警覺 token 放大效應
- Session management 的操作習慣不用改，context rot 仍是長期議題
