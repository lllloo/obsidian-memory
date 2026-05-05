---
title: Claude Code 規則系統設計
created: 2026-05-05
updated: 2026-05-05
tags:
  - claude-code
  - claude-md
  - agent
---

涵蓋 CLAUDE.md 與 Rules 兩個官方規則機制：放置位置、`@import`、200 行上限、`paths:` 條件載入、AGENTS.md 整合、規則範本、升級到 Skills / Hooks 的判準。

## CLAUDE.md

每次 session 啟動時 Claude 讀取的持久指示檔。**官方建議 200 行內**（“target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence”）。塞太多會讓重要規則被淹沒，模型反而忽略。

`/init` 會掃描專案、產出基礎 CLAUDE.md（偵測 build system、test framework、code patterns）。

### 官方放置位置（4 類 scope）

按 scope 從廣到窄。所有層都會被載入並 concat 進 context（不互相覆寫），更具體的讀在後面、優先級高：

| Scope | 位置 | 用途 |
|---|---|---|
| Managed policy | 系統層 CLAUDE.md（依 OS 不同） | 組織統一政策，不能被個人設定排除 |
| User | `~/.claude/CLAUDE.md` | 個人偏好，跨所有專案 |
| Project | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 團隊共享，commit 進 git |
| Local | `./CLAUDE.local.md` | 個人專案私記事，加 `.gitignore` |

判準：「換一個專案還適用嗎？適用 → user；不適用 → project；只跟特定模組相關 → Rules（path-scoped）或子目錄 CLAUDE.md」。

### `@import` 語法

CLAUDE.md 內可用 `@path/to/import` 引用其他檔案，最多 5 層遞迴。相對路徑相對於含 import 的檔案：

```markdown
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Personal overrides: @~/.claude/my-project-instructions.md
```

注意：import 的檔案是在 launch 時 **全部展開進 context**，不省 token，僅幫助組織。

### AGENTS.md 整合

Claude Code **只讀 CLAUDE.md，不讀 AGENTS.md**。若 repo 已有 AGENTS.md（其他 agent 工具用），建立 CLAUDE.md import 它：

```markdown
@AGENTS.md

## Claude Code

Use plan mode for changes under `src/billing/`.
```

兩工具讀同一份內容，CLAUDE.md 補 Claude 特化指示。

### 該寫什麼 / 不該寫什麼

| ✅ 應該寫 | ❌ 不該寫 |
|---|---|
| Claude 猜不到的 Bash 指令 | Claude 讀程式碼就能知道的事 |
| 與預設不同的 code style | Claude 已知的標準語言慣例 |
| 測試指令、偏好的 test runner | 詳細 API 文件（連結到 docs 即可） |
| Repo 慣例（branch / PR 規則） | 經常變動的資訊 |
| 專案特有的架構決策 | 長段解釋或教學 |
| 開發環境怪癖（必要的 env vars） | 整個 codebase 的 file-by-file 描述 |
| 常見陷阱、非顯而易見的行為 | 「寫乾淨程式碼」這種廢話 |

每行寫進去前先問：「拿掉這行 Claude 會出錯嗎？」不會就刪掉。

### 強化遵循度

- **加強調**：在重要規則加 `IMPORTANT` 或 `YOU MUST`（官方明確建議）
- **像 code 一樣維護**：出錯就 review，定期 prune，改完觀察 Claude 行為是否真的變了
- **HTML 註解**：`<!-- maintainer notes -->` 在 CLAUDE.md 內會被剝除不進 context（code block 內保留），可留人類維護筆記不耗 token

### 規則範本（社群整理）

`forrestchang/andrej-karpathy-skills`（社群整理 Karpathy 對 LLM coding pitfalls 觀察的單一 CLAUDE.md，**非 Karpathy 本人 repo**）四大原則：

