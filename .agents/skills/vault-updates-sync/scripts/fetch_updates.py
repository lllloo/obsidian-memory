"""
Fetch high-trust developer tooling updates for vault-updates-sync.

Inputs:
    python fetch_updates.py --since YYYY-MM-DD --repo openai/codex --repo anthropics/claude-code

Outputs:
    META:since|||<YYYY-MM-DD>
    OFFICIAL:<name>|||<url>|||<tag>
    CHANGELOG:<source>|||<published>|||<title>|||<url>
    RELEASE:<repo>|||<published>|||<tag>|||<name>|||<url>
    ISSUE:<repo>|||<updated>|||<state>|||<comments>|||<labels>|||<title>|||<url>
    ERROR:<source>:<message>

This script intentionally keeps the first pass mechanical. The skill/analyzer
does the semantic high-precision filtering before writing notes.
"""

from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ObsidianVaultBot/1.0)",
    "Accept": "application/vnd.github+json, application/json;q=0.9, */*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

DEFAULT_REPOS = ["openai/codex", "anthropics/claude-code"]
OFFICIAL_SOURCES = [
    ("OpenAI Codex", "https://help.openai.com/en/articles/11428266-codex-changelog", "codex"),
    ("Claude Code", "https://code.claude.com/docs/en/changelog", "claude-code"),
    ("GitHub Changelog", "https://github.blog/changelog/feed/", "copilot"),
    ("Cursor Changelog", "https://www.cursor.com/changelog", "cursor"),
]
CHANGELOG_KEYWORDS = [
    "agent",
    "agents",
    "anthropic",
    "claude",
    "code review",
    "codex",
    "copilot",
    "cursor",
    "gpt",
    "mcp",
    "model",
    "openai",
]
ISSUE_LABEL_HINTS = [
    "area:",
    "bug",
    "connectivity",
    "context",
    "has repro",
    "hook",
    "mcp",
    "packaging",
    "regression",
    "sandbox",
    "security",
    "skills",
    "tool-calls",
]
ISSUE_TITLE_HINTS = [
    "auth",
    "broken",
    "cannot",
    "compact",
    "context",
    "crash",
    "does not",
    "error",
    "fail",
    "hang",
    "hook",
    "limit",
    "mcp",
    "regression",
    "sandbox",
    "slow",
    "timeout",
    "unable",
    "workaround",
]
RETRY_BACKOFF_SECONDS = [3, 8, 20]


def _sanitize(value: object) -> str:
    if value is None:
        return ""
    return str(value).replace("|||", " ").replace("\n", " ").replace("\r", "").strip()


def _parse_date(value: str) -> dt.datetime:
    return dt.datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)


def _parse_iso(value: str) -> dt.datetime | None:
    if not value:
        return None
    try:
        normalized = value.replace("Z", "+00:00")
        parsed = dt.datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    except ValueError:
        return None


def _parse_rss_date(value: str) -> dt.datetime | None:
    if not value:
        return None
    try:
        parsed = email.utils.parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    except (TypeError, ValueError):
        return None


def request_text(url: str) -> str:
    headers = dict(HEADERS)
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {token}"

    curl = shutil.which("curl")
    last_error: Exception | None = None
    for attempt in range(len(RETRY_BACKOFF_SECONDS) + 1):
        try:
            if curl:
                cmd = [
                    curl, "-sS", "--fail", "-L",
                    "-H", f"User-Agent: {headers['User-Agent']}",
                    "-H", f"Accept: {headers['Accept']}",
                    "-H", f"Accept-Language: {headers['Accept-Language']}",
                ]
                if "Authorization" in headers:
                    cmd += ["-H", f"Authorization: {headers['Authorization']}"]
                cmd.append(url)
                proc = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=25)
                return proc.stdout
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=25) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except subprocess.CalledProcessError as e:
            last_error = RuntimeError((e.stderr or "").strip() or f"curl exit {e.returncode}")
        except Exception as exc:  # noqa: BLE001 - preserve short script portability
            last_error = exc
        if attempt >= len(RETRY_BACKOFF_SECONDS):
            break
        time.sleep(RETRY_BACKOFF_SECONDS[attempt])
    raise RuntimeError(str(last_error or "unknown request error"))


def request_json(url: str) -> object:
    return json.loads(request_text(url))


def fetch_releases(repo: str, since: dt.datetime) -> None:
    url = f"https://api.github.com/repos/{repo}/releases?per_page=30"
    try:
        data = request_json(url)
    except RuntimeError as exc:
        print(f"ERROR:releases:{repo}:{exc}")
        return

    if not isinstance(data, list):
        print(f"ERROR:releases:{repo}:unexpected response")
        return

    for item in data:
        if not isinstance(item, dict):
            continue
        published = _parse_iso(str(item.get("published_at") or ""))
        if not published or published < since:
            continue
        tag = _sanitize(item.get("tag_name"))
        name = _sanitize(item.get("name") or tag)
        html_url = _sanitize(item.get("html_url"))
        print(f"RELEASE:{repo}|||{published.isoformat()}|||{tag}|||{name}|||{html_url}")


