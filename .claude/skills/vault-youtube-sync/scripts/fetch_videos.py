"""
抓取 YouTube 頻道影片清單與頻道簡介。

用法：
    python fetch_videos.py <handle>

輸出格式（每行一條）：
    DESC:<頻道簡介前 300 字>
    VIDEO:<videoId>|||<標題>
    ERROR:<錯誤訊息>  → 出現時立即停止

輸出筆數：ytInitialData 一次 HTTP 請求能拿到幾筆就幾筆（YouTube 上限約 30）。

範例：
    python fetch_videos.py Chase-H-AI
"""

import sys
import json
import re
import urllib.request
import html as html_module

# Windows 預設 stdout 是 cp950，遇到 emoji（如 🚀）print 會炸 UnicodeEncodeError
# 強制 UTF-8 輸出，主 skill bash heredoc 才不會收到 partial output。
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass  # Python <3.7 沒有 reconfigure，但本 repo 要求 3.7+

def main():
    if len(sys.argv) < 2:
        print("ERROR:usage: fetch_videos.py <handle>")
        sys.exit(1)

    handle = sys.argv[1].lstrip("@")

    url = f"https://www.youtube.com/@{handle}/videos"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"ERROR:{e}")
        sys.exit(1)

    # 頻道簡介（解碼 HTML entities，如 &#39; → '）
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', html)
    desc = html_module.unescape(desc_m.group(1)[:300]) if desc_m else ""
    print("DESC:" + desc)

    # 影片清單（從 ytInitialData SSR 物件取出，不需執行 JS）
    m = re.search(r"var ytInitialData = ", html)
    if not m:
        print("ERROR:ytInitialData not found")
        sys.exit(1)

    try:
        decoder = json.JSONDecoder()
        data, _ = decoder.raw_decode(html[m.end():])
        tabs = data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]
        count = 0
        for tab in tabs:
            grid = tab.get("tabRenderer", {}).get("content", {}).get("richGridRenderer")
            if not grid:
                continue
            for item in grid.get("contents", []):
                r = item.get("richItemRenderer", {}).get("content", {}).get("videoRenderer")
                if r:
                    title = r["title"]["runs"][0]["text"]
                    print(f"VIDEO:{r['videoId']}|||{title}")
                    count += 1
    except Exception as e:
        print(f"ERROR:{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
