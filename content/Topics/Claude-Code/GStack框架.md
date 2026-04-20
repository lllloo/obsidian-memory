---
title: GStack 框架
created: 2026-04-20
updated: 2026-04-20
tags:
  - claude-code
  - agent-framework
  - planning
---

Y Combinator CEO **Garry Tan** 開源的 Claude Code 完整工具包（23+ skills）。把 Claude Code 轉成虛擬軟體開發團隊，包辦從規劃、設計、開發到 QA、部署的全流程。涵蓋是什麼、23+ skills 清單、規劃管線（planning pipeline）、五層機制、與其他框架的位置、常見陷阱。

## 核心概念

**GStack** 是 Garry Tan（YC CEO）公開的自用 Claude Code 配置，GitHub `garrytan/gstack`，MIT 授權，累積 **66K+ stars**。

與 Superpowers、GSD 不同的是：GStack 的本體是 **CLAUDE.md + 23+ skills** 的組合，**安裝就是把一組 Markdown skill 檔與 compiled binary 放進 `~/.claude/skills/gstack/`**，沒有 SaaS 依賴、沒有 telemetry、沒有 vendor lock-in。

支援 Claude Code 以及其他七個 AI coding agent。

## 23+ Skills 一覽

分六類：

| 類別 | Slash commands |
|------|----------------|
| **Planning** | `/office-hours`、`/plan-ceo-review`、`/plan-eng-review`、`/plan-design-review`、`/plan-devex-review` |
| **Design** | `/design-consultation`、`/design-shotgun`、`/design-html`、`/design-review` |
| **Development** | `/review`、`/investigate`、`/autoplan` |
| **QA** | `/qa`、`/qa-only` |
| **Deployment** | `/ship`、`/land-and-deploy`、`/canary`、`/document-release` |
| **Utilities** | `/browse`、`/cso`（security）、`/codex`（second opinion）、`/pair-agent`、`/careful`、`/freeze`、`/guard`、`/learn` |

下節聚焦最常被社群討論的 **planning pipeline** 與 **design-shotgun** 兩組。

## Planning Pipeline（收斂 MVP）

規劃階段用三個 skill 串接，每個 skill 跑在獨立 Claude Code session，保持乾淨 context。

### Office Hours（定義問題）

1. 多個 sub-agent 理解 codebase、data model、service
2. 框架設定：是否能複製其他專案的 coding pattern、專案階段（ideation / 有付費用戶 / hackathon）
3. 依階段追問關鍵問題（有付費用戶情境的例子）：
   - 這週就能交付的最小版本是什麼
   - 用戶做了哪些設計者沒預期到的事
4. **Market research**（對該功能領域的競品分析）
5. **Phase 3 — 挑戰前提**：列出 6 個 premise 逐條要求確認
6. **Phase 3.5 — Cross Model Second Opinion**：啟動沒看過對話歷史的獨立 sub-agent，只看 problem statement / key answers / premise / landscape 給第二意見
7. **Phase 4 — Alternative Generation**：提出多技術方案並評估
8. 輸出 design doc 到根目錄 `.md`

> 常見模式：Claude 對用戶說「這不是 wedge，這是 platform」並 push back，要求挑出最能製造 word of mouth 的單一功能（社群實測）。

### Plan Reviews（多 persona 審查）

用 `/autoplan` 串接，或分別啟動：

- `/plan-ceo-review` — 整體架構、專案可行性
- `/plan-design-review` — 設計
- `/plan-eng-review` — 工程
- `/plan-devex-review` — DX
- 搭配 `/codex` 提供獨立 second opinion

實測結果（brownfield 上規劃新功能）：共 **41 findings**（CEO 10、Design 15、Engineering 16），22 個決策自動下定，其餘標記需用戶決策（社群實測）。

### Design Doc 到 Spec（技術決策細化）

在規劃末端對 design doc 逐項追問技術決策，典型項目：

- Chat UI 擺放：dedicated page / slide-out panel / floating widget
- Conversation context 長度：5 / 10 / session only / single query
- 資料 aggregation：Postgres RPC vs ORM backend service layer（考量未來換 DB 的 migration 成本）
- Table UI：inline markdown、筆數限制、預設收合、過多記錄時先追問澄清
- Credits 計費、edge case（空資料引導匯入、模糊查詢要求澄清、跨幣別分開顯示、rate limit）

## Design Shotgun Pipeline（視覺迭代）

`/design-shotgun` 的流程：

1. 用戶描述想要的頁面 / 元件
2. 平行生成 **4–6 個 AI mockup variants**（以 GPT Image 產生）
3. 瀏覽器開 comparison board，所有變體並列
4. 用戶挑喜歡的、留口頭 feedback（例：「more whitespace」、「bolder headline」、「lose the gradient」）
5. 依 feedback 生成下一輪
6. 反覆直到定稿；幾輪後 **taste memory** 會開始偏向用戶的偏好

