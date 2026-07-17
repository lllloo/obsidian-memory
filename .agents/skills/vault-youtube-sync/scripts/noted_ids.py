"""列出某頻道資料夾中的 videoId（每行一個）。

用法（cwd = repo root）：
    python3 .agents/skills/vault-youtube-sync/scripts/noted_ids.py "feeds/youtube/<頻道名>"
    python3 .agents/skills/vault-youtube-sync/scripts/noted_ids.py --draft "feeds/youtube/<頻道名>"

預設輸出非 draft 完整筆記，供 Source URL 去重；`--draft` 改為輸出
draft 占位，供 checkpoint 過濾後強制納回重試，以及收尾判斷是否可以推進 checkpoint。
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

# cwd 必為 vault root：cwd 錯時 notes_dir 解不到 → 誤回空集合 → 去重失效重建重複筆記
if not os.path.isfile("schema/vault-map.md"):
    sys.exit("ERROR: cwd 不在 vault root（找不到 schema/vault-map.md）")

draft_only = len(sys.argv) > 1 and sys.argv[1] == "--draft"
arg_pos = 2 if draft_only else 1
notes_dir = sys.argv[arg_pos] if len(sys.argv) > arg_pos else ""
if not notes_dir or not os.path.isdir(notes_dir):
    raise SystemExit(0)

for f in sorted(os.listdir(notes_dir)):
    if not f.endswith(".md") or f == "01.index.md":
        continue
    try:
        with open(os.path.join(notes_dir, f), encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        # 單檔讀取失敗（權限/鎖定）不中斷整體去重，但要留訊號供排查
        print(f"WARN: 讀取失敗，略過 {f}: {exc}", file=sys.stderr)
        continue
    is_draft = bool(re.search(r"^draft:\s*true", text, re.M))
    if is_draft != draft_only:
        continue
    m = re.search(r"^source: https://www\.youtube\.com/watch\?v=([A-Za-z0-9_-]+)", text, re.M)
    if m:
        print(m.group(1))
