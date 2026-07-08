# Vault 寫入流程

執行 Obsidian vault 寫入任務：建立筆記、追加內容、改 frontmatter。

**查詢不是此流程的工作** — 查詢請走 `/ob-read`。若被誤派查詢任務，回覆「查詢請改走 /ob-read」並停止。

呼叫端（`ob-write` SKILL.md）會在 prompt 標明 `MODE=local` 或 `MODE=cross`。**先依模式跑 §1 前置 gate**，通過後 §2–§5 建檔與驗證大致共用，差異處會標註模式。

---

## §1. 模式前置 gate（先做，未通過不得寫入）

### MODE=local（cwd 已在 vault root）

本模式契約是 **cwd 必須是 vault root**（底下直接有 `vault-map.md`、`raw/`、`wiki/`）。所有路徑 cwd-relative。

用 `Read vault-map.md` 確認存在（讀得到 → local 確立；讀不到 → 停止，不要猜測寫到別處，請 cd 到 obsidian-memory，或在其他專案改用跨專案模式）。**此檢查走 harness-native 工具，不經 shell、不分 PowerShell/bash。**

- 讀不到就停止，不要猜測寫到別的地方。
- vault 身分天然確定（`vault-map.md` 在 = 就是這個 vault），不需額外比對 path。
- 讀 vault 規則（見 §2）：`Read CLAUDE.md`（cwd-relative）。
- 工具策略：**harness-native 工具直寫（Write/Edit）**（見 §3）。

### MODE=cross（cwd 在其他專案）

cwd 不在 vault，走**定位鏈**找本機 clone：`Read` 固定路徑 `~/code/obsidian-memory/vault-map.md`（`~` 先展開為當前使用者 home 絕對路徑；Windows 即 `%USERPROFILE%\code\obsidian-memory\vault-map.md`），讀到且內容含錨點 `title: Vault Map` 即驗明身分（harness-native，不經 shell、不依賴 obsidian CLI）。此路徑是**唯一候選**，不在它之外猜路徑；此約定與全域 `~/.claude/rules/obsidian.md`、ob-read `references/query.md` 同步維護，改一處要三處同改。

**命中**：`$VAULT_ROOT` = 該 clone 根目錄，後續寫入用檔案工具**直寫該 clone**（Write/Edit 帶 `$VAULT_ROOT` 絕對路徑），**不 commit、不 push**。接著讀規則：`Read $VAULT_ROOT/CLAUDE.md`，成功且內容含錨點（字串「Karpathy LLM Wiki」與「Frontmatter schema」）→ 通過；讀取失敗或缺錨點 → 中止。

**找不到**：**中止**，不寫檔、不降級寫到別處、不做任何 fallback——跨專案寫入沒有任何遠端寫入路徑。提示使用者對齊路徑：尚未 clone → `git clone https://github.com/lllloo/obsidian-memory ~/code/obsidian-memory`（Windows 目標寫 `%USERPROFILE%\code\obsidian-memory`）；clone 在別處 → 建連結（Windows `mklink /J "%USERPROFILE%\code" "C:\code"`、WSL `ln -s /mnt/c/code ~/code`）。

- 無論 §2 的 CLAUDE.md 是否讀到，**§6 的 inline 最低慣例一律生效**。

---

## §2. 讀 vault 規則

CLAUDE.md 是 vault 規則的唯一來源，此 reference 不重複內嵌完整規則（§6 的最低慣例除外）。subagent 進場自己讀一次，確保規則到位：

- `MODE=local`：`Read CLAUDE.md`（cwd-relative）。
- `MODE=cross`：§1 已讀 `$VAULT_ROOT/CLAUDE.md`，直接沿用。

依 CLAUDE.md「寫入慣例」章節逐項自檢（frontmatter schema、tag 沿用、命名、wikilink），確認後才寫入。這些是寫作慣例，不是拍板 gate——vault 唯一人工守門是 `git push`，本流程不做額外守門。

---

## §3. 工具使用規則

| 操作 | MODE=local | MODE=cross |
|---|---|---|
| 建檔（新檔） | **用 Write 直寫**（不經 shell、最可靠，見 §5） | **用 Write 直寫**（帶 `$VAULT_ROOT` 絕對路徑，見 §5） |
| append / 改 frontmatter/tags | Edit 直改 | Edit 直改（帶 `$VAULT_ROOT` 絕對路徑） |
| rename、batch regex、精準 old_string 局部修改 | `mv`/Write/Edit，事後提醒 reload | 不做（提示使用者回 repo 處理） |
| 查找/確認 vault 檔是否存在 | Glob/Grep/Read | Glob/Grep/Read 帶 `path=$VAULT_ROOT` |
| 當前工作目錄的非 vault 檔（程式碼、文件） | Glob/Grep/Read/Edit/Write 皆可 | 同左（非 vault 不受限） |

