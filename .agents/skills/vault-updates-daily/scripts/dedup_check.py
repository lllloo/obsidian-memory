"""判斷某 source URL 是否已在 vault 出現過（daily updates 去重，fixed-string 比對）。

用法（cwd = repo root）：
    python3 .agents/skills/vault-updates-daily/scripts/dedup_check.py "<url>" [<YYYY-MM-DD>]

兩層檢查：
  1. 舊個別筆記格式：Inbox/Updates / Cards / Topics 任一 .md 含 `source: <url>`
  2. 所有日報正文：Inbox/Updates/*-daily-updates.md 任一含 <url>（日報是合併格式、無
     source: 欄位，改以 inline URL 比對；掃全部日報而非當天，否則前幾天已報過的條目對
     去重隱形 → 重複寫入）。日期參數現為相容保留，不再用來限制掃描範圍。

輸出：
    DUP:<命中檔案相對路徑>   （第一個命中即印出）
    UNIQUE                    （皆未命中）

用 fixed-string（非 regex）比對，避開 URL 裡 ?、& 等 regex metachar。
"""
import os
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

# cwd 必為 vault root：cwd 錯時 rglob 會靜默空集合 → 誤回 UNIQUE 放行重複；hard-fail 較安全
if not Path("vault-map.md").is_file():
    sys.exit("ERROR: cwd 不在 vault root（找不到 vault-map.md）")

if len(sys.argv) < 2:
    print("UNIQUE")
    raise SystemExit(0)

url = sys.argv[1]
needle = f"source: {url}"

# 1. 個別筆記格式
for base in ("Inbox/Updates", "Cards", "Topics"):
    root = Path(base)
    if not root.is_dir():
        continue
    for p in sorted(root.rglob("*.md")):
        try:
            if needle in p.read_text(encoding="utf-8", errors="replace"):
                print(f"DUP:{p.as_posix()}")
                raise SystemExit(0)
        except OSError:
            continue

# 2. 所有日報正文（合併格式，inline URL 比對；掃全部日報而非當天，否則前幾天已報過的條目會重複）
updates_dir = Path("Inbox/Updates")
if updates_dir.is_dir():
    for p in sorted(updates_dir.glob("*-daily-updates.md")):
        try:
            if url in p.read_text(encoding="utf-8", errors="replace"):
                print(f"DUP:{p.as_posix()}")
                raise SystemExit(0)
        except OSError:
            continue

print("UNIQUE")
