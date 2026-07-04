"""判斷某候選是否已在 vault 出現過（daily updates 去重，fixed-string 比對）。

用法（cwd = repo root）：

    # release：穩定 URL + 工具/版本鍵一起比（交叉去重——同版本可能已由官方 changelog 報過）
    python3 .agents/skills/vault-updates-daily/scripts/dedup_check.py \
        "<url>" --tool "<工具名>" --key "<版本>"

    # 官方網頁 changelog 條目：anchor 會漂（每次跑 slug 不同），只用穩定鍵，不傳 URL
    python3 .agents/skills/vault-updates-daily/scripts/dedup_check.py \
        --tool "<工具名>" --key "<版本或標題關鍵字>"

為什麼要 --tool/--key（治本）：
  官方 changelog 的單條沒有獨立 URL，過去用「頁面 URL + 自行編的 #anchor」當 canonical。
  但 anchor 由 analyzer 每次自由編 slug，同一條在不同日的日報 anchor 不一致（如
  `#21161` vs `#2-1-161`、`#sites-preview` vs `#build-and-deploy-websites-with-sites`），
  fixed-string 比 URL 就漏抓 → 同一條重報。改以「工具 + 版本／標題」這種穩定識別比對，
  與 anchor 無關，根治重複。

為什麼 release 也要帶 --tool/--key（交叉去重）：
  同一個版本可能兩條路都抓到——官方 changelog（頁面 URL + anchor）與 GitHub release
  （`.../releases/tag/<版本>` 穩定 URL）。兩者 URL 格式不同，只比 URL 撞不到 → 同版本
  重報。release 額外帶「工具 + 版本」穩定鍵，就能命中先前由官方 changelog 報過的同一版
  （反向亦然：官方 changelog 條目的版本鍵也會命中先前的 release 標題）。

URL 是否參與比對由呼叫端決定：
  release 的 URL 是 per-entry 穩定連結，安全，照傳；官方 changelog 的頁面 URL 為整頁
  條目共用，傳了會讓新條目誤判 DUP（默默漏報），故官方 changelog **只傳 --tool/--key、
  不傳 URL**。腳本不猜，依你傳不傳 URL 而定。

檢查層（任一命中即 DUP；給了什麼跑什麼，可同時）：
  1. 舊個別筆記格式（僅當給 URL）：Inbox/Updates / Cards / Topics 任一 .md 含 `source: <url>`。
  2. 所有日報正文（僅當給 URL）：任一 `*-daily-updates.md` 含完整 <url>（release 的穩定 URL 走這層）。
     比對有右邊界檢查：命中後下一字元不得仍是 URL 字元，避免短 URL 前綴誤命中長 URL
    （如 `...#2-1-19` 誤中 `...#2-1-198`、裸頁面 URL 誤中帶 anchor 連結）。
  3. 穩定鍵（僅當給 --key）：在日報的 `### ` 標題行找 <key>；給 --tool 時，只在該
     `## <tool>` section 內找（避免跨工具撞版本號）。只比標題行，不比內文——內文順帶
     提到的版本（如某版說明寫「regression in 2.1.161」）不算已報。
     注意：`### ` 標題的 META 需含該版本字串（組裝格式 `### <META>（...）` 已保證），
     且 release 與官方 changelog 對同一版本要用一致的工具名，--tool scope 才對得上。

輸出：
    DUP:<命中檔案相對路徑>   （第一個命中即印出）
    UNIQUE                    （皆未命中）

全程 fixed-string（非 regex）比對，避開 URL 裡 ?、& 等 regex metachar。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

# cwd 必為 vault root：cwd 錯時 rglob 會靜默空集合 → 誤回 UNIQUE 放行重複；hard-fail 較安全
if not Path("vault-map.md").is_file():
    sys.exit("ERROR: cwd 不在 vault root（找不到 vault-map.md）")


# URL 續行字元集：命中片段後緊接這些字元，代表正文裡是更長的 URL（帶 anchor / 更長版本號），不算命中
_URL_CHARS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#/?&=%._~+-"
)


def url_hit(text: str, needle: str) -> bool:
    """fixed-string 找 needle，且命中處右側不是 URL 續行字元（防前綴誤命中）。"""
    pos = text.find(needle)
    while pos != -1:
        end = pos + len(needle)
        if end >= len(text) or text[end] not in _URL_CHARS:
            return True
        pos = text.find(needle, pos + 1)
    return False


def _heading_tool(line: str) -> str | None:
    """`## <tool>` → '<tool>'；非 H2 回 None。"""
    s = line.strip()
    if s.startswith("## ") and not s.startswith("### "):
        return s[3:].strip()
    return None


def key_hit_in_daily(text: str, tool: str | None, key: str) -> bool:
    """key 是否出現在（指定 tool 的）`### ` 標題行。"""
    in_scope = tool is None
    for line in text.splitlines():
        t = _heading_tool(line)
        if t is not None:                       # 進入新的 ## section
            in_scope = (tool is None) or (t.lower() == tool.lower())
            continue
        if in_scope and line.lstrip().startswith("### ") and key in line:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs="?", default="")
    parser.add_argument("date", nargs="?", default="")  # 相容保留，不再使用
    parser.add_argument("--tool", default=None, help="工具名（對應日報 `## <tool>` 標題），限縮 --key 比對範圍")
    parser.add_argument("--key", default=None, help="穩定鍵（版本號或標題關鍵字），在 `### ` 標題行比對")
    args = parser.parse_args()

    # URL 與 --key 可並存：release 帶穩定 URL + 工具/版本鍵交叉去重。是否傳 URL 由呼叫端
    # 決定——官方 changelog 不傳頁面 URL（會誤判 DUP），release 傳 per-entry 穩定 URL。
    url = args.url
    if not url and not args.key:
        print("UNIQUE")
        return 0

    # 1. 個別筆記格式（source: <url>）
    if url:
        needle = f"source: {url}"
        for base in ("Inbox/Updates", "Cards", "Topics"):
            root = Path(base)
            if not root.is_dir():
                continue
            for p in sorted(root.rglob("*.md")):
                try:
                    if url_hit(p.read_text(encoding="utf-8", errors="replace"), needle):
                        print(f"DUP:{p.as_posix()}")
                        return 0
                except OSError:
                    continue

    # 2 + 3. 日報正文：URL 完整比對（含右邊界檢查）或標題行穩定鍵比對（--key 模式）
    updates_dir = Path("Inbox/Updates")
    if updates_dir.is_dir():
        for p in sorted(updates_dir.glob("*-daily-updates.md")):
            try:
                body = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if url and url_hit(body, url):
                print(f"DUP:{p.as_posix()}")
                return 0
            if args.key and key_hit_in_daily(body, args.tool, args.key):
                print(f"DUP:{p.as_posix()}")
                return 0

    print("UNIQUE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
