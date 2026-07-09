---
title: Claude Code 規則系統設計
created: 2026-05-05
updated: 2026-05-15
tags:
  - claude-code
  - claude-md
  - ai-agent
---

CLAUDE.md 與 Rules 兩個規則機制的設計判斷：怎麼放、寫什麼、何時拆 Rules、何時升 Hook。

## CLAUDE.md

每次 session 啟動時 Claude 讀的持久指示檔。**官方建議 200 行內**——塞太多會讓重要規則被淹沒，模型反而忽略。

`/init` 會掃描專案產出基礎 CLAUDE.md（偵測 build system、test framework、code patterns）。

### 4 類 scope（範圍從廣到窄）

所有層都會載入並 concat 進 context（不互相覆寫），更具體的讀在後面、優先級高：

| Scope | 位置 | 用途 |
|---|---|---|
| Managed | 系統層 CLAUDE.md（依 OS 不同） | 組織統一政策，不能被個人設定排除 |
| User | `~/.claude/CLAUDE.md` | 個人偏好,跨所有專案 |
| Project | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 團隊共享，commit 進 git |
| Local | `./CLAUDE.local.md` | 個人專案私記事，加 `.gitignore` |

判準：「換一個專案還適用嗎？適用 → user；不適用 → project；只跟特定模組相關 → Rules（path-scoped）或子目錄 CLAUDE.md」。

### AGENTS.md 整合

Claude Code **只讀 CLAUDE.md，不讀 AGENTS.md**。若 repo 已有 AGENTS.md（其他 agent 工具用），CLAUDE.md 第一行 `@AGENTS.md` import 它，下方再補 Claude 特化規則。

### 常用規則模組

直接可貼進 CLAUDE.md 的 4 條判斷型模組：

- **Tool Overrides**：列出 Claude 不主動採用、但你要求採用的工具（如 `gh` 取代 `git`、`pnpm` 取代 `npm`）
- **Verify, Don't Just Check**：完成標準是「功能實際運作」，要求 lint / typecheck / 測試實際通過才能回報
- **UI Verification**：UI 任務指示用 [Claude in Chrome extension](https://code.claude.com/docs/en/chrome) 或 Puppeteer MCP 觀察畫面再修正
- **Git Commit Safety**：不可逆指令（`git push --force`、`git reset --hard`、`rm -rf` 等）必須先取得使用者同意

## CLAUDE.md vs Rules vs Skills

| 機制 | 載入時機 | 適合用途 |
|---|---|---|
| CLAUDE.md | 每次 session 全載 | 跨任務通則、code style、build 指令 |
| Rules（`.claude/rules/*.md`，無 paths） | 每次 session 全載 | 想拆分但仍每次都用的規則 |
| Rules（有 paths frontmatter） | 動到匹配檔案時 | 特定模組規則（API / 前端 / 測試） |
| Skills（`.claude/skills/`） | 你 invoke 或 Claude 判斷相關時 | 領域知識、可重用 workflow |

判準：每次都該讀 → CLAUDE.md；只在某類檔案讀 → Rules（paths）；按需 invoke → Skills。

## 規則升級路徑

自然語言層（CLAUDE.md / Rules）本質是**建議性**的（advisory）——Claude 通常遵守，但無法 100% 強制。代價大、不可妥協的事 → 升級到 [Hook](https://code.claude.com/docs/en/hooks-guide)，事件觸發必跑（如 Gmail 寄信前確認、刪檔擋下、API key 偵測）。

四步走：

1. `/init` 起點：產出基礎 CLAUDE.md
2. 規則累積：對話中希望它記住的事，請它寫進 CLAUDE.md
3. CLAUDE.md > 200 行 → 拆 Rules（path-scoped 優先）
4. 仍偶爾被忽略 + 違反代價大 → 改 Hook

## 常見陷阱

| 徵兆 | 原因 | 解法 |
|---|---|---|
| 每個任務都要反覆 course correction | CLAUDE.md 只用 `/init` 預設、沒補規則 | 加 verification criteria + 具體 code style |
| Claude 順手「優化」鄰近程式 / 重新格式化 codebase | 沒寫 Surgical Changes 類規則 | 明文要求只動與當前任務相關的程式 |
| 寫程式但沒驗證就回報完成 | 沒寫 verification 規則 | 強制 lint / typecheck / 測試實際通過才能回報 |
| CLAUDE.md 越寫越長、模型開始忘事 | 把 path-specific 規則塞進主檔 | 拆 Rules（`paths:` frontmatter） |
| Claude 一直忽略某條規則 | 檔案太長，重要規則被淹沒 | 大砍：「拿掉這行會出錯嗎？」 |
| 兩處規則矛盾、Claude 隨機選 | 跨檔案沒對齊 | 用 `/memory` 列出載入檔案找衝突 |
| 規則寫了還是被略過、且代價大 | 自然語言層無法 100% 強制 | 改 Hook |

## 來源

- [How Claude remembers your project](https://code.claude.com/docs/en/memory) — 4 類 scope、Rules、200 行上限
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [Hooks guide](https://code.claude.com/docs/en/hooks-guide)
