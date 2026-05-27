---
title: Claude Design 全景評估
created: 2026-04-30
updated: 2026-05-27
tags:
  - claude-design
  - claude-code
  - design
---

> Claude Design 是 Anthropic Labs 推出的視覺化設計工具，在 `claude.ai/design` 上把 Claude 的生成能力包裝成可互動的 prototype/slide/mock-up 介面，並可一鍵 hand-off 到 Claude Code 接續工程化。但它與 Claude Code 的關係並不對等——對「需要原生 GUI 操作」的人是真補強，對「只要設計成品」的人多半繞得開。本文整合三派立場：原生使用、繞道用 Claude Code、開源 Skill 替代。

## 核心問題

Anthropic 把 Claude Design 拆成獨立產品，補的是 Claude Code 長期最弱的一環：**前端設計**。

但獨立產品意味著：

- 獨立的 weekly usage（與既有訂閱分開計）
- 獨立的 GUI 操作層（draw / comment / edit / share）
- 獨立的 hand-off 機制（要 export 才能進 Claude Code）

這三個獨立性既是 Claude Design 的賣點，也是社群質疑「是不是只是 Claude Code 包裝再賣」的原因。

## 三派立場速查

| 立場 | 主張 | 代表筆記 |
|---|---|---|
| **原生派** | Claude Design 真正的價值不在 one-shot，而在 variants + tweaks 的視覺迭代 | Chase H：快速上手、Masterclass |
| **繞道派** | 同樣的工作流可在 Claude Code 用 Skill + library + parallel agents 複製，且更便宜可控 | AILABS-393：陷阱解析 |
| **開源替代派** | 用開源工具（Huashu Design / Open Design）把 Claude Design 的設計哲學裝進 Claude Code，不被 weekly usage 卡住 | Chase H：Huashu Design、Open Design |
| **混合派** | Claude Design 做設計決策（80–90%）→ hand off 到 Claude Code 工程化收尾 | Chase H：Seedance 動畫網站、Masterclass |

**三派並非互斥**：實務上多數人會混合——重要 landing page 在 Claude Design 試 variants、日常頁面用 Skill 在 Claude Code 跑。

## Claude Design 的真正價值：Variants + Tweaks

一次成形（one-shot）的結果，Claude Design 與 Claude Code 差距已經很小（同 prompt 平起平坐）。**真正拉開的是視覺化 A/B 迭代速度**：

- **Variants（巨觀）**：一次產數種完全不同風格（terminal / editorial / brutalist / synth wave / soft pastel...），在 macro 層挑方向
- **Tweaks（微觀）**：對選中版本即時調整 accent、corner radius、字型、layout、headline——所見即所得，不用重新生成。`Variants` 與 `Tweaks` 是 Anthropic 公告中的用語（當動詞用），社群（尤其 Chase H 系列影片）採用為通行稱呼
- **Custom properties**（官方文件補充，影片摘要未涵蓋）：可在 tweaks window 額外加新的調整旋鈕（dark mode 切換、corner radius、glow slider、color selector）
- **Web capture tool**（官方文件補充，影片摘要未涵蓋）：直接從現有網站抓取元素塞進 prototype，讓 mock 看起來像實際產品

**正確的工作流**：

1. 先跑 variants 選定大方向
2. 鎖定一版後 aggressively 加 tweaks（從 ~5 擴到 ~15）
3. 80–90% 完成度時 hand off 到 Claude Code 收尾

順序反過來（每個 variant 都跑 tweaks）會吃掉大量 weekly usage。

## Usage 經濟：為什麼成本是中心議題

Claude Design 的 weekly usage **與 Claude Code/Chat 訂閱分開計**，且非常吃資源——這是所有立場的爭點。

幾個經驗法則（相對關係，不寫絕對數字）：

- 建立一個 Design System ≈ 吃掉週額度的五分之一以上，所以**只在確定要大量沿用某品牌時才建一個**
- Variants + tweaks + mobile 轉換都會咬額度，越早做越好（最後微調留給 Claude Code）
- 高 plan 用戶實測下 20 次左右迭代就可能耗光週額度
- 完整跑一次「圖 → Design → 影片 → hand-off」的流程，外加成本約幾美元等級

