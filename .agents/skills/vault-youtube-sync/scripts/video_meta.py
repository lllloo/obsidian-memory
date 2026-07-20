"""抓 YouTube 影片頁面的可用性與上傳日期（取代 subagent 流程裡的 curl|python）。

用法（cwd = repo root）：
    python3 .agents/skills/vault-youtube-sync/scripts/video_meta.py <videoId>

輸出（每行一條）：
    STATUS:available | STATUS:unavailable | STATUS:error
    DATE:<YYYY-MM-DD>   （抓不到則空字串）

`unavailable` 只代表頁面明確證實影片不可用；網路中斷、429、5xx 等
無法完成查核的狀況回 `error`，避免上層誤判為影片已刪除。

純 urllib，無 curl 依賴，跨平台（Windows/mac/Linux 行為一致）。
"""
import re
import sys
import urllib.error
import urllib.request

# Windows 預設 stdout cp950，遇 emoji / 非 cp950 字元會炸，強制 UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def main():
    if len(sys.argv) < 2:
        print("STATUS:error")
        print("DATE:")
        return 1
    vid = sys.argv[1]
    url = f"https://www.youtube.com/watch?v={vid}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        if exc.code in (404, 410):
            print("STATUS:unavailable")
            print("DATE:")
            return 0
        print("STATUS:error")
        print("DATE:")
        print(f"ERROR:HTTP {exc.code}: {exc.reason}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print("STATUS:error")
        print("DATE:")
        print(f"ERROR:{exc}", file=sys.stderr)
        return 2

    avail = "unavailable" if "videoUnavailableRenderer" in html else "available"
    m = re.search(r'itemprop="datePublished" content="([^"]+)"', html)
    date = m.group(1)[:10] if m else ""
    print("STATUS:" + avail)
    print("DATE:" + date)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
