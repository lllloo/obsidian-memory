---
title: OpenAI 與美軍 AI 協議風波
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-05
source: https://www.youtube.com/watch?v=K6CCw1DK1EQ
---

## 事件背景

- Anthropic 拒絕與美國國防部（Department of War）簽署協議，原因是政府要求「不受限制使用 AI 於任何合法目的」
- Anthropic 的底線：禁止自主武器（無人類監督的 AI 殺人決策）、禁止大規模國內監控
- Anthropic 採用「提供模型權重讓政府自行部署」的方式，因此必須靠政策合約來限制使用

## OpenAI 的做法

- 在 Anthropic 談判截止日的幾分鐘後，Sam Altman 宣布與國防部達成協議
- **關鍵差異**：OpenAI **不**提供模型權重，政府透過 OpenAI 的 API 使用——OpenAI 保留 API 控制層，可隨時更新、阻擋不當請求
- 協議內容：部署前置工程師（FDTE）監督使用，加入禁止國內監控和自主武器的語言

## API 控制層的技術意義

LLM 安全機制的兩層架構：
1. **模型訓練層**：訓練時植入安全限制，但可被 jailbreak
2. **API 控制層**：在請求抵達模型前/後由另一個模型審查，可隨時修補無需重訓練

Anthropic 給出模型權重 → 失去 API 控制層 → 只能靠政策合約
OpenAI 維持 API 控制層 → 政策違反時技術上可阻擋

## 各方反應

**Dario Amodei（Anthropic CEO）**
- 稱 OpenAI 的說法是「直接的謊言」和「安全劇場」
- 認為 OpenAI 加那些保護語言只是為了安撫員工，並非真心
- OpenAI 協議允許「任何政府認為合法的用途」——法律可隨行政命令改變

**Trump**
- 稱 Anthropic 是「極左 woke 公司」、「左翼瘋子」，宣布聯邦機構停止使用 Anthropic
- 這使協議選擇變成純政治決策，與安全機制無關

## Theo 的解讀

**Sam 為何這樣做**（steel man）
- 擔心 Trump 的報復性行動會摧毀 Anthropic，而 Anthropic 消失對 OpenAI 也是壞事（會成為壟斷並被拆分）
- 試圖找到「雙方都能接受的技術方案」取代「政策限制」
- 本意是幫 Anthropic 解困，提議政府給其他 AI 公司同樣條件

**但這樣做是錯的**
- 假設政府和 Trump 是善意行事——這個假設錯誤
- 「合法用途」的定義可隨行政命令改變，等於沒有保護
- 選擇在 Anthropic 截止日當天宣布，看起來完全是趁火打劫
- Sam 的行為被 Theo 形容為「最蠢的舉動，不是出於惡意，只是嚴重誤判情勢」

## 後續影響

- ChatGPT 出現大量卸載，Claude 成為美國 App Store 第一名
- 影片拍完後，Anthropic 也重啟與五角大樓的談判
