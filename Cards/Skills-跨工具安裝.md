---
title: Skills 跨工具安裝
created: 2026-06-03
updated: 2026-06-30
tags:
  - skill
  - claude-code
  - copilot
  - cli
  - security
---

# Skills 跨工具安裝

[vercel-labs/skills](https://github.com/vercel-labs/skills) 的核心價值是**一份 skill 多工具共用**：安裝到共用的 `~/.agents/skills/`，再讓 Claude Code、GitHub Copilot、OpenCode 各自的技能目錄 symlink 指向同一份源頭，更新一次全部生效。

## symlink vs copy：怎麼選

這是安裝時唯一要做的判斷：

- **symlink（預設）**：多工具指向同一份源頭，改一次到處生效。日常自用、想保持各工具一致時選這個。
- **copy**：每個工具各存一份副本，彼此隔離。要在某工具改 skill 而不影響其他、或要釘住特定版本不被更新波及時才選 copy。

> 取捨本質：symlink 換「一致與省維護」，copy 換「隔離與可釘版本」。沒有隔離需求就用 symlink。

## 常用指令

```bash
npx skills find                                   # 互動式探索可用技能（也可逛 skills.sh）
npx skills add anthropics/skills --skill frontend-design  # 安裝指定 skill（選 symlink）
npx skills ls -g                                  # 列出已安裝
npx skills update                                 # 更新
npx skills remove <skill-name>                    # 移除（或直接刪共用目錄的檔）
```

`add` 也接受完整 URL（`npx skills add https://github.com/anthropics/skills --skill ...`）。

## 安裝前安全檢查

Skill 是會被 agent 當指令讀進去的程式化內容，不能只看 README 就信任。安裝陌生 skill 前至少檢查六類風險：

- 隱藏指令：註解、不可見字元、編碼文字藏 prompt injection。
- 冒充工具：用相似 Unicode 字元偽裝成可信工具或命令。
- 描述與行為不一致：自稱 formatter，實際連網、寫檔或跑 shell。
- 憑證外洩：讀取本機 key、token、cookie 後送出。
- 惡意程式：reverse shell、下載執行檔、可疑外部腳本。
- 依賴毒化：安裝 typo package 或未知來源 CLI。

Skill Specter 類工具代表一個方向：先做 pattern scan，再用 AI 掃描 description 與實作是否一致。實務流程應是「搜尋 skill → 掃描 → 看 findings → 修或拒裝 → 重掃」，不要讓 discovery 與 installation 直接相連。

## 參考資源

- [Skills GitHub](https://github.com/vercel-labs/skills)
- [skills.sh](https://skills.sh/)
- [Skill Specter 安全掃描解讀（AI Labs）](https://www.youtube.com/watch?v=KiTmBtyaeXg)
