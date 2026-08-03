"""抓 YouTube 影片 transcript，整併 defuddle 抓取 + videoId 硬驗證 + transcript-api fallback。

取代 subagent 流程裡的 `defuddle ... || npx`、`echo "$JSON" | python3` 驗證、
`pip install youtube-transcript-api` + 抓字幕三段 shell 膠水，全程無 shell pipe / bash-ism。

用法（cwd = repo root）：
    python3 .agents/skills/vault-youtube-sync/scripts/transcript.py <url> <videoId>

輸出（stdout，固定順序）：
    RESULT:MATCH | THIN | MISMATCH:<detail> | UNKNOWN | TRANSCRIPT | FAIL:<reason>
    PUBLISHED:<YYYY-MM-DD 或空>
    ---CONTENT---
    <contentMarkdown（MATCH/THIN）或時間戳 transcript（TRANSCRIPT）；FAIL/MISMATCH/UNKNOWN 時為空>

判讀（對齊原 SKILL 流程）：
    MATCH      → defuddle 內容可信且確為 transcript，用 CONTENT 當筆記來源（步驟 3-6）
    TRANSCRIPT → defuddle 不可信但 transcript-api 成功，用 CONTENT（時間戳）當來源
    THIN       → videoId 驗證過，但 defuddle 只抓到說明欄（無時間戳）且 transcript-api
                 亦無字幕。CONTENT 為該說明欄，依「情況 B」寫摘要並標註無字幕；
                 這是已確認的終態、不是抓取失敗，不寫 draft 占位
    FAIL:*     → 三層皆失敗，走 curl/video_meta 確認狀態 + draft 占位（步驟 2/2b）
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

ID_RE = r'(?:watch\?v=|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})'
# defuddle 正常抓到 YouTube transcript 時每段都帶 `**0:00**` 時間戳；沒有就代表
# 抓回的是說明欄之類的替代內容（字幕停用時常見），videoId 對得上也不能當 transcript 用
TS_RE = re.compile(r'\*\*\d+:\d+\*\*')


def validate(data: dict, target: str) -> str:
    """videoId 兩階段硬驗證。回傳 MATCH / MISMATCH:<detail> / UNKNOWN。"""
    # 階段 1：defuddle 主來源欄位（最硬）
    for k in ("url", "source", "canonical"):
        v = data.get(k) or ""
        m = re.search(ID_RE, v)
        if m:
            return "MATCH" if m.group(1) == target else f"MISMATCH:{k}={m.group(1)}"
    # 階段 2：fallback — contentMarkdown 前 2000 字第一個 ID
    blob = (data.get("contentMarkdown") or "")[:2000]
    ids = re.findall(ID_RE, blob)
    if not ids:
        return "UNKNOWN"
    return "MATCH" if ids[0] == target else f"MISMATCH:first={ids[0]}"


def run_defuddle(url: str) -> dict | None:
    """跑 defuddle parse <url> --json，全域找不到 fallback npx。回傳解析後 dict 或 None。"""
    candidates = []
    if shutil.which("defuddle"):
        candidates.append(["defuddle", "parse", url, "--json"])
    if shutil.which("npx"):
        candidates.append(["npx", "defuddle", "parse", url, "--json"])
    for cmd in candidates:
        try:
            proc = subprocess.run(
                cmd, check=True, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=60,
            )
            return json.loads(proc.stdout)
        except Exception as exc:  # noqa: BLE001
            # fallback 鏈刻意吞錯，但把原因寫到 stderr 供排查（stdout 契約不變）
            print(f"DIAG:defuddle:{cmd[0]}:{exc}", file=sys.stderr)
            continue
    if not candidates:
        print("DIAG:defuddle:not-installed（defuddle/npx 都不在 PATH）", file=sys.stderr)
    return None


def transcript_api(video_id: str) -> str | None:
    """youtube-transcript-api fallback；缺套件時嘗試安裝一次。回傳時間戳文字或 None。"""
    def _fetch():
        from youtube_transcript_api import YouTubeTranscriptApi  # noqa: PLC0415
        # 新版 instance API（v0.6+）；舊版 get_transcript 已移除
        return YouTubeTranscriptApi().fetch(
            video_id, languages=["zh-Hant", "zh-TW", "zh", "en"]
        )

    try:
        items = _fetch()
    except ImportError:
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-q", "youtube-transcript-api"],
                check=True, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=120,
            )
            items = _fetch()
        except Exception as exc:  # noqa: BLE001
            print(f"DIAG:transcript-api:install-or-fetch:{exc}", file=sys.stderr)
            return None
    except Exception as exc:  # noqa: BLE001
        print(f"DIAG:transcript-api:fetch:{exc}", file=sys.stderr)
        return None

    lines = []
    for t in items:
        start = getattr(t, "start", None)
        text = getattr(t, "text", None)
        if start is None and isinstance(t, dict):
            start, text = t.get("start", 0), t.get("text", "")
        lines.append(f"**{int(start // 60)}:{int(start % 60):02d}** {text}")
    return "\n".join(lines) if lines else None


def emit(result: str, published: str = "", content: str = "") -> int:
    print(f"RESULT:{result}")
    print(f"PUBLISHED:{published}")
    print("---CONTENT---")
    if content:
        print(content)
    return 0


def main() -> int:
    if len(sys.argv) < 3:
        return emit("FAIL:usage transcript.py <url> <videoId>")
    url, video_id = sys.argv[1], sys.argv[2]

    data = run_defuddle(url)
    thin_content = thin_published = ""
    if data is not None:
        verdict = validate(data, video_id)
        if verdict == "MATCH":
            content = data.get("contentMarkdown") or ""
            published = (data.get("published") or "")[:10]
            if TS_RE.search(content):
                return emit("MATCH", published, content)
            # ID 對得上但無時間戳 → 內容非 transcript，先試 API；失敗才回退成 THIN
            print("DIAG:defuddle:no-timestamps（內容非 transcript，續走 transcript-api）",
                  file=sys.stderr)
            thin_content, thin_published = content, published
        # MISMATCH / UNKNOWN → 落 transcript-api（不信任污染的 contentMarkdown）

    text = transcript_api(video_id)
    if text:
        return emit("TRANSCRIPT", "", text)
    if thin_content:
        return emit("THIN", thin_published, thin_content)
    return emit("FAIL:no-transcript")


if __name__ == "__main__":
    raise SystemExit(main())
