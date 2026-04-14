---
title: Gemini 3 提示工程三步驟方法
tags:
  - youtube
  - gemini
  - prompt-engineering
created: 2026-04-14
updated: 2026-04-14
published: 2025-11-23
source: https://www.youtube.com/watch?v=UuyaeSLRTkE
---

## Gemini 3 的特性

Gemini 3 是 reasoning model，與傳統模型的關鍵差異：
- 過長/過複雜的 prompt 反而讓它過度分析，效果更差
- 需要簡潔、直接的指令
- 但同時極度 steerable，一個關鍵詞（如「with linear style」）就能大幅改變輸出品質

## Distributional Convergence 問題

模型預設輸出符合訓練資料統計分佈的「安全設計」——通用、無爭議但平庸。這不只適用於前端設計，同樣適用於 debug、資料分析、寫作等任何任務。

## 三步驟提示工程方法（源自 Anthropic 的 Sonnet 4 前端設計 Skill 案例）

### 步驟 1：找出 Convergent Defaults

用最基本的 prompt 讓模型輸出，觀察哪些地方不如預期（typography 無聊、動畫像 PPT、顏色套模板）。

### 步驟 2：找根本原因

不要只描述症狀，要理解為何模型有這個行為。

技巧：在模型輸出不好的結果後，加一條 user message：
```
Debug mode, don't generate again. Why did you set the width to zero for type text?
```

讓模型解釋自己的推理，找出知識缺口。

### 步驟 3：給「正確高度」的替代指令

- 太具體：`<type>text</type> must have width=container_width` → 容易 overfit，邊角案例失敗
- 正確高度：`The best way to align text is to set width equal to the container and use text-align for positioning` → 解釋原則，讓模型舉一反三

反覆迭代直到 prompt 覆蓋所有主要 convergent default。

## Anthropic 前端設計 Skill 的具體做法

他們識別出四個最影響最終設計的區域（typography、animations、background effects、themes），對每個區域：
1. 找出 default 壞行為
2. 翻譯成模型可遵循的程式碼指引
3. 加入 prompt，避免過度注入（每個新 section 都會影響其他行為）

安裝方式：
```
/plugin install anthropic/claude-code-plugins frontend-design
```

## Excalidraw 線框圖案例

示範如何用同樣三步驟優化模型生成 Excalidraw JSON：
- 發現：模型對 `text` 元素設 width=0，因為誤以為會 auto-resize
- 根因：模型不知道 Excalidraw 不支援 intrinsic width
- 指令：改為「text 元素 width 應等於 container，用 text-align 控制位置」
- 還發現：模型使用了不存在的 element type，以及 line 的座標格式錯誤
- 原則：只輸出影響 styling 的屬性，省略 seed/version 等無用欄位
