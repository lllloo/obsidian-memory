---
name: ask-vault
description: 向使用者的中央 Obsidian 第二大腦(LLM Wiki vault)查詢過往研究、決策與累積知識。在**任何專案**中,當使用者問「我之前對 X 的結論/想法是什麼」「查我的筆記/第二大腦」「vault 裡有沒有關於 X」「我以前研究過的 Y」,或需要跨專案的既有研究脈絡時使用——即使沒明講「查 vault」,只要在問累積知識就用。唯讀、附引用、隨叫隨起,不需常駐。**不要**用於:查當前專案自身的程式碼/檔案/決策(那用一般工具直接讀),或修改 vault(那需在 vault 內操作)。
---

# ask-vault — 查詢中央第二大腦

使用者的長期研究、決策與知識累積在一個中央 Obsidian LLM Wiki vault(與當前專案不同的 repo)。本 skill 讓你在**任何專案**中,以「請求/回應」方式查詢它,而不必把整個 vault 讀進當前 context。

## 怎麼做

本 skill 目錄(即這份 SKILL.md 所在資料夾)下有腳本 `scripts/ask_vault.py`。以 `python3` 執行、把使用者問題當引數傳入:

```
python3 <本 skill 目錄>/scripts/ask_vault.py "使用者的問題(繁體中文、盡量具體)"
```

命令的 cwd 是使用者當前專案、不是 skill 目錄,所以要用**絕對路徑**——裸 `scripts/ask_vault.py` 會找不到。Claude Code 把 skill 目錄放在最上方「Base directory for this skill」那行,取來接上 `scripts/ask_vault.py` 即可。

腳本會依呼叫環境自動選 headless CLI(claude/codex/opencode)在 vault root 走 Query(讀索引 → 定位相關頁 → 讀頁 → 附引用綜合),答案印到 stdout。唯讀、不改動 vault、答完即退、不需常駐。

## 使用要點

- 把使用者的問題原意轉成一句清楚的查詢傳進去;涉及多面向時可分多次呼叫問不同角度。
- **原樣轉述**回傳答案給使用者,並**保留其中的來源頁引用與證據強度標註**——vault 的回答會就地標來源與強度(如「單一 preprint、未同儕審查」),轉述時不要丟掉這些。
- 若回傳「vault 無此資料」,如實告知,不要自行編造 vault 內容,也不要用當前專案的資訊臆測 vault 裡有什麼。
- 這是查詢**另一個 repo** 的知識,不是查當前專案。

## 前置

需要 `python3`(純 stdlib、跨平台)與本 skill 目錄內的 `scripts/ask_vault.py`。若執行失敗,告知使用者 vault 查詢工具尚未就緒。
