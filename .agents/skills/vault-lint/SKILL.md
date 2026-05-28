---
name: vault-lint
description: Vault 健檢：掃描孤立頁面、死連結、Inbox 積壓、tag 同義異寫、frontmatter 缺欄位、Topics 缺 index.md、vault-map 未收錄、extracted_to 遺留等問題。列出報告後互動確認，等用戶拍板再修。使用時機：使用者說「健檢」、「lint」、「vault 健康檢查」、「掃問題」、「vault 狀態」，或直接呼叫 /vault-lint。
---

# /vault-lint — Vault 健檢

掃描 → 列分類報告 → 等用戶拍板 → 修。

## 前置條件

```bash
[ -f "vault-map.md" ] || { echo "ERROR: cwd 不在 vault root"; exit 1; }
```

check 失敗就停止，告知用戶 cd 到 vault root。

## 掃描項目（依序執行，全部跑完再統一報告）

### 1. Inbox 積壓

```bash
find Inbox -name "*.md" ! -path "Inbox/Updates/*" | wc -l
```

- > 50 → 嚴重
- > 20 → 警告
- ≤ 20 → 正常

### 2. extracted_to 遺留

```bash
rg 'extracted_to:' Inbox --glob "*.md" -l
```

列出半消化 Inbox 筆記（有 `extracted_to` = 還有剩餘段落）。

### 3. Frontmatter 缺欄位

```bash
# 缺 title（Cards/ Topics/ 正式筆記）
rg --files-without-match '^title:' Cards Topics --glob "*.md" 2>/dev/null

# 缺 tags（排除 index.md，index 頁允許不加 tags）
rg --files-without-match '^tags:' Cards Topics --glob "*.md" --glob "!index.md" 2>/dev/null

# 缺 updated
rg --files-without-match '^updated:' Cards Topics --glob "*.md" 2>/dev/null
```

### 4. Topics 資料夾缺 index.md

```bash
for d in Topics/*/; do
  [ -f "${d}index.md" ] || echo "$d"
done
```

### 5. vault-map 未收錄的 Topics

```bash
for d in Topics/*/; do
  name=$(basename "$d")
  grep -q "$name" vault-map.md || echo "$name"
done
```

### 6. Tag 同義異寫

```bash
rg -oI '^\s+- "?[A-Za-z0-9_-]+"?\s*$' . --glob "*.md" | sed 's/^[[:space:]]*- //;s/^"//;s/"$//;s/[[:space:]]*$//' | sort | uniq -c | sort -rn | head -60
```

輸出 top 60 英數 tag 及使用次數，讓用戶肉眼辨識同義異寫（如 `claude-code` vs `claudeCode`）。regex 支援帶引號形式（`  - "clippings"`），sed 剝除外層引號後與裸值合併統計。用 `-oI`（only-matching + no-filename），**勿用 `-oh`**——`-h` 會被當 `--help` 而印出 ripgrep 說明。

### 7. 孤立頁面（無入站 wikilink）

Topics 孤立 = 異常（升級主題理應連成網）；Cards 孤立 = 常態（吸收型卡片盒允許單張存在），僅供新建時補連結參考，**不視為待修問題**。掃描指令對兩者皆跑，但報告時分層標記（見報告格式）。

對 Cards/ 與 Topics/ 下所有 .md（排除 index.md）確認有無被引用：

```bash
for f in $(find Cards Topics -name "*.md" ! -name "index.md" 2>/dev/null); do
  title=$(basename "$f" .md)
  rg -ql "\[\[$title" . --glob "*.md" 2>/dev/null || echo "$f"
done
```

### 8. 死連結（wikilink 目標不存在）

```bash
rg -oI '\[\[[^]|#]+' . --glob "*.md" | sed 's/.*\[\[//' | sort -u | while IFS= read -r t; do
  t="$(echo "$t" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  [ -z "$t" ] && continue
  case "$t" in *"<"*) continue;; esac          # 跳過 schema 佔位符如 [[<整合頁名>]]
  base="${t##*/}"                                # 取 basename，容許帶路徑 wikilink
  if [[ "$base" == *.base ]]; then
    find . -name "$base" 2>/dev/null | grep -q . || echo "[[${t}]]"
  else
    find . -name "${base}.md" 2>/dev/null | grep -q . || echo "[[${t}]]"
  fi
done
```

> 用 `-oI`，**勿用 `-oh`**（`-h` = `--help`）。判定已排除三類誤報：schema 佔位符 `[[<...>]]`、帶路徑 wikilink（取 basename 比對）、`.base` 連結（按副檔名比對）。

### 9. 規範資料夾實體存在

`vault-map.md` 列出的常設資料夾必須存在（git 不追蹤空目錄，清空後資料夾會消失）。

```bash
required_dirs=(
  "Inbox"
  "Inbox/Clippings"
  "Inbox/Updates"
  "Inbox/YouTube"
  "Cards"
  "Topics"
)

for d in "${required_dirs[@]}"; do
  [ -d "$d" ] || echo "$d"
done
```

報告為 🟡 警告。自動修補：`mkdir -p <dir> && touch <dir>/.gitkeep`。

> 動態子資料夾（`Inbox/YouTube/<頻道>/`、`Topics/<主題>/`）不在此檢查；前者隨 sync 變動，後者已由 #5 vault-map 未收錄檢查覆蓋。

### 10. description 缺失

