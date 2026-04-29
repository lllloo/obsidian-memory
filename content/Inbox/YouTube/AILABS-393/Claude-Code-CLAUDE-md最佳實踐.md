---
title: Claude Code CLAUDE.md 最佳實踐
created: 2026-04-29
updated: 2026-04-29
source: https://www.youtube.com/watch?v=fMY5Sdj2DMk
published: 2026-04-28
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - claude-md
  - agent
  - prompt-engineering
---

## 核心觀念

Agent 的產出品質高度取決於 `CLAUDE.md`（Claude Code）或 `AGENTS.md`（其他 agent）這一份檔案。`init` 指令產出的預設內容遠遠不夠，必須依專案特性手動補上結構化規則，否則每個任務都會在 agent 與你之間反覆拉鋸。`CLAUDE.md` 不是「寫一次用到底」的靜態檔，而是要持續迭代的活文件。

## Think Before Coding（先思考再動手）

來源：Andrej Karpathy 的 skills repo。

- 明確要求 Claude 在動工前先說明假設（state assumptions explicitly）
- 若存在多種可行解讀，必須全部列出讓使用者選擇
- 效果：Claude 在開始實作前會主動提問澄清，避免直接套用訓練資料中的常見模式去硬幹
- 大幅減少事後反覆 course correction 的成本

## Simplicity First（優先選擇簡單方案）

- 預設行為：agent 容易把可以簡單解決的問題寫成龐大解法，造成日後重構與功能擴充困難
- 規則：禁止實作超過需求範圍的功能，並要求妥善處理錯誤
- 硬門檻：若一個解法可在 200 行內完成、且能再精簡到 50 行，就要 Claude 重寫
- 防止寫出大量無用的 overhead code 與方向錯誤的實作

## Surgical Changes（外科手術式修改）

- 問題：Claude 處理單一任務時，常順手「優化」鄰近程式或重新格式化整個 codebase，注意力被分散
- 規則：只動與當前任務直接相關的程式；發現無關的 dead code 只回報，不擅自修改
- 心智模型：每個改動必須能追溯到「使用者原始要求」；無法追溯就不該動
- 執行結果：Claude 會把其他發現以清單形式回報，由使用者決定是否處理

## Goal-Driven Execution（目標驅動執行）

- 核心問題：agent 不知道「正確輸出長什麼樣子」
- 規則：每個任務都要 Claude 先把它轉換成可驗證的成功標準（verifiable goal）
- 例：被要求加 input validation → 自動寫好涵蓋 invalid input 的測試，再迭代到測試通過
- UI 任務無法用單元測試驗證 → 在規則裡指示 Claude 透過 Chrome extension 或 Puppeteer MCP 觀察實際畫面再修正

## Tool Overrides（工具覆寫）

- `claude code init` 預設加入的 dev server、build server 指令多半已在訓練資料裡，重複寫只是浪費 context
- 真正該寫的是「非預設」的工具與指令：
  - 偏好用 GitHub CLI 取代 `git` → 明確聲明改用 `gh`
  - 套件管理改用 `pnpm` 而非 `npm` → 明確聲明
- 原則：只列 Claude 不會主動採用、但你要求採用的工具

## 動態更新 CLAUDE.md（Update as You Build）

- 來自 Claude Code 創作者本身的工作流：`CLAUDE.md` 應當是會持續被改寫、累積經驗的活檔案
- 規則寫法：當使用者指出實作錯誤時，Claude 必須
  1. 先依使用者指示修正
  2. 接著把這次的教訓寫入專屬的知識檔，建立「不要做什麼／正確做法」的累積知識庫
- 後續任務 Claude 可回頭參考這份知識，不重複犯同樣錯誤

## Git Commit Safety（不可逆指令需確認）

- 規則：不可逆指令在執行前必須先取得使用者同意
- 典型危險指令：`git push --force`、`git reset --hard HEAD`、merge branch、`rm -rf` 之類的強制刪除
- 若 Claude 不確定指令是否具破壞性 → 要求它停下來問，而非自行判斷
- 實際效果：避免 agent 在無人確認下合併錯誤分支或覆寫遠端歷史

## Path-Scoped Rule Files（路徑作用域規則）

- 把所有規則塞進單一 `CLAUDE.md` 會讓檔案膨脹，並讓 agent 在不相關任務時被無關規則干擾
- 做法：建立分檔規則，第一行宣告適用範圍（scope），內含針對該範圍的指示
- 在主 `CLAUDE.md` 提及這些檔案的位置即可，不重複貼內容
- 例：API 相關規則放在 API 模組底下的規則檔；Claude 動到 API 才載入，動其他模組時不載入
- 益處：減少 context bloat，agent 只看到當下任務需要的指令

## Monorepo 用 Scoped CLAUDE.md

- 大型 monorepo 各子專案職責不同，全部塞進根 `CLAUDE.md` 會干擾 agent 的注意力
- 規則：每個子 repo 自帶 `CLAUDE.md`，內容只談自身模組
- 根 `CLAUDE.md` 只放跨整個系統都適用的通則
- agent 進入對應子目錄時，自動載入該層的局部規則，行為更聚焦

## Project Description First（專案描述放最前面）

- 在 `CLAUDE.md` 開頭就寫清楚整個專案在做什麼
- 內容包含：應用整體目的、結構、主要服務與依賴、執行方式
- 讓 agent 第一時間建立 mental model，不必透過讀程式去猜整體脈絡

## Verify, Don't Just Check（要驗證，不只是檢查存在）

- 完成任務的標準不只是「程式碼存在」，而是「功能實際運作正常」
- 規則：使用所有可用的驗證機制（unit test、lint、type check）確認 build 與測試皆通過後才能回報完成
- 強迫 Claude 用真實驗證步驟回報，避免「程式存在 = 任務完成」的誤報

## Order by Priority（依優先級排列）

規則的書寫順序會直接影響 agent 遵循度，必須由高至低排：

1. **Hard rules**：永不可違反、零例外的硬規則 → 放最前面
2. **Medium priority**：重要但可協商的規則 → 居中
3. **Low priority**：純參考、便利資訊 → 放最後，不應作為核心決策依據

## 長度上限：300 行

- 建議的最佳長度上限為 300 行
- 超過後 agent 表現會開始下降（context bloat / attention dilution）
- 透過 path-scoped rule files 與 scoped `CLAUDE.md` 來分散內容、控制總長

## 實作 Checklist

整理本影片的可直接套用要點：

- [ ] 開頭放 project description（用途、結構、主要依賴、執行方式）
- [ ] 加入 think before coding：要求列出假設、列出多種解讀
- [ ] 加入 simplicity first：含 200/50 行重寫硬門檻
- [ ] 加入 surgical changes：dead code 只回報不修
- [ ] 加入 goal-driven execution：強制定義 verifiable goal
- [ ] UI 任務指定使用 Chrome extension / Puppeteer MCP 驗證
- [ ] Tool overrides：列出非預設工具（如 `gh`、`pnpm`）
- [ ] 自我更新規則：錯誤修正後要寫入知識檔
- [ ] Git commit safety：不可逆指令需確認
- [ ] 拆分 path-scoped rule files；monorepo 每個子 repo 自帶 `CLAUDE.md`
- [ ] Verify-not-just-check：用 lint / typecheck / 測試實際驗證
- [ ] 規則按 hard → medium → low 排序
- [ ] 控制總長 < 300 行