**反方派的核心攻擊點**就在這：當 designer 需要大量試錯，週額度就是上限。**繞道派的對策**是用 Claude Code 跑同樣工作流，吃的是相對寬鬆的 Claude Code 額度。

## 決策：什麼時候選哪個

| 你的情境 | 建議 |
|---|---|
| 需要 GUI 操作（在畫布上 draw 註解、團隊 review、comment 批次送） | **Claude Design 原生** — Skill 替代不了真實 GUI |
| 已有 design system 或品牌模板要重複沿用 | **Claude Design** — 預載 design system 是它的強項 |
| 想在 5–10 個 variants 之間視覺挑選 | **Claude Design** — 視覺化 A/B 是它最值錢的能力 |
| 要產出可上線 code、不只是 prototype | **Claude Code**（或 Claude Design hand-off 後接 Claude Code） |
| 要 git workflow（branching / revert / parallel agents） | **Claude Code** — Claude Design 的 GitHub 整合僅讀取參考 |
| 高頻迭代、實驗多種設計、額度敏感 | **Claude Code + Skill**（front-end design skill / Huashu / 自製） |
| 已有 codebase 要在現站疊加新區塊 | **Claude Code** — 不必從零開始 |
| 純設計師、不熟 terminal | **Claude Design 原生** |

## 繞道派的實作策略（在 Claude Code 上覆刻 Claude Design）

當決定不走原生 Claude Design，繞道派的工具組：

### 1. 問答式設計流（Skill 化）

Claude Design 最有效的特色之一是**先問 10–15 題澄清需求再開工**。Claude Code 裡用一個 Skill 就能複製：

- Skill 內含問題庫、follow-up 觸發條件、不同類型網站的 layout 草稿
- 在 prompt 結尾加一句 `Ask me any questions before you begin.` 也能在 Claude Design 端觸發類似 plan mode

### 2. 用設計 library 而非純生成

避免「一看就是 AI 做的」感的關鍵：靠成熟元件而非靠模型憑空生 SVG/CSS。

- **Lenis**：production 級滾動套件
- **GSAP**：主流動畫函式庫，能做沉浸式互動
- **Shadcn / Aceternity / Hero UI**：UI library，已內建大量動畫，模型可以專注整體設計
- **Shadcn MCP**：agent 自動安裝對的元件

詳見 [[GSAP-與-Lenis-捲動動畫分工]]。

### 3. Parallel agents + git worktree（覆刻 variants）

這是繞道派最強的一招：

- 用多個 sub-agent 在獨立 worktree 各做一個變體
- 同時得到多種設計，挑最喜歡的合進 main、其餘刪掉
- 比 Claude Design 的 variants 更可控、可 revert、可組合

詳見 [[Claude-Code-多-Agent-協作]]。

### 4. 開源 Skill 直接包入

**Huashu Design**（開源 Skill）把 Claude Design 的 system prompts、設計哲學、components/assets 庫、HTML→MP4 toolchain、Playwright 渲染驗證打包成單一 Skill，吃 Claude Code 的訂閱額度。

實測三輪頭對頭比對中，Test 1（從零生成）與 Test 3（簡報）結果接近；Test 2（套既有 design system）Claude Design 整體略勝（預載 design system 是它的強項）。整體上 Huashu Skill 在不需 GUI 的場景已可替代，且 token 用量低一個數量級。**真空比較 Claude Design 仍勝**（GUI 是 Skill 永遠做不到的），但對「只要拿到設計成品」的人已經夠用。

**Open Design** 是另一個開源克隆，與 Huashu 的關鍵差別在它**帶 GUI**（Huashu 只有 terminal），核心價值同樣在建 prototype / slide deck（與 Claude Design 機制幾乎相同），並可額外掛 media providers 做 image / video 生成（Claude Design 沒有）。但它**無原生上傳 design system 介面**，要繼承既有品牌得繞 Claude Design 出口或讓 agent 讀資料夾仿造——反而比 Huashu「terminal 直接讀整個資料夾繼承風格」綁手。定位取捨：**要 GUI 又被 usage 卡 → Open Design；要更彈性、更快、能直接繼承資料夾 → Huashu**。Image / Video templates 分頁多屬 bloat。