`CLAUDE.md` schema 規定必有 `description` 的三類筆記，若缺欄位列出（要求由 Web Clipper / vault-youtube-sync skill 範本帶入；漏掉代表手動建檔未補）：

- `Topics/<主題>/index.md` — 全部
- `Inbox/Clippings/*.md` — 全部
- `Inbox/YouTube/<頻道>/*.md` — 排除 `01.index.md`

```bash
{
  for d in Topics/*/; do echo "${d}index.md"; done
  ls Inbox/Clippings/*.md 2>/dev/null
  find Inbox/YouTube -name "*.md" ! -name "01.index.md" 2>/dev/null
} | while IFS= read -r f; do
  [ -f "$f" ] && ! grep -q '^description:' "$f" && echo "$f"
done
```

報告為 🔴 嚴重（規範必填）。修補需手動寫 30–80 字摘要，不自動產生。

> 書籤型與判斷型 Cards 不在此檢查（規範明訂不加 description，靠第一段定位段）。

### 11. Frontmatter 欄位順序錯亂 / 白名單外游離欄位

`CLAUDE.md` schema 規定欄位採白名單與固定順序：`title` > `description` > `created` > `updated` > `source` > `published` > `parent` > `last_sync_id` > `draft` > `extracted_to` > `tags`。本檢查抓兩類問題：
1. **ORDER**：實際出現的白名單欄位相對順序不符
2. **ROGUE**：出現白名單外的欄位（如 `author`、`category`）

```bash
whitelist="title description created updated source published parent last_sync_id draft extracted_to tags"

find Cards Topics Inbox -name "*.md" 2>/dev/null | while IFS= read -r f; do
  keys=$(awk '/^---[[:space:]]*$/{c++; if(c==2) exit; next} c==1 && /^[a-zA-Z_][a-zA-Z0-9_]*:/{sub(/:.*/, ""); print}' "$f")
  [ -z "$keys" ] && continue

  rogue=""
  inwl=""
  while IFS= read -r k; do
    [ -z "$k" ] && continue
    case " $whitelist " in
      *" $k "*) inwl="$inwl$k"$'\n' ;;
      *) rogue="$rogue $k" ;;
    esac
  done <<< "$keys"
  [ -n "$rogue" ] && echo "ROGUE $f:$rogue"

  expected=$(printf '%s' "$inwl")
  sorted=$(printf '%s' "$inwl" | awk -v wl="$whitelist" '
    BEGIN{n=split(wl,a," "); for(i=1;i<=n;i++) ord[a[i]]=i}
    NF{print ord[$0]"\t"$0}
  ' | sort -n | cut -f2)
  [ "$expected" != "$sorted" ] && echo "ORDER $f"
done
```

報告為 🟡 警告。

- ORDER 修補：手動調整欄位順序，不自動動（順序錯亂常意味手動編輯時失誤，需逐篇確認）
- ROGUE 修補：白名單外欄位無語意，需人工判斷該補進白名單還是刪除

## 報告格式

掃描完畢後**統一輸出**分類報告：

```
## Vault 健檢報告（YYYY-MM-DD）

### 🔴 嚴重（N 項）
- 死連結：[[xxx]]、[[yyy]]
- 缺 title：Cards/foo.md
- 缺 description：Inbox/Clippings/foo.md
- Topics/bar/ 無 index.md

### 🟡 警告（N 項）
- Inbox 積壓：42 篇（> 20）
- 孤立 Topics：Topics/foo/bar.md（升級主題卻無入站連結）
- vault-map 未收錄：SomeTopic
- 規範資料夾遺漏：Inbox/Clippings
- frontmatter 欄位順序 / 白名單外欄位：ORDER Cards/foo.md、ROGUE Cards/bar.md: author
- extracted_to 遺留：Inbox/abc.md

### 🔵 資訊（N 項）
- 孤立 Cards：7 張（吸收型卡片盒，孤立可接受；摺疊成數量，不逐張列）
- 缺 updated：N 篇
- tag 同義異寫候選：（列出疑似重複的 tag 對）
```

## 互動確認

報告後**逐類**列出「可自動修補」vs「需人工判斷」：

**可自動修補（問用戶是否執行）：**
- 補 Topics 缺失的 index.md（建含基本 frontmatter 的空白檔）
- 在 vault-map 補收錄缺漏的 Topics
- 補缺失的 `updated` 欄位（設為今日日期）
- 補回規範資料夾遺漏（`mkdir -p <dir> && touch <dir>/.gitkeep`）

**需人工判斷（只列出，不自動動）：**
- 孤立頁面 — **Topics 孤立**才需處置（補連結／檢查升級是否成立）；Cards 孤立預設保留，除非用戶主動要連。
- 死連結 — 改外部 URL？刪 wikilink？補建目標頁？
- tag 同義異寫 — 哪個是正典？
- frontmatter 欄位順序 / 白名單外欄位 — ORDER 手動調整欄位順序；ROGUE 判斷該補進白名單還是刪除
- extracted_to 遺留 — 何時消化剩餘段落？
- Inbox 積壓 — 批次清理時機由用戶自選
- description 缺失 — 需手動寫 30–80 字摘要，不自動產生

**執行前給用戶看確認，確認後才動檔。一次修一個類別。**

## 執行方式

直接在主 agent 執行以上 bash 命令，輸出同格式報告，互動確認同規則。
