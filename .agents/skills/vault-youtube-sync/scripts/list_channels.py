"""模式 B：列出所有已建 index 的頻道 source URL（每行一個 @handle URL）。

用法（cwd = repo root）：
    python3 .agents/skills/vault-youtube-sync/scripts/list_channels.py

掃 raw/YouTube/*/01.index.md，從 frontmatter 的 source: 抽 @handle 頻道 URL。
"""
import glob
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

# cwd 必為 vault root：cwd 錯時 glob 靜默空 → 模式 B 誤判「無既有頻道」
if not os.path.isfile("CLAUDE.md"):
    sys.exit("ERROR: cwd 不在 vault root（找不到 CLAUDE.md）")

for idx in sorted(glob.glob("raw/YouTube/*/01.index.md")):
    with open(idx, encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"^source:\s*(https://www\.youtube\.com/@[^/\s]+)", text, re.M)
    if m:
        print(m.group(1))