- **Think Before Coding** — Don't assume. Don't hide confusion. Surface tradeoffs.
- **Simplicity First** — Minimum code that solves the problem. Nothing speculative.
- **Surgical Changes** — Touch only what you must. Clean up only your own mess.
- **Goal-Driven Execution** — Define success criteria. Loop until verified.

具體硬門檻（forrestchang 規則）：「If you write 200 lines and it could be 50, rewrite it.」

其他常用：

- **Tool Overrides**：列出 Claude 不會主動採用、但你要求採用的工具（如 `gh` 取代 `git`、`pnpm` 取代 `npm`）；預設指令在訓練資料裡，重複寫只是浪費 context
- **Verify, Don't Just Check**：完成標準是「功能實際運作」，要求用 lint / typecheck / 測試實際驗證再回報（官方：「the single highest-leverage thing you can do」）
- **UI Verification**：UI 任務指示用 [Claude in Chrome extension](https://code.claude.com/docs/en/chrome) 或 Puppeteer MCP 觀察實際畫面再修正
- **Git Commit Safety**：不可逆指令（`git push --force`、`git reset --hard`、`rm -rf` 等）必須先取得使用者同意

### 載入行為（debug 時用得到）

- **載入順序**：filesystem root 往下到 working directory，後讀的優先級高
- **`/compact` 之後**：project root CLAUDE.md 會 re-inject；**子目錄 CLAUDE.md 不會**，要等 Claude 再次讀子目錄底下檔案才載
- **`--add-dir`**：預設**不**載入該目錄的 CLAUDE.md，需設 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`
- **`/memory` 指令**：列出當前 session 載入的所有 CLAUDE.md / CLAUDE.local.md / rules 檔
- **`InstructionsLoaded` hook**：debug 哪些指示檔被載入、何時、為何
- **`claudeMdExcludes` 設定**（`.claude/settings.local.json`）：monorepo 內排除其他團隊的 CLAUDE.md

## Rules（`.claude/rules/`）

CLAUDE.md 過長就拆 Rules — 把規則分散到多個 topic 檔，**並可條件載入**（path-scoped）。

### 結構

```
your-project/
├── .claude/
│   ├── CLAUDE.md           # 主指示
│   └── rules/
│       ├── code-style.md   # 沒 paths → 與 CLAUDE.md 同優先級，每次載入
│       ├── testing.md
│       └── security.md
```

`.md` 檔遞迴搜尋，可建 `frontend/`、`backend/` 等子目錄分組。

### Path-scoped rules（核心優勢）

YAML frontmatter 加 `paths:` 欄位，只有 Claude 動到匹配檔案時才載入：

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules
- All API endpoints must include input validation
- Use the standard error response format
- Include OpenAPI documentation comments
```

Glob 模式：

| Pattern | 命中 |
|---|---|
| `**/*.ts` | 所有 TypeScript 檔 |
| `src/**/*` | `src/` 底下全部 |
| `*.md` | 專案根目錄的 markdown |
| `src/components/*.tsx` | 特定目錄的 React 元件 |

支援多 pattern 與 brace expansion：

```yaml
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
```

### User-level rules（`~/.claude/rules/`）

跨所有專案套用，比 project rules 優先級低（project 覆寫 user）：

```
~/.claude/rules/
├── preferences.md    # 個人偏好
└── workflows.md      # 個人 workflow
```

### Symlink 共享

`.claude/rules/` 支援 symlink — 維護一份 shared rules 連到多個專案：

```bash
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

### CLAUDE.md vs Rules vs Skills

| 機制 | 載入時機 | 適合用途 |
|---|---|---|
| CLAUDE.md（含 `@import`） | 每次 session 全載 | 跨任務通則、code style、build 指令 |
| Rules（無 paths） | 每次 session 全載 | 想拆分但仍每次都用的規則 |
| Rules（有 paths） | 動到匹配檔案時 | 特定模組 / 檔案類型的規則（API / 前端 / 測試） |
| Skills（`.claude/skills/`） | 你 invoke 或 Claude 判斷相關時 | 領域知識、可重用 workflow（不該污染每次 conversation） |

判準：每次都該讀 → CLAUDE.md；只在某類檔案讀 → Rules（paths）；按需 invoke → Skills。

## 規則升級路徑

自然語言層（CLAUDE.md / Rules）本質上是**建議性**的（advisory）— Claude 通常會遵守，但無法 100% 強制。代價大、不可妥協的事 → 升級到 [Hook](https://code.claude.com/docs/en/hooks-guide)，事件觸發必跑（如 Gmail 寄信前確認、刪檔擋下、API key 偵測）。

四步走：

1. `/init` 起點：產出基礎 CLAUDE.md
2. 規則累積：對話中希望它記住的事，請它寫進 CLAUDE.md
3. CLAUDE.md > 200 行 → 拆 Rules（path-scoped 優先）
4. 仍偶爾被忽略 + 違反代價大 → 改 Hook

## 常見陷阱

| 徵兆 | 原因 | 解法 |
|---|---|---|
| 每個任務都要反覆 course correction | CLAUDE.md 只用 `/init` 預設、沒補規則 | 加入 verification criteria + 具體 code style，先讓 agent 對齊再動手 |
| Claude 順手「優化」鄰近程式 / 重新格式化整個 codebase | 沒寫 Surgical Changes 類規則 | 明文要求只動與當前任務直接相關的程式 |
| Claude 寫程式但功能沒驗證就回報完成 | 沒寫 verification 規則 | 強制 lint / typecheck / 測試實際通過才能回報 |
| CLAUDE.md 越寫越長、模型開始忘事 | 把 path-specific 規則塞進主檔 | 拆 Rules（`paths:` frontmatter），只在動到匹配檔案時載入 |
| Claude 一直忽略某條 CLAUDE.md 規則 | 檔案太長，重要規則被淹沒 | 大砍：「拿掉這行 Claude 會出錯嗎？」不會就刪 |
| 兩處 CLAUDE.md 規則矛盾、Claude 隨機選 | 跨檔案沒對齊 | 用 `/memory` 列出載入的檔案，找衝突；monorepo 用 `claudeMdExcludes` 排除無關的 |
| `/compact` 後子目錄規則消失 | 子目錄 CLAUDE.md 不會 re-inject | 等 Claude 再次讀該子目錄檔案才會載入；或改寫進 project root |
| `@import` 把檔案組織得很漂亮但 context 沒省 | import 的檔案 launch 時就全展開 | 想省 context 用 Rules（path-scoped），不要靠 import |
| 規則寫了還是被略過、且代價大 | 自然語言層無法 100% 強制 | 改寫成 Hook |

## 來源

**官方文件**
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) — CLAUDE.md 寫法、verification、prompt 建議
- [How Claude remembers your project](https://code.claude.com/docs/en/memory) — CLAUDE.md 4 類 scope、Rules（`.claude/rules/` + paths frontmatter）、200 行上限、`/memory`、auto memory
- [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory) — CLAUDE.md / settings.json / hooks / skills / commands / subagents / rules / auto memory 全景
- [Hooks guide](https://code.claude.com/docs/en/hooks-guide)
- [Skills](https://code.claude.com/docs/en/skills)

**社群**
- [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) — 把 Karpathy 對 LLM coding pitfalls 的觀察整理成單一 CLAUDE.md（**非 Karpathy 本人 repo**，作者 Forrest Chang）
- [Claude Code CLAUDE.md 最佳實踐（AILABS 393）](https://www.youtube.com/watch?v=fMY5Sdj2DMk)
- [Claude 一直忘規則？四個設定一次解決（AgentcrewAcademy）](https://www.youtube.com/watch?v=kSFty4XwXS8)

## 相關閱讀（vault 內）

- [[Context-Engineering]] — context window 角度的 CLAUDE.md 精簡原則、文件拆分策略
