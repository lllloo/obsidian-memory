---
title: "2026-06-10 Daily Updates"
created: 2026-06-10
updated: 2026-06-10
tags:
  - updates
  - claude-code
  - codex
  - copilot
---

## Claude Code

### 2.1.170 · 2026-06-09（[Changelog](https://code.claude.com/docs/en/changelog)）

**繁中摘要**：2.1.170 主要是開放 Claude Fable 5（Mythos 類模型），Anthropic 稱其能力超越所有曾公開發佈的模型，更新至此版本即可使用；同時修復 VS Code 整合終端啟動時 session transcript 未儲存的 bug。

- **Fable 5 GA**：Mythos 類首款模型，Anthropic 稱能力超越歷來所有公開模型；升級至 2.1.170 即可在互動 session 選用
- **VS Code transcript 修復**：從 VS Code 整合終端或繼承了 Claude Code 環境變數的 shell 啟動時，transcript 未儲存（`--resume` 看不到）的問題已修復

---

## OpenAI Codex

### 0.139.0 · 2026-06-09（[Changelog](https://developers.openai.com/codex/changelog)）

**繁中摘要**：0.139.0 在 code mode 加入獨立 web search（回傳純文字結果），並改善 tool definition schema 保留、`codex doctor` 診斷輸出與 plugin marketplace CLI。

- **Code mode 新增 web search**：獨立可用，回傳 plaintext 結果，不需切換模式
- **Tool definitions schema 改善**：`oneOf`/`allOf` 結構現在可正確保留，不再被攤平
- **`codex doctor` 強化**：診斷報告更豐富
- **Plugin marketplace JSON 輸出**：指令加上 `--json` 可取得含 source 資訊的機器可讀結果；catalog 建議改用快取提升回應速度

### 0.138.0 · 2026-06-08（[Changelog](https://developers.openai.com/codex/changelog)）

**繁中摘要**：0.138.0 主要亮點是 `/app` 指令可從 CLI 直接 handoff 到 Codex Desktop（Windows 可直接開啟 workspace），以及本地圖片附件現在會把檔案路徑傳給模型。

- **`/app` 指令**：在 macOS/Windows 上可從 CLI handoff 到 Codex Desktop；Windows 支援直接開啟 workspace
- **圖片附件路徑暴露**：本地圖片附件的檔案路徑現在會傳給模型，讓模型可參照路徑做後續操作
- **Auth**：支援 v2 personal access token
- **Plugin automation**：`add`/`remove` 與 marketplace 操作新增 JSON support

---

## GitHub Changelog

### 2026-06-09（[Claude Fable 5 is generally available for GitHub Copilot](https://github.blog/changelog/2026-06-09-claude-fable-5-is-generally-available-for-github-copilot)）

**繁中摘要**：Claude Fable 5（Anthropic Mythos 類首款模型）正式在 GitHub Copilot 上線，主打長時程、自主 coding 與知識工作任務。

- **Fable 5 GA on Copilot**：可在 Copilot model selector 選用，定位長時程自主 coding 場景

### 2026-06-09（[Security validation for third-party coding agents](https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents)）

**繁中摘要**：第三方 coding agent（含 Claude、OpenAI Codex）在 repo 內操作的安全驗證機制正式 GA，確保 agent 變更在合併前通過安全審核。

- **Security validation GA**：包含 Claude 與 Codex 在內的 repo 操作型 coding agents，統一受安全驗證保障（非 preview）

---
