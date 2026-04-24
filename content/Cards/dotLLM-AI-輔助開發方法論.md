---
title: dotLLM — AI 輔助開發方法論的大型驗證
created: 2026-04-24
updated: 2026-04-24
source: https://kokosa.dev/blog/2026/dotllm/
published: 2026-04-14
tags:
  - claude-code
  - ai-coding
  - workflow
---

## 為什麼這個案例值得記

一個資深 .NET 開發者（Konrad Kokosa）用 Claude Code + Codex + Gemini，**兩個月單人**做出 dotLLM——純 C#/.NET 10 從零實作的 LLM 推論引擎（GGUF loader、SIMD kernels、CUDA backend、OpenAI 相容 API、Chat UI）。CPU decode 達 llama.cpp 的 66-88%。

這不是小專案 demo，是驗證了「**結構化文件 + 多 agent 分工**」這套方法論能 scale 到 systems-level 工程。跟我在 `obsidian-memory` 做的工作流同構，但規模大一個量級。

## 可直接借鏡的做法

### 1. 文件即方法論，不是 overhead

他最高 ROI 的投資是 `ROADMAP.md` + `CLAUDE.md`：

- **ROADMAP.md**：60 個實作步驟 / 7 個 phase。每步有 feature 名、描述、要改的檔案、依賴的上游步驟
- **CLAUDE.md**：180+ 行的專案「憲法」，定義架構原則（native .NET、NativeMemory 不用 managed array）與硬性規則（SIMD 必有 scalar fallback）
- **22 份 `/docs/` 設計文件**：每個子系統一份（ARCHITECTURE、QUANTIZATION、ATTENTION、CUDA…），規則是「AI 在動某模組前先讀該模組的 spec」

關鍵體會：**寫 ROADMAP 的過程強迫他先做完架構決策**。等於用寫文件代替白板會議。

### 2. 寫 code 的 AI 不要同時 review code

三個模型分工：

- **Claude Code (Opus 4.6)**：實作
- **Codex + Gemini**：PR review（在 PR 留言裡 `@codex` / `@gemini` 觸發）

實際抓到的不是 cosmetic bug，是 **ring-buffer indexing bug、race condition、cache key collision、CUDA kernel 的 thread underutilization**——會直接 ship 出去的炸彈。他強調「**不同模型盲點不同，Codex 跟 Gemini 幾乎不會 flag 同一個問題**」。

### 3. 六個 Claude Code skills 自動化 PR 生命週期

- `/plan-step` — 讀 ROADMAP + 相關 docs，進 plan mode 產計畫，**等人核准才寫 code**
- `/create-pr` — commit、push、開 PR
- `/apply-pr-comments` — 讀 review 留言，進 plan mode，**等人核准才改**
- `/finish-pr-comments` — 改完推上去、對每條 review 留言回覆「已修，commit hash XXX」
- `/merge-pr` — squash merge、刪 branch、切回 main
- `/plan-issue` — 從 issue（而非 roadmap step）起頭的變體

閉環可追溯：Codex 找到 bug → Claude 修 → reply 附 commit hash。**PR thread 自己就是 audit trail**。

### 4. 拒絕 YOLO loop

他明確表態不用 Ralph Wiggum 之類的 fire-and-forget。每個 plan 都要人核准。理由是「我想 **drive** 工作，不是燒 token」。單一任務幾分鐘到 30-40 分鐘，剛好是喝咖啡等其他東西的長度。

## 反面教訓（AI 會在哪裡卡住）

- **架構級決策**：選哪種 attention、GPU interop 怎麼切、PagedAttention vs staging-buffer gather——這些要人看過 llama.cpp / vLLM / 論文才能判斷。AI 能照架構實作，不擅長選架構
- **踩到平台硬限制會卡死**：prefill 慢 2-5x 的原因是 AVX2 outer-product tiled matmul 需要 23 個 YMM 暫存器，但 AVX2 只有 16 個，RyuJIT spill 到 stack 吃掉所有增益。AI 很會診斷（看 JIT disasm、逐一試 tile size），但跨不過語言 runtime 限制
- **守不住自己訂的規則**：他 CLAUDE.md 裡強調不要 compound tool call（`cd XXX && git ...`），Claude 三不五時還是會寫——最後他的結論是「**需要 pre-tool hook**」。這點跟我在 obsidian-memory 用 `scripts/vault-check.mjs` 兜底 agent 漏網的邏輯一樣：**不要指望 prompt，要在執行路徑上加閘門**
- **偶爾會卡住好幾小時在 loop 裡**：2-3 次 Claude 自己鬼打牆試錯幾個小時才通——驚人的是最後真的通了。代表深度 stuck 時**人要進來 brainstorm，不是加更多 prompt**

## 金句

> AI amplifies discipline; it doesn't replace it.
> （AI 放大紀律，不取代紀律。）

## 對自己工作流的啟示

- `obsidian-memory` 的 `content/CLAUDE.md` + `scripts/vault-check.mjs` + `.claude/agents/` 就是小型版本。dotLLM 驗證了同樣模式能撐到 60 步 / 兩個月 / 跨 CPU+GPU+server+UI 的規模
- 「**寫 code 的 AI 不要 review code**」這點以前沒明確做過，以後跨模型 review 可以當慣例。現在 vault 的 `vault-auditor` 是 subagent 自審，之後多 agent 稽核（例如換個模型跑 dry-run）可以考慮
- **pre-tool hook 勝過 prompt**：我已經在做（`scripts/vault-check.mjs` 擋敏感資料），但可以再往前推——寫入前 checklist 能自動化的部分都應該 hook 掉
