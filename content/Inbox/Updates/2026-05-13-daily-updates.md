---
title: "2026-05-13 Daily Updates"
created: 2026-05-13
updated: 2026-05-13
tags:
  - updates
  - claude-code
  - codex
  - copilot
  - gemini-cli
  - playwright
---

## Claude Code

### v2.1.140 · 2026-05-12（[changelog](https://code.claude.com/docs/en/changelog#may-12-2026)）

> **繁中摘要**：Claude Code v2.1.140 主要是 agent / background / Windows 穩定性修正：Agent tool 的 `subagent_type` 現在接受大小寫與分隔符差異，`/goal` 在 hooks 全關或 managed-only 時不再 silent hang，Windows missing executable 檢查造成 event-loop stall 的問題也修掉。

**變更重點**
- Agent tool `subagent_type` matching 改為大小寫與分隔符不敏感，例如 `"Code Reviewer"` 可解析成 `code-reviewer`
- `/goal` 在 `disableAllHooks` 或 `allowManagedHooksOnly` 設定下會清楚報錯，不再只顯示永遠不結束的 indicator
- Settings hot-reload 修正 symlinked settings files 造成的 misattributed change events 與多餘 `ConfigChange` hooks
- `claude --bg` 在 background service 即將 idle-exit 時不再因 connection dropped mid-request 失敗
- Background service startup 對 enterprise endpoint security 環境給更長等待時間
- Remote managed settings 遇到 401 會強制 refresh token 後重試一次
- `/loop` 不再為已能通知完成的 background tasks 排 redundant wakeups
- Windows 上 missing executable（例如 `gh`）不再反覆同步呼叫 `where.exe` 導致 event-loop stall
- `Read` tool 的 `offset` 參數可接受前後空白或 `+` prefix
- Plugin 現在會警告 default component folder 被 `plugin.json` 對應 key 靜默忽略的情況

**實務影響**
- Agent / subagent 呼叫對人工輸入更寬容，plugin 或 script 不必精準維持 role id 字串格式
- 使用 `/goal` 搭 hooks policy 的環境更容易診斷失敗原因，不會誤以為任務還在跑
- Windows + enterprise endpoint security 使用者應減少 background mode 啟動與工具探測卡頓
- Plugin 作者要留意 component folder 被 manifest key 覆蓋時的新警告，避免以為 commands / agents 已被載入

---

## OpenAI Codex

### 2026-05-11（[Expanded Auto-review documentation](https://developers.openai.com/codex/changelog#expanded-auto-review-documentation)）

> **繁中摘要**：OpenAI Codex 新增 Auto-review 專頁，補齊 reviewer lifecycle、trigger conditions、failure behavior，以及 local / managed configuration 的說明；同時更新 Agent approvals & security 與 Sandbox 文件，釐清 Auto-review 與 sandbox boundary 的關係。

**變更重點**
- 新增 Auto-review 專頁，集中說明 reviewer lifecycle、觸發條件與失敗行為
- 文件補上 local configuration 與 managed configuration 的設定路徑
- Agent approvals & security 與 Sandbox 文件同步更新，讓 Auto-review 和 sandbox boundary 的責任分界更清楚

**實務影響**
- 設計 Codex review workflow 時，可把 Auto-review 當獨立 reviewer lifecycle 看待，而不是把它混同於 sandbox 或 approval policy
- 企業 managed configuration 要查 reviewer 行為時，有了更直接的官方入口

### Codex CLI 0.130.0 · 2026-05-08（[changelog](https://developers.openai.com/codex/changelog#codex-cli-01300)）

> **繁中摘要**：Codex CLI 0.130.0 加入 `codex remote-control` headless app-server entrypoint、plugin details / sharing metadata、app-server thread paging，以及多項 remote / diff / Windows sandbox 修正。

