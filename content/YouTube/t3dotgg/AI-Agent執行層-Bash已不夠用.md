---
title: AI Agent 執行層：Bash 已不夠用
tags:
  - youtube
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-07
source: https://www.youtube.com/watch?v=TilDSWeiAlw
---

## 核心論點：Bash 是過渡期解法

AI coding agent（Cursor、Claude Code、Codex CLI）目前透過 bash 操作系統，但 bash 只是一個「重要的踏腳石」，不是終點。問題在於：

- 無標準定義哪些操作具破壞性
- 無法共享已批准的指令（每個 agent 獨立）
- 持續詢問用戶審核讓人麻木，最終大家乾脆開 dangerously skip permissions
- 無法做到 wildcard 批准、細粒度權限控制、跨 agent 共享簽入狀態

## 為何大量 context 有害

- LLM 本質是「超強自動補全」：context 越多，下一個 token 越難預測正確
- 把整個 codebase 塞進 context（如 Repo Mix）是最差做法：花費倍增、回應品質下降
- 現代做法：讓 model 用 bash 寫 grep 指令找到它需要的那幾十行 code，而非丟入整個 repo
- 這讓 token 從 100k+ 降至 40 以內，效果從「非確定性賭博」變成「接近確定性」

## Tokenization 與脈絡管理

- 新版 tokenizer 針對 code 優化，同一段 code 的 token 數大幅減少
- 舊版：空格各自是一個 token；新版：可視語意分組
- 同語言的 context 讓 model 更易生成同語言輸出（context 決定輸出傾向）

## Bash 工具的真正意義

Bash 的強大在於它是「單一工具」——不需給 model 幾十個細分工具（edit、rename、move、check 等），只要一個 bash，model 就能用它做一切。給 model 太多工具反而讓 Gemini 之類的 model 全部亂用。

> Bash 不只是個工具，它是第一個「執行層」（execution layer）的引入。

## 下一代執行層：TypeScript

Cloudflare 的 Code Mode 與 Vercel 的 just-bash 已在探索以 TypeScript 取代 bash 作為執行環境：

- TypeScript 有型別，可定義哪些操作是破壞性的
- 可在 V8 isolate / Cloudflare Workers / Node 中執行，不需要每個 agent 有獨立 VM
- 多用戶隔離：每個用戶的 FS 操作只在自己的 isolate 內，不能跨用戶存取
- just-js：讓 model 寫的 fs 操作永遠只在 RAM 中執行，不碰真實 kernel

好處：
- 型別安全：可用型別系統表達「此操作需要用戶確認」
- 可攜帶：一個 TypeScript 檔案描述 agent 的執行環境，可共享給整個團隊
- Cloudflare 的 Code Mode 測試顯示，平均 token 從 43,500 降到 27,000（減少 40%），準確率也提升

## 現況與展望

- Dax（open code 作者）正在實驗完全移除 bash tool，改用 JS 執行
- just-bash（Vercel 的虛擬 bash）、Rivet、Sandbox 等新公司都在解決這個問題
- 執行層的標準化、共享、安全隔離，仍是「完全開放問題」——這代表有巨大機會

> "Every single thing around us was made by a person just like you or me based on their understanding of the world." — Steve Jobs
