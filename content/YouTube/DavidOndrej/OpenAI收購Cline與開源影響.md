---
title: OpenAI 收購 Cline 對開源的影響與替代方案
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-29
source: https://www.youtube.com/watch?v=yk088BCn4Vk
---

## 事件背景：OpenAI 悄悄終結 Cline

- OpenAI 以祕密協議從 Cline 挖走至少 5 名核心工程師加入 Codex 團隊，但沒有正式收購。
- 在此之前，Cline 的 AI 主管已被解雇，後續又有多名工程師跟著離開並加入 OpenAI。
- 效果：Cline 的核心人才消失，但公司仍「活著」——事件後 GitHub commit 數量降至 2024 年以來最低，功能更新大幅減少。
- 這讓數百萬 Cline 用戶面臨不確定的未來。

## 這是業界的慣用骯髒手段

- **Scale AI 案例**：Meta 的 Zuckerberg 以 140 億美元拿下 49% 股份（主要為挖走 CEO Alexander Wang），之後 Google、OpenAI、XAI 撤銷與 Scale AI 的合約，Scale 目前被投資人稱為「殭屍公司」。
- **Windsurf 案例**：Google 花 24 億美元挖走 Windsurf CEO 及共同創辦人、40 位資深工程師，但沒有收購公司。4 個月後 Google 推出 Anti-Gravity——這兩個工具幾乎完全相同，Anti-Gravity 甚至不小心保留了 Windsurf 的助理名稱。
- **統一規律**：挖走人才 → 複製產品 → 留下空殼公司自生自滅。

## 最佳替代方案：Kilo Code

- Kilo Code 是 Cline 和 RooCode 的超集（superset）——包含所有功能，且持續新增更多。
- 核心差異：**承諾永遠開源**，且這不只是口頭承諾：
  - 共同創辦人 Sid 是 GitLab 的共同創辦人，讓 GitLab 保持開源超過 10 年，成功上市且市值達 110 億美元，從未背棄社群。
  - Kilo Code 採用 **Apache 2.0 授權**，法律上綁定必須保持開源。
- 市場表現：在 OpenRouter 上依 token 使用量排名第一，累計超過 1000 億 token，超越 Claude。截至 2026 年，活躍用戶超過 100 萬人。

## 如何使用 Kilo Code

1. 前往 kilo.ai 或搜尋 Kilo Code，右上角點擊「Sign Up」建立免費帳號。
2. 在 VS Code 擴充套件市場搜尋「Kilo Code」並安裝（點擊 Install → Trust）。
3. 點擊左側 Kilo Code 圖示，登入帳號。
4. 在模型選擇器選擇 **Kimi K2.5（Free）**——限時一週完全免費，不需要信用卡或 API key。
5. 在左下角選擇工作模式（architect、code、debug、orchestrator 等）。

## Kilo Code 實測：流體模擬遊戲

- 任務：用 Python + Pygame + Numpy 建立互動式流體模擬器（支援滑鼠拖動添加染料與力、多色煙霧效果、60fps 全螢幕）
- Kilo Code 的處理方式：
  1. 自動建立待辦清單，拆分複雜目標為小任務
  2. 逐一請求操作授權（建立資料夾、安裝相依套件等）
  3. 程式碼以即時打字方式生成，可見每一行的寫入過程
- 特色功能：
  - **Checkpoint 系統**：自動建立還原點，可隨時跳回任何節點，不需要從頭開始
  - **Context 用量儀表板**：清楚顯示每個提示、工具呼叫的 token 消耗、快取命中、輸入/輸出、程式碼行數
  - 透明度遠超其他 AI 工具

## 結語

- 使用 Kilo Code + Kimi K2.5（免費），就能使用世界頂尖的開源 AI 模型建構任何 App，完全免費。
- 如果你是 Cline 用戶，或不信任 OpenAI 對開源社群的態度，Kilo Code 是目前最值得信任的替代方案。
