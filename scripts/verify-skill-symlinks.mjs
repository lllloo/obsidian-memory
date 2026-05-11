#!/usr/bin/env node
/**
 * 驗證 `.claude/skills` 是指向 `.agents/skills` 的 symlink。
 *
 * CLAUDE.md 規定 `.agents/skills/` 是 repo-local skill 的唯一維護來源；
 * `.claude/skills` 應該是 symlink 指過去，避免兩份內容無聲漂移。
 *
 * 本檢查作為 `npm run check` 的一環，每次 type-check / format-check 時都會跑。
 *
 * 不檢查全域 `~/.claude/skills/<name>` 的掛載狀態——那是跨機器 / 跨使用者的設定，
 * 本 repo CI 無法可靠判斷。安裝指引見 README.md「全域掛載」段。
 */
import { lstatSync, readlinkSync, existsSync, readdirSync } from "node:fs";
import { resolve, join } from "node:path";

const REPO_ROOT = resolve(import.meta.dirname, "..");
const CLAUDE_SKILLS = join(REPO_ROOT, ".claude", "skills");
const AGENTS_SKILLS = join(REPO_ROOT, ".agents", "skills");

const errors = [];

function check() {
  let stat;
  try {
    stat = lstatSync(CLAUDE_SKILLS);
  } catch (e) {
    errors.push(`.claude/skills 不存在：${e.message}`);
    return;
  }

  if (!stat.isSymbolicLink()) {
    errors.push(
      `.claude/skills 必須是 symlink，但實際是${stat.isDirectory() ? "實體目錄" : "其他類型"}。\n` +
        `  CLAUDE.md 要求 .claude/skills 指向 .agents/skills，避免兩份內容漂移。\n` +
        `  修法：刪除 .claude/skills 後重新建立 symlink（指令見 README.md「全域掛載」段）。`,
    );
    return;
  }

  const target = readlinkSync(CLAUDE_SKILLS);
  const resolvedTarget = resolve(REPO_ROOT, ".claude", target);
  if (resolvedTarget !== AGENTS_SKILLS) {
    errors.push(
      `.claude/skills symlink target 錯誤：\n` +
        `  實際：${target}（解析為 ${resolvedTarget}）\n` +
        `  應為：指向 ${AGENTS_SKILLS}（相對寫法：..\\.agents\\skills 或 ../.agents/skills）`,
    );
    return;
  }

  if (!existsSync(AGENTS_SKILLS)) {
    errors.push(`.agents/skills target 不存在：${AGENTS_SKILLS}`);
    return;
  }

  // 透過 symlink 列出的子項目應等於 .agents/skills 直接列出
  const viaSymlink = new Set(readdirSync(CLAUDE_SKILLS));
  const direct = new Set(readdirSync(AGENTS_SKILLS));
  const onlyInSymlink = [...viaSymlink].filter((x) => !direct.has(x));
  const onlyInDirect = [...direct].filter((x) => !viaSymlink.has(x));
  if (onlyInSymlink.length || onlyInDirect.length) {
    errors.push(
      `symlink 內容與 target 不一致（symlink 應 fully transparent）：\n` +
        (onlyInSymlink.length
          ? `  僅在 symlink 看到：${onlyInSymlink.join(", ")}\n`
          : "") +
        (onlyInDirect.length
          ? `  僅在 target 看到：${onlyInDirect.join(", ")}`
          : ""),
    );
  }
}

check();

if (errors.length) {
  console.error("Skill symlink 驗證失敗：\n");
  for (const e of errors) console.error(`- ${e}\n`);
  process.exit(1);
}

console.log("Skill symlink OK（.claude/skills → .agents/skills）");
