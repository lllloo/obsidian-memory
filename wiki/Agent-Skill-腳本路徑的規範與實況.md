---
title: Agent Skill 腳本路徑的規範與實況
description: SKILL.md 呼叫 bundled 腳本該怎麼寫路徑：規範明訂裸相對路徑、主流集合一致照做，但規範內部對誰負責解析自相矛盾，實測會找不到檔
created: 2026-08-13
updated: 2026-08-13
parent: "[[wiki/01.index]]"
tags:
  - claude-code
  - coding-agent
  - ai-agent
  - skill
---

`SKILL.md` 裡寫 `python3 scripts/x.py`，執行時到底相對於誰？這個看似瑣碎的問題沒有單一答案：**規範規定一種、harness 實作另一種、主流集合照規範寫但很少真的踩到**。本頁把三者分開記，因為混談正是踩坑的來源。

## 規範怎麼規定

Agent Skills 規範（agentskills.io）`skill-creation/using-scripts` L98 逐字：

> Use **relative paths from the skill directory root** to reference bundled files. The agent resolves these paths automatically — no absolute paths needed.

頁內範例一律 `bash scripts/validate.sh`、`python3 scripts/process.py`、`uv run scripts/extract.py`。對 rendered HTML、canonical `.md` 與全站 `llms-full.txt` grep `CLAUDE_SKILL_DIR|CLAUDE_PLUGIN_ROOT|SKILL_DIR|PLUGIN_ROOT` **皆零命中**——規範不認任何環境變數形式。

**但規範內部自相矛盾**，這正是落差的根源：

| 頁 | 主張 |
|---|---|
| `skill-creation/using-scripts` | agent 自動解析（cwd 語意：「because the agent runs commands from there」） |
| `client-implementation/adding-skills-support` | **client 端**負責改寫：「resolve them against the skill's directory (the parent of SKILL.md) and **use absolute paths in tool calls**」，並要暴露 skill 的 location 給 model |

兩套機制不等價。「agent 會自動解析」是**對 conforming client 的規範性要求**，不是任何 harness 的實證保證——harness 沒實作那層改寫，裸相對路徑就會壞。

## 實況分布（2026-08-13 抽樣）

逐檔核對過的樣本，未做 GitHub code search 普查：

| 寫法 | 樣本 | 代表 |
|---|---|---|
| (a) 裸相對 `scripts/x.py` | 絕對主流 | `anthropics/skills` 8 個含 `scripts/` 的 skill 全數採用；`obra/superpowers` 唯一的腳本呼叫行亦然 |
| (b) `${CLAUDE_SKILL_DIR}` | **0** | — |
| (c) `${CLAUDE_PLUGIN_ROOT}` | **0** | — |
| (d) 專案根相對 `.claude/skills/<name>/scripts/…` | **0** | 只作為 opencode#6900 的事後 workaround 出現，無人主動如此撰寫 |
| (e) 佔位符 `<skill-root>/scripts/…` | ≥4，全在跨工具集合 | `MengTo/Skills`（Codex-first） |
| (f) 腳本自我定位（`__file__`／`dirname "$0"`） | 0 確認樣本 | — |

`obra/superpowers` 該列為本機實查（v6.3.0）：28 個 `SKILL.md`、3 個 `scripts/` 目錄，`CLAUDE_SKILL_DIR` 與 `CLAUDE_PLUGIN_ROOT` 命中數皆 0——**它是 plugin、用得到 `${CLAUDE_PLUGIN_ROOT}` 卻沒用**。`SKILL.md` 內唯一腳本呼叫是 `writing-skills/SKILL.md:320` 的 `./render-graphs.js ../some-skill`，配散文「Use `render-graphs.js` in this directory」，且那是給人手動跑的工具、不在 agent 流程上。

### 主流沒被燙到的真正原因

不是 (a) 可靠，而是**主流很少從 `SKILL.md` 呼叫 bundled 腳本**：

- `wshobson/agents`：180 個 `SKILL.md`，只有 4 個 `scripts/` 目錄；放寬到 `assets/` 下被呼叫的可執行檔也才 6/180（3.3%）
- `MengTo/Skills`：127 個 `SKILL.md`、10 個 skill 級 `scripts/`
- `obra/superpowers`：3/28
- `vercel-labs` 的 `find-skills`（skills.sh 顯示約 2.9M installs，人氣最高的單一 skill）：目錄下**只有 `SKILL.md`**，六條可執行指令全是外部 CLI（`npx skills find/add/update/init`）——把邏輯發佈成套件，路徑問題不存在

推論：**把邏輯包進 bundled 腳本、`SKILL.md` 只留呼叫行**這種設計（本 vault 的 skill 全走這條）落在主流最少踩、也最容易壞的那格，「主流用 (a)」對這種設計的參考價值低於表面。