## 進階工作流：動畫 Hero 網站（混合派代表流）

Chase H 的 Seedance 動畫網站影片給的是當前最務實的混合工作流，固定五步：

1. **Nano Banana Pro**（Higgsfield）出靜態起始圖——構圖先行，決定 hero 留白與文字位置
2. **Claude Design**：把圖 + Dribbble 參考一起丟，跑 variants → 鎖一版 → 狂開 tweaks
3. **Seedance 2.0**（Higgsfield）把同一張圖轉 15 秒 hero 背景影片
4. **Claude Design**：上傳 MP4 替換 hero 背景
5. **Hand off Claude Code**：用 Download zip 而非 copy（避免 MP4 漏抓），解壓後拖進 Claude Code 跑 dev server，git commit、Vercel 部署

關鍵原則：

- **構圖比 prompt 重要**：先決定版面再下 prompt（沒靈感先去 Dribbble 拆解）
- **動作極小**：hero 影片要像 low-key GIF，不是電玩動畫；Prompt 範例：「clouds barely moving, embers from the fire, his hands slowly drifting」
- **桌面用影片、手機用靜態圖**：避免 mobile 體驗被大影片拖垮
- **Seedance 設定**：15 秒、16:9、≥1080p、關掉 enhance prompt（要完整控制）、預期重抽 4–5 次
- **替代影片模型**：Kling 3.0、VO 3.1（社群實測當前 Seedance 2.0 略勝）

## 共識點

不論立場，五篇都同意：

- **Claude Design 的 one-shot 結果 ≈ Claude Code（Opus high effort）**——拉開差距的不是工具本身
- **Claude Design 的 GitHub 整合僅讀取參考**，不做 commit/branch；要 git workflow 必須回 Claude Code
- **80–90% 完成就 hand off**——剩下的 10–20% 留給 Claude Code 工程化更便宜可控
- **Variants + tweaks 是 Claude Design 唯一無可取代的賣點**（GUI 操作層）
- **Usage 經濟是核心議題**：所有人都同意 weekly usage 燒得很快，分歧只在「值不值」

## 分歧點

| 問題 | 原生派 | 繞道派 |
|---|---|---|
| 「Claude Design 是新工具還是 Claude Code 包裝？」 | 新工具，GUI 與 variants 不可替代 | 包裝，能力差距來自模型升級而非工具 |
| 「Designer 該切換到 Claude Design 嗎？」 | 該，視覺迭代速度有質變 | 不該，被週額度卡住、無法疊在現有 codebase 上 |
| 「scroll-interactive 那些炫技 demo 多酷？」 | Claude Design 微互動加分 | 多半是 video 背景 + 模板，任何 agent 都能跑 |

## 外部來源

來自 Inbox/YouTube 的影片摘要：

- Chase H — [Claude Design 快速上手導覽](https://www.youtube.com/watch?v=-tGH2tLwCEw)
- Chase H — [Claude Design Masterclass 深度指南](https://www.youtube.com/watch?v=iJRq1kLLRmY)
- Chase H — [Claude Design + Seedance 2.0 動畫網站](https://www.youtube.com/watch?v=7uW1SKmx-Ic)
- AILABS-393 — [Claude Design 其實是個大坑](https://www.youtube.com/watch?v=GbuwosWEvHo)
- Chase H — [Huashu Design 開源版實測](https://www.youtube.com/watch?v=Nmk1wxoi6ys)
- Chase H — [Open Design 開源 Claude Design 替代](https://www.youtube.com/watch?v=BGQ9i3fvNds)

相關主題：

- [[Claude-Code-前端設計工作流]]（既有 Topics/UI設計/）
- [[GSAP-與-Lenis-捲動動畫分工]]（既有 Topics/前端技術/）
- [[Claude-Code-多-Agent-協作]]（既有 Topics/Claude-Code/，parallel agents 細節）
- [[Claude-Code-Skills]]（既有 Topics/Claude-Code/，Skill 通用規格）
