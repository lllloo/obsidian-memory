---
title: "2026-05-24 Daily Updates"
created: 2026-05-24
updated: 2026-05-24
tags:
  - updates
  - gemini-cli
  - npm
---

## Gemini CLI

### v0.44.0-preview.0 · 2026-05-22（[release](https://github.com/google-gemini/gemini-cli/releases/tag/v0.44.0-preview.0)）

> **繁中摘要**：Gemini CLI v0.44.0 preview 把多個 Auto 模式合併為單一 Auto mode、引入 agent session 架構（LocalSessionInvocation / RemoteSessionInvocation）、新增 Sublime Text 與 Emacs Client 編輯器支援，並加入 gemini-3.1 model alias 與 thinking config。

**變更重點**

- Multiple Auto modes 合併成單一 Auto mode，降低選項複雜度。
- Agent 框架新增 `LocalSessionInvocation` / `RemoteSessionInvocation`，agent-tool 已與 AgentSession 串接；新增 `adk.agentSessionSubagentEnabled` flag 控制 subagent 行為。
- Agent registration 改為 first-wins 優先、project 優先，避免命名衝突時行為不可預期。
- 新增 Sublime Text 與 Emacs Client 編輯器支援。
- Gemini 3.1 新增 model aliases 與 thinking config 設定。
- RAG snippets 露出到 local log 供除錯。
- 新增 `agent-tui` 與 `tui-tester` skills。
- 修正 OAuth refresh token 在 rotation / retrieval 時遺失的問題；補上 keychain auth 對 `--list-sessions` 與 non-interactive mode 的支援。
- Windows PowerShell 預設改為 `pwsh.exe`。
- Shell text output 加 throttle，live UI buffer 加上限，防止大量輸出卡住介面。
- 修正 subagent thread context 隔離、context file append/replace、restricted preview model fallback 等問題。

**實務影響**

- Auto mode 合併後 model routing 更透明，不需手動在多種 Auto 變體間選擇；適合用作 daily driver 的 fallback model 設定。
- Agent session 架構奠定 local / remote agent 分離的基礎，未來 remote-controlled Gemini agent 與 background session 可能藉此延伸。
- Emacs / Sublime Text 支援擴大了 IDE 整合範圍；若使用這兩款編輯器，值得測試 `@editor` 整合。
- 仍為 preview 版本，不建議用於 production CI；但 agent / OAuth 修正有直接穩定性收益。

---

## npm

### v11.15.0 · 2026-05-22（[changelog](https://github.blog/changelog/2026-05-22-staged-publishing-and-new-install-time-controls-for-npm)）

> **繁中摘要**：npm v11.15.0 把 Staged Publishing（供應鏈安全機制，需人工 2FA 核准才能安裝）設為 GA，並新增三個 install-source flags（`--allow-file`、`--allow-remote`、`--allow-directory`）細化非 registry 依賴的允許範圍。

**變更重點**

- **Staged Publishing GA**：`npm stage publish` 把 tarball 推入 staging queue，需維護者持 2FA 裝置手動核准後才開放安裝；適用 npmjs.com 與 CLI。CI/CD 流程需改為 `npm stage publish`，並搭配 OIDC trusted publishing 讓 CI 非互動式推送、人工在可信裝置核准。
- **新 install-source flags**（v11.15.0 起）：
  - `--allow-file`：控制 local file path 與 tarball 安裝
  - `--allow-remote`：控制 remote URL（含 HTTPS tarball）安裝
  - `--allow-directory`：控制 local directory 安裝
  - 現有 `--allow-git`：控制 Git 來源（已有）
  - 各 flag 接受 `"all"`（目前預設）或 `"none"`，可寫入 `.npmrc` 或 `package.json`。
- **重要前瞻**：`--allow-git` 的預設值將在 npm CLI v12 從 `"all"` 改為 `"none"`，屆時 Git 依賴需明確啟用。

**實務影響**

- Staged Publishing 是 supply chain 防護的重要機制；對公開發佈套件的維護者，升到 v11.15.0 後應評估是否把 CI publish workflow 改為 `npm stage publish`。
- `--allow-remote` / `--allow-file` 可在 enterprise / monorepo 環境中鎖定安裝來源，降低依賴注入風險。
- v12 的 `--allow-git` 預設收緊是 breaking change，現在使用 git 依賴的專案需在升版前加上明確 flag 或改為發佈到 registry。
