# Vault 寫入流程

執行 Obsidian vault 寫入任務：建立筆記、追加內容、改 frontmatter。

**查詢不是此流程的工作** — 查詢請走 `/ob-read`。若被誤派查詢任務，回覆「查詢請改走 /ob-read」並停止。

呼叫端（`ob-write` SKILL.md）會在 prompt 標明 `MODE=local` 或 `MODE=cross`。**先依模式跑 §1 前置 gate**，通過後 §2–§5 建檔與驗證大致共用，差異處會標註模式。

---

## §1. 模式前置 gate（先做，未通過不得寫入）

> **shell 註記**（兩模式皆適用）：`obsidian` 在 PowerShell 經 PATHEXT 可直接用；Git Bash 不認 `.com`，會 `command not found`——此時改用 `Obsidian.com <cmd>` 或 `powershell.exe -Command "obsidian ..."`，不要把它誤判成「CLI 不可用」而中止。

### MODE=local（cwd 已在 vault root）

本模式契約是 **cwd 必須是 vault root**（底下直接有 `vault-map.md`、`Cards/`、`Topics/`）。所有路徑 cwd-relative。

用 `Read vault-map.md` 確認存在（讀得到 → local 確立；讀不到 → 停止，不要猜測寫到別處，請 cd 到 obsidian-memory，或在其他專案改用跨專案模式）。**此檢查走 harness-native 工具，不經 shell、不分 PowerShell/bash。**

- 讀不到就停止，不要猜測寫到別的地方。
- vault 身分天然確定（`vault-map.md` 在 = 就是這個 vault），不需額外比對 path。
- 讀 vault 規則（見 §2）：CLI 可用 `obsidian read file="CLAUDE.md"`，不可用 `Read CLAUDE.md`（cwd-relative）。
- 工具策略：**CLI 優先，不可用降級 Write/Edit**（見 §3）。

### MODE=cross（cwd 在其他專案）

cwd 不在 vault，只能靠 obsidian CLI 定位與寫入。下列 gate **全部通過才可寫入；任一失敗即中止、不寫檔、不降級**：

1. **CLI 可用**：執行 `obsidian vault`（PowerShell；Git Bash 用 `Obsidian.com vault`）。exit 0 且印出 vault path → 通過；非 0 / 找不到指令 / 空輸出 → 中止，提示使用者啟用 Obsidian CLI（設定 → General → Command line interface 並重開 terminal）。

2. **vault 身分**：CLI 回傳的 vault path 正規化後（大小寫、分隔符、尾斜線）必須 `== C:\code\obsidian-memory`。不符 → 中止（避免寫進錯的 vault）。

3. **規則讀取**：
   ```
   obsidian read file="CLAUDE.md"
   ```
   （shell 差異同上：Git Bash 用 `Obsidian.com read ...`）成功且內容含錨點（字串「寫入前 Checklist」與「Frontmatter schema」）→ 通過；讀取失敗或缺錨點 → 中止。

- 工具策略：**嚴格 CLI，無 Write/Edit 降級**。
- 無論 §2 的 CLAUDE.md 是否讀到，**§6 的 inline 最小保護一律生效**。
- 不做歸檔 / `git mv`（§7 僅 local）。

---

## §2. 讀 vault 規則

CLAUDE.md 是 vault 規則的唯一來源，此 reference 不重複內嵌完整規則（§6 的最小保護除外）。subagent 進場自己讀一次，確保規則到位：

- `MODE=local`：CLI 可用 → `obsidian read file="CLAUDE.md"`；否則 `Read CLAUDE.md`。
- `MODE=cross`：§1 gate 3 已讀到，直接沿用。

依 CLAUDE.md 的「寫入前 Checklist」逐項自檢（敏感資料、frontmatter schema、tag 沿用、命名），通過才寫入。

---

## §3. 工具使用規則

| 操作 | MODE=local | MODE=cross |
|---|---|---|
| 建檔（新檔） | **用 Write 直寫**（不經 shell、最可靠，見 §5） | obsidian CLI 的 `content=`（不用 stdin pipe）；不可用即中止 |
| append / 改 frontmatter/tags | obsidian CLI 優先；不可用降級 Edit | **一律 obsidian CLI；不可用即中止** |
| CLI 無對應操作（rename、batch regex、精準 old_string 局部修改） | 可用 `mv`/Write/Edit fallback，事後提醒 reload | 不做（提示使用者回 repo 處理） |
| 查找/確認 vault 檔是否存在 | Glob/Grep/Read | 經 CLI（`obsidian read`/`obsidian search`） |
| 當前工作目錄的非 vault 檔（程式碼、文件） | Glob/Grep/Read/Edit/Write 皆可 | 同左（非 vault 不受限） |

判斷原則：**能用 harness-native 工具（Glob/Read/Write/Grep/Edit）就用它**——不經 shell、不分 PowerShell/bash，沒有「挑錯 shell」失敗點。只有兩件事真需 shell：(1) `obsidian` CLI（要 Obsidian 即時感知變更，harness 工具做不到）、(2) 真需 pipeline 的聚合。落 shell 時範例直接寫對某一支（標 PowerShell / Git Bash），別寫含糊版讓模型臨場翻譯。走 Write/Edit 改 vault 檔後，提醒使用者 `Ctrl+P → Reload app without saving`。

---

## §4. 建檔位置判斷

依來源決定位置：

| 來源 | 位置 |
|---|---|
| 個人想法（「我想到」「我認為」「筆記一下」） | `Cards/<標題>.md` |
| 外部來源抄錄（網頁剪貼、影片摘要） | `Inbox/<類別>/<標題>.md`（如 `Inbox/Clippings/`、`Inbox/YouTube/<頻道>/`） |
| 已知歸屬主題（使用者明確指定主題） | `Topics/<主題>/<標題>.md` |

