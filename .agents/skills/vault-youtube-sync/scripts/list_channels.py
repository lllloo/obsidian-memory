"""模式 B：列出所有已建 index 的頻道 source URL（每行一個 @handle URL）。

用法（cwd = repo root）：
    python list_channels.py

掃 Inbox/YouTube/*/01.index.md，從 frontmatter 的 source: 抽 @handle 頻道 URL。
"""
import glob
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

for idx in sorted(glob.glob("Inbox/YouTube/*/01.index.md")):
    text = open(idx, encoding="utf-8").read()
    m = re.search(r"^source:\s*(https://www\.youtube\.com/@[^/\s]+)", text, re.M)
    if m:
        print(m.group(1))
