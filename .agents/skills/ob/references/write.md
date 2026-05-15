# Vault 寫入流程

執行 Obsidian vault 寫入任務：建立筆記、追加內容、改 frontmatter。

**查詢不是此流程的工作** — `/ob` skill 會把查詢分派給 `references/query.md`，不會路由到此處。若被誤派，回覆「查詢請改走 query 流程」並停止。

實際時序：**路徑解析（env 檢查）→ CLI 偵測 → 讀 vault 規則 → 判斷位置 → 寫入 → 驗證**。下列各段照此順序排列。

## 1. Vault 路徑解析（必先執行）

`$OBSIDIAN_VAULT_ROOT` 必須指向 repo 的 `content/` 目錄（也就是底下直接有 `master-index.md`、`Cards/`、`Topics/`）。env 未設或該路徑底下找不到 `master-index.md` → 告知用戶「`$OBSIDIAN_VAULT_ROOT` 未設或無效，設定方式見 README」並停止，不要猜測寫到錯誤位置。

CLI 路徑與 Write/Edit fallback 路徑都需要這條檢查。CLI 可用時 `obsidian create path="Cards/..."` 雖可自動定位 vault，但 env 不正確時建檔位置仍會偏（CLI 也讀同一份 env）。一律先檢查 env，再走後續步驟。

走 Write/Edit fallback 時，`Cards/<標題>.md` 會被當 cwd-relative，從其他專案呼叫會寫到錯地方，**fallback 路徑必須用絕對路徑**（以 `$OBSIDIAN_VAULT_ROOT` 為 base）。

若任務需要執行 git 操作（例如歸檔搬移），先解析 repo root：

```bash
REPO_ROOT=$(git -C "$VAULT_ROOT" rev-parse --show-toplevel 2>/dev/null)
```

解析失敗時不要用 cwd-relative 路徑猜測；改用絕對路徑 fallback，並提醒使用者在 Obsidian reload。

## 2. CLI 可用性偵測（第一次寫入前必做）

Obsidian CLI 依賴 macOS XPC/IPC，沙箱模式會擋；Windows Git Bash 有時回 exit 127。**不偵測就直衝 CLI 會 silently fail，然後誤報成功**。

Session 首次需要寫入時，先跑一次輕量探測：

```bash
obsidian vault 2>&1; echo "EXIT=$?"
```

- `EXIT=0` 且有輸出 vault 路徑 → CLI 可用，走 CLI 路徑（下方「工具使用規則」優先順序 1）
- 其他（exit 非 0、127、空輸出）→ CLI 不可用，**全程改走 Write/Edit fallback**，並在首次使用時告知用戶：
  > 「obsidian CLI 不可用（可能沙箱模式或未安裝），改用 Write 直寫檔案。完成後請在 Obsidian 按 `Ctrl+P → Reload app without saving` 讓實例感知變更。」

本 session 內偵測一次即可，結果自己記著。

## 3. 前置作業（讀 vault 規則）

**為什麼要讀 CLAUDE.md：**
此流程可能從任何工作目錄被呼叫（不一定在 obsidian-memory 目錄下）。若直接在 obsidian-memory 目錄工作，CLAUDE.md 會自動載入為 system context；但透過 `/ob` 從其他專案呼叫時，必須自己讀取 CLAUDE.md 才能取得 vault 規則。CLAUDE.md 是 vault 規則的唯一來源，此 reference 不重複內嵌這些規則，以避免兩者不同步。

1. 取得 vault 規則：
   - CLI 可用 → `obsidian read file="CLAUDE.md"`
   - CLI 不可用（偵測失敗）→ `Read $OBSIDIAN_VAULT_ROOT/CLAUDE.md`
2. 每次寫入前依 CLAUDE.md 的「寫入前 Checklist」逐項自檢（敏感資料、frontmatter schema、tag 沿用、命名），通過才寫入；這是寫入路徑的主要職責，不要把規則預防外包給 `/vault-check`

## 4. 工具使用規則（依優先順序）

前提：步驟 2 的 CLI 可用性偵測通過。若偵測失敗，全部跳到 fallback。

1. **vault 檔案內容讀寫**（建檔、追加、改 frontmatter、改 tags）：**一律 Bash 執行 obsidian CLI**，確保 Obsidian 能即時感知變更
2. **Obsidian CLI 無對應的操作**（如重命名、批次 regex 替換、需要精準 old_string 匹配的局部修改）：可用 Bash `mv` 或 Write/Edit 當 fallback。**事後提醒用戶**在 Obsidian 內執行 `Ctrl+P → Reload app without saving` 讓實例感知變更
3. **查找或確認 vault 檔案是否存在**：Glob/Grep/Read
4. **當前工作目錄的非 vault 檔案**（程式碼、文件）：Glob/Grep/Read/Edit/Write 皆可

判斷原則：**有 obsidian CLI 指令就用 CLI**，沒有才 fallback。不要因「Write 比較方便」就繞過 CLI。

## 5. 建檔位置判斷

依來源決定檔案位置：