判斷原則：**一律用 harness-native 工具（Glob/Read/Write/Grep/Edit）**——不經 shell、不分 PowerShell/bash，沒有「挑錯 shell」失敗點。obsidian CLI 唯一剩餘用途是 `MODE=local` 寫完後選用 `obsidian open`（見 §5），CLI 不可用不影響任何流程。走 Write/Edit 改 vault 檔後，Obsidian file watcher 通常自動抓到；沒更新就提醒使用者 `Ctrl+P → Reload app without saving`。

---

## §4. 建檔位置判斷

依內容性質決定位置：

| 內容性質 | 位置 |
|---|---|
| 外部原料（網頁剪貼、貼上的文章、影片摘要等未經消化的原文/摘錄） | `raw/<類別>/<標題>.md`（依既有子夾慣例，如 `raw/Clippings/`、`raw/YouTube/<頻道>/`；無對應子夾就近建立） |
| 需要 agent 綜合/內化成知識頁（摘要、實體、概念、比較、綜合） | `wiki/<標題>.md`，並更新 `wiki/01.index.md`（新頁登錄一行摘要 + wikilink，避免孤立頁） |

**絕不寫入 `Cards/` 或 `Topics/`**——那是使用者私人策展區，同時是 Quartz 唯一公開層，agent 一律不寫、不掃描。若使用者明確要求把內容寫進 `Cards/` 或 `Topics/`，先提醒這點並請使用者確認是否要破例；使用者確認後才照做。

優先採用使用者明示的位置；未明示時依上述判斷。

> **MODE=cross 輕量原則**（跨專案寫入必守）：只收束這次真正值得留下的重點 + 必要回查線索（原專案、檔案、指令、關鍵字）；不要把整段對話、完整 log、一次性過程或未整理的外部資料倒進 vault。整理成 wiki 頁留待回 vault 本地 session 再做。此原則 subagent 在跨專案時讀不到全域 rules，故於此自包含。

建立筆記前先蒐集素材：優先用對話上下文；無上下文時可 Glob/Grep 瀏覽當前專案檔案，或上網搜尋（WebSearch/WebFetch）補料，避免空殼筆記。

> 此「寫筆記前素材蒐集」的 WebSearch，與全域協議「查詢分派階段不額外觸發 web」不衝突——後者指分派階段，前者是 subagent 內部寫作補料，兩件事。

---

## §5. 建檔與寫入後驗證

frontmatter 含完整 tags YAML 清單，依 CLAUDE.md 的 Frontmatter schema 與 §6；tags 直接寫進 frontmatter 文字。

建檔兩模式都用 **Write**（filesystem 寫入不經 shell、百分百可靠，沒有 PowerShell/bash 方言差異），路徑依 §4 判斷（`raw/<類別>/<標題>.md` 或 `wiki/<標題>.md`）：

- `MODE=local`：`Write "<路徑>"`（cwd-relative）帶完整 frontmatter + 正文；寫入 `wiki/` 時另用 Edit 同步更新 `wiki/01.index.md`。
- `MODE=cross`：`Write "$VAULT_ROOT/<路徑>"`（絕對路徑）帶完整 frontmatter + 正文；寫入 `wiki/` 時同樣更新 `$VAULT_ROOT/wiki/01.index.md`。

**寫入後驗證（一律檢查，不可只看「無 error」）**：`Read` 剛寫的檔（cross 帶 `$VAULT_ROOT` 絕對路徑），看得到完整 frontmatter（開頭 `---` 與 `title:`）+ 正文即過；讀取失敗／內容缺損 → **中止並如實回報**，不盲目重寫。

Obsidian file watcher 通常自動抓到外部新檔；沒更新就提醒 `Ctrl+P → Reload app without saving`。`MODE=local` 要 app 立刻開該檔可選 `obsidian open file="<路徑>"`（PowerShell 直接 `obsidian`；Git Bash 不認 `.com`，用 `Obsidian.com open ...`）；`MODE=cross` 省略 `open`（人在他專案，別彈 vault UI）。

完成後回應：「已建立筆記《標題》✓」+ 路徑（+ 模式）。

---

## §6. inline 最低慣例（cross 模式 fallback）

`MODE=cross` 用：即使 §1/§2 已讀到 `$VAULT_ROOT/CLAUDE.md` 的完整「寫入慣例」，此處仍列最低要求防漏讀；`MODE=local` 直接以 CLAUDE.md「寫入慣例」為準，此處僅供對照。

**最低 frontmatter** — `title`、`created`、`updated`、`tags`（YAML list，不用 inline array/字串）；檔名不含空格（空格改 `-`）；wikilink 必須對應實存檔案，否則改外部 URL。

這些是寫作慣例、不是拍板 gate——vault 唯一人工守門是 `git push`，本流程不做敏感資料自檢等額外攔截。
