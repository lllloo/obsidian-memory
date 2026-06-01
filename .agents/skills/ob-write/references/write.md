# Vault 寫入流程

執行 Obsidian vault 寫入任務：建立筆記、追加內容、改 frontmatter。

**查詢不是此流程的工作** — 查詢請走 `/ob-read`。若被誤派查詢任務，回覆「查詢請改走 /ob-read」並停止。

呼叫端（`ob-write` SKILL.md）會在 prompt 標明 `MODE=local` 或 `MODE=cross`。**先依模式跑 §1 前置 gate**，通過後 §2–§5 建檔與驗證大致共用，差異處會標註模式。

---

## §1. 模式前置 gate（先做，未通過不得寫入）

> **shell 註記**（兩模式皆適用）：`obsidian` 在 PowerShell 經 PATHEXT 可直接用；Git Bash 不認 `.com`，會 `command not found`——此時改用 `Obsidian.com <cmd>` 或 `powershell.exe -Command "obsidian ..."`，不要把它誤判成「CLI 不可用」而中止。

### MODE=local（cwd 已在 vault root）

本模式契約是 **cwd 必須是 vault root**（底下直接有 `vault-map.md`、`Cards/`、`Topics/`）。所有路徑 cwd-relative。

```bash
[ -f "vault-map.md" ] || { echo "ERROR: cwd 不在 vault root，請 cd 到 obsidian-memory；或在其他專案改用跨專案模式"; exit 1; }
```

- 失敗就停止，不要猜測寫到別的地方。
- vault 身分天然確定（`vault-map.md` 在 = 就是這個 vault），不需額外比對 path。
- 讀 vault 規則（見 §2）：CLI 可用 `obsidian read file="CLAUDE.md"`，不可用 `Read CLAUDE.md`（cwd-relative）。
- 工具策略：**CLI 優先，不可用降級 Write/Edit**（見 §3）。

### MODE=cross（cwd 在其他專案）

cwd 不在 vault，只能靠 obsidian CLI 定位與寫入。下列 gate **全部通過才可寫入；任一失敗即中止、不寫檔、不降級**：

1. **CLI 可用**：
   ```bash
   obsidian vault 2>&1; echo "EXIT=$?"
   ```
   exit 0 且有輸出 vault path → 通過；其他（非 0 / 127 / 空輸出）→ 中止，提示使用者啟用 Obsidian CLI（設定 → General → Command line interface 並重開 terminal）。

2. **vault 身分**：CLI 回傳的 vault path 正規化後（大小寫、分隔符、尾斜線）必須 `== C:\code\obsidian-memory`。不符 → 中止（避免寫進錯的 vault）。

3. **規則讀取**：
   ```bash
   obsidian read file="CLAUDE.md"
   ```
   成功且內容含錨點（字串「寫入前 Checklist」與「Frontmatter schema」）→ 通過；讀取失敗或缺錨點 → 中止。

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
| vault 檔案內容讀寫（建檔、append、改 frontmatter/tags） | 一律 obsidian CLI；CLI 不可用才降級 Write/Edit | **一律 obsidian CLI；不可用即中止** |
| CLI 無對應操作（rename、batch regex、精準 old_string 局部修改） | 可用 `mv`/Write/Edit fallback，事後提醒 reload | 不做（提示使用者回 repo 處理） |
| 查找/確認 vault 檔是否存在 | Glob/Grep/Read | 經 CLI（`obsidian read`/`obsidian search`） |
| 當前工作目錄的非 vault 檔（程式碼、文件） | Glob/Grep/Read/Edit/Write 皆可 | 同左（非 vault 不受限） |

判斷原則：**有 obsidian CLI 指令就用 CLI**（確保 Obsidian 即時感知變更）。`MODE=local` 不要因「Write 比較方便」就繞過 CLI。降級走 Write/Edit 後，提醒使用者在 Obsidian 內 `Ctrl+P → Reload app without saving`。

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

`content=` 直接帶完整 frontmatter（含 tags YAML 清單），**不要事後用 `property:set` 設 tags**（會變 inline 字串）。frontmatter 依 CLAUDE.md 的 Frontmatter schema 與 §6。

建檔優先 **stdin 傳入**，不要把多行 frontmatter 塞進 `content='...'`（字面 `\n` 解碼行為依 CLI 版本未定義）：

```bash
printf '%s\n' "---" "title: <標題>" "created: <今日>" "updated: <今日>" "tags:" "  - <tag1>" "---" \
  | obsidian create path="Cards/<標題>.md" --stdin open
```

`open` 旗標會在 Obsidian UI 開檔：`MODE=local`（人就在 vault）保留以利確認；`MODE=cross`（人在他專案）省略 `open`，避免無預警彈開 vault UI。

若該版 CLI 不支援 `--stdin`，退走 `content=` 行內版，但**呼叫後必須 `obsidian read file=...` 驗證 frontmatter 真為多行**。

**寫入後驗證（一律檢查，不可只看「無 error」）**——CLI 把「建檔」與「寫內容」當兩步，Windows/沙箱下 `--stdin` 可能斷掉留 0 bytes 空檔。驗證機制**依模式分流**：CLI 的 `file=`/`path=` 一律 vault-relative、跨 cwd 也定位得到；filesystem 路徑只在 cwd=vault root 時才解得到。

### MODE=local（cwd=vault root，可用 filesystem）

vault-relative 路徑在此模式天然有效，用檔案工具確認：

- 檔案存在且內容非空——`Read "Cards/<標題>.md"` 能看到完整 frontmatter（或等效 filesystem 檢查，能跑就好，不綁特定 shell）。
- 驗證失敗 → 降級 Write 直寫，繼續完成；如實告知走 fallback。

### MODE=cross（嚴格 CLI，禁碰 filesystem）

cwd 不在 vault，filesystem 既解不到 vault 路徑、又違反本模式「不降級」契約，**只能經 CLI 驗證**：

```bash
obsidian read file="Cards/<標題>.md"   # file= 為 vault-relative，CLI 自行定位
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
