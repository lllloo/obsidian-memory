"""
抓取單篇 Reddit 貼文完整內容與熱門留言（供 Reddit daily analyzer 使用）。

用法：
    python fetch_post.py <subreddit> <post_id>

範例：
    python fetch_post.py ClaudeCode 1svdm1w

輸出格式（key 出現順序固定，全部到 stdout）：
    TITLE:<標題>
    SCORE:<分數>
    NUMCOMMENTS:<留言數>
    URL:<外部連結；selftext post 為 reddit permalink 的 https://www.reddit.com/...>
    PERMALINK:<reddit permalink，已含前綴 /r/...>
    CREATED:<YYYY-MM-DD>
    SELFTEXT_LINES:<行數>
    SELFTEXT_TRUNCATED:<true|false>
    SELFTEXT_BEGIN
    <selftext 原文，多行；以 SELFTEXT_END 結尾>
    SELFTEXT_END
    COMMENT:<score>|||<留言內文，已 collapse 為單行；上限 500 字>
    ...（最多 5 條）
    ERROR:<錯誤訊息>  → 出現時 exit 1

設計：
- 不用 ||| 切 selftext，改用 BEGIN/END marker 包多行原文，避免內文 ||| 衝突
- selftext 上限 4000 字，超過截斷並 mark TRUNCATED:true（subagent 用得到的本就不需全文）
- title / comment 只去 control char，不做 escape；標題可能含 |||，但只在 COMMENT 行用作分隔，COMMENT 內文已先去 |||
"""

import sys
import json
import shutil
import subprocess
import time
import urllib.request
import urllib.error
import datetime

# Windows cp950 stdout 對 emoji 會炸，強制 UTF-8 避免 partial output。
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
SELFTEXT_MAX_CHARS = 4000
COMMENT_MAX_CHARS = 500
TOP_COMMENTS = 5


def build_url(subreddit, post_id):
    return f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json?limit=25&sort=top&raw_json=1"


def fetch_json(url):
    """curl 優先、urllib fallback、有限重試。"""
    curl = shutil.which("curl")
    last_error = None

    for attempt in range(len(RETRY_BACKOFF_SECONDS) + 1):
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
            last_error = RuntimeError((e.stderr or "").strip() or f"curl exit {e.returncode}")
        except urllib.error.HTTPError as e:
            last_error = RuntimeError(f"HTTP {e.code}")
        except Exception as e:
            last_error = RuntimeError(str(e))

        if attempt >= len(RETRY_BACKOFF_SECONDS):
            break
        time.sleep(RETRY_BACKOFF_SECONDS[attempt])

    raise last_error or RuntimeError("unknown error")


def _flatten_oneline(s, limit):
    """把任意字串壓成單行：去 CR/LF/Tab、去 control char、截 limit。"""
    if not s:
        return ""
    out = []
    for ch in s:
        code = ord(ch)
        if ch in ("\r", "\n", "\t"):
            out.append(" ")
        elif code < 0x20:
            continue
        else:
            out.append(ch)
    flat = "".join(out).replace("|||", " ").strip()
    if len(flat) > limit:
        flat = flat[:limit].rstrip() + "…"
    return flat


def _truncate_selftext(s, limit):
    """保留多行結構，只截總長度，回 (text, was_truncated)。"""
    if not s:
        return "", False
    if len(s) <= limit:
        return s, False
    return s[:limit] + "\n\n[...truncated]", True


def main():
    if len(sys.argv) < 3:
        print("ERROR:usage: fetch_post.py <subreddit> <post_id>")
        sys.exit(1)

    subreddit = sys.argv[1].strip()
    post_id = sys.argv[2].strip()
    if post_id.startswith("t3_"):
        post_id = post_id[3:]
    if not subreddit or not post_id:
        print("ERROR:subreddit / post_id 不可為空")
        sys.exit(1)

    try:
        data = fetch_json(build_url(subreddit, post_id))
    except RuntimeError as e:
        print(f"ERROR:{e}")
        sys.exit(1)

    try:
        post = data[0]["data"]["children"][0]["data"]
    except (KeyError, IndexError, TypeError):
        print("ERROR:unexpected reddit payload shape")
        sys.exit(1)

    title = _flatten_oneline(post.get("title", ""), 500)
    score = int(post.get("score", 0))
    num_comments = int(post.get("num_comments", 0))
    url = post.get("url", "")
    permalink = post.get("permalink", "")
    ts = post.get("created_utc", 0)
    try:
        created = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).strftime("%Y-%m-%d")
    except (OSError, ValueError, OverflowError):
        created = ""

    selftext_raw = post.get("selftext") or ""
    selftext, truncated = _truncate_selftext(selftext_raw, SELFTEXT_MAX_CHARS)
    selftext_lines = selftext.count("\n") + 1 if selftext else 0

    print(f"TITLE:{title}")
    print(f"SCORE:{score}")
    print(f"NUMCOMMENTS:{num_comments}")
    print(f"URL:{url}")
    print(f"PERMALINK:{permalink}")
    print(f"CREATED:{created}")
    print(f"SELFTEXT_LINES:{selftext_lines}")
    print(f"SELFTEXT_TRUNCATED:{'true' if truncated else 'false'}")
    print("SELFTEXT_BEGIN")
    if selftext:
        print(selftext)
    print("SELFTEXT_END")

    try:
        children = data[1]["data"]["children"]
    except (KeyError, IndexError, TypeError):
        children = []

    count = 0
    for c in children:
        if count >= TOP_COMMENTS:
            break
        if c.get("kind") != "t1":
            continue
        cd = c.get("data", {}) or {}
        body = _flatten_oneline(cd.get("body", ""), COMMENT_MAX_CHARS)
        if not body:
            continue
        cscore = int(cd.get("score", 0))
        print(f"COMMENT:{cscore}|||{body}")
        count += 1


if __name__ == "__main__":
    main()
