#!/usr/bin/env python3
"""為 vault-lint 語意層選出每日穩定、跨日輪替的頁面批次。

從 git log 取得近 N 天變動的 wiki 內容頁，依最新變動順序分成固定大小
批次，再用日期決定當天批次。穩定的頁面集合會在連續 K 天內完整覆蓋，
其中 K = ceil(頁數 / cap)；腳本本身不寫入任何檔案。

輸出格式：

  SEMANTIC:<file>            本輪應審頁面
  DEFERRED:<file>            本輪未審、由後續日期輪替覆蓋的頁面
  SUMMARY:semantic=<count>   本輪應審頁數
  SUMMARY:deferred=<count>   本輪未審頁數
  SUMMARY:batch=<i>/<total>  當日批次（1-based；無頁面時為 0/0）
  SELECT:complete            選頁正常完成；缺少此行或出現 ERROR 即視為異常

用法：
  python3 .agents/skills/vault-lint/scripts/semantic_select.py \
    --days 7 --cap 10 --date 2026-07-18 --utc-offset +08:00
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable


sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def positive_int(raw: str) -> int:
    value = int(raw)
    if value < 1:
        raise argparse.ArgumentTypeError("必須是正整數")
    return value


def iso_date(raw: str) -> date:
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("日期格式必須是 YYYY-MM-DD") from exc


def utc_offset(raw: str) -> str:
    match = re.fullmatch(r"([+-])(\d{2}):(\d{2})", raw)
    if not match:
        raise argparse.ArgumentTypeError("UTC offset 格式必須是 +HH:MM 或 -HH:MM")
    hours, minutes = int(match.group(2)), int(match.group(3))
    if hours > 23 or minutes > 59:
        raise argparse.ArgumentTypeError("UTC offset 超出有效範圍")
    return raw


def discover_changed_pages(
    root: Path, days: int, on_date: date, offset: str
) -> list[str]:
    """依最近一次變動由新到舊列出仍存在的 wiki 內容頁。"""
    if days < 1:
        raise ValueError("days 必須是正整數")
    window_start = on_date - timedelta(days=days - 1)
    since = f"{window_start.isoformat()}T00:00:00{offset}"
    until = f"{on_date.isoformat()}T23:59:59{offset}"
    result = subprocess.run(
        [
            "git",
            "-c",
            "core.quotepath=false",
            "log",
            f"--since={since}",
            f"--until={until}",
            "--name-only",
            "--pretty=format:",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        detail = next((line for line in result.stderr.splitlines() if line.strip()), "未知錯誤")
        raise RuntimeError(f"git log 失敗：{detail.strip()}")

    pages: list[str] = []
    seen: set[str] = set()
    for raw in result.stdout.splitlines():
        page = raw.strip()
        if (
            page in seen
            or not page.startswith("wiki/")
            or not page.endswith(".md")
            or page == "wiki/01.index.md"
            or not (root / page).is_file()
        ):
            continue
        seen.add(page)
        pages.append(page)
    return pages


def select_daily_batch(
    pages: Iterable[str], cap: int, on_date: date
) -> tuple[list[str], list[str], int, int]:
    """選出當日批次；回傳 selected、deferred、0-based index、批次總數。"""
    if cap < 1:
        raise ValueError("cap 必須是正整數")

    ordered = list(dict.fromkeys(pages))
    if not ordered:
        return [], [], 0, 0

    batch_count = (len(ordered) + cap - 1) // cap
    batch_index = on_date.toordinal() % batch_count
    start = batch_index * cap
    selected = ordered[start : start + cap]
    selected_set = set(selected)
    deferred = [page for page in ordered if page not in selected_set]
    return selected, deferred, batch_index, batch_count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=positive_int, default=7)
    parser.add_argument("--cap", type=positive_int, default=10)
    parser.add_argument("--date", type=iso_date, default=date.today())
    parser.add_argument("--utc-offset", type=utc_offset, default="+08:00")
    parser.add_argument("--root", type=Path, default=Path("."), help=argparse.SUPPRESS)
    args = parser.parse_args()

    root = args.root.resolve()
    if not (root / "schema" / "vault-map.md").is_file():
        print("ERROR:not-vault-root（找不到 schema/vault-map.md，請在 vault root 執行）")
        return 1

    try:
        pages = discover_changed_pages(root, args.days, args.date, args.utc_offset)
        selected, deferred, batch_index, batch_count = select_daily_batch(
            pages, args.cap, args.date
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR:semantic-select（{exc}）")
        return 1

    for page in selected:
        print(f"SEMANTIC:{page}")
    for page in deferred:
        print(f"DEFERRED:{page}")
    print(f"SUMMARY:semantic={len(selected)}")
    print(f"SUMMARY:deferred={len(deferred)}")
    if batch_count:
        print(f"SUMMARY:batch={batch_index + 1}/{batch_count}")
    else:
        print("SUMMARY:batch=0/0")
    print("SELECT:complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
