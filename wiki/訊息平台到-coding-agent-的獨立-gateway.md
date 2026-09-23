---
title: 訊息平台到 coding agent 的獨立 gateway
description: 不綁 Hermes／OpenClaw 的訊息橋接工具盤點：多 agent 通吃的 cc-connect、接 tmux／herdr 的 ccgram、各家官方 channel，依綁定緊密度分三層
created: 2026-09-23
updated: 2026-09-23
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - automation
---

2026-09-23 回答「有沒有像 Hermes gateway 那樣、但獨立不綁在 Hermes 內的東西」的 Query 回存。星數、授權、最後 push 為 GitHub API 當日查得；功能描述經 README 或官方文件複核，WebSearch 摘要未複核的不列。**強度**：目錄層事實「高」；未實測任何一套。

**一句話**：Hermes 與 OpenClaw 的 gateway 是「gateway 內含 agent runtime」；獨立 gateway 是「gateway 外接既有 CLI agent」。多 agent 通吃的是 cc-connect；已用 tmux／herdr 跑 agent 的人零改動可接 ccgram；各家官方 channel 只綁自家。

## 三層盤點

### 第一層：獨立、多 agent 通吃

| 工具 | 星數／授權／最後 push | 平台 | 後端 agent | 備註 |
|---|---|---|---|---|
| [cc-connect](https://github.com/chenhg5/cc-connect)（Go） | 約 15.6k／**無 LICENSE 檔**／2026-09-22 | 13 個：Telegram、Slack、Discord、Matrix、LINE、Feishu、DingTalk、WeCom、QQ 等，多數 long polling 免公網 IP | Claude Code、Codex、OpenCode、Copilot、Gemini CLI、Kimi CLI、任何 ACP 相容 agent（README 支援矩陣） | README 大半是中國 API 中繼商贊助廣告；「Pi」在矩陣標為「Cursor Background Agent」，語意待確認 |
| OpenClaw Gateway | 隨 OpenClaw | OpenClaw 全部通道 | `agentRuntime.id` 可設 `openclaw`（預設，pi SDK 為底）、`codex`、`claude-cli`；`pi` 為舊別名 | 不能單獨裝，但可拿它前置 Claude Code／Codex；信任域設計見 [[OpenClaw-與-Hermes-Agent-比較]] |
| [claw-orchestrator](https://github.com/Enderfga/claw-orchestrator) | 約 580／MIT／2026-09-22 | 非訊息 gateway | Claude Code、Codex、agy、Cursor、OpenCode 統一 runtime，對外 OpenAI 相容端點、MCP server、ACP agent | 是「gateway 底下那層」，不是 gateway 本身 |

**勿依賴**：OpenACP（Open-ACP/OpenACP）在搜尋結果常出現，2026-09-23 主 repo 已 404，只剩 2026-04 的 Telegram／Signal／WhatsApp／Mattermost adapter 殘件。

### 第二層：Telegram 對終端多工器的橋，agent 不限

- [ccgram](https://github.com/alexei-led/ccgram)（Python 3.14+，MIT，約 269 星，2026-09-14）：一個 Telegram topic 對應一個 tmux 視窗、**herdr** session 或 agterm session；監看終端輸出並送鍵，故 Claude Code、Codex、Gemini、pi、純 shell 皆可。herdr 模式需先 `herdr integration install`。與 [[Herdr-使用方法]] 的環境直接相容。
- [ccbot](https://github.com/six-ddc/ccbot)（MIT，約 274 星，2026-07-08）：同路線，只做 Claude Code 與 tmux。

### 第三層：綁單一 agent

- **Claude Code Channels**（官方，research preview）：Telegram、Discord、iMessage 三個 plugin，需 Bun；`claude --channels plugin:telegram@claude-plugins-official` 啟動；配對碼加 sender 白名單；可轉發 permission prompt。Team／Enterprise 需管理員開 `channelsEnabled`。另有 Remote Control 從 claude.ai 或手機 app 接本機 session。
- **pi**：[pi-messenger-bridge](https://github.com/tintinweb/pi-messenger-bridge)（MIT，約 74 星，2026-05-09 後未動；Telegram、WhatsApp、Slack、Discord、Matrix）、[pi-chat](https://github.com/earendil-works/pi-chat)（官方組織，Apache-2.0，約 401 星，2026-06-05；Discord／Telegram 各頻道一個 Gondolin micro-VM）、pi-telegram、TelePi。
- **Codex**：ChatGPT 手機 app 的 Remote 遙控桌機（見 [[四套-coding-agent-能力差異對照]] client 列）。

## 判讀

三層的差別是「誰持有 session」：第一層由 gateway 起 agent；第二層 session 在你的多工器裡，gateway 只是看得到、按得到；第三層 session 在 agent 自己的 process 裡，channel 是它的 plugin。要「換 agent 不換 gateway」選第一或第二層；要最少元件、且只用一家 agent，第三層官方方案最省事。

## 關聯

- [[Hermes-Agent]]——本頁起點：Hermes 的 messaging gateway 是內含 runtime 的設計，本頁列的是把 gateway 拆出來的替代品。
- [[OpenClaw-與-Hermes-Agent-比較]]——OpenClaw Gateway 的信任域設計在該頁；本頁補它可前置 Claude Code／Codex 的設定事實。
- [[四套-coding-agent-能力差異對照]]——四家 client 型態與 headless 入口在該頁；本頁第二、三層的橋都建在那些入口上。
- [[Herdr-使用方法]]——ccgram 的 herdr 模式對應的本機環境。