def fetch_issues(repo: str, since: dt.datetime) -> None:
    since_param = urllib.parse.quote(since.isoformat().replace("+00:00", "Z"))
    url = (
        f"https://api.github.com/repos/{repo}/issues"
        f"?state=all&since={since_param}&sort=updated&direction=desc&per_page=50"
    )
    try:
        data = request_json(url)
    except RuntimeError as exc:
        print(f"ERROR:issues:{repo}:{exc}")
        return

    if not isinstance(data, list):
        print(f"ERROR:issues:{repo}:unexpected response")
        return

    for item in data:
        if not isinstance(item, dict) or item.get("pull_request"):
            continue
        updated = _parse_iso(str(item.get("updated_at") or ""))
        if not updated or updated < since:
            continue
        labels = ",".join(_sanitize(label.get("name")) for label in item.get("labels", []) if isinstance(label, dict))
        title = _sanitize(item.get("title"))
        state = _sanitize(item.get("state"))
        comments = int(item.get("comments") or 0)
        if not _issue_is_candidate(labels, title, comments, state):
            continue
        html_url = _sanitize(item.get("html_url"))
        print(f"ISSUE:{repo}|||{updated.isoformat()}|||{state}|||{comments}|||{labels}|||{title}|||{html_url}")


def _issue_is_candidate(labels: str, title: str, comments: int, state: str) -> bool:
    label_text = labels.lower()
    if "security" in label_text:
        return True
    if any(marker in label_text for marker in ("duplicate", "invalid", "stale")) and comments < 10:
        return False
    if state.lower() == "closed" and comments < 3 and "has repro" not in label_text:
        return False
    if comments >= 3:
        return True
    haystack = f"{labels} {title}".lower()
    return any(hint in haystack for hint in ISSUE_LABEL_HINTS + ISSUE_TITLE_HINTS)


def fetch_github_changelog(since: dt.datetime) -> None:
    url = "https://github.blog/changelog/feed/"
    try:
        text = request_text(url)
        root = ET.fromstring(text)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR:GitHub Changelog:{exc}")
        return

    for item in root.findall(".//item"):
        title = _sanitize(item.findtext("title"))
        link = _sanitize(item.findtext("link"))
        published = _parse_rss_date(item.findtext("pubDate") or "")
        if not published or published < since:
            continue
        haystack = title.lower()
        if not any(keyword in haystack for keyword in CHANGELOG_KEYWORDS):
            continue
        print(f"CHANGELOG:GitHub Changelog|||{published.isoformat()}|||{title}|||{link}")


def fetch_discussions_with_gh(repo: str, since: dt.datetime) -> None:
    gh = shutil.which("gh")
    if not gh:
        return
    owner, name = repo.split("/", 1)
    query = """
query($owner:String!, $name:String!) {
  repository(owner:$owner, name:$name) {
    discussions(first: 20, orderBy: {field: UPDATED_AT, direction: DESC}) {
      nodes {
        title
        updatedAt
        url
        comments { totalCount }
      }
    }
  }
}
"""
    try:
        proc = subprocess.run(
            [
                gh,
                "api",
                "graphql",
                "-f",
                f"owner={owner}",
                "-f",
                f"name={name}",
                "-f",
                f"query={query}",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=25,
        )
        payload = json.loads(proc.stdout)
    except subprocess.CalledProcessError as e:
        print(f"ERROR:discussions:{repo}:{(e.stderr or '').strip() or f'gh exit {e.returncode}'}")
        return
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR:discussions:{repo}:{exc}")
        return

    nodes = (
        payload.get("data", {})
        .get("repository", {})
        .get("discussions", {})
        .get("nodes", [])
    )
    for item in nodes:
        updated = _parse_iso(str(item.get("updatedAt") or ""))
        if not updated or updated < since:
            continue
        title = _sanitize(item.get("title"))
        url = _sanitize(item.get("url"))
        comments = int(item.get("comments", {}).get("totalCount") or 0)
        print(f"DISCUSSION:{repo}|||{updated.isoformat()}|||{comments}|||{title}|||{url}")


def main() -> int:
    default_since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=7)).date().isoformat()
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", default=default_since, help="YYYY-MM-DD, default: 7 days ago")
    parser.add_argument("--repo", action="append", default=[], help="GitHub repo owner/name; repeatable")
    args = parser.parse_args()

    try:
        since = _parse_date(args.since)
    except ValueError:
        print(f"ERROR:usage:invalid --since date {args.since!r}; expected YYYY-MM-DD")
        return 1

    repos = args.repo or DEFAULT_REPOS
    print(f"META:since|||{since.date().isoformat()}")
    for name, url, tag in OFFICIAL_SOURCES:
        print(f"OFFICIAL:{name}|||{url}|||{tag}")

    fetch_github_changelog(since)
    for repo in repos:
        if not re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", repo):
            print(f"ERROR:repo:{repo}:invalid owner/name")
            continue
        fetch_releases(repo, since)
        fetch_issues(repo, since)
        fetch_discussions_with_gh(repo, since)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
