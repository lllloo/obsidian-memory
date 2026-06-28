---
title: "2026-06-28 Daily Updates"
created: 2026-06-28
updated: 2026-06-28
tags:
  - updates
  - claude-code
---

## Claude Code

### v2.1.195 · 2026-06-26（[Changelog](https://code.claude.com/docs/en/changelog#2-1-195)）

**繁中摘要**：以 bug 修補為主的小版，最值得注意的是修掉 hook matcher 對含連字號識別子（如 `code-reviewer`、`mcp__brave-search`）會誤觸 substring 比對的 regression——改成精確比對，先前依賴模糊比對的 hook 設定需重新確認。

- **Hook matcher 改精確比對**：含連字號的 matcher（`code-reviewer`、`mcp__brave-search`）不再 substring 誤中，只精確匹配；若你的 hook 原本靠部分字串命中，行為會變。
- **`CLAUDE_CODE_DISABLE_MOUSE_CLICKS`**：新增環境變數，可在 fullscreen 模式停用滑鼠點擊／拖曳／hover，同時保留滾輪捲動。
- **Voice dictation 修補**：修掉 macOS 長 session 換預設輸入裝置後錄到靜音、以及日文／中文／泰文等無空格語言 auto-submit 永遠不觸發的問題；Linux 端則改善「沒麥克風」與「未裝 SoX」的錯誤訊息區分。
- **Plugin 安裝同意一致化**：修掉僅由專案 `.claude/settings.json` 啟用的外部 plugin 在某些載入路徑未要求明確安裝同意；並修 `/plugin` 啟用／停用在 plugin.json `name` 與 marketplace 名稱不同時失效。
- **背景 agent 穩定性**：修掉背景工作被新版 Claude Code 寫入後在 `claude agents` 消失或掉資料、control socket 啟動失敗導致 daemon 不可達而擋住重啟、以及重開 crash 工作時空白畫面長達 5 秒等問題。

---
