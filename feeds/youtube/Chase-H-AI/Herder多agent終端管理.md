---
title: Herder——解決 Claude Code 與 Codex 並用的多終端痛點
description: 開源 terminal multiplexer Herder 用 spaces／tabs／panes 三層與 agent 面板，解決多個 coding agent 同時跑時的組織、監控與持久化問題
created: 2026-07-21
updated: 2026-07-21
source: https://www.youtube.com/watch?v=neK8ydl0Vlk
published: 2026-07-16
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - codex
  - workflow
  - tmux
  - harness
---

## 要解決的問題

同時用 Claude Code 與 Codex（或任何幾種 coding agent 組合）時，桌面上散著六七八個終端：既要同時盯著全部，又要判斷哪個先需要你介入，還可能手滑把正在跑事情的視窗關掉。

Herder 是一個開源的 terminal multiplexer，Mac 與 Windows 皆可用，用來收拾這種混亂。

## Herder 買到的三件事

- **組織**：多個終端集中在一個畫面，左側列出各個 agent，agent-forward 而非單純的終端格子。
- **監控**：直接顯示哪些 agent 正在工作、哪些已完成、哪些卡住——包含視覺上看不到的那些。
- **持久化**：Herder 以 server 形式運作。中途完全退出視窗，工作仍在背景繼續；重開終端輸入 `herder` 即可回到現場，也能從手機或 SSH 接回去。

## 與 tmux／zellij 的差異

- tmux 存在多年，同樣能從單一位置控制所有終端，但**不具備 agent 面板**：無法開箱看出哪個 agent 在跑、哪個等你輸入、哪個結束。這是 Herder 的主要差異點。
- 影片中另提到與 Cmux 相比時，主要差別在持久化，以及 Herder 在 Windows 上很容易使用。

## 安裝

一行指令，可在 herder.dev 或 Herder 的 GitHub 頁面找到；複製貼進終端執行即可。裝完後在終端輸入：

```
herder
```

## 三層結構：spaces / tabs / panes

把它想成資料夾層級：

- **spaces = 專案**，是最高層。可新建、可重新命名（例如一個叫 Chase、一個叫 web design）。不同 space 內的 agent 都會列在左側面板，即使其終端當下不可見也看得到狀態。
- **tabs = space 底下的子資料夾**，等同一般終端的分頁。可自由命名，例如 tab 1 叫 research（裡面跑 Claude 與 Codex）、tab 2 叫 dev server 專門處理開發伺服器。
- **panes = tab 內同時可見的分割區**。右鍵 split right／up／down 就能在同一個 tab 裡並排開 Claude Code 與 Codex，也可 zoom in／out、重新命名。

操作不限鍵盤——滑鼠點選與右鍵選單都能用。

## Herder skill 與 plugin marketplace

- **Herder skill** 教你的 agent 怎麼用 Herder：agent 可以自行在 Herder 裡開新的 pane、建立新的 space，不需要你手動安排版面。安裝同樣是一行指令，連結在 Herder GitHub 的 agent skills 段落。
- 另有一整個 **plugin marketplace**，社群已在上面累積各種 add-on。

## 實際用途：讓 headless 的 agent 互動變可見

影片示範的情境是一個讓 Claude Code 與 Codex 來回審查計畫的 skill：Claude 產出計畫、送給 Codex 當 critic，Codex 列出對計畫的所有意見，Claude 再送回修訂版，反覆迭代直到雙方對齊。

這種流程平常跑在 headless 模式下，你看不到中間發生什麼。要求 Claude 「用 Herder skill 開一個新 pane 顯示來回過程」之後，整段對抗式審查就在右側 pane 即時可見——包含 Codex 給出的 verdict（例如 revised）。

這正是 Herder 補上的空缺：Claude Code 內建的 agent view 很好用，但只在 Claude Code 內有效；一旦跨到 Codex 或 opencode 就失效。

## 持久化與關閉

- 兩個 agent 工作到一半時完全退出終端，工作照跑。重開 PowerShell 輸入 `herder` 即回到現場。只要電腦沒關（筆電闔蓋但仍在執行也算），agent 就能一直跑下去。
- 真要結束時：右鍵 pane → close pane；整個 space 則是右鍵 → close。

## 鍵盤快捷鍵

menu → key binds 可查看全部。設計上與 tmux 類似，採 prefix 模式：先按 `Ctrl` + `B` 進入 prefix，稍待一拍後再按功能鍵。例如說明寫 prefix + V 代表垂直分割，實際操作就是 `Ctrl` + `B` 然後按 V。多數操作也可用右鍵完成。

## 總評

價值集中在三點：跨 harness 的監控、專案層級的組織、以及避免誤關終端的持久化。開源免費，Windows 與 Mac 皆可用。
