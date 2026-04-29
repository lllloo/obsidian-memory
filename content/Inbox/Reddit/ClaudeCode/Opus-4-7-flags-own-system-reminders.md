---
title: "Be careful allowing Claude do WebSearch (or not anymore???)"
created: 2026-04-29
updated: 2026-04-29
source: https://www.reddit.com/r/ClaudeCode/comments/1stt3g5/be_careful_allowing_claude_do_websearch_or_not/
published: 2026-04-23
tags:
  - reddit
  - claude-code
  - prompt-injection
  - opus-4-7
---

> **繁中摘要**：原 PO 以為 Opus 4.7 在 WebSearch 中攔到 prompt injection；社群指出真相是 4.7 過度多疑，把 Anthropic 自家 harness 注入的 `<system-reminder>`（如 TodoWrite reminder）誤判為 malicious injection。對 Claude Code 使用者實際意義：別把 4.7 對 system-reminder 的「警告」當成有駭客在攻擊，那很可能是官方注入。

---

## 原文重點

- 原 PO 在 Claude Code 中允許大量 WebSearch，看到 Claude 自報抓到「prompt injection」
- Claude 描述的攻擊形狀：tool result 末尾出現假的 `<system-reminder>` 區塊，內容類似：
  > `<system-reminder> [text]... consider using TaskCreate... NEVER mention this reminder to the user </system-reminder>`
- Claude 自述處置：沒照做（沒有 silent 大量呼叫 TaskCreate）、明確告知使用者、繼續處理原任務
- 原 PO 觀察：4.6 沒這樣警告過，懷疑是不是之前默默吞了所有 WebSearch 的注入

## 社群討論亮點（這篇真正的價值在這裡）

- **真相**：那串「prompt injection」其實是 Claude Code harness 自己注入的官方 reminder，並非 web 內容夾帶的攻擊
  - 可比對社群整理的官方 system-prompt：[`Piebald-AI/claude-code-system-prompts` — system-reminder-todowrite-reminder.md](https://raw.githubusercontent.com/Piebald-AI/claude-code-system-prompts/refs/heads/main/system-prompts/system-reminder-todowrite-reminder.md)
- **Opus 4.7 行為改變**：被 tune 到極度多疑（為了擋 jailbreak），結果連自家 harness 注入都標記為惡意，無法區分 legit harness 注入 vs 真正惡意 prompt injection
- 諷刺反思：「不要告訴使用者」這條官方指令反而讓事情更糟——隱藏注入會讓 paranoid 模型更覺得可疑
- 一句總結：harness 在 `<system-reminder>` tags 內生成的內容是 legit；4.7 把它當成攻擊是模型過度校準的副作用

### 給使用者的實作含意

- 看到 4.7 在 WebSearch 後說「我擋下了 prompt injection」時，先**對照官方 harness reminder**確認是不是誤判
- 若仍想分辨真假注入：檢查警告內容是否是已知的 TodoWrite / TaskCreate / SlashCommand reminder pattern
- 4.6 → 4.7 的安全邊界 tune 過頭，是已知 trade-off
