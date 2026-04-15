---
title: Anthropic 自稱是 Apple，實則是偽善者
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-04-14
source: https://www.youtube.com/watch?v=ysS8GDwsaK8
---

## 事件起因：Anthropic 員工推廣違反 Apple ToS 的 iMessage plugin

一位 Anthropic 員工在 Twitter 上推廣「Claude Code iMessage plugin」，讓用戶可以用 iMessage 和 Claude 對話（買 Mac Mini 取得藍色氣泡）。

此 plugin 明確違反 Apple 服務條款：
- iMessage 不得用於商業活動
- 不得對 Apple 軟體進行逆向工程或解密
- 不得以自動化方式存取其伺服器

Community Notes 直接標記了多項 ToS 違規。

## Anthropic 的訂閱端點限制政策

Anthropic 有兩組 API：
- **使用量計費端點**（`/API/usage-based`）：直接付費使用
- **訂閱端點**（Claude Code 專用）：$200/月訂閱，給更高的使用配額

Anthropic 明確禁止用戶以訂閱 OAuth token 在第三方工具（如 OpenClaw、Open Code、T3 Code）中存取訂閱端點。理由是鎖定用戶只能透過自家 UI（Claude Code、Claude.ai）使用。

Claude Code 官方文件明定：「以 OAuth 取得的認證 token 僅供 Claude Code 與 Claude.ai 使用，在任何其他產品、工具或服務（含 Agent SDK）中使用均違反消費者條款。」

## 偽善的核心：對 Open Code 發法律警告，卻自己做相同的事

Anthropic 在事件發生前一週半，向 Open Code 發送法律要求，強制其下架讓用戶在 Open Code 中使用 Claude Code 訂閱的 plugin——理由是違反「只能在自家 UI 使用訂閱」政策。

同一時間，Anthropic 員工卻在宣傳一個繞過 Apple iMessage 服務條款的 plugin，性質完全相同：用非原廠 UI 存取受限服務。

事後洩漏的 Claude Code 原始碼更顯示，Anthropic 工程師自己在程式碼中參照 Open Code 作為 autoscroll 行為與視窗大小的實作參考。

## Apple vs Anthropic 的比較

Theo 對 Apple 鎖定 iMessage API 的立場：
- Apple 有權選擇不開放 API，使用者自願接受其生態系
- Apple 不應被法律強制提供不想做的產品
- Apple 的行為至少符合一致性，條款清楚

Anthropic 的問題不是鎖定政策本身（這是合法且合理的商業決策），而是**對自己和對別人套用不同標準**。

## 其他 AI 公司的對比做法

- **OpenAI**：允許用戶跨工具使用訂閱；收購 Stipe（OpenClaw 創作者）但不限制其開放性
- **GitHub Copilot**：允許跨工具使用訂閱
- **Kilo**：允許跨工具使用
- **Open Code**：Zen 訂閱可跨工具使用

Anthropic 是目前唯一大幅限制訂閱跨工具使用的主要 AI 提供商。

## 開發者的實際處境

Matt PCO 長達一個月嘗試聯繫 Anthropic，想確認能否用 Claude Code SDK 為開發者建立開源工具，始終得不到明確答覆。Anthropic 刻意保持模糊，保留任意封禁用戶的權利。

T3 Code 被迫完全依賴 Anthropic 的封閉原始碼 CLI（TypeScript Agent SDK 閉源，Python 版開源），才能安全提供 Claude 整合，無法實作更好的用戶體驗。
