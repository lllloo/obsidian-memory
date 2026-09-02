---
title: Herdr 按鍵設定
description: 把 agent 面板導覽提升為一等公民的 herdr keys 設定，含官方預設未綁 agent 導覽、改設定必須 reload 兩個踩雷點
created: 2026-09-02
updated: 2026-09-02
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - automation
---

# Herdr 按鍵設定

Herdr 是專為 agent 設計的終端多工器（相對於 tmux／zellij），側邊欄可即時看各 pane 內 agent 的狀態。本頁記錄 2026-09-02 對 `~/.config/herdr/config.toml` `[keys]` 區段的一次設定變更與其取捨，同目錄留有 `config.toml.bak` 備份。

## 設計意圖

把**左側 agent 面板的導覽變成一等公民**：數字鍵直跳第 1～9 個 agent，Tab／Shift+Tab 前後循環 agent。代價明確——讓出原本的 pane 循環與 tab 數字直跳。

這是在「pane 是主體」與「agent 是主體」之間選了後者。用 herdr 的前提就是同時盯多個 agent，所以最短的鍵位該給 agent 而不是 pane。

## 變更後的 `[keys]`

| 設定 | 值 | 說明 |
|---|---|---|
| `prefix` | 反引號 | |
| `previous_agent` | prefix+shift+tab | 前一個 agent |
| `next_agent` | prefix+tab | 下一個 agent |
| `focus_agent` | prefix+1..9 | 直跳第 1～9 個 agent |
| `cycle_pane_next` | 空字串 | 停用，把 prefix+tab 讓給 agent 循環 |
| `cycle_pane_previous` | 空字串 | 停用 |
| `switch_tab` | 空字串 | 停用數字直跳 tab，改用預設的 prefix+p／prefix+n 前後切 tab |

## 兩個踩雷點

**一、agent 導覽官方預設全部 unset。** `focus_agent`、`next_agent`、`previous_agent`、`keys.indexed.agents` 開箱都沒綁——**不是鍵位衝突，是根本沒綁**，要自己設才有。少了這一步會誤以為「這個功能不存在」。

**二、改完 `config.toml` 必須 `herdr server reload-config`（或 prefix+shift+r）。** 否則正在跑的實例仍吃舊設定。實際踩過：先前把 `prefix` 改成反引號後按了沒反應，原因就是沒 reload，**不是設定寫錯**——這個誤判很貴，因為它會把人推去反覆檢查一份其實正確的設定檔。

## 關聯

- [[Agent-Harness-Engineering-框架綜述]]——herdr 屬於 harness **之外**的一層：它不介入 agent 的 loop、tools 或 memory，只解決「同時盯著多個 harness 實例」的操作面問題，因此該頁的 harness 定義範疇不涵蓋它。