**變更重點**
- 新增 `codex remote-control`，用較簡單的 entrypoint 啟動 headless、可遠端控制的 app-server
- Plugin details 顯示 bundled hooks；plugin sharing 增加 link metadata 與 discoverability controls
- App-server clients 可用 unloaded / summary / full turn item views 對大型 threads 分頁
- Bedrock auth 可使用 `aws login` profiles 的 AWS console-login credentials
- `view_image` 可透過 selected environment 解析 multi-environment session 中的檔案
- Live app-server threads 可吃到 config changes，不需重啟
- Turn diff tracking 在 `apply_patch` 部分失敗但已改檔時仍維持準確
- Remote compaction 對 v2 streams emits `response.processed`，API-key compact requests 不再送 `service_tier`
- Windows sandbox setup 會授權 sandbox users 存取 desktop runtime binary cache

**實務影響**
- Remote-control / app-server workflow 更接近一級入口，automation 可直接呼叫 `codex remote-control`
- Plugin 分享與稽核資訊更完整，可把 hooks inventory 納入安全 review
- 大型 session 的 thread paging 與 turn diff 修正降低 remote UI / app-server 對長任務的操作成本
- Windows sandbox 使用者升級後應減少 runtime binary cache 權限問題

---

## GitHub Copilot

### 2026-05-12（[Copilot code review comment experience improvements](https://github.blog/changelog/2026-05-12-copilot-code-review-comment-experience-improvements)）

> **繁中摘要**：GitHub 改善新版 pull requests experience 裡的 Copilot code review comments，讓建議更容易掃描與處理，並加入 grouped suggestions、severity levels 與更新後的 comment styling。

**變更重點**
- Copilot code review suggestions 會以更容易掃描的方式呈現
- 新 pull requests experience 支援 grouped suggestions
- Review comments 加入 severity levels，方便先處理高風險項目
- Comment styling 更新，降低和一般討論留言混淆的機率

**實務影響**
- PR review triage 可以先依 severity 排序，減少逐條讀 Copilot comment 的成本
- 團隊若已啟用新版 PR experience，Copilot review 的可操作性會比舊 UI 更好

### 2026-05-08（[More flexible secrets and variables for Copilot cloud agent](https://github.blog/changelog/2026-05-08-more-flexible-secrets-and-variables-for-copilot-cloud-agent)）

> **繁中摘要**：Copilot cloud agent 現在可在委派 task 時帶入 secrets 與 variables 到其 GitHub Actions development environment，讓背景 agent 更容易處理需要環境設定或 credential 的工作。

**變更重點**
- Copilot cloud agent task 可傳入 secrets
- Copilot cloud agent task 可傳入 variables
- 這些值會提供給背景 agent 使用的 GitHub Actions development environment

**實務影響**
- 需要 staging token、package registry credential 或 feature flag 的 agent task 不必再手動改 repo 設定
- 權限面要同步檢查：cloud agent 能讀到的 secrets / variables 應維持最小化，避免把長期 credential 給短期任務

### 2026-05-08（[Copilot code review comment types now in usage metrics API](https://github.blog/changelog/2026-05-08-copilot-code-review-comment-types-now-in-usage-metrics-api)）

> **繁中摘要**：Copilot usage metrics API 新增 `copilot_suggestions_by_comment_type`，可把 Copilot code review suggestions 依 comment type 拆開統計。

**變更重點**
- Usage metrics API 新增 `copilot_suggestions_by_comment_type`
- Copilot code review suggestions 可依 comment type 分組觀測

**實務影響**
- 管理者可區分 Copilot review 產生的是哪類建議，不再只看總量
- 若已有內部 adoption dashboard，需要把新的 metric 納入 ETL 或報表 schema

### Copilot CLI 1.0.46 → 1.0.47-0 · 2026-05-12 ~ 2026-05-13（[v1.0.47-0 release](https://github.com/github/copilot-cli/releases/tag/v1.0.47-0)）

> **繁中摘要**：Copilot CLI 1.0.46 修正 PowerShell shim、diff 長行、HTTP2 crash、deprecated version warning 與 read-only `gh` auto-approval；1.0.47-0 則補上 `/diff` j/k 導覽，並改善 `--resume` 對尚未 push branch 的 cloud agent sessions 支援。

