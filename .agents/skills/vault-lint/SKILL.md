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
rg -oI '^\s+- [A-Za-z0-9_-]+\s*$' . --glob "*.md" | sed 's/^[[:space:]]*- //;s/[[:space:]]*$//' | sort | uniq -c | sort -rn | head -60
```

輸出 top 60 英數 tag 及使用次數，讓用戶肉眼辨識同義異寫（如 `claude-code` vs `claudeCode`）。用 `-oI`（only-matching + no-filename），**勿用 `-oh`**——`-h` 會被當 `--help` 而印出 ripgrep 說明。

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

## 報告格式

掃描完畢後**統一輸出**分類報告：

```
## Vault 健檢報告（YYYY-MM-DD）

### 🔴 嚴重（N 項）
- 死連結：[[xxx]]、[[yyy]]
- 缺 title：Cards/foo.md
- Topics/bar/ 無 index.md

### 🟡 警告（N 項）
- Inbox 積壓：42 篇（> 20）
- 孤立 Topics：Topics/foo/bar.md（升級主題卻無入站連結）
- vault-map 未收錄：SomeTopic
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

**需人工判斷（只列出，不自動動）：**
- 孤立頁面 — **Topics 孤立**才需處置（補連結／檢查升級是否成立）；Cards 孤立預設保留，除非用戶主動要連。
- 死連結 — 改外部 URL？刪 wikilink？補建目標頁？
- tag 同義異寫 — 哪個是正典？
- extracted_to 遺留 — 何時消化剩餘段落？
- Inbox 積壓 — 批次清理時機由用戶自選

**執行前給用戶看確認，確認後才動檔。一次修一個類別。**

## 執行方式

直接在主 agent 執行以上 bash 命令，輸出同格式報告，互動確認同規則。