### 宣告不是通例

`anthropics/skills` 8 個含 `scripts/` 的 skill 只有 5 個帶「路徑相對於本 skill 目錄」宣告（最嚴格讀法 4/8，因 `pdf` 那句只覆蓋 11 處呼叫中的 1 處）；`web-artifacts-builder`、`mcp-builder`、`webapp-testing` 全文 grep `relative|director|cwd|dirname|__file__` 零命中。實際措辭如 `docx/SKILL.md:17`「> Script paths below are relative to this skill's directory.」

「先 cd 到 skill 目錄」幾乎不存在：8 個裡只有 `skill-creator` 一處（且它用 `python -m scripts.aggregate_benchmark`，module 形式本來就依賴 cwd）。**主流的緩解手段是一句散文宣告，不是 cd、不是變數、不是絕對路徑構造。**

## 失敗證據

裸相對路徑在真實使用中會壞，跨平台、跨版本、跨工具皆有第一手 repro：

| issue | 內容 | 修法 |
|---|---|---|
| `anthropics/claude-code#11011` | `scripts/jenkins.sh` → `No such file or directory`；**至查證日仍 open** | agent 第二次自行改絕對路徑成功——失敗型態是「首次失敗、重試自救」，成本是浪費回合而非不可恢復 |
| `anthropics/claude-code#17741` | references 檔案版：「Claude guesses the path location … rather than resolving relative to the skill file」 | — |
| `anthropics/claude-code#56325` | 「the LLM has no way to resolve it because it doesn't know the skill's install directory」 | 建議 workaround 正是宣告寫法：'Read the file `references/style-guide.md` **located in this skill's directory**' |
| `anthropics/claude-code#18013` | plugin skill 路徑解析找錯目錄 | — |
| `anomalyco/opencode#6900` | `uv run scripts/tasks.py` 在 Claude Code 能跑、OpenCode 找不到 | 回報者改成專案根相對，自評「this is not friendly for skill portability」 |

無失敗率數據，只有回報頻率（相關 issue 搜尋 34 筆，其中 3–4 筆為獨立第一手 repro）。

## 跨工具分歧

差異方向是「**放棄自動解析、改用佔位符或絕對路徑**」，不是統一到某個變數：

- **OpenCode** 的機制根因：同一 skill 可能從六個位置之一載入（專案 `.opencode/`／`.claude/`／`.agents/` 三處，加對應三個家目錄全域路徑），專案層從 cwd 往上走到 git worktree 為止逐層收集——**skill 目錄相對 cwd 的深度不固定**，所以 (a) 與 (d) 在跨工具情境都結構上不可保證，佔位符／絕對路徑成了唯一「一定對」的選項。它讀得懂 `.claude/skills/**` 與 `.agents/skills/**`，但只承認 `name`／`description`／`license`／`compatibility`／`metadata`，`allowed-tools`、`model` 等會被靜默忽略。
- **MengTo/Skills**（同一份 SKILL.md 供 Codex／Claude Code／Cursor 手動載入）：10 個 `scripts/` 抽讀以佔位符為主（`<skill-root>`／`<skills-root>`／`/path/to/…`）。
- **wshobson/agents** 走生成路線：source of truth 是 Claude-native `plugins/` 樹，其他 harness 收到 `make generate-all` 的轉換樹——其 `SKILL.md` 仍是 Claude 原生寫法，**靠轉換過關而非原生中立**。

## Claude Code 專屬機制（規範不認）

官方文件記載兩個替換變數，社群滲透率為零（見上表）：

| 變數 | 值 | 範圍 |
|---|---|---|
| `${CLAUDE_SKILL_DIR}` | `SKILL.md` 所在目錄；plugin skill 時指向 skill 在 plugin 內的**子目錄**，非 plugin 根 | personal／project／plugin 三層皆可用 |
| `${CLAUDE_PLUGIN_ROOT}` | plugin 安裝目錄絕對路徑 | 文件明載「Substituted only in plugin skills」 |

**關鍵限制：這是字串替換，不是 shell 環境變數。** 官方只保證兩個替換位置——skill 的 markdown 正文，與 frontmatter `allowed-tools` 內的 Bash 規則。bundled 腳本自己的 process 環境不保證看得到 `$CLAUDE_SKILL_DIR`（`plugins-reference` 的 export 條款只涵蓋 hook process 與 MCP／LSP subprocess）。官方文件推薦寫法為 `python3 ${CLAUDE_SKILL_DIR}/scripts/visualize.py .`，理由是「不論安裝在 personal、project 或 plugin 層級都解析正確」，且只有這種寫法能讓 `allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/render.sh *)` 比對成功而免權限提示。