**變更重點**
- CLI 版本 deprecated 且可能失去 premium model access 時會顯示 warning
- PowerShell 透過 .NET global tool shim 安裝時可正確啟動
- Diff view 長行會依 terminal width wrap，不再截斷
- Read-only `gh` commands（list、view、status、diff 等）自動核准，不再要求 user confirmation
- Session 不再因 `ERR_HTTP2_INVALID_SESSION` mid-turn crash
- `/diff` view 支援 `j` / `k` 上下導覽
- `--resume` 可處理 Copilot cloud agent 尚未 push branch 的 sessions

**實務影響**
- Windows / PowerShell 使用者升級後能避開 shim 啟動問題
- Autopilot 類 workflow 會少卡在唯讀 `gh` command confirmation
- 使用 cloud agent 的團隊更容易 resume 還沒 push branch 的背景工作

---

## Gemini CLI

### 2026-05-13 · 71 comments（[Addressing Antigravity Bans & Reinstating Access](https://github.com/google-gemini/gemini-cli/discussions/20632)）

> **繁中摘要**：Gemini CLI team 說明近期 Antigravity bans 造成 Gemini CLI / Gemini Code Assist 存取中斷，原因是濫用防護位於共用 backend layer；官方已與 Antigravity 協調進行 system-wide automated unban。

**變更重點**
- 近期帳號中斷與 Antigravity bans 有關，針對違反 Antigravity ToS 的第三方工具或 proxy 使用
- 因濫用防護位於共用 backend layer，Antigravity ban 也影響 Gemini CLI 與 Gemini Code Assist
- 官方進行 system-wide automated unban，讓近期被標記帳號恢復存取
- 後續會調整偵測與溝通，降低誤傷合法 Gemini CLI 使用者

**實務影響**
- 若 Gemini CLI / Code Assist 近期突然 403 或失去 access，先對照是否受這波 Antigravity ban 波及
- 企業或個人 automation 應避免經第三方 proxy 使用 Antigravity quota，否則可能連帶影響 CLI / Code Assist

### 2026-05-09 · 402 comments（[Service update: mitigating abuse and prioritizing traffic](https://github.com/google-gemini/gemini-cli/discussions/22970)）

> **繁中摘要**：Gemini CLI service backing 正在強化濫用偵測並調整流量優先序；官方明說 2026-03-25 起會依 license type 與 account standing 調整 priority，因此不同帳號在 capacity 壓力下的可用性可能不同。

**變更重點**
- 將加強偵測違規 use cases，例如用 Gemini CLI OAuth 搭第三方軟體
- 若帳號疑似被誤標，建議透過 Google Cloud support ticket 處理
- 自 2026-03-25 起，流量 routing 會依 license type 與 account standing 給不同 priority
- capacity 壓力下，不同帳號會看到不同的服務穩定性與錯誤率

**實務影響**
- Gemini CLI 免費 / 付費 / 企業帳號的可用性差異變成 workflow risk，不能只用「有登入」當成功條件
- 自動化或長任務應加 retry / fallback，並把 account standing / license type 納入排障資訊
- 使用第三方 wrapper 或 proxy 前要先確認不會違反 Gemini CLI / Antigravity policy

---

## Playwright

### v1.60.0 · 2026-05-11（[release](https://github.com/microsoft/playwright/releases/tag/v1.60.0)）

> **繁中摘要**：Playwright v1.60.0 把 HAR recording 提升為 tracing API，新增 `tracing.startHar()` / `tracing.stopHar()`，並加入 `locator.drop()` 模擬外部檔案 drag-and-drop。

**變更重點**
- 新增 `tracing.startHar()` / `tracing.stopHar()`，讓 HAR recording 和 tracing 使用同一套 API lifecycle
- HAR recording 支援與 `recordHar` 相同的 `content`、`mode`、`urlFilter` 選項
- 回傳 Disposable，可搭配 `await using` 控制 HAR scope
- 新增 `locator.drop()`，用來模擬外部拖放檔案到頁面元素

**實務影響**
- E2E 失敗排查可在 tracing scope 內順手收 HAR，不必另外配置 browser context 的 `recordHar`
- 測試檔案上傳 / dropzone UI 時，`locator.drop()` 比手寫 drag event 更接近使用者操作

