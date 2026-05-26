---
title: "2026-05-26 Daily Updates"
created: 2026-05-26
updated: 2026-05-26
tags:
  - updates
  - copilot
---

## GitHub Changelog

### 2026-05-20（[Copilot usage metrics reports now use GitHub-owned download URLs](https://github.blog/changelog/2026-05-20-copilot-usage-metrics-reports-now-use-github-owned-download-urls)）

> **繁中摘要**：Copilot usage metrics 報告的下載 URL 已從 Azure Front Door domain 遷移到 GitHub 自有 custom domain，URL 穩定性提升；有自動化腳本抓取此報告的用戶需更新 URL。

**變更重點**

- 下載 URL 從 Azure Front Door domain 遷移至 GitHub-owned custom domain（stable URL）。
- 此變更為先前已公告的計劃性遷移，正式生效。
- API 與 Copilot 管理介面回傳的報告連結已自動更新為新 domain。

**實務影響**

- 若有 CI/CD 腳本、cron job 或 dashboard 使用硬編碼舊 Azure Front Door URL 下載 Copilot usage metrics 報告，需更新為新的 GitHub-owned URL（從 GitHub API 或 Copilot 管理介面重新取得最新下載連結）。
- 新連結穩定性更高，不依賴第三方 CDN 設定；日後 URL 格式不應再因 CDN 遷移而變更。

---

**同步統計**

- 來源抓取：14 筆（7 GitHub Changelog RSS + 4 OpenAI Codex + 3 Claude Code）
- 粗篩通過：8 筆
- 去重後留存：1 筆
- 已寫入：1 筆
- 略過重複：13 筆（Claude Code v2.1.147–149 已收錄於 05-22~05-23；GitHub Copilot Eclipse/model/Gemini 3.5/review 已收錄於 05-20~05-23；OpenAI Codex 05-21 已收錄於 05-22；Claude Code v2.1.150 僅 internal changes 略過）