搭配 `/design-html` 轉 HTML、`/design-review` 審查。

## 五層機制（Persona 不漏軌）

確保各 persona sub-agent 不破壞角色設定：

1. **Role Focus** — 戴上眼罩，只看自己職責範圍（code style 是工程師的事，QA 不管）
2. **Data Flow** — 工作建立在前一階段輸出之上（QA 接收 Reviewer 結果）
3. **Quality Control** — 各角色完成項目的 checklist
4. **Boil the Lake** — 只做能 100% 完成的事，能燒小湖（職責內）不去燒大海
5. **Keep it Simple** — 結論只說三件事：發現了什麼 / 為何重要 / 下一步是什麼

## Token 成本（planning pipeline）

| 階段 | 消耗 |
|------|------|
| Office Hours | 170K |
| 技術決策細化 | 200K |
| Plan Reviews（autoplan） | 200K |
| **合計** | **~600K** |

在 brownfield 專案規劃一個新功能的規劃階段成本。執行、QA、部署不計入。

## 在三框架中的位置

| 面向 | GStack | Superpowers | GSD |
|------|--------|-------------|-----|
| 範圍 | **完整 toolkit**（plan / design / QA / deploy） | 實作 TDD workflow | Orchestration CLI |
| 約束目標 | 視角（Perspective） | 流程（TDD） | 環境（fresh context per task） |
| 擅長階段 | **策略規劃、設計、QA、發佈** | 實作 TDD | 專案管理、里程碑 |
| 對需求的處理 | **主動 push back、強制收斂** | 依 spec 直做 | 研究＋驗證 |
| 部署形態 | ~/.claude/skills 下的 MD + binary | Claude plugin | standalone CLI |

詳細對比見 [[Superpowers框架]]、[[GSD框架]]。

## 安裝

約 30 秒：

1. 在 Claude Code 貼 git clone 指令，安裝到 `~/.claude/skills/gstack`
2. 執行內建 setup script
3. 把 GStack 的配置更新到專案的 `CLAUDE.md`
4. 多人協作可選 `./setup --team`

MIT License，可 fork 與自訂 skill。

## 組合使用：Power Stack

依開發階段串接（社群策略）：

```
策略規劃 → GStack planning pipeline（CEO / Eng / Design review 驗證架構）
視覺迭代 → GStack /design-shotgun（多方案並列挑選）
執行規劃 → GSD（拆分里程碑，fresh context per task）
實際執行 → Superpowers（TDD，先測試再寫程式）
QA 收尾  → GStack /qa（Playwright UI 測試）
部署     → GStack /ship、/land-and-deploy、/canary
```

## 何時該用

- **適合**：有付費用戶的 SaaS 新功能規劃、brownfield 專案加新模組、需要把發散 idea 強制收斂成 MVP、需要跨 session 的一致性（CLAUDE.md 驅動）、完整開發生命週期管理
- **不適合**：極簡 side project（600K token 規劃過於昂貴）、需求已完全鎖定（planning pipeline 無用武之地）

## 常見陷阱

**規劃完不接執行框架**
- 徵兆：design doc 寫完放著不動
- 原因：GStack 的 planning skills 只負責到 spec
- 解法：規劃末尾記下 handoff prompt，開新 session 接 Superpowers（Garry 本人推薦）或 GSD

**Phase 3.5 被省略**
- 徵兆：design doc 看起來完善但藏著同 session 的盲點
- 原因：Cross Model Second Opinion 是單獨步驟，容易被跳過
- 解法：強制用 `/codex` 啟獨立 sub-agent 審查

**把「boil the lake」當口號**
- 徵兆：Persona 跨出職責亂給建議（QA 管 code style）
- 原因：五層機制中的 Role Focus 未落實
- 解法：審查 sub-agent prompt，檢查是否只看該 persona 該看的資料

**安裝後不更新 CLAUDE.md**
- 徵兆：slash command 可用但 agent 行為沒變
- 原因：GStack 的核心是 CLAUDE.md 驅動 persona，skill 只是觸發入口
- 解法：依官方 README 把 GStack 配置段貼進專案 CLAUDE.md

## 來源

**官方 / 開發者**
- [garrytan/gstack (GitHub)](https://github.com/garrytan/gstack) — Garry Tan (YC CEO), MIT License
- [gstacks.org](https://gstacks.org/) — 官方介紹頁

**影片 / 社群**
- https://www.youtube.com/watch?v=6kM27uGP4n4
- https://www.youtube.com/watch?v=bzutStZJ1Ig
- [GStack on Hacker News](https://news.ycombinator.com/item?id=47355173)