**這與 Anthropic 自家 skills repo 的做法不一致**：官方文件推薦替換變數，官方 skills repo 一律裸相對路徑。「官方建議」取決於問的是 CLI 文件還是 skills repo。

## 連帶查清的 cwd 行為

排查此題時一併釐清的 Claude Code Bash 工具行為（官方 `tools-reference`「What persists between commands」）：

- **讀取／載入 `SKILL.md` 不會切換 cwd**——文件對「路徑穩定性」開的處方是替換變數，不是 cd 進 skill 目錄
- **cwd 跨呼叫會保留**：main session 中 `cd` 的新目錄延續到後續 Bash 指令，條件是落點仍在專案目錄或 `--add-dir`／`additionalDirectories` 加入的目錄內；越界則自動重置回專案目錄並附 `Shell cwd was reset to <dir>`（本頁撰寫過程實地觸發過）。**subagent session 永不延續**
- **環境變數與臨場定義的 shell 函式不保留**（每次新 process）；但 startup file（`~/.zshrc` 等）的 alias／函式每個指令都可用——session 開始 source 一次後套用到每次呼叫，不是狀態延續
- **`cd` 預設不觸發權限提示**（屬內建 read-only 指令集），`cd packages/api && ls` 各段合格時亦然。兩個例外：`cd` 後接 `git`（新目錄的 hooks 可能被執行）、`cd` 後接輸出重導向且無法判定重導向目標的解析基準（唯一目標為 `/dev/null` 則免）

末項須標明是「文件如此規定」而非「實際永遠如此」：`#67947`、`#28240` 等回報實作與此規則有出入。

## 本 vault 的拍板（2026-08-13）

**採純 (a)**：全域 `~/.claude/rules/skill-writing.md` 改為「一律寫相對於 skill 目錄根的裸相對路徑，不用工具專屬替換變數」，`vault-lint`／`vault-watch`／`vault-youtube-sync` 共 11 處呼叫同步改寫（commit `b095ff1`）。取捨是接受首次 not-found 的風險，換取跨工具寫法統一——本 vault 的 skill 實體在 `.agents/skills/`，需被 Codex／OpenCode 讀到，`${CLAUDE_SKILL_DIR}` 與此目標直接衝突。

**`ask-vault` 為明列例外**：它由其他專案呼叫，cwd 既不在 vault root 也不在 skill 安裝根，裸相對路徑**結構上無基準可解析**，維持佔位符寫法。這是 (e) 在本 vault 的唯一適用情境，與 `MengTo/Skills` 的選擇同因。

同輪連帶修正 `vault-youtube-sync` 兩處路徑契約敘述：原寫「所有路徑為 repo root 相對」，機械替換後會自相矛盾，各標出 `scripts/` 相對 skill 目錄根的例外。

## 證據強度與勿引用

全部結論建立在一手官方文件、GitHub API 與逐檔核對上；星數為 2026-08-13 GitHub API 同日快照。

**勿引用**（三票對抗中被否決或有實質限制）：

- ~~「`anthropics/skills` 是遙遙領先的最高星 skill 集合」~~ — 0-3 否決。它是第二（`obra/superpowers` 較高）。且其 skill 標 `license: Proprietary`，屬 Anthropic 第一方家規，做「第三方社群實況」統計時不應與社群樣本混計
- ~~「規範文件宣稱 cwd 即 skill 目錄」~~ — 0-3 否決。`using-scripts` 只在散文因果子句提到，非 normative 條款
- ~~「find-skills 是為規避路徑問題而設計」~~ — 那是效果不是意圖，它本來就是查詢型 skill。且它對 (a)–(f) 分布屬 **null 樣本**，不進任何類別分母
- ~~「Cursor 文件禁止絕對路徑」~~ — 實為「只規定 skill-root 相對路徑這一種形式」，未明文禁止其他
- ~~repo 全庫層級的百分比計數~~ — 兩筆「100%／42 處」層級 claim 在三票查證中以 1-2 被駁回，本頁只保留逐檔可複現的部分
- **WebSearch 合成摘要不可作為本題來源**：它會把 `using-scripts` 的散文因果句誤植為規格 normative 條款，兩位查證者都踩到後回溯排除

**樣本限制**：分母極小（含 `scripts/` 的 skill 在各集合都只有個位數），任何量化分布都建立在數十筆而非數百筆樣本上；僅涵蓋 public repo。

## 關聯

- [[Claude-Code-Hook-能力邊界]] — 同屬「Claude Code 機制的實測邊界」：該頁的結論是能力上限由輸出契約決定，本頁的結論是路徑可靠性由 harness 有沒有實作 client 端改寫決定，兩者都指向「規範寫得到 ≠ 實作做得到」
- [[跨專案第二大腦整合模式]] — `ask-vault` 的跨 CLI 定位在該頁展開，本頁記的是它在路徑寫法上為何必須是例外
