"""列出某頻道資料夾中「已有非 draft 完整筆記」的 videoId（每行一個）。

用法（cwd = repo root）：
    python3 .agents/skills/vault-youtube-sync/scripts/noted_ids.py "Inbox/YouTube/<頻道名>"

供 SKILL 步驟 2 的 Source URL 去重用：把輸出的 ID 集合與待處理清單比對，
移除已出現在非 draft 筆記 source 欄位的影片。draft 占位**不算**去重命中
（要留給 subagent 覆寫重抓），故跳過。
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

# cwd 必為 vault root：cwd 錯時 notes_dir 解不到 → 誤回空集合 → 去重失效重建重複筆記
if not os.path.isfile("vault-map.md"):
    sys.exit("ERROR: cwd 不在 vault root（找不到 vault-map.md）")

notes_dir = sys.argv[1] if len(sys.argv) > 1 else ""
if not notes_dir or not os.path.isdir(notes_dir):
    raise SystemExit(0)

for f in sorted(os.listdir(notes_dir)):
    if not f.endswith(".md") or f == "01.index.md":
        continue
    text = open(os.path.join(notes_dir, f), encoding="utf-8").read()
    if re.search(r"^draft:\s*true", text, re.M):
        continue  # draft 占位讓 subagent 重抓覆寫，不去重
    m = re.search(r"^source: https://www\.youtube\.com/watch\?v=([A-Za-z0-9_-]+)", text, re.M)
    if m:
        print(m.group(1))
