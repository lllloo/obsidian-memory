---
title: "2026-05-11 Daily Updates"
created: 2026-05-11
updated: 2026-05-11
tags:
  - updates
  - opencode
  - get-shit-done
  - codex
  - gemini-cli
---

## opencode

### v1.14.47 · 2026-05-11（[release](https://github.com/anomalyco/opencode/releases/tag/v1.14.47)）

> **繁中摘要**：opencode v1.14.47 修復 TUI prompt 編輯與 model 切換的可靠性問題，並讓 Scout 預先物化參考 repo、大圖片自動縮放，HTTP API schema 錯誤回傳可讀的 400 body。

**變更重點**
- TUI textarea 回復 prompt editing 鍵綁，包括 `esc` / `enter` 等 alias
- Model 切換在 session 活動中持續生效，不再漂移
- HTTP API schema validation 錯誤改回傳可讀的 400 response body
- Scout 可預先 materialize 設定中的 reference repositories 以供搜尋
- 大型 image attachment 在送出前自動 resize，size limit 可設定
- TUI 中檔案／資料夾路徑盡量以 session directory 的相對路徑顯示

**實務影響**
- 長 session 中切 model 不再被靜默還原，可放心混用不同 model
- 把常用 reference repo 放進 Scout 設定後可直接被搜尋，少了臨時索引成本
- HTTP API 客端的錯誤處理可解析 400 body，CI／automation 寫死的 error parser 可改抓 message

---

## get-shit-done

### v1.41.0 → v1.42.0-rc2 · 2026-05-07 ~ 2026-05-10（[v1.42.0-rc2 release](https://github.com/gsd-build/get-shit-done/releases/tag/v1.42.0-rc2)）

> **繁中摘要**：get-shit-done 在 v1.41.x 連續修了 Windows 安裝、phase planning 拓樸排序、state snapshot canonical 來源等老問題，並在 v1.42.0-rc 線新增 slopsquatting package legitimacy gate、worktree 子程序 timeout 與多項 seam refactor。

