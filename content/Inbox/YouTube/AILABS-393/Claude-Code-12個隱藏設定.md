---
title: Claude Code 12 個你應該立即啟用的隱藏設定
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: ""
source: https://www.youtube.com/watch?v=pDoBe4qbFPE
parent: "[[01.index]]"
---

## 對話保留期設定

Claude Code 預設只保留 1 個月的對話記錄。可在 `~/.claude/settings.json` 加入：

```json
{
  "cleanupPeriodDays": 365
}
```

設為 0 則不保留任何對話；設為 365 則保留一整年，適合搭配 1M context window 做長期分析。

## Path-Specific 規則

在專案的 `.claude/` 資料夾下設定路徑對應的規則檔，只在 Claude 讀取特定路徑時才載入。避免把所有指令都塞進一個 `CLAUDE.md`，導致 Claude 忽略某些指令。

## Terminal 輸出字元上限

預設 30,000 字元（為舊版 200K context 設計）。使用 1M context window 時可提高：

```json
{
  "terminalOutputCharLimit": 150000
}
```

適用於測試報告、build log、資料庫遷移等大量輸出場景。

## 以 Sub-Agent 模式啟動 Claude

用 `--agent` flag 直接以指定 sub-agent 身份執行任務，跳過 Claude 先載入再切換的開銷：

```bash
claude --agent <agent-name>
```

## Sub-Agent 進階設定

sub-agent 的 config 支援以下進階項目（通常被忽略）：

- `--skill`：讓 agent 繼承特定 skill
- `effort`：控制思考用 token 量
- `hooks`：agent 專屬 hooks
- `background: true`：完全背景執行
- `isolation`：在獨立 work tree 中執行，變更不影響主 codebase
- `permittedAgentNames`：限制該 agent 可以 spawn 的子 agent

## 檔案讀取上限

預設讀取上限為 25K token，可調高：

```json
{
  "fileReadTokenLimit": 100000
}
```

另一個問題：不論 token 上限多高，Claude 預設只讀 2,000 行。Anthropic 不開放修改此限制，但可在 `CLAUDE.md` 寫指令：遇到超過 2,000 行的檔案，先用 `wc -l` 確認行數，再以 `offset` + `limit` 參數分段讀取。也可配合 hook 自動觸發此流程。

## Auto-Compact 觸發比例

預設在 context 填到 95% 時才 compact，但輸出品質在 70% 就開始下降：

```json
{
  "autoCompactPercentageOverride": 75
}
```

## Agent Teams（實驗功能）

- 一個 team leader + 多個 team member，各自是獨立的 Claude session
- Team member 之間可以互相溝通、共享資訊（這是 sub-agent 做不到的）
- 適合大型任務的多 agent 協作

## Claude CTX — 多 Profile 切換工具

開源工具，管理多份 `settings.json` + `CLAUDE.md` 設定。

```bash
# Mac
brew install claude-ctx

# 查看目前 profile
claude-ctx -c

# 切換 profile
claude-ctx <profile-name>
```

切換時自動備份當前設定，各 profile 只含各自需要的 permissions，互不干擾。

## 停用 GitHub Co-Author 標注

Claude 預設在每個 commit 加自己為 co-author。可在 `settings.json` 關閉：

```json
{
  "attribution": {
    "commit": "",
    "pr": ""
  }
}
```

也可設為自訂字串，讓 commit 顯示指定作者名稱。

## 停用 Telemetry

Claude Code 預設傳送使用數據至 Statsig 與 Sentry。在 `settings.json` 加入三個變數可完全停用：

```json
{
  "disableTelemetry": true,
  "disableErrorReporting": true,
  "disableFeedbackDisplay": true
}
```

注意：CLI 的 `--disable-non-essential-traffic` flag 也能停用 telemetry，但同時會停用自動更新，不建議用這個方式。

## Prompt Stashing

正在輸入 prompt 時，若需要先送另一個任務：按 `Ctrl+S` 暫存目前的 prompt。送完新任務後，暫存的 prompt 自動回到輸入框。

## Hook Exit Codes

Hook 可透過 exit code 控制 Claude 的行為：

| Exit Code | 行為 |
|-----------|------|
| 0 | 成功，輸出通常不進 context |
| 其他（非 0/2）| 錯誤訊息顯示於 verbose mode，不阻斷流程 |
| 2 | **強制** Claude 讀取錯誤訊息並採取行動 |

範例：用 pre-bash hook 攔截不想用的套件管理器（如 pip），強制導向 uv：

```bash
#!/bin/bash
if echo "$1" | grep -q "pip install"; then
  echo "請使用 uv 而非 pip 安裝套件"
  exit 2
fi
```

Exit code 2 是 RALF loop（反覆迭代直到達標）的基礎機制。
