"""核對批次完整性後，更新頻道 index 的 checkpoint（跨平台）。

用法（cwd = repo root）：
    python3 .agents/skills/vault-youtube-sync/scripts/update_checkpoint.py \
      "feeds/youtube/<頻道名>/01.index.md" <TODAY> --new-id=<NEW_ID> \
      --expected=<videoId> [--expected=<videoId> ...] \
      [--filtered=<videoId> ...] [--unavailable=<videoId> ...]

完整性核對是此更新器不可繞過的內建條件；漏項、draft、重複來源、讀取錯誤
或參數不一致時，檔案維持原樣。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from verify_batch import verify_batch

# print 的 OK 行含中文頻道路徑，Windows cp950 會炸，強制 UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("index_path", help="頻道 01.index.md 路徑")
    parser.add_argument("today", help="updated 日期（YYYY-MM-DD）")
    parser.add_argument(
        "--new-id", required=True, help="要寫入的最新 videoId"
    )
    parser.add_argument(
        "--expected",
        action="append",
        required=True,
        help="本輪 checkpoint ledger 的 videoId；每支重複傳入一次",
    )
    parser.add_argument(
        "--filtered",
        action="append",
        default=[],
        help="依內容規則明確篩除的 videoId；可重複",
    )
    parser.add_argument(
        "--unavailable",
        action="append",
        default=[],
        help="video_meta 明確判定 unavailable 的 videoId；可重複",
    )
    args = parser.parse_args()

    if not Path("schema/vault-map.md").is_file():
        print("ERROR: cwd 不在 repo root，中止 checkpoint 更新")
        return 2

    index = Path(args.index_path)
    if not index.is_file():
        print(f"ERROR: 找不到 index 檔：{index}")
        return 2

    try:
        original_text = index.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR:read-index:{index}:{exc}")
        print("VERIFY:blocked")
        return 2

    current_match = re.search(
        r"^last_sync_id:\s*(.*)$", original_text, flags=re.MULTILINE
    )
    current_id = current_match.group(1).strip() if current_match else None
    if args.new_id not in set(args.expected) and args.new_id != current_id:
        print(f"ERROR:config:new-id-not-expected-or-current:{args.new_id}")
        print("VERIFY:blocked")
        return 2

    ready, lines = verify_batch(
        index.parent, args.expected, args.filtered, args.unavailable
    )
    print("\n".join(lines))
    if not ready:
        print("ERROR: checkpoint 未更新，批次終態核對未通過")
        return 2

    # 只有舊 draft 重試時，最新影片本來就等於現有 checkpoint。整批核對仍要跑，
    # 但通過後 index 應保持逐 byte 不變，不把 retry 誤報成一次 checkpoint 更新。
    if args.new_id == current_id:
        print(f"NOOP: {index} last_sync_id 已是 {args.new_id}，checkpoint 未變")
        return 0

    text = original_text
    text, n_id = re.subn(
        r"^last_sync_id: .*",
        f"last_sync_id: {args.new_id}",
        text,
        flags=re.MULTILINE,
    )
    text, n_upd = re.subn(
        r"^updated: .*", f"updated: {args.today}", text, flags=re.MULTILINE
    )
    # re.sub 沒命中會靜默不換：欄位缺失時 checkpoint 沒更新卻回報 OK，
    # 下次同步會重複處理。
    missing = [
        name
        for name, count in (("last_sync_id", n_id), ("updated", n_upd))
        if count == 0
    ]
    if missing:
        print(
            f"ERROR: {index} frontmatter 缺 {'、'.join(missing)} 欄位，"
            "checkpoint 未更新"
        )
        return 2

    index.write_text(text, encoding="utf-8")
    print(
        f"OK: {index} last_sync_id={args.new_id} updated={args.today}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
