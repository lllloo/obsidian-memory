"""更新頻道 01.index.md 的 last_sync_id 與 updated 欄位（跨平台，取代 sed -i）。

用法（cwd = repo root）：
    python3 .agents/skills/vault-youtube-sync/scripts/update_checkpoint.py "feeds/youtube/<頻道名>/01.index.md" <NEW_ID> <TODAY>

僅在本次有新影片且頻道內已無 draft 時呼叫；無新影片或仍有 draft 時保留 checkpoint。
"""
import os
import re
import sys
from pathlib import Path

# print 的 OK 行含中文頻道路徑，Windows cp950 會炸，強制 UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

if len(sys.argv) < 4:
    sys.exit("ERROR: usage update_checkpoint.py <index_path> <new_id> <today>")
if not os.path.isfile("schema/vault-map.md"):
    sys.exit("ERROR: cwd 不在 repo root，中止 checkpoint 更新")

path, new_id, today = sys.argv[1], sys.argv[2], sys.argv[3]
if not os.path.isfile(path):
    sys.exit(f"ERROR: 找不到 index 檔：{path}")

index = Path(path)
text = index.read_text(encoding="utf-8")
text, n_id = re.subn(r"^last_sync_id: .*", f"last_sync_id: {new_id}", text, flags=re.MULTILINE)
text, n_upd = re.subn(r"^updated: .*", f"updated: {today}", text, flags=re.MULTILINE)
# re.sub 沒命中會靜默不換：欄位缺失時 checkpoint 沒更新卻回報 OK，下次同步重複處理
missing = [name for name, n in (("last_sync_id", n_id), ("updated", n_upd)) if n == 0]
if missing:
    sys.exit(f"ERROR: {path} frontmatter 缺 {'、'.join(missing)} 欄位，checkpoint 未更新")
index.write_text(text, encoding="utf-8")
print(f"OK: {path} last_sync_id={new_id} updated={today}")
