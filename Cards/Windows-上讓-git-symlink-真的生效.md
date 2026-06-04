---
title: Windows 上讓 git symlink 真的生效
created: 2026-05-19
updated: 2026-06-04
tags:
  - windows
  - git
  - cli
  - workflow
---

跨平台 repo 用 symlink 維護「單一來源」（例如本 vault 的 `.claude/skills` 與 `.codex/skills` 同時指向 `.agents/skills`，讓 Claude Code 與 Codex 共用同一份 skill），Windows 上 clone 完常變成 17 bytes 文字檔，內容是字串 `../.agents/skills`，驗證腳本直接 fail。每個指向同一目標的 symlink 都會踩到，要逐個還原。

> symlink 的概念與「一份內容、多入口」用途見 [[symlink-讓一份內容多個入口]]。

## 兩層根因

- **Git 層**：`core.symlinks` 預設 `false`，git 把 symlink 物件 checkout 成文字檔
- **OS 層**：Windows 預設不給非管理員建 symlink，即使 git 試了也 fallback 成文字檔

兩層都修才會生效。

## 修法

```bash
# 1. 全域開 git symlink（只影響之後 clone 的 repo）
git config --global core.symlinks true

# 2. 清掉 local 覆蓋（最容易漏；舊 repo 常留著 false）
git config --local --get core.symlinks   # 先看
git config --local --unset core.symlinks # 清掉讓 global 生效
```

**3. 開 Windows 開發者模式**（OS 層權限放行，GUI 設定）

- Win10：設定 → 更新與安全性 → 開發人員專用 → 開啟「開發人員模式」
- Win11：設定 → 隱私權與安全性 → 開發人員 → 開啟「開發人員模式」

不需重啟，但 shell session 要重開。

```bash
# 4. 還原已 checkout 成文字檔的假 symlink（每個都要做）
rm .claude/skills && git checkout -- .claude/skills
rm .codex/skills  && git checkout -- .codex/skills
```

驗證（每個 symlink 都要檢查）：

```bash
ls -la .claude/skills .codex/skills
# 兩個都應為 lrwxrwxrwx ... -> ../.agents/skills
```

## 坑

- **PowerShell `New-Item -ItemType SymbolicLink` 不吃開發者模式**（Windows PowerShell 5.1 實測；7+ 行為可能不同）——堅持要管理員。手建 symlink 用 `cmd /c mklink /D`，或讓 git checkout 自己處理
- **`git config --global` 不溯及既往**——舊 repo 必須手動 `rm` + `git checkout --` 才會修復，這是步驟 4 必要的原因
- **Symlink 沒生效時第一步**：`git config --local --get core.symlinks`，幾乎都是 local 沒清
