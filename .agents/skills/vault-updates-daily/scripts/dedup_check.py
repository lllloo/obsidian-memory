"""判斷某 source URL 是否已在 vault 出現過（daily updates 去重，fixed-string 比對）。

用法（cwd = repo root）：
    python dedup_check.py "<url>" [<YYYY-MM-DD>]

兩層檢查：
  1. 舊個別筆記格式：Inbox/Updates / Cards / Topics 任一 .md 含 `source: <url>`
  2. 當日日報：Inbox/Updates/<date>-daily-updates.md 正文含 <url>（日期參數提供時）

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
except AttributeError:
    pass

if len(sys.argv) < 2:
    print("UNIQUE")
    raise SystemExit(0)

url = sys.argv[1]
date = sys.argv[2] if len(sys.argv) > 2 else ""
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

# 2. 當日日報正文
if date:
    daily = Path(f"Inbox/Updates/{date}-daily-updates.md")
    if daily.is_file():
        try:
            if url in daily.read_text(encoding="utf-8", errors="replace"):
                print(f"DUP:{daily.as_posix()}")
                raise SystemExit(0)
        except OSError:
            pass

print("UNIQUE")
