#!/usr/bin/env python3
"""在更新 YouTube checkpoint 前，核對本批每個 videoId 都有明確終態。

完整筆記與 draft 以頻道資料夾內實際檔案為準；只有內容篩除與已確認不可用
的影片可由呼叫端明確傳入。任何漏項、重複來源、讀檔錯誤或尚存 draft 都
回傳 ``VERIFY:blocked`` 並以非零狀態結束，讓 checkpoint 維持原值。

用法（cwd = repo root）：
    python3 .agents/skills/vault-youtube-sync/scripts/verify_batch.py \
      "feeds/youtube/<頻道名>" --expected=<videoId> [--expected=<videoId> ...] \
      [--filtered=<videoId> ...] [--unavailable=<videoId> ...]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass


SOURCE_RE = re.compile(
    r"^source:\s*https://www\.youtube\.com/watch\?v=([A-Za-z0-9_-]+)", re.MULTILINE
)
DRAFT_RE = re.compile(r"^draft:\s*true\s*$", re.MULTILINE)
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def unique(values: list[str]) -> list[str]:
    """去重並保留輸入順序。"""
    return list(dict.fromkeys(values))


def scan_notes(notes_dir: Path) -> tuple[dict[str, list[tuple[str, Path]]], list[str]]:
    """回傳 videoId -> [(complete|draft, path)]，以及讀取錯誤。"""
    states: dict[str, list[tuple[str, Path]]] = {}
    errors: list[str] = []
    for path in sorted(notes_dir.glob("*.md")):
        if path.name == "01.index.md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{path}:{exc}")
            continue
        match = SOURCE_RE.search(text)
        if not match:
            continue
        video_id = match.group(1)
        state = "draft" if DRAFT_RE.search(text) else "complete"
        states.setdefault(video_id, []).append((state, path))
    return states, errors


def verify_batch(
    notes_dir: Path,
    expected_values: list[str],
    filtered_values: list[str] | None = None,
    unavailable_values: list[str] | None = None,
) -> tuple[bool, list[str]]:
    """核對批次終態，回傳是否可前推 checkpoint 與機器可讀結果行。"""
    lines: list[str] = []
    if not notes_dir.is_dir():
        return False, [f"ERROR:notes-dir-not-found:{notes_dir}", "VERIFY:blocked"]

    expected = unique(expected_values)
    filtered = set(filtered_values or [])
    unavailable = set(unavailable_values or [])
    expected_set = set(expected)
    config_errors: list[str] = []

    if not expected:
        config_errors.append("expected-empty")
    for video_id in expected_set | filtered | unavailable:
        if not VIDEO_ID_RE.fullmatch(video_id):
            config_errors.append(f"invalid-video-id:{video_id}")
    for video_id in sorted((filtered | unavailable) - expected_set):
        config_errors.append(f"terminal-id-not-expected:{video_id}")
    for video_id in sorted(filtered & unavailable):
        config_errors.append(f"conflicting-terminal-state:{video_id}")

    states, read_errors = scan_notes(notes_dir)
    blocked = bool(config_errors or read_errors)
    counts = {
        "complete": 0,
        "draft": 0,
        "filtered": 0,
        "unavailable": 0,
        "missing": 0,
        "duplicate": 0,
    }

    for error in config_errors:
        lines.append(f"ERROR:config:{error}")
    for error in read_errors:
        lines.append(f"ERROR:read:{error}")

    for video_id in expected:
        entries = states.get(video_id, [])
        if len(entries) > 1:
            paths = "|".join(path.as_posix() for _, path in entries)
            lines.append(f"DUPLICATE:{video_id}:{paths}")
            counts["duplicate"] += 1
            blocked = True
            continue
        if entries:
            state, path = entries[0]
            lines.append(f"RESULT:{video_id}:{state}:{path.as_posix()}")
            counts[state] += 1
            if state == "draft":
                blocked = True
            continue
        if video_id in filtered:
            lines.append(f"RESULT:{video_id}:filtered:-")
            counts["filtered"] += 1
            continue
        if video_id in unavailable:
            lines.append(f"RESULT:{video_id}:unavailable:-")
            counts["unavailable"] += 1
            continue
        lines.append(f"MISSING:{video_id}")
        counts["missing"] += 1
        blocked = True

    # 沿用既有安全語意：頻道內任何舊 draft 都要阻止 checkpoint 前推，
    # 即使該影片已不在本次 ytInitialData 清單裡，也不能靜默跨過。
    extra_drafts = sorted(
        video_id
        for video_id, entries in states.items()
        if video_id not in expected_set and any(state == "draft" for state, _ in entries)
    )
    for video_id in extra_drafts:
        lines.append(f"EXTRA_DRAFT:{video_id}")
        blocked = True

    lines.append(
        "SUMMARY:"
        f"expected={len(expected)}|complete={counts['complete']}|draft={counts['draft']}|"
        f"filtered={counts['filtered']}|unavailable={counts['unavailable']}|"
        f"missing={counts['missing']}|duplicate={counts['duplicate']}|"
        f"extra_draft={len(extra_drafts)}|errors={len(config_errors) + len(read_errors)}"
    )
    lines.append("VERIFY:blocked" if blocked else "VERIFY:ready")
    return not blocked, lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("notes_dir", help="頻道筆記資料夾")
    parser.add_argument(
        "--expected",
        action="append",
        required=True,
        help="checkpoint 候選 videoId；每支重複傳入一次",
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
        print("ERROR:not-vault-root（找不到 schema/vault-map.md）")
        print("VERIFY:blocked")
        return 2

    ready, lines = verify_batch(
        Path(args.notes_dir), args.expected, args.filtered, args.unavailable
    )
    print("\n".join(lines))
    return 0 if ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
