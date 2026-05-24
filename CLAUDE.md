# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Obsidian Memory Vault — 吸收型卡片盒

**本檔涵蓋**：Vault 內容規則——卡片盒哲學、Inbox/Cards/Topics 工作流、寫入前 Checklist、frontmatter schema、tag/命名、敏感資料。
**不涵蓋**：Quartz 部署（不在本 repo 範圍）。

## 三條原則

此 vault 採用「吸收型卡片盒」，核心如下：

1. **吸收並內化** — 筆記是「我理解的版本」，不是別人說法的保存
2. **不留原料，留參考資料** — Inbox 抄錄整篇消化完刪除（多主題筆記允許保留未消化段落，加 `extracted_to` 標記指回 MOC）；Card 保留參考資料（來源網址等），用於回查原文，不作為證據
3. **正確 + 不斷更新** — Card 可覆寫、永不定稿（持續修改）

**一句話：Vault 是腦的延伸，不是倉庫。**

## Vault 結構（三層成熟度）

| 資料夾           | 角色                                | 成熟度 | 生命週期                                  |
| ---------------- | ----------------------------------- | ------ | ----------------------------------------- |
| `Inbox/`         | AI 抄錄的外部原料                   | 未消化 | 暫存，消化完刪除                          |
| `Cards/`         | 未歸屬的完整概念 Card               | 待歸類 | 累積同主題或裂變後批次搬進 Topics/<主題>/ |
| `Topics/<主題>/` | 已歸檔的完整概念 Cards + 主題入口頁 | 已歸檔 | 長期，可持續覆寫                          |

## 三層工作流

### Inbox → Cards（消化）

三條清空路徑：

- A. 寫新 Card（放 `Cards/`） — 真有新啟發（少數）
- B. 強化既有 Card / Topic 內容 — 呼應舊想法（多數）
- C. 直接刪除 — 沒學到新東西、品質差（多數）

三條都以「刪除 Inbox/ 原篇」作結。Inbox 空 = 無積欠。

路徑 A、B 寫 Card 時，按既有慣例附上來源連結（回查用）。

**多主題例外**：若 Inbox 筆記同時涵蓋多個主題、本次整理只內化其中一個切角，允許從原筆記移除已內化段落、保留剩餘段落，並在 frontmatter 加 `extracted_to: "[[<MOC 名>]]"` 指回 MOC。半消化筆記仍是 Inbox 的「待消化」狀態，鼓勵下次同主題整理時再消化剩餘。

### Cards → Topics/<主題>/（歸檔）

**Card = 完整概念**（獨立可讀，不需搭配其他筆記或原文就能理解），不是零碎斷句。兩種批次觸發：

- **A. 同主題累積**：多張同主題 Cards 一起搬
- **B. Card 裂變**：單張長大後拆成多張，同時搬

動作：

1. 找到或建立 `Topics/<主題>/` 資料夾（含 `index.md` 作為主題入口頁）
2. **一次 `git mv` 整組 Cards** 搬入 `Topics/<主題>/`（內容不動）
3. 在 `index.md` 補上 wikilink 清單

跨主題靠 `tags` 串連：`Topics/` 第一層不做跨主題巢套（不建「AI-工具/Claude-Code/」這種群組）；單一主題內 Cards 過多時，可在 `Topics/<主題>/` 底下再分子資料夾。

升 Topic 前的品質門檻、退回 Cards 的反指標：見 repo 根 [`topics-review.md`](topics-review.md)。**已升 Topic 重看時若命中反指標，可隨時退回**。

### 防爆量

- Inbox 靠「消化完刪除」
- Cards 靠「成批搬走」
- Topics 靠「第一層不跨主題聚合 + 主題數有限」

不靠紀律，靠流動。

## 寫入前 Checklist（所有 agent 寫入 vault 前必做）

寫入 `.md` 前必須自檢。這是 vault 健康的唯一防線——任何修改 vault 內容的流程（`/ob` 寫入流程、其他 skills、手動編輯）在寫入前逐項檢查。

> 注意：vault 內容會公開發佈，敏感資料一節（下方 §1）尤其零容忍。

### 1. 敏感資料（零容忍）

寫入前掃正文與 frontmatter，確認不含：

- **Token / Key**：`sk-`、`sk-ant-`、`ghp_`、`gho_`、`AKIA`、`AIza`、`xox[baprs]-`、`eyJ`（JWT）
- **Private key header**：`-----BEGIN ... PRIVATE KEY-----`
- **自然語言密碼**：「密碼是 …」、「password: …」後接明文
- **客戶 / 公司內部資訊、個資**：身分證、私人電話、地址、內部 IP / 網址

命中 → 移除或告知使用者中止，不寫入。若發現既有筆記含有敏感資料，立即移除並通知用戶。

### 2. Tag 沿用既有

