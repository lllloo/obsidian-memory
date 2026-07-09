---
title: tmux 讓背景行程在連線斷後續跑
created: 2026-06-16
updated: 2026-06-16
tags:
  - tmux
  - cli
  - terminal
  - devops
---

在雲端開發環境（如 Coder）的「網頁 Terminal」裡跑 `quasar dev` 這類長駐 dev server，掛一段時間後會無故失效。根因是行程的生命被綁在「你正在看的那條連線」上；用 tmux 把行程交給背景 daemon 持有，就能在連線斷掉後續跑。

## 為什麼網頁 Terminal 一斷線行程就死

網頁 Terminal 是瀏覽器透過 WebSocket 連到 workspace 內一個互動式 shell session。`quasar dev` 是這個 session 的 child process，與 session 綁在同一個 PTY。當 WebSocket 斷線（關分頁、電腦睡眠、網路斷、閒置 timeout）→ PTY 關閉 → 系統對掛在該 PTY 的行程送出 SIGHUP → `quasar dev` 預設收到 SIGHUP 就結束。

## 為什麼 tmux 能讓行程持續

真正擁有行程的不再是你的 terminal，而是常駐在 workspace 背景的 `tmux server` daemon。網頁 terminal 只是臨時接上的 tmux client。`quasar dev` 跑在 tmux server 維護的、屬於 server（不屬於你連線）的獨立 PTY 上。WebSocket 斷線時只是 client 被 detach，server 與其 PTY 不受影響、不發 SIGHUP，行程照跑；重連後 `tmux attach` 再接一個 client 回去，畫面與 log 都還在。

## 常用指令

- `tmux new -s dev`：建 session（名稱 dev）
- 在 session 裡跑 `quasar dev`
- `Ctrl+b` 然後 `d`：detach，離開但行程續跑
- `tmux ls`：列出 session
- `tmux attach -t dev`：重連接回
- `tmux kill-session -t dev`：砍掉 session
- 若 `tmux new -s dev` 報 `duplicate session: dev`，代表 session 已存在，改用 `tmux attach -t dev`

## 重要限制

tmux 只能擋「連線斷線」這種死法。若 Coder 的 autostop（閒置自動停機）把整台 workspace 關掉，tmux server 一起被關，行程一樣會沒——那要靠調 workspace 的 autostop TTL 設定，不是 tmux 能救的。

## 回查線索

專案 ps-contract-analysis-page、Coder（coder/coder）網頁 Terminal、quasar dev、SIGHUP、PTY、autostop。