**變更重點**
- **Windows 安裝可靠性**（[v1.41.2](https://github.com/gsd-build/get-shit-done/releases/tag/v1.41.2) #3211）：`gsd-sdk` 安裝器改用 PowerShell 探測持久化 Windows PATH、過濾暫時性 `npx` PATH、替換指向已棄用 `gsd-tools.cjs` 的舊 shim；npm-prefix bin 非持久時改 warn 而非假回報 ready
- **CJS bridge 修復**（v1.41.2 #3293）：install payload 補上 `sdk/shared/model-catalog.json`，`model-catalog.cjs` 解析順序為 install path → source repo → `GSD_MODEL_CATALOG`
- **Codex hooks 接受**（v1.41.2）：`get-shit-done-cc --codex` 接受 Codex `hooks.state.*` trust-persistence tables，schema 驗證放寬
- **Phase planning 拓樸排序**（[v1.41.1](https://github.com/gsd-build/get-shit-done/releases/tag/v1.41.1) #3276）：`phase-plan-index` 以 Kahn 拓樸排序＋週期偵測導出 wave，不再單信 frontmatter `wave:`；`wave: 0` 保留不被 `parseInt(...) || 1` 吃掉；宣告值與計算值不一致以非致命 warning 呈現
- **execute-phase cross-wave 清理**（v1.41.1 #3273）：step 5.5 文件化 deviation cleanup tail，跨 wave 間不再靜默跳過清理
- **State snapshot 來源優先**（v1.41.1）：canonical 欄位優先取 YAML frontmatter，body 表格如 `**Status:** ✅ COMPLETE` 不再覆寫
- **Worktree 子程序 bound**（[v1.42.0-rc2](https://github.com/gsd-build/get-shit-done/releases/tag/v1.42.0-rc2) #3281）：git subprocess 加上 timeout，degraded health 會被回報
- **Slopsquatting gate**（[v1.42.0-rc1](https://github.com/gsd-build/get-shit-done/releases/tag/v1.42.0-rc1)）：research → plan → execute 三層防禦，預先註冊的幻覺套件名在 install / build 前就被攔
- **Seam refactor**（[v1.41.0](https://github.com/gsd-build/get-shit-done/releases/tag/v1.41.0)、rc1）：抽出 GSDTools transport seam、command catalog seam、dispatch policy 結構化 result contract、command definition seam

**實務影響**
- Windows 使用者升 v1.41.2 後可解掉「安裝看似成功實際 shim 壞掉」的偽 ready 訊號；含 Codex 整合的 setup（`--codex`）應同步升以避免 hooks schema 卡關
- 用 phase plan 的工作流：原本 wave 0 任務會被誤併進 wave 1、`depends_on` 也被忽略，升 v1.41.1 後行為才符合宣告；既有 plan 升版後需檢查 wave 是否變動
- state snapshot 升 v1.41.1 後以 frontmatter 為準，先前靠 body 文字覆寫狀態的 hack 會失效，需改寫 frontmatter
- 採 rc 線者可拿到 slopsquatting gate 與 worktree timeout，但仍是 release candidate

**待追蹤**
- v1.42.0 GA 時程未明；採用 rc2 須自行追線

---

## OpenAI Codex

### 2026-05-08 · 15 comments（[Memories in Codex](https://github.com/openai/codex/discussions/12567)）

> **繁中摘要**：OpenAI Codex 團隊公開徵詢 memories 功能的設計取向——是否需引用 previous threads、自動 vs 手動觸發、跨 project 範圍、以及自動 sanitise credentials 是否影響 workflow。

**變更重點**
- 設計問題 1：模型若使用過去 thread 的記憶，是否需明確 cite 那些 thread（1–5 評分）
- 設計問題 2：偏好背景自動生成 memory，或手動觸發以控制成本
- 設計問題 3：memory 範圍應限於單一 project，或跨多個 project 共享
- 設計問題 4：是否接受對 memory 自動 sanitise API key / credentials（避免被記住）

**實務影響**
- Codex 即將加入 memories；現在表態可影響預設行為（autonomy vs cost、scope、sanitisation）
- 若已預期跨 project 共用知識，需在 issue 留意該選項是否被採納，否則可能只能 per-project
- 自動 sanitise 預期會擋 credential 類記憶，依賴「Codex 記住某個內部端點 token」的 workflow 應改用設定檔

**待追蹤**
- 最終設計與 default 設定（auto/manual、scope、citation 強度）尚未定案

### 2026-05-07（[Codex Attention Notifier: macOS notifications for approval requests](https://github.com/openai/codex/discussions/21354)）

> **繁中摘要**：社群釋出 codex-attention-notifier，用 hook 在 macOS 對 Codex `PermissionRequest` 事件發原生通知，補上長任務在 approval prompt 卡住卻沒提示的 UX gap。

**變更重點**
- 工具：`constansino/codex-attention-notifier`，hook-based
- 對 Codex `PermissionRequest` hook event 發原生 macOS notification
- 事件 log 寫到 `~/.codex/logs/codex-attention-notifier.log`
- 不會 approve / deny / 修改任何 tool call
- 預設停用 `PreToolUse`，因 Codex 目前每個 matched shell command 都會留可見的 hook record

**實務影響**
- macOS 使用者跑長任務時不必盯螢幕，approval prompt 會推播
- 純讀取 / 不修改 tool call，安全面與 audit 友善
- 想連 PreToolUse 都通知的人需自行打開，但會多出 hook record 噪音

**待追蹤**
- 僅 macOS；Linux / Windows 等價方案未提供

### 2026-05-07 · 2 comments（[Better compaction](https://github.com/openai/codex/discussions/17330)）

> **繁中摘要**：社群 maintainer 分享長期 fork 的 compaction 改良版，把 compaction summary 顯示給使用者並重寫 compaction prompt，在 GPT 5.2 / 5.3-Codex / 5.4 都實測長 session 不再掉 context。

**變更重點**
- 自 PR #8605 起持續 fork patch，將 compaction summary 印給使用者以便發現失誤
- 經多次迭代後改寫 compaction prompt，長 session 中跨 compaction 邊界不再遺失重要工作
- 在 GPT 5.2、5.3-Codex、5.4 皆測試通過
- 目前主線 Codex 仍未採用，作者表示準備分享改進

**實務影響**
- 想做長 session（多次 compaction）的工作流可關注此 fork 或等其進主線
- 提示「compaction summary 可見性」是優化 long-running session 的關鍵——遇到問題時先確認 summary 內容是否遺漏

**待追蹤**
- 主線 Codex 是否吸收此 compaction prompt 與 summary 顯示尚未表態

---

## Gemini CLI

### 2026-05-08 · 3 comments（[Proposed Fix: Resolving Rate Limiting by Removing AI Studio API Keys](https://github.com/google-gemini/gemini-cli/discussions/24430)）

> **繁中摘要**：Gemini CLI 初始化會自動建立或連結 AI Studio API Key，導致 Pro / Ultra 訂閱用戶被計入 Free Tier rate limit；社群驗證移除 AI Studio API Key 後 CLI 會純走訂閱 auth，限制解除。

**變更重點**
- 症狀：付費 Pro / Ultra 訂閱者仍撞到 Free Tier rate limit
- 成因：CLI 初始化時生成或連結 AI Studio API Key，billing 系統獨立並優先採用 API Key 的 Free / Pay-as-you-go 狀態
- 解法：在 AI Studio Portal 移除該 API Key，CLI 改純以訂閱帳號認證
- 付費訂閱者並不需要 AI Studio API Key 即可使用 CLI

**實務影響**
- 已是 Pro / Ultra 但仍被限流者，先到 AI Studio 後台檢查並刪除 CLI 自動建立的 Key
- 新裝 Gemini CLI 時留意不要被引導建立 API Key，以免日後再次踩坑

**待追蹤**
- Google 是否修改 CLI 初始化流程以避免錯誤連結 Free Tier Key 尚未公告

### 2026-05-05 · 18 comments（[\[403 Error\] The caller does not have permission](https://github.com/google-gemini/gemini-cli/discussions/25794)）

> **繁中摘要**：Ultra 訂閱使用者以 `gemini -m {model} -p {message}` 平行呼叫 CLI 撞到 403「caller does not have permission」，TOS 並未明確禁止此用法，目前無官方說明，屬未解 issue。

**變更重點**
- 症狀：Ultra 訂閱用 `gemini -m {model} -p {message}` 平行觸發 message，回 403「caller does not have permission」
- 報告者未使用 antigravity、cron jobs、第三方工具
- 18 則 comment 持續討論但無 Google team 官方回覆
- TOS 與規則中找不到明確禁止平行呼叫的條款

**實務影響**
- 想 script 化或批次跑 Gemini CLI（多 prompt 並行）的工作流目前不穩定，可能撞 403
- 短期建議改 serial 或加 retry / backoff，避免 burst
- Ultra 訂閱不代表可平行；待 Google 表態前不要把 CLI 平行當生產假設

**待追蹤**
- Google team 對「平行呼叫 CLI 是否允許」尚未回應
- 是否有官方 rate / concurrency 上限與正確的批次方式待釐清