寫入前先查現有 tags（`obsidian tags`，或 `rg -A5 '^tags:' . -g '*.md'`），優先沿用，避免製造同義異寫（`claude-code` vs `claudeCode` vs `claude_code`）。真無合適才建新 tag，小寫、`-` 連接。

### 3. 命名

檔名不含空格，空格一律改為 `-`（例：`Obsidian-CLI-整合指南.md`）；wikilink 對應實際檔名（含 `-`）。`title:` 用主題名，不加日期前綴。

### 4. Frontmatter schema

`.md` frontmatter 欄位採白名單與固定順序；新增欄位前先確認既有筆記是否已使用。

建議順序：

1. `title`
2. `created`
3. `updated`
4. `source`
5. `published`
6. `parent`
7. `last_sync_id`
8. `draft`
9. `extracted_to`
10. `tags`

必要欄位：一般筆記需有 `title`、`created`、`updated`、`tags`；`index.md` 作為公開首頁可不加 `tags`。`tags` 一律用 YAML list，不用 inline array 或字串。

## 規則

### Wikilink

寫入 wikilink 前確認目標檔案實際存在；不存在就改用外部 URL，不留死連結。（語法細節：`.base` 連結加副檔名、值含 `[[...]]` 用雙引號包，見下方對應節。）

### Commit

不自動 commit。除非使用者明確要求，否則只彙整變更交使用者審核，不在流程中自動提交。

### 查詢回存（提議，不自動）

查詢或討論結束時，若這次產出了有複利價值的綜合分析（比較、取捨結論、發現的連結），**主動提議「要不要回存成 Card?」**——不自動寫，也不默默讓它蒸發。使用者拍板才寫。判斷節點：這次結論下次會不會被重問?會 → 提議回存；一般唯讀查詢、閒聊不必每次都問。

此規則是「禁止不請自來寫 vault、建檔須使用者授權」的延伸：把「自動回存」降級成「提議回存」，授權權留在使用者手上，agent 只負責偵測「這段值得留」並提醒。

### Obsidian Bases（.base 檔案）

- wikilink 必須加副檔名：`[[02.影片清單.base]]`，不加會找不到檔案
- embed 同理：`![[02.影片清單.base]]`
- `.base` 檔案的內容**不會在圖譜產生連結**，這是 Obsidian 已知限制
- 要讓筆記出現在圖譜中，需在筆記 frontmatter 加 `parent` property 指向 index：
  ```yaml
  parent: "[[01.index]]"
  ```

### 色碼與特殊符號

- `#` 開頭的內容（如 hex 色碼 `#57F287`）在 Obsidian 會被解讀為 tag，**必須用反引號包住**：`` `#57F287` ``

### `updated` 欄位（盡力而為）

修改 `.md` 內容時**盡量**同步 frontmatter 的 `updated` 為今日日期（`YYYY-MM-DD`），但不強制 — 偶爾漂移可接受，不需為此中斷流程或裝 hook。

## YouTube 筆記語言規範

所有 YouTube 影片筆記正文內容一律以**繁體中文**撰寫。

- 技術名詞、品牌名、工具名保留英文（例：Claude Code、OpenAI、defuddle）
- 若 defuddle 取得英文 transcript，需翻譯整理為繁體中文後再寫入筆記

## 查詢規則

查詢相關知識時：

1. 先讀 `master-index.md` 確認資料位置（含完整 Tag 查詢指南）
2. 主題筆記 → 對應 `Topics/` 子目錄
3. 影片摘要 → 依主題選對應 `Inbox/YouTube/<頻道>/`
4. 跨主題 → Grep 搜尋 tag：`rg -A5 '^tags:' . -g '*.md'`

## 可用 Skills

本 repo 在 `.agents/skills/`（`.claude/skills` 為 symlink）提供以下 skill：

| Skill | 用途 |
|---|---|
| `ob` | 筆記建立／查詢分派入口 |
| `vault-distill` | 多筆記整合為 MOC |
| `vault-youtube-sync` | YouTube 影片摘要同步至 Inbox |
| `vault-updates-daily` | 日常更新彙整 |

**共用契約**：所有 vault skills 要求 **cwd 必須是 vault root**（本 repo 根目錄，底下直接有 `master-index.md`）。路徑都是 cwd-relative，不依賴環境變數。呼叫前若 cwd 不對，skill 會用以下 check 主動停止：

```bash
[ -f "master-index.md" ] || { echo "ERROR: cwd 不在 vault root"; exit 1; }
```

從別的專案想呼叫，需先 `cd` 到本 repo 根目錄。

## Cards → Topics 升級限制

**升 Topic 不由 agent 自主執行**。流程：

1. 列出候選 Cards + 對照 `topics-review.md` 的 5 條保留條件 + 反指標
2. 給出傾向與理由
3. 等使用者拍板後才執行 `git mv`

改寫優於直接決定；改寫後必須重跑審核再決定。
