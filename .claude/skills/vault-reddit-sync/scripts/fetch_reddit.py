"""
抓取 Reddit 各 subreddit 一週內熱門 AI 相關貼文。

用法：
    python fetch_reddit.py <subreddit> [<subreddit> ...]

範例：
    python fetch_reddit.py ClaudeCode LocalLLaMA singularity codex

輸出格式（每行一條，全部輸出到 stdout）：
    META:<subreddit>|||<post_count>
    POST:<post_id>|||<subreddit>|||<score>|||<num_comments>|||<title>
    ERROR:<subreddit>:<錯誤訊息>  → 該 subreddit 失敗但繼續處理下一個

時窗用 week 而非 day：當日榜偏 meme/抱怨；一週讓技術討論文有時間冒上來。
頻道清單由主 skill 端從 vault `Inbox/Reddit/*/` 子資料夾名取得後傳入；
本 script 不 hardcode 任何 sub 名稱，也不對訂閱的 sub 做主題過濾
（訂閱的 sub 本身就是 AI 廣域或工具直接相關，全收 top week）。
"""

import sys
import json
import shutil
import subprocess
import time
import urllib.request
import urllib.error

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ObsidianVaultBot/1.0)",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
}

MAX_RETRIES = 2
RETRY_DELAY_SECONDS = 3


def build_url(subreddit):
    return f"https://www.reddit.com/r/{subreddit}/top.json?t=week&limit=50&raw_json=1"


def fetch_json(url):
    curl = shutil.which("curl")
    last_error = None

    for attempt in range(MAX_RETRIES + 1):
        try:
            if curl:
                proc = subprocess.run(
                    [
                        curl,
                        "-sS",
                        "--fail",
                        "-L",
                        "-H",
                        f"User-Agent: {HEADERS['User-Agent']}",
                        "-H",
                        f"Accept: {HEADERS['Accept']}",
                        "-H",
                        f"Accept-Language: {HEADERS['Accept-Language']}",
                        url,
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=20,
                )
                return json.loads(proc.stdout)

            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except subprocess.CalledProcessError as e:
            stderr = (e.stderr or "").strip()
            last_error = RuntimeError(stderr or f"curl exit {e.returncode}")
        except urllib.error.HTTPError as e:
            last_error = RuntimeError(f"HTTP {e.code}")
        except Exception as e:
            last_error = RuntimeError(str(e))

        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY_SECONDS)

    raise last_error or RuntimeError("unknown error")


def fetch_subreddit(subreddit):
    url = build_url(subreddit)
    data = fetch_json(url)

    children = data.get("data", {}).get("children", [])
    posts = []
    for child in children:
        d = child.get("data", {})
        post_id = d.get("id", "")
        title = d.get("title", "").replace("|||", " ").replace("\n", " ").replace("\r", "")
        score = int(d.get("score", 0))
        num_comments = int(d.get("num_comments", 0))
        if post_id:
            posts.append((post_id, score, num_comments, title))
    return posts


def main():
    if len(sys.argv) < 2:
        print("ERROR:usage:fetch_reddit.py <subreddit> [<subreddit> ...]")
        sys.exit(1)

    for subreddit in sys.argv[1:]:
        subreddit = subreddit.strip()
        if not subreddit:
            continue
        try:
            posts = fetch_subreddit(subreddit)
        except RuntimeError as e:
            print(f"ERROR:{subreddit}:{e}")
            continue

        print(f"META:{subreddit}|||{len(posts)}")
        for post_id, score, num_comments, title in posts:
            print(f"POST:{post_id}|||{subreddit}|||{score}|||{num_comments}|||{title}")


if __name__ == "__main__":
    main()
