---
title: OpenAI Symphony 協作開發新範式
created: 2026-05-04
updated: 2026-05-04
source: https://www.youtube.com/watch?v=M_AmPWmkpwA
published: 2026-05-02
parent: "[[01.index]]"
tags:
  - youtube
---

## 核心轉變：從管理 session 到管理 ticket

過去幾個月使用 coding agent 的方式經歷三階段：

- 最初僅作為 auto-complete
- 中期以單一互動式 session 為主
- 現在多數人會同時開兩三個 isolated work tree，平行處理不同 feature 或 bug

`Superset`、`Conductor` 等工具雖能管理多 session，但人類在三個以上 session 下會頻繁 context switch，甚至把指令送錯 thread。**瓶頸從模型能力轉移到人類注意力與認知負擔**。

OpenAI Symphony 的觀察：軟體工作流原本就以 **deliverable**（issue、task、ticket、milestone）為單位，工程主管管理上千員工不是逐 PR 審查，而是看最終產出。Symphony 的解法是 **把人類往上抬一層**——人管 ticket，agent 在 ticket 層工作並透過 ticket 回報，人不必盯個別 session。

ticket tracker 因此變成 **state machine**：人與 agent 透過它互動。

## Symphony 架構

三個關鍵元件：

- **Scheduler**：背景程序，每 30 秒掃 Linear board，發現 to-do ticket 就建立 isolated workspace 並啟動 agent session，管理 lifecycle
- **workflow.md**：放在 repo 內、版控管理的單一設定檔
- **外部系統**：例如 Linear，作為 durable state machine

整個設計刻意保持彈性：不一定要用 Linear、不一定要用 Codex，OpenAI 提供 `spec.md` 描述設計，可丟給任何 coding agent 改寫到 Trello/Jira 或其他語言。已有社群把 Codex 換成 Claude Code、用 Python 重寫官方 Elixir 版本，並有人在 task 資料上做自訂 TUI。

## workflow.md 結構

只有一個檔案，分兩部分：

- **YAML frontmatter**：scheduler 設定
  - 對應的 Linear project slug
  - 要撿哪種 status 的 ticket
  - agent 在哪建 workspace
  - workspace 建好後跑哪些 programmatic hook（環境設定不再依賴 agent 自己摸索）
  - 平行 agent 數上限與 agent 設定
- **Markdown 本體**：每回合渲染給 agent 的 system prompt
  - 此 repo 處理 ticket 的 SOP
  - 如何規劃任務、如何驗證工作、何謂「完成」、何時找人 review

設計上的優點：

- 與程式碼放在一起、版本控管、走一般 PR 流程修改
- 沒有獨立的 config service、admin panel、UI
- 新增 agent 能力等同改一份 markdown，其餘流程自動跟上

## Harness setup：讓 agent 能 end-to-end 完成 ticket

Symphony 的前提是 coding agent 的環境能 atomically 完成 ticket。所謂 harness engineering 本質是把環境調好，讓 agent 拿到所有需要的東西。

多數團隊已備齊：

- **可開機**：一個 script 即可備齊環境，agent 不必花時間摸索
- **文件結構**：在 `CLAUDE.md` / `agents.md` 編好不同主題的索引

多數團隊缺的是：

- **self-verifying tools**：實作完能跑端到端測試，並把錄影證據附到 ticket

## Playwright CLI：補上自我驗證的關鍵工具

研究後最佳解是 Playwright CLI（不是 Playwright MCP）：

- Playwright MCP 在 context 中常駐，即使不用也吃大量 token
- Playwright CLI 是 agent skill，按需呼叫
- 提供 `video start` / `video stop` 把瀏覽器 session 錄成 MP4 / WebM
- 進階 video rendering：可在畫面上加章節、用 HTML element 標註 agent 動作
- 錄影直接 upload 到 Linear ticket，人類能輕鬆驗證
- 對比 Chrome DevTools MCP、agent browser 等，目前只有它內建錄影

## 完整 skill 清單建議

範例 repo 內配置的 skill：

- **Playwright CLI skill**：含錄影、trace debug log 的 reference
- **Local server start skill**：教 agent 怎麼起本地服務（簡單情境寫 skill 即可，複雜情境改用預先寫好的 script，讓 agent 不必花腦力）
- **Linear skill**：用 Linear API 操作 ticket、上傳測試錄影證據
- **Grafana log skill**：production log 用 Grafana 集中，agent 可查 production log 修 bug

`agents.md` / `CLAUDE.md` 維持為各 skill / 文件的 index。即使不用 Symphony，這些 skill 也能單獨提升 agent 端到端完成 ticket 的能力。

## 上手步驟

### Step 1：clone Symphony repo

repo 內含 OpenAI 的 Elixir 實作，多數情境直接用即可。要換 Trello/Jira 或換語言時，把 `spec.md` 丟給 coding agent 即可重寫。

### Step 2：建立 Linear 專案與 API key

- 建立 Linear 帳號與 project
- 從 project 取得 project slug
- 在 settings → security and access 建 personal API key
- 跑指令把 API key 全域儲存，agent 後續可存取所有有權限的 project

### Step 3：設定 Linear status flow

Symphony 預設依賴特定 status：

- ticket 進 **to-do** → Symphony 自動 pick up，改為 **in progress** 並起 agent session
- agent 完工 → 改為 **human review**
- 人類 approve → 設為 **merging** → 自動開 PR

### Step 4：產生 workflow.md

打開任意 coding agent（Codex / Claude Code），指向 `spec.md` 並下指令：「I want to set up Symphony for my repo, reuse the Elixir implementation, and help me build the workflow.md file for my repo.」coding agent 會掃 repo 並產出對應的 workflow.md，含 project slug、API key 與其他設定。

### Step 5：執行 Symphony

- 先 `symphony --help` 確認指令格式
- 執行 Symphony 並指向 workflow.md
- 預設會跳警告，需加旗標確認「running without the usual guardrail」
- 啟動後：終端機顯示所有 task、project、下次 refresh 時間

### Step 6：建立 Linear board view

設定 Kanban view 操作 ticket。建立測試 ticket 並設為 to-do，Symphony 會：

1. 撿起 ticket → 改為 in progress
2. 在 isolated workspace 起 agent session
3. agent 規劃任務並逐項打勾
4. 跑端到端測試、上傳驗證錄影
5. 人類設為 merging → 自動開 PR

範例實作另含一個 web UI dashboard，列出與終端機相同資訊（影片作者認為非必要）。

## 關鍵啟發

- coding agent 的瓶頸已從模型能力轉到人類注意力，**「人管什麼」是 paradigm 設計核心**
- 把 ticket tracker 當 state machine，比另建 admin panel / UI 更穩、更可版控
- workflow.md 把 scheduler config 與 agent SOP 合併進 repo，新增能力等同走 PR
- harness 三件事：可開機、文件 index、自我驗證；多數團隊缺第三項
- Playwright CLI + 錄影是補齊自我驗證的高 ROI 工具
