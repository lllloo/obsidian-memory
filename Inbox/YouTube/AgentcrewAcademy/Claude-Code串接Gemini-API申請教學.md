---
title: Claude Code 怎麼使用 Gemini？Google Gemini API Key 免費申請教學
created: 2026-05-09
updated: 2026-05-09
source: https://www.youtube.com/watch?v=7q2jUth57X8
published: 2026-05-07
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - gemini
---

## 為什麼用 Gemini API 而非 Claude API

Claude（Anthropic）的 API 費用較高，處理大量長文本或批次簡單任務時成本不划算。Google Gemini 的 API：

- 比 Claude API 便宜很多
- Google 的基礎設施，可信任的資料環境
- 適合輕量任務的替代模型

### Gemini 模型選擇

- **Gemini Flash**：速度快、夠聰明，適合大多數日常任務
- **Flash Light**（更便宜）：適合以下場景：
  - 檔案分類與資料標記
  - 簡單翻譯
  - 長文本快速重點提取
  - 非結構化資料轉結構化資料

## API Key 三個不能

API Key 綁定帳號，費用算在你的帳上，洩露後所有用量都算你的：

1. **不能給任何人**
2. **不能 commit 進 Git**（版本紀錄公開後所有人都看得到）
3. **不能直接貼給 Claude Code 讓它幫你設定**（key 會被送到 Anthropic 伺服器並留在對話紀錄）

## 申請流程

1. 搜尋「Google AI Studio」，確認網址為 `aistudio.google.com`
2. 右上角點「Create API key」
3. 選擇或建立一個專案，為 key 取名說明用途
4. 複製生成的 key，**立刻存到安全地方**

## 正確設定 API Key 的方式

不要把 key 貼進對話，而是：

1. 告訴 Claude Code：「我拿到了 API key，我想把它存在我的電腦上，我該怎麼做？」
2. 讓 Claude Code 引導你建立環境變數檔案（`.env`）、加進 `.gitignore`
3. **自己手動貼上 key**，不讓 Claude Code 看到

## 後續維護

- 定期回到 Google AI Studio 檢查用量，異常流量代表可能洩露
- 設定預算上限，防止帳單爆掉
- 若懷疑洩露，立即刪除該 key 並重新申請