| 來源                                             | 位置                                                                       |
| ------------------------------------------------ | -------------------------------------------------------------------------- |
| 個人想法（「我想到」、「我認為」、「筆記一下」） | `Cards/<標題>.md`                                                          |
| 外部來源抄錄（網頁剪貼、影片摘要）               | `Inbox/<類別>/<標題>.md`（如 `Inbox/Clippings/`、`Inbox/YouTube/<頻道>/`） |
| 已知歸屬主題（使用者明確指定主題）               | `Topics/<主題>/<標題>.md`                                                  |

優先採用使用者明示的位置；未明示時依上述判斷。

## 6. 建立新筆記

建立筆記前，先蒐集內容素材：

1. **優先使用對話上下文** — 若用戶已提供主題說明或內容，直接採用
2. **無上下文時自行補充** — 可用 Glob/Grep 瀏覽當前工作專案的檔案取得脈絡，或上網搜尋（WebSearch/WebFetch），確保筆記內容有實質內容，不要建空殼筆記
   - 注意：此 WebSearch 是「寫筆記前的素材蒐集」，與全域協議「`/ob` 不做 WebSearch」不衝突——後者指的是「分派階段不額外觸發 web 並行查詢」，跟 subagent 內部寫作補料是兩件事

```bash
obsidian tags                    # 查看現有 tags
```

建立筆記時，`content=` 直接帶入完整 frontmatter（含 tags YAML 清單），**不要事後用 `property:set` 設定 tags**（會產生 inline 字串格式）。frontmatter 格式依 `content/CLAUDE.md` 的「Frontmatter Schema」與「寫入前 Checklist」。

建檔一律優先從 **stdin 傳入內容**，不要把多行 frontmatter 塞進 `content='...'` 參數——字面 `\n` 是否被 CLI 解成換行是未定義行為（依 obsidian CLI 版本而異），stdin 方式行為穩定。

**POSIX shell（macOS / Linux / Windows Git Bash 通用）**：

```bash
printf '%s\n' "---" "title: <標題>" "created: <今日>" "updated: <今日>" "tags:" "  - <tag1>" "---" \
  | obsidian create path="Cards/<標題>.md" --stdin open
```

若 obsidian CLI 該版不支援 `--stdin`，退而走 `content=` 行內版本，但需記住：PowerShell/Bash 單引號內的字面 `\n` 在不同 shell 與 CLI 版本的解碼行為不同，會讓 frontmatter 壞成單行字串。退到 `content=` 方案時，**呼叫後必須 `obsidian read file=...` 驗證 frontmatter 真的是多行**。

> ⚠ 不論走 `--stdin` 或 `content=`，呼叫完都要跑下一節「寫入後驗證」的 size 檢查（≥ 10 bytes），不可只看 exit code。Windows 環境 `--stdin` 已知會 silent fail 留 0 bytes 空檔。

建立後若需追加正文內容，再用 `append`。

規則：

- 命名、tags、frontmatter 格式等規則依 CLAUDE.md 執行
- 完成後回應：「已建立筆記《標題》✓」+ 路徑

## 7. 每次寫入後驗證

CLI 呼叫後**一律檢查 exit code、檔案存在、且檔案非空**，不要信任「沒 error 訊息 = 成功」。

**重點：CLI 把「建檔」與「寫內容」當兩個獨立步驟。** Windows / 沙箱等環境下 `--stdin` 管道可能斷掉但建檔成功，留下 0 bytes 空檔。只檢查 `-f` 會漏掉這種 silent failure，**必須加 size 檢查**：

```bash
FILE="<vault_root>/Cards/<標題>.md"
printf '%s\n' "---" "title: ..." "---" "正文" | obsidian create path="Cards/<標題>.md" --stdin open
EXIT=$?
SIZE=$(wc -c < "$FILE" 2>/dev/null || echo 0)
if [ $EXIT -ne 0 ] || [ ! -f "$FILE" ] || [ "$SIZE" -lt 10 ]; then
  echo "CLI 建檔失敗或檔案空（exit=$EXIT, size=$SIZE），降級為 Write"
  # 用 Write 直寫，並提示用戶 reload
fi
```

驗證三項缺一不可：

1. `EXIT == 0`
2. 檔案存在（`-f`）
3. **檔案大小 > 10 bytes**（純 frontmatter 都會超過 10 bytes，0 bytes 一定是 stdin 沒灌進去）

失敗降級後繼續完成任務，不要中止；但回報時要如實告知用戶走了 fallback 路徑，並附上實際 byte 數作為證據。

## 8. 歸檔協助模式

當使用者說「這張 Card 我想歸到 X 主題」、「幫我把這幾張搬到 Y 主題」等類似需求時：

1. 確認或建立 `Topics/<主題>/` 資料夾（含 `index.md` 作為主題入口頁）
2. 對每張指定 Card 優先執行 `git -C "$REPO_ROOT" mv "content/Cards/<標題>.md" "content/Topics/<主題>/<標題>.md"`（保持內容不動）
3. 提示使用者在 `Topics/<主題>/index.md` 補上對應的 wikilink 清單
4. 若是批次搬多張（同主題累積或 Card 裂變），一次處理完再回報

搬移後 `git status` 應顯示為 `R`（rename），不是 `D` + `A`。
