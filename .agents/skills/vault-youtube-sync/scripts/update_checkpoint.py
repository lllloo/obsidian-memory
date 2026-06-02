"""更新頻道 01.index.md 的 last_sync_id 與 updated 欄位（跨平台，取代 sed -i）。

用法（cwd = repo root）：
    python3 .agents/skills/vault-youtube-sync/scripts/update_checkpoint.py "Inbox/YouTube/<頻道名>/01.index.md" <NEW_ID> <TODAY>

僅在本次有新影片時呼叫；無新影片不需更新 checkpoint。
"""
import os
import re
import sys

# print 的 OK 行含中文頻道路徑，Windows cp950 會炸，強制 UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

if len(sys.argv) < 4:
    sys.exit("ERROR: usage update_checkpoint.py <index_path> <new_id> <today>")
if not os.path.isfile("vault-map.md"):
    sys.exit("ERROR: cwd 不在 repo root，中止 checkpoint 更新")

path, new_id, today = sys.argv[1], sys.argv[2], sys.argv[3]
if not os.path.isfile(path):
    sys.exit(f"ERROR: 找不到 index 檔：{path}")

text = open(path, encoding="utf-8").read()
text = re.sub(r"^last_sync_id: .*", f"last_sync_id: {new_id}", text, flags=re.MULTILINE)
text = re.sub(r"^updated: .*", f"updated: {today}", text, flags=re.MULTILINE)
open(path, "w", encoding="utf-8").write(text)
print(f"OK: {path} last_sync_id={new_id} updated={today}")
