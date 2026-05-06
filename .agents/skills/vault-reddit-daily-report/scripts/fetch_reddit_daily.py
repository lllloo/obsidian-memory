"""
抓取 Reddit 各 subreddit 當日熱門 AI 相關貼文。

用法：
    python fetch_reddit_daily.py <subreddit> [<subreddit> ...]

輸出格式：
    META:<subreddit>|||<post_count>
    POST:<post_id>|||<subreddit>|||<score>|||<num_comments>|||<title>
    ERROR:<subreddit>:<錯誤訊息>
"""

import json
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ObsidianVaultBot/1.0)",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
}

RETRY_BACKOFF_SECONDS = [3, 8, 20]
MAX_RETRY_AFTER_SECONDS = 60


def build_url(subreddit):
    return f"https://www.reddit.com/r/{subreddit}/top.json?t=day&limit=50&raw_json=1"


def _parse_retry_after(value):
    if value is None:
        return None
    s = str(value).strip()
    if s.isdigit():
        return min(int(s), MAX_RETRY_AFTER_SECONDS)
    return None


def _retry_after_from_curl_stderr(stderr):
    if not stderr:
        return None
    m = re.search(r"[Rr]etry-[Aa]fter:\s*(\d+)", stderr)
    return _parse_retry_after(m.group(1)) if m else None


def _is_local_proxy_refused(stderr):
    if not stderr:
        return False
    return "via 127.0.0.1" in stderr and "Could not connect to server" in stderr


def fetch_json(url):
    curl = shutil.which("curl")
    last_error = None
    proxy_bypass = False

    for attempt in range(len(RETRY_BACKOFF_SECONDS) + 1):
        retry_after = None
        try:
            if curl:
                cmd = [
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
                ]
                if proxy_bypass:
                    cmd[1:1] = ["--noproxy", "*"]
                proc = subprocess.run(
                    cmd,
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
            retry_after = _retry_after_from_curl_stderr(stderr)
            if _is_local_proxy_refused(stderr) and not proxy_bypass:
                proxy_bypass = True
                continue
        except urllib.error.HTTPError as e:
            last_error = RuntimeError(f"HTTP {e.code}")
            if e.code == 429:
                retry_after = _parse_retry_after(e.headers.get("Retry-After"))
        except Exception as e:
            last_error = RuntimeError(str(e))

        if attempt >= len(RETRY_BACKOFF_SECONDS):
            break
        delay = retry_after if retry_after else RETRY_BACKOFF_SECONDS[attempt]
        time.sleep(delay)

    raise last_error or RuntimeError("unknown error")


def fetch_subreddit(subreddit):
    data = fetch_json(build_url(subreddit))
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
        print("ERROR:usage:fetch_reddit_daily.py <subreddit> [<subreddit> ...]")
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
