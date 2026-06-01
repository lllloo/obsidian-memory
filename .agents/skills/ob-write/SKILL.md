---
name: ob-write
description: 把內容「寫進／建立／新增」到 Obsidian vault（obsidian-memory）。用於：使用者要記下想法或結論、剪貼摘要、寫一篇筆記、追加內容或改 frontmatter，常見說法如「記一下」「筆記關於…」「寫一篇」「日記」「存進 vault」「記到 ob」「寫進 obsidian」。即使沒明說「寫」，只要意圖是把某段內容留存進 vault 就用本 skill。任何專案皆可呼叫，skill 內部判 cwd 決定寫入模式（本地不限工具 / 跨專案嚴格 CLI）。純查詢／搜尋既有筆記（找、有沒有、搜）請改用 ob-read，本 skill 不查詢；「daily updates 變更彙整」走 vault-updates-daily。
---

# /ob-write — 寫進 Obsidian Vault

建立筆記、追加內容、改 frontmatter。查詢請改用 `/ob-read`。

## 模式判斷（必先執行）

寫入分兩種模式，先判 cwd——用 `Read vault-map.md` 確認存在（harness-native，不經 shell、不分 PowerShell/bash）：讀得到 → `MODE=local`；讀不到 → `MODE=cross`。

- `MODE=local`：cwd 已是 vault root → 本地模式，不限工具（建檔用 Write，其餘 CLI 優先）。
- `MODE=cross`：cwd 在其他專案 → 跨專案模式，嚴格 CLI + vault 身分硬 gate，不降級。

## 執行

呼叫 Agent tool：

- `subagent_type`: `"general-purpose"`
- `prompt`: `references/write.md` 全文 + `\n\n## 本次模式\nMODE=<local|cross>\n\n## 本次需求\n` + 使用者原始輸入

subagent 完成後直接回報結果（建檔路徑、模式、是否走降級等）。

## 無 subagent 環境的 fallback

無 Agent 工具的環境（Cursor / Codex / Gemini CLI 等）由主 agent 直接 Read `references/write.md`，依上面判得的模式跑同一流程。
