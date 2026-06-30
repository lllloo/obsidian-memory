---
title: "2026-06-30 Daily Updates"
created: 2026-06-30
updated: 2026-06-30
tags:
  - updates
  - copilot
  - codex
---

## GitHub Copilot

### 2026-06-29（[Claude Opus 4.8 (fast mode) is now in preview for GitHub Copilot](https://github.blog/changelog/2026-06-29-claude-opus-4-8-fast-mode-is-now-in-preview-for-github-copilot)）

**繁中摘要**：Copilot 開始預覽 Claude Opus 4.8 的 fast mode，主打輸出 token 速度大幅提升、但模型智能與標準 Opus 4.8 相同，適合在不犧牲品質前提下換取更快回應。

- **fast mode 預覽上線**：在 GitHub Copilot 逐步推送，鎖定「同等智能、更快輸出」的使用情境；模型選擇時可優先用於互動式 coding 來縮短等待。

---

## OpenAI Codex

### 2026-06-25（[Codex Remote reaches general availability](https://developers.openai.com/codex/changelog#codex-2026-06-25)）

**繁中摘要**：Codex Remote 正式 GA，可從 ChatGPT 手機 app 啟動／接續連線到 Mac 或 Windows 主機的工作，並在手機上審查進度、核可動作；配對改用更安全的一對一 QR 驗證機制。

- **手機遠端操作 GA**：用 ChatGPT mobile app 從手機驅動桌機端 Codex，review 進度與 approve actions 都能在手機完成。
- **Remote Control 改用一對一 QR 配對**：每台 iOS／Android 裝置與每台 host 間做 authenticated QR 配對；6/8 之後使用過的連線維持配對，較舊的閒置連線需重新配對。連線前需先更新 ChatGPT mobile app 與 Codex App。
- **新增 DigitalOcean plugin**：讓 Codex 自動 provision DigitalOcean Droplet、設定 SSH，並把它接成 Codex App 的 remote workspace。
