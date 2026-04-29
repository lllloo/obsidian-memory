---
title: "The most useful Claude skill I ever created: humanizer"
created: 2026-04-29
updated: 2026-04-29
source: https://www.reddit.com/r/ClaudeCode/comments/1sy4137/the_most_useful_claude_skill_i_ever_created/
published: 2026-04-28
tags:
  - reddit
  - claude-code
  - skill
  - prompting
---

> **繁中摘要**：vybe.build 創辦人分享他自用的 humanizer skill，掃描 AI 寫作慣性詞與結構問題並改寫，核心參考 Wikipedia「Signs of AI writing」與 WikiProject AI Cleanup。重點不只去 AI-ism，還要主動「加靈魂」（觀點、節奏、不確定性）。

---

## 原文重點

### Skill 的兩段任務

1. **辨識 AI patterns**：掃文字找下列 pattern
2. **重寫**：替換 AI-isms 為自然版本，保留原意與目標語氣
3. **加 soul**：不只移除壞 pattern，主動注入個性
4. **最後 anti-AI 自審**：
   - prompt 自己「What makes the below so obviously AI generated?」列出殘留 tells
   - 再 prompt「Now make it not obviously AI generated.」並改寫

### 「無靈魂寫作」的特徵（即使無 AI-ism 也要避免）

- 每句長度結構雷同
- 只有中性陳述、沒有觀點
- 不承認不確定性 / 矛盾感
- 該用第一人稱卻沒用
- 沒有幽默、銳利、人格
- 像 Wikipedia 條目或 press release

### 加聲音的方法

- **有觀點**：不只報事實，要 react。例：「Part of me thinks this is genius. Another part thinks it's a terrible idea.」
- **變化節奏**：短促句配上慢長句
- **承認複雜性**：「It works, but it also feels like a workaround more than a real solution.」
- **適當用 `I`**
- **容許凌亂**：題外話與離題是人類的特徵
- **感受要具體**：不是「this is concerning」，要寫出具體感受

### Content patterns 黑名單（節錄）

| 類別 | 警示詞 |
| --- | --- |
| 過度強調意義／傳承／大趨勢 | stands/serves as, testament, pivotal, underscores, highlights its importance, reflects broader, symbolizing, contributing to, setting the stage, evolving landscape, key turning point |
| 過度強調知名度／媒體曝光 | independent coverage, media outlets, leading expert, active social media presence |
| 表面分析（-ing 結尾） | highlighting, emphasizing, ensuring |

範例改寫：
- Before：「The company's rebranding in 2021 marked a pivotal moment in its evolution, reflecting broader shifts in the digital marketplace.」
- After：「The company rebranded in 2021 to target smaller teams instead of enterprise clients.」

> 原貼文 selftext 已被截斷（>4000 字），以上為前段重點；完整 pattern 清單回 reddit 原文取。

## 社群討論亮點

- 另一份社群維護的同類規則：[`Anbeeld/WRITING.md`](https://github.com/Anbeeld/WRITING.md/blob/main/WRITING.md)
- 有人指出更省 token 的做法：把這份規則作為**生成期 constraint**，而不是後處理 editing pass
- 進階提醒：盯「過度結構化的 transition」（first / next / finally）——原文若不會自然這樣寫就是 tell
- 反對意見：寫 code 時不需要這種 humanizer，反而想要簡短事實陳述