優先採用使用者明示的位置；未明示時依上述判斷。

> **MODE=cross 輕量原則**（跨專案寫入必守）：只收束這次真正值得留下的重點 + 必要回查線索（原專案、檔案、指令、關鍵字）；不要把整段對話、完整 log、一次性過程或未整理的外部資料倒進 vault。整理成 Card／升 Topic 留待回 vault 本地 session 再做。此原則 subagent 在跨專案時讀不到全域 rules，故於此自包含。

建立筆記前先蒐集素材：優先用對話上下文；無上下文時可 Glob/Grep 瀏覽當前專案檔案，或上網搜尋（WebSearch/WebFetch）補料，避免空殼筆記。

> 此「寫筆記前素材蒐集」的 WebSearch，與全域協議「查詢分派階段不額外觸發 web」不衝突——後者指分派階段，前者是 subagent 內部寫作補料，兩件事。

---

## §5. 建檔與寫入後驗證

frontmatter 含完整 tags YAML 清單，依 CLAUDE.md 的 Frontmatter schema 與 §6；tags 直接寫進 frontmatter 文字，**不要事後用 `obsidian property:set` 補**（會變 inline 字串）。

建檔機制依模式分流，主軸是**避開 shell 脆弱點**——Windows 上 stdin 經 `.com` redirector 餵 obsidian 已知會留 0 bytes 空檔，且 shell 語法 PowerShell/bash 不通用：

#### MODE=local 建檔 → 用 Write

filesystem 寫入百分百可靠、不經 shell。**直接 `Write "Cards/<標題>.md"` 帶完整 frontmatter + 正文**，不走 `obsidian create`（stdin/CLI 多一次必然偶爾失敗的往返）。Obsidian file watcher 通常自動抓到外部新檔；沒更新就提醒 `Ctrl+P → Reload app without saving`。要 app 立刻開該檔可選 `obsidian open file="Cards/<標題>.md"`（Git Bash 用 `Obsidian.com open ...`）。

#### MODE=cross 建檔 → 用 `content=` 參數，不用 stdin pipe

cross 不能 Write，只能 CLI，但**避開 stdin pipe**（redirector 透傳不穩）。用 `content=` 帶整段內容：

- PowerShell：**直接在字串內用 `` `n `` 換行**，不要先存進多行變數再展開——多行 here-string 變數展開後經 CLI redirector 會丟內容：
  ```powershell
  obsidian create path="Cards/<標題>.md" content="---`ntitle: <標題>`ntags:`n  - foo`n---`n正文"
  ```
- Git Bash：`Obsidian.com create path="Cards/<標題>.md" content="---\ntitle: <標題>\n---\n正文"`

省略 `open`（人在他專案，別彈 vault UI）。寫入後必走下方驗證。

**寫入後驗證（一律檢查，不可只看「無 error」）**——cross 經 CLI 寫入時，驗證才能確認內容有確實寫進去。驗證機制**依模式分流**：CLI 的 `file=`/`path=` 一律 vault-relative、跨 cwd 也定位得到；filesystem 路徑只在 cwd=vault root 時才解得到。

### MODE=local（cwd=vault root，可用 filesystem）

建檔走 Write，工具寫失敗會直接報錯；仍 `Read "Cards/<標題>.md"` 確認一次，看得到完整 frontmatter + 正文即過——不經 shell、不分 PowerShell/bash。

### MODE=cross（嚴格 CLI，禁碰 filesystem）

cwd 不在 vault，filesystem 既解不到 vault 路徑、又違反本模式「不降級」契約，**只能經 CLI 驗證**：

```
obsidian read file="Cards/<標題>.md"   # file= 為 vault-relative，CLI 自行定位（Git Bash 用 Obsidian.com）
```

- 回傳內容非空、且含 frontmatter 錨點（開頭 `---` 與 `title:`）→ 通過。
- 讀取失敗 / 空內容 / 缺錨點 → **中止並如實回報**（附 CLI 輸出），不降級。

完成後回應：「已建立筆記《標題》✓」+ 路徑（+ 模式 / 是否降級）。

---

## §6. inline 最小保護（不可跳過）

`MODE=cross` 必套（即使 §2 的 CLAUDE.md 沒讀到也生效）；`MODE=local` 亦遵守（與 CLAUDE.md 一致）。

**敏感資料零容忍** — 正文與 frontmatter 不得含：
- Token/Key：`sk-`、`sk-ant-`、`ghp_`、`gho_`、`AKIA`、`AIza`、`xox[baprs]-`、`eyJ`（JWT）
- Private key header：`-----BEGIN ... PRIVATE KEY-----`
- 明文密碼（「密碼是…」「password: …」後接明文）
- 客戶/公司內部資訊、個資（身分證、私人電話、地址、內部 IP/網址）

命中：本次寫入剔除敏感片段後再寫；無法拆解則中止並告知使用者。

**最低 frontmatter** — `title`、`created`、`updated`、`tags`（YAML list，不用 inline array/字串）；檔名不含空格（空格改 `-`）；wikilink 必須對應實存檔案，否則改外部 URL。

---

## §7. 歸檔協助模式（僅 MODE=local）

使用者說「這張 Card 歸到 X 主題」「把這幾張搬到 Y」時：

1. 確認或建立 `Topics/<主題>/`（含 `index.md` 主題入口）。
2. 每張 Card：`git mv "Cards/<標題>.md" "Topics/<主題>/<標題>.md"`（內容不動）。
3. 提示在 `Topics/<主題>/index.md` 補 wikilink 清單。
4. 批次搬完一次回報。搬移後 `git status` 應顯示 `R`（rename）。

`MODE=cross` 不提供歸檔，提示使用者回 repo（cwd=vault root）處理。
