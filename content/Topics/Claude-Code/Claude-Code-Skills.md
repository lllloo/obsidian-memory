---
title: Claude Code Skills
created: 2026-03-29
updated: 2026-04-24
tags:
  - claude-code
  - ai-tools
---

Claude Code 的 Skills 主題 MOC，整理 Agent Skills 的核心概念、Claude Code 的實作差異、建立方式與常見坑。

## 先分清兩個語境

這個主題很容易把兩層東西混在一起：

- **Agent Skills 通用規格**：Anthropic 文件與 [Agent Skills open standard](https://agentskills.io/) 談的是這一層。重點是 `SKILL.md`、progressive disclosure、supporting files。
- **Claude Code Skills**：Claude Code 對同一概念的實作，另外支援 `/skill-name`、`disable-model-invocation`、`context: fork`、`agent`、dynamic context injection 等欄位。

所以本文若提到「三層載入」「`name`/`description` 的格式限制」，多半是在講通用規格；若提到「怎麼觸發」「怎麼和 subagent 配合」，則以 Claude Code docs 為準。

## 核心概念

**Skill 是什麼**：把可重複使用的流程、知識與 best practices 打包給 agent 的可重用能力。最小單位是**一個包含 `SKILL.md` 的資料夾**；其他檔案都是選配。

最小結構通常長這樣：

```text
my-skill/
├── SKILL.md
├── reference.md / examples.md / template.md   # 選配
└── scripts/                                   # 選配
```

重點不是資料夾名稱一定要叫 `references/` 或 `prompts/`，而是：**`SKILL.md` 要清楚告訴 Claude 這些檔案各自是什麼、何時該讀、何時該執行。**

**Progressive Disclosure 三層載入**（官方概念）：

- **L1 metadata**：`name` + `description` 先載入。官方文件用量級估算為每個 skill 約 100 tokens。
- **L2 instructions**：skill 被觸發時才讀 `SKILL.md` body。官方建議把主體控制在 **500 行內**。
- **L3 supporting files / scripts**：其他 markdown、資源檔、腳本按需讀取或執行。腳本被執行時，**script 本身不進 context，只有 output 進 context**。

## 在 Claude Code 裡怎麼觸發

Claude Code 主要有三種情況：

1. **自動觸發**：Claude 依 `description` 與可選的 `when_to_use` 判斷是否載入 skill。
2. **手動觸發**：直接用 `/skill-name` 呼叫，例如 `/explain-code src/auth/login.ts`。
3. **限制觸發**：
   - `disable-model-invocation: true`：禁止 Claude 自動載入，只能手動呼叫。
   - `user-invocable: false`：不顯示在 `/` 選單，但 Claude 仍可在需要時自動使用。

補一個容易忽略的點：在 Claude Code 裡，一旦 skill 被 invoke，渲染後的 `SKILL.md` 內容會留在當前 session；它不是每回合都重新讀一次原檔。

## 它和 Command / Subagent / MCP 的關係

這幾個東西相關，但**不是同一層抽象**：

| 元件 | 本質 | 主要用途 | 和 Skill 的關係 |
|------|------|----------|----------------|
| Custom command | Claude Code 的 prompt 入口 | 手動執行 `/name` 類工作流 | `.claude/commands/*.md` 仍可用，但官方已把 custom commands 併入 skills 概念；需要 supporting files、auto invocation 時，優先用 skill |
| Subagent | 隔離執行環境 | 讓任務在獨立 context 內執行 | skill 可用 `context: fork` + `agent` 指定由某種 subagent 執行 |
| MCP server | 外部工具介面 | 讓 agent 連外部服務或系統 | skill 可以教 Claude **何時、如何** 使用 MCP，但 MCP 本身不是 prompt 封裝 |
| Skill | 可重用的 instructions package | 封裝工作流、知識、scripts、supporting files | 可把 command 風格的入口、subagent 執行、MCP 工具使用串成一套固定做法 |

如果要一句話總結：**Skill 不是比 command / subagent / MCP 更高階的「宇宙真理」，而是把這些能力組裝成可重用 workflow 的封裝。**

## Skill vs MCP

這兩者不是互斥，而是解不同問題：

- **Skill**：解決「流程怎麼做、何時做、有哪些慣例」
- **MCP**：解決「可以呼叫哪些外部能力」

實務上常見的是兩者搭配：例如 skill 裡寫清楚「先查 Linear issue、再讀相關 docs、最後建立 review」，而真正查 issue / 建 comment 的能力來自 MCP。

從 context 成本來看，Skill 的優勢在於：

- 常駐的只有 metadata
- 長篇說明、範例、腳本都能延後到需要時才載入

MCP 的工具 schema 則是另一種成本模型；**實際 token 開銷會依 client、server 與工具數量而變，不適合把單一案例的節省比例當成通則。**

[MCPorter](https://github.com/steipete/mcporter) 是一個有趣的折衷方案：它可以把 MCP server 包成 CLI 或 TypeScript client，讓某些穩定的 MCP 互動改走 code execution，再由 skill 負責 workflow。這是實用的架構選項，但不是所有場景都一定比直接用 MCP 好。

## 建立 Skill

自己手寫 `SKILL.md` 當然可以，但最省力的方式通常是用 **skill-creator**（Anthropic 在 `anthropics/skills` 開源的 skill）：

- 先釐清需求與觸發情境
- 主動追問 edge cases、輸入輸出格式、成功條件
- 草擬 `SKILL.md`
- 產生測試 prompts
- 視情況跑 with-skill vs baseline benchmark
- 最後再優化 description 的觸發率

詳見 [[skill-creator-是什麼]]。

寫完後可以用這個清單自檢：

- `SKILL.md` 主體盡量控制在 **500 行內**；細節移到 supporting files
- **通用 Agent Skills 規格**裡，`name` 與 `description` 都是 required
- **Claude Code** 裡，`description` 是強烈建議；`name` 可省略，預設回退到資料夾名稱
- `name` 限制：**≤ 64 字元**、只能小寫字母 / 數字 / 連字號、不可含 XML tag、不可用保留字 `anthropic` / `claude`
- `description` 要用**第三人稱**，同時描述「做什麼」與「何時該用」
- 若以通用規格看，`description` 上限是 **1024 字元**；在 Claude Code 中，`description` 與 `when_to_use` 合併後在 skill listing 會有 **1536 字元**截斷上限，因此關鍵詞要前置
- 會造成副作用、且不想讓模型自動亂觸發的 skill，記得加 `disable-model-invocation: true`
- 需要隔離上下文時，再考慮 `context: fork`

## 常見陷阱

### 1. Skill bloat（裝太多、描述太像）

- **徵兆**：Claude 選錯 skill，或該觸發時反而沒觸發
- **原因**：description 重疊、粒度太細、功能邊界不清
- **解法**：保留真正常用、界線清楚的 skills；重疊功能寧可合併

### 2. 把 Skill 當一次性 prompt template

- **徵兆**：寫完 skill 只用一次，之後完全不會再用
- **原因**：Skill 適合重複工作流，不適合所有零碎任務
- **解法**：一次性需求先用普通 prompt 或手動 command；重複出現後再抽成 skill

### 3. 混淆不同 surface 與 scope

- **徵兆**：以為 Claude.ai、API、Claude Code 會自動同步同一批 custom skills
- **事實**：官方明確說 custom skills **不會跨 surface 自動同步**
- **補充**：Claude Code 內部也分 personal / project / plugin / managed 等 scope
- **解法**：把分發與同步當成另一個問題處理；像 Library Meta-Skill 這類做法可參考，但它是**社群模式，不是官方內建同步機制**

### 4. `description` 寫太泛或太保守

- **徵兆**：skill 長期 undertrigger，明明該用卻沒用到
- **原因**：只寫「做什麼」，沒寫「何時該用」；或關鍵詞太少
- **解法**：把使用情境寫進 `description` / `when_to_use`，並把常見 phrasing 放前面

## 社群精選 Skills 實例

以下是社群釋出的 skill / plugin，展示 skill 概念的實用範圍——從通知、token 壓縮到設計規範、對抗式審查。具體名稱與 repo 可能變化，此處記錄**問題與 pattern**供參考。

| Skill | 問題 | 做法 |
|---|---|---|
| Peon Ping | 多 session 並行時忘記某個 session 跑完或卡在 permission prompt | 完成或需權限時主動通知；可改用遊戲角色語音 |
| Dogfood | Agent 生出的 web app 缺真人視角審查 | 以 adversarial review 風格走查頁面，產 critical/medium/low 分級 bug 報告（仰賴 agent browser） |
| Caveman | Claude 過度解釋、回覆塞贅詞 | 強制穴居人語氣回話砍 filler，多種強度等級可調；內建 Wyan 中文模式每 token 承載語意更多，但非英文準確度較低 |
| Git Time Travel | Agent 判斷「為何某段歷史出錯」困難 | 讀全 git 歷史 + references 內建地雷 pattern（force push、沒備份就 rebase 等），產問題報告 |
| Pre-mortem | 上線後才發現架構弱點 | 掃 codebase 挑脆弱區塊，預測尚未發生但可能發生的 bug |
| Mutation Testing | 測試套件是否真能抓 bug 無從驗證 | 注入 mutation bug 看測試是否抓到，產 mutation score 與漏網清單；**執行前必須 commit 所有改動**（會 git revert） |
| The Fool | 想法 / decision / plan 缺批判性壓力測試 | 多種挑戰模式逐一套用，輸出 failure mode 報告與連鎖後果 |
| Reddit Fetch | Reddit 封鎖 bot 讓市場研究難抓內容 | Gemini CLI + Tmux 當 primary，curl Reddit JSON API 當 fallback |
| Color Expert | Agent 常收斂到千篇一律紫+白 UI | 帶 100+ references（WCAG、palette、色彩科學），agent 讀完再實作 |

> 這些是共通 pattern 的實例化，不必全裝；依痛點挑選。

## 來源

**官方文件（本文主要依據）**
- [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Equipping agents for the real world with Agent Skills（Engineering blog）](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Extend Claude with skills](https://code.claude.com/docs/en/skills)

**工具 / 範例**
- [anthropics/skills](https://github.com/anthropics/skills)
- [MCPorter](https://github.com/steipete/mcporter)

**社群延伸（適合拓展視角，不作為本文主要事實依據）**
- Claude Skills 概念介紹（AIJasonZ）— https://www.youtube.com/watch?v=1WImBwiA7RA
- 工程師視角的 Skills 完整解析（indydevdan）— https://www.youtube.com/watch?v=kFpLzCVLA20
- 用 Skill 包 workflow 與 MCP 的討論（AIJasonZ）— https://www.youtube.com/watch?v=fG95XsBO5U4
- Library Meta-Skill 跨裝置分發（indydevdan）— https://www.youtube.com/watch?v=_vpNQ6IwP9w
- 意想不到好用的 Claude Code Skills 合集（AILABS-393）— https://www.youtube.com/watch?v=qQ5uObNKBOU（本文「社群精選 Skills 實例」章節來源）
