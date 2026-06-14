---
title: "2026-06-14 Daily Updates"
created: 2026-06-14
updated: 2026-06-14
tags:
  - updates
  - claude-code
---

## Claude Code

### v2.1.176 · 2026-06-12（[Changelog](https://code.claude.com/docs/en/changelog#2-1-176)）

**繁中摘要**：2.1.176 帶來多項 UX 與企業管控改善：session 標題語言跟著對話走、footer badge 可正則自訂、Bedrock credential 快取改照實際到期時間，並修了兩個模型管控漏洞。

- **Session 標題語言**：標題現在依對話語言自動生成；若需固定語言可設 `language` 設定。
- **`footerLinksRegexes`**：新 setting，可透過 user 或 managed settings 以 regex 在 footer row 加自訂連結 badge。
- **Bedrock credential 快取修正**：`awsCredentialExport` 的 credential 現在快取到實際 `Expiration`，而非固定 1 小時，減少不必要的重新鑑權。
- **`availableModels` 管控修補**：alias model 選取不再可被 `ANTHROPIC_DEFAULT_*_MODEL` 環境變數繞過指向被封鎖的 model；`/fast` 在目標 model 不在 allowlist 時會直接拒絕切換。
- **Fable 5 auto mode 修補**：組織未啟用 Opus 4.8 時 auto mode 不再失敗，classifier 會 fallback 到最佳可用 Opus model。
