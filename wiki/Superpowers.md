---
title: Superpowers
description: obra 的 agentic skills 框架：SessionStart 注入機制、無官方開關的維護者立場、小需求放行的版本分水嶺與官方 marketplace 版本落後成因
created: 2026-10-15
updated: 2026-10-15
source: https://github.com/obra/superpowers
published: ""
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - agent-framework
  - claude-code
  - skill
---

`obra/superpowers` 是一套 agentic skills 框架：brainstorming → spec → 實作計畫 → subagent-driven development，內建 TDD、systematic debugging 等紀律 skill。選型定位與 README 層描述見 [[長跑-Agent-的目標定義與計畫工具]]；本頁補的是該頁標為「未核實」的**機制實作**與**使用面的可調性**。

> 證據強度：本頁主張除另標者外，皆為 2026-10-15 以 `gh` 直讀 GitHub 一手來源（repo 檔案、issue／PR 本文與維護者留言、release tag sha）＋本機外掛快取實查；未做跨 harness 實測。

## 注入機制：SessionStart hook

- `hooks/hooks.json` 只註冊一個 `SessionStart` hook，matcher 為 `startup|clear|compact`——每次開 session、`/clear`、壓縮後都會重新注入。
- `hooks/session-start` 把 `skills/using-superpowers/SKILL.md` **全文**包進 `<EXTREMELY_IMPORTANT>` 當 `additionalContext` 注入。全文核心是「有 1% 可能適用就 ABSOLUTELY MUST invoke」與 Red Flags 表。
- 腳本內**沒有任何跳過條件**（無 env var、不讀 settings），只依宿主（Claude Code／Cursor／Copilot CLI／Muse）切輸出格式；`claude plugin configure` 亦回報此外掛無可設定選項。
- 這條 1% 規則管的是**所有外掛的所有 skill**，不只 Superpowers 自己的（[#2299](https://github.com/obra/superpowers/issues/2299) 的實例：無關的 `deploy` 字眼被當成 Airflow skill 的強制觸發）。

社群對此的批評集中在「現行 Claude 模型照字面執行，導致一行小事也叫流程 skill」：[#2377](https://github.com/obra/superpowers/issues/2377)（開著，有對照實驗留言）、[#2487](https://github.com/obra/superpowers/issues/2487)（以 completed 關閉，但 v7.0.0 tag 的 `using-superpowers/SKILL.md` 第 11 行 1% 措辭仍在）、[#2514](https://github.com/obra/superpowers/issues/2514)。

## 能不能關：沒有官方開關

**維護者立場（拍板）**：on/off 開關已多次被拒——[#938](https://github.com/obra/superpowers/issues/938) obra 答「不是外掛自己能控制的，Claude Code 本身能開關外掛」；[#951](https://github.com/obra/superpowers/issues/951)、[#1501](https://github.com/obra/superpowers/issues/1501) 以重複關閉，維護者 arittr 指出**官方支援路徑是直接叫 agent 別用，或寫進 CLAUDE.md**。加 `SUPERPOWERS_SKIP_SESSION_CONTEXT` env var 的 [PR #1006](https://github.com/obra/superpowers/pull/1006) 已關閉未合併。obra 另開的可設定性總追蹤單 [#2398](https://github.com/obra/superpowers/issues/2398) 收的是寫入路徑、流程參數、擴充 hook 點，**不含**關閉注入。

**實際可用的手段**（由硬到軟）：

| 手段 | 效果 | 代價 |
|---|---|---|
| `claude plugin disable superpowers@claude-plugins-official`（`--scope user／project／local`） | 整個外掛停用，含 skill | 要用時得再 enable；且見下方 hook 殘留疑慮 |
| 全域 `disableAllHooks: true` | 注入停止 | 連使用者自己與其他外掛的 hook 一起關，通常不可接受 |
| 清空快取中的 `hooks/hooks.json` | 只關注入、保留 skill | 外掛更新會裝成新版本目錄，hook 自動回來 |
| 本地 fork 成自有 marketplace、刪 `hooks/` | 只關注入、`superpowers:` 命名空間不變 | 失去自動更新，需自行同步上游 |
| 把 skills 搬進個人 skills 目錄 | 只關注入 | 失去 `superpowers:` 前綴，skill 間互相引用對不上，不建議 |
| CLAUDE.md 寫啟動條件（官方支援路徑） | 注入照舊，靠指示優先序壓制行為 | 每 session 仍付注入 token |

**hook 殘留疑慮（狀態不明）**：Claude Code 端曾有「`enabledPlugins` 設 `false` 後外掛的 SessionStart hook 仍觸發」的回報（[anthropics/claude-code#41919](https://github.com/anthropics/claude-code/issues/41919) 以 NOT_PLANNED 關閉、[#59496](https://github.com/anthropics/claude-code/issues/59496) 標重複）。NOT_PLANNED 可能只是過期自動關閉，**是否已修未查證**——停用後開新 session 看開頭是否仍有 "You have superpowers." 即可確認。

## 小需求能不能直接改：版本分水嶺

這是行為關鍵的版本差異，故保留版本號（來源：各版 tag 的 `skills/brainstorming/SKILL.md`）。

- **v6.3.0–v6.4.x：三路分流仍要核准。** 來自 [#2063](https://github.com/obra/superpowers/issues/2063) 的 Spike／Bounded／Architectural 路由。小改動歸 Bounded：不寫 spec、不寫 plan 文件，但必須先在對話中給簡短設計並**停下等使用者說 yes**，檔案明寫「approval is as hard a gate as an architectural one」；加上「拿不準就走較重路徑」與「This is too simple to need a design」紅旗，小需求易被拖慢。三路路由前的極端案例見 [#2079](https://github.com/obra/superpowers/issues/2079)（一段規則修改產出 3,061 行、約 10 小時）。
- **v7.0.0 起：需求完整就直接做。** brainstorming 第一步改為自問「我對對方要什麼知道多少」——需求本身已含所有要素（例：「把 icon 改成 cornflower blue」）即為 quick, clear task，「Do it, and say what you did」；缺要素才開始對話，且第一則訊息須告知「想跳過提問直接開工就說一聲」，對方說了 brainstorming 即結束。
- 注意：bootstrap 的 1% 規則在 v7.0.0 仍在，所以 brainstorming 仍會被叫起來，差別是叫起後對小需求放行。僅核對了 brainstorming 與 using-superpowers 兩檔，v7 其他 skill 的變動未查。

## 官方 marketplace 為何落後上游

- `anthropics/claude-plugins-official` 的 `marketplace.json` 以 **commit sha 釘選**每個外掛；作者發新版不會自動傳到使用者端。
- 更新靠 `github-actions[bot]` 驗證（`claude plugin validate`）後開 bump PR，PR 說明明寫「not auto-merged by default」，需 Anthropic 人工審核合併。Superpowers 歷次 bump（如 [#5253](https://github.com/anthropics/claude-plugins-official/pull/5253)）都走此流程。
- 該 repo 曾停用每夜 bump workflow，改由員工分批手動追版本（[#6284](https://github.com/anthropics/claude-plugins-official/pull/6284) 說明）；落後幅度因此可能拉長。
- OpenAI 端同理：Codex 版落後時 obra 回「There's a manual review process on the OpenAI side」（[#1790](https://github.com/obra/superpowers/issues/1790)）——作者自己也只能等。
- **狀態快照（2026-10-15）**：官方 marketplace 釘在 v6.4.1（sha `5bf4e78`），v6.4.2 未曾上架（推斷為手動追版空窗期被略過，無明確紀錄）；bump 到 v7.0.0 的 [#6565](https://github.com/anthropics/claude-plugins-official/pull/6565) 10/13 開出、`REVIEW_REQUIRED` 待審。GitHub 上未見其他使用者抱怨此落差。此快照會過期，自行確認方式：

```bash
# 官方 marketplace 目前釘的 sha
gh api repos/anthropics/claude-plugins-official/contents/.claude-plugin/marketplace.json --jq .content \
  | base64 -d | jq '.plugins[] | select(.name=="superpowers") | .source.sha'
# 某 release tag 對應的 sha
gh api repos/obra/superpowers/commits/<tag> --jq .sha
```

合併後才跑 `claude plugin marketplace update claude-plugins-official` → `claude plugin update superpowers@claude-plugins-official`；未合併前跑了不會有變化。

## 其他

- 非官方精簡分支 [Superpowers Lite](https://github.com/nanyumeng/superpowers-lite)（以 v6.1.1 為基底的 skills overlay），未評估品質。
- 外掛在 `hooks/hooks.json` 用 `${CLAUDE_PLUGIN_ROOT}`、`SKILL.md` 正文則用裸相對路徑，屬 [[Agent-Skill-腳本路徑的規範與實況]] 統計中的 plugin 型樣本。
