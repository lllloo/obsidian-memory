# Obsidian Memory Vault

由 AI 在本 repo 執行 Ingest／Query／Lint，維護 Karpathy LLM Wiki。只保留核心知識庫、流程規範、`vault-lint` 與必要設定（2026-10-13 使用者拍板）；查詢入口是 `wiki/01.index.md`。

## 執行入口

在 repo 根目錄開啟 AI session，先讀 [AGENTS.md](AGENTS.md)、[MEMORY.md](schema/MEMORY.md) 與 [BACKLOG.md](schema/BACKLOG.md)。

- **Ingest**：提供來源 URL，或明確指定處理既有 raw；AI 依規範更新 wiki。
- **Query**：直接提問；AI 先讀 wiki 索引，再讀相關頁，附引用回答。
- **Lint**：呼叫 `/vault-lint`；AI 自主修補，需使用者決策的項目留在 BACKLOG。

執行 skill 需要 Python 3；`.agents/skills/` 為實作位置，`.claude/skills` 為相容 symlink。

資料夾與 tag 導航見 [vault-map.md](schema/vault-map.md)，設計取捨見 [SYSTEM-DESIGN.md](schema/SYSTEM-DESIGN.md)。私人筆記位於 Notion，不納入本 repo 的日常流程。
