#!/usr/bin/env node
import { readFileSync, writeFileSync, renameSync, existsSync } from "node:fs";
import { basename, dirname, join, parse, relative, resolve } from "node:path";
import { globby } from "globby";
import matter from "gray-matter";
import yaml from "js-yaml";
import { parseArgs } from "node:util";

const yamlEngine = {
  parse: (s) => yaml.load(s, { schema: yaml.CORE_SCHEMA }),
  stringify: (o) =>
    yaml.dump(o, {
      schema: yaml.CORE_SCHEMA,
      lineWidth: -1,
      noRefs: true,
      quotingType: '"',
      forceQuotes: false,
    }),
};
const matterOptions = { engines: { yaml: yamlEngine } };
import {
  DATE_FIELDS,
  FIELD_ORDER,
  REQUIRED_FIELDS,
  codeLabel,
  frontmatterSchema,
  reorderFields,
  tryNormalizeDate,
  validateFieldOrder,
} from "./vault-schema.mjs";

const REQUIRED_SET = new Set(REQUIRED_FIELDS);

/**
 * 敏感資料 high-precision regex（CI 最後一道防線）。
 *
 * 原則：只收進「幾乎不可能誤判」的 token shape，寧可漏也不要誤報。
 * 完整語意層檢查（自然語言密碼、個資、內部資訊）仍由語意層稽核流程（/vault-check skill 內 audit reference）處理。
 */
const SENSITIVE_PATTERNS = [
  { name: "Anthropic key", regex: /sk-ant-[A-Za-z0-9_-]{20,}/ },
  { name: "OpenAI key", regex: /sk-(?:proj-)?[A-Za-z0-9_-]{32,}/ },
  { name: "GitHub token", regex: /gh[pousr]_[A-Za-z0-9]{36,}/ },
  { name: "Google API key", regex: /AIza[0-9A-Za-z_-]{35}/ },
  { name: "AWS access key", regex: /\bAKIA[0-9A-Z]{16}\b/ },
  { name: "Slack token", regex: /xox[baprs]-[A-Za-z0-9-]{10,}/ },
  { name: "Private key header", regex: /-----BEGIN[ A-Z]*PRIVATE KEY-----/ },
  {
    name: "JWT",
    regex: /\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}/,
  },
];

const REPO_ROOT = resolve(import.meta.dirname, "..");
const CONTENT_DIR = join(REPO_ROOT, "content");
// Site-level 索引頁（非筆記）與 vault 規則文件，豁免 schema 必填。
// index.md 是 Quartz 首頁、master-index.md 是 vault 入口、CLAUDE.md 是規則本身，
// 三者不受卡片盒 frontmatter 規範約束。
const EXCLUDED = new Set([
  "content/index.md",
  "content/master-index.md",
  "content/CLAUDE.md",
]);

// Schema / 檔名豁免：Web Clipper 剪下的原料，整理進 Cards 前不檢查檔名空格與 frontmatter schema。
// 注意：敏感資料 high-precision 硬掃（scanSensitive）仍會跑——剪貼網頁正是最容易夾帶 token 的地方。
const SCHEMA_EXEMPT_PREFIXES = ["content/Inbox/Clippings/"];

function isSchemaExempt(absPath) {
  const r = rel(absPath);
  return SCHEMA_EXEMPT_PREFIXES.some((p) => r.startsWith(p));
}

const { values: args } = parseArgs({
  options: {
    fix: { type: "boolean", default: false },
    json: { type: "boolean", default: false },
    help: { type: "boolean", short: "h", default: false },
  },
});

if (args.help) {
  console.log(`Usage: node scripts/vault-check.mjs [--fix] [--json]

掃描 content/ 下所有 .md，只處理硬規則（檔名、frontmatter 結構、日期 normalize）。
語意層稽核（wikilink 斷鏈、敏感資料、tag 一致性、缺 title/created/tags、parse error）
由語意層稽核流程（/vault-check skill 內 audit reference）處理，不在此 script。

豁免：content/Inbox/Clippings/ 為 Web Clipper 剪下的原料，跳過檔名 / schema 檢查，
但敏感資料 high-precision 硬掃照跑。

  --fix    自動修可修項目（欄位順序、白名單外欄位、補 updated、日期 normalize、檔名空格）
  --json   以 JSON 輸出（預設為人類可讀）`);
  process.exit(0);
}

const today = new Date().toISOString().slice(0, 10);

/** 將路徑轉成 repo-relative、forward-slash 形式 */
function rel(p) {
  return relative(REPO_ROOT, p).replaceAll("\\", "/");
}

async function listMarkdown() {
  const patterns = ["content/**/*.md", "!content/.obsidian/**"];
  const files = await globby(patterns, { cwd: REPO_ROOT, absolute: true });
  return files.filter((f) => !EXCLUDED.has(rel(f)));
}

/** 檢查檔名是否含空格；回傳建議的新檔名（若需要） */
function checkFilename(absPath) {
  const name = basename(absPath);
  if (!name.includes(" ")) return null;
  const dir = dirname(absPath);
  const { name: stem, ext } = parse(name);
  const normalizedStem = stem
    .replaceAll(/\s+/g, "-")
    .replaceAll(/-+/g, "-")
    .replace(/^-+|-+$/g, "");
  if (!normalizedStem) return null;
  const renamed = normalizedStem + ext;
  if (renamed === name) return null;
  return { dir, from: name, to: renamed, toAbs: join(dir, renamed) };
}

/**
 * 對單一檔案做稽核，回傳 issues 陣列。
 * 只回 autofix=true 的硬規則；不能自動修的（parse error、缺 title/created/tags、
 * 不可推斷的 INVALID_VALUE）一律跳過交語意層稽核流程（audit reference）處理。
 */
function auditFile(absPath) {
  const issues = [];
  const relPath = rel(absPath);
  const raw = readFileSync(absPath, "utf8");

  let parsed;
  try {
    parsed = matter(raw, matterOptions);
  } catch (e) {
    issues.push({
      code: "PARSE_ERROR",
      severity: "error",
      file: relPath,
      message: `frontmatter 解析失敗：${e?.message ?? String(e)}`,
      autofix: false,
    });
    return { issues, parsed: null, raw };
  }

  const data = parsed.data ?? {};

  const fnIssue = checkFilename(absPath);
  if (fnIssue) {
    issues.push({
      code: "FILENAME_HAS_SPACE",
      severity: "error",
      file: relPath,
      message: `檔名含空格：'${fnIssue.from}' → '${fnIssue.to}'`,
      autofix: true,
      fix: { kind: "rename", ...fnIssue },
    });
  }

  const ALLOWED_SET = new Set(FIELD_ORDER);
  for (const [k, v] of Object.entries(data)) {
    if (REQUIRED_SET.has(k)) continue;
    if (!ALLOWED_SET.has(k)) continue;
    if (v === "" || v === null) {
      issues.push({
        code: "EMPTY_OPTIONAL_FIELD",
        severity: "warn",
        file: relPath,
        field: k,
        message: `選填欄位 ${k} 為空值（${v === null ? "null" : "空字串"}），應刪除`,
        autofix: true,
        fix: { kind: "strip", keys: [k] },
      });
    }
  }

  const schemaResult = frontmatterSchema.safeParse(data);
  if (!schemaResult.success) {
    for (const iss of schemaResult.error.issues) {
      const field = iss.path.join(".") || "(root)";
      const unknown = iss.code === "unrecognized_keys";
      const missing =
        iss.code === "invalid_type" && data[iss.path[0]] === undefined;
      const actualValue = !unknown && !missing ? data[iss.path[0]] : undefined;
      const normalizedDate =
        !unknown && !missing && DATE_FIELDS.has(field)
          ? tryNormalizeDate(actualValue)
          : null;

      if (unknown) {
        issues.push({
          code: "UNKNOWN_FIELD",
          severity: "error",
          file: relPath,
          field,
          message: `白名單外欄位：${iss.keys.join(", ")}`,
          autofix: true,
          fix: { kind: "strip", keys: iss.keys },
        });
      } else if (missing && field === "updated") {
        issues.push({
          code: "MISSING_REQUIRED_FIELD",
          severity: "error",
          file: relPath,
          field,
          message: `缺必填欄位：updated`,
          autofix: true,
          fix: { kind: "fill", field: "updated", value: today },
        });
      } else if (normalizedDate) {
        issues.push({
          code: "INVALID_VALUE",
          severity: "error",
          file: relPath,
          field,
          message: `${field}: ${iss.message}（實際值：${JSON.stringify(actualValue)}）→ 自動 normalize 為 ${normalizedDate}`,
          autofix: true,
          fix: { kind: "fill", field, value: normalizedDate },
        });
      }
    }
  }

  const orderCheck = validateFieldOrder(data);
  if (!orderCheck.ok) {
    issues.push({
      code: "FIELD_ORDER",
      severity: "warn",
      file: relPath,
      message: `欄位順序錯誤：實際 [${orderCheck.actual.join(", ")}]，應為 [${orderCheck.expected.join(", ")}]`,
      autofix: true,
      fix: { kind: "reorder" },
    });
  }

  return { issues, parsed, raw };
}

/**
 * 敏感資料硬掃。以行為單位掃描。
 *
 * Fence 行為（path-aware）：
 * - `content/Inbox/**`（外部不可信原料：Reddit / Clippings / YouTube 等）→ **連 fence 內也掃**。
 *   這類目錄的 code block 正是別人會貼 token 的地方，跳過就完全失守。
 * - 其餘路徑 → 跳過 fence 內，避免 Cards/Topics/CLAUDE.md 中的範例 / 文件誤報。
 *
 * 命中一律 autofix=false，只 flag。
 *
 * `raw` 由 caller 傳入避免重複讀檔；schema-exempt 路徑因 auditFile 沒跑，由 caller 自行讀後傳入。
 */
function scanSensitive(absPath, raw) {
  const relPath = rel(absPath);
  const isUntrustedSource = relPath.startsWith("content/Inbox/");
  const lines = raw.split(/\r?\n/);
  const hits = [];
  let inFence = false;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/^\s*```/.test(line)) {
      inFence = !inFence;
      continue;
    }
    if (inFence && !isUntrustedSource) continue;
    for (const { name, regex } of SENSITIVE_PATTERNS) {
      const m = line.match(regex);
      if (m) {
        hits.push({
          code: "SENSITIVE_DATA",
          severity: "error",
          file: relPath,
          line: i + 1,
          kind: name,
          match: m[0].slice(0, 12) + "…",
          message: `疑似 ${name}（line ${i + 1}）：${m[0].slice(0, 12)}…`,
          autofix: false,
        });
      }
    }
  }
  return hits;
}

/** 套用自動修正到單一檔案，回傳 { applied, blocked, renamedTo } */
function applyFixes(absPath, issues, parsed, raw) {
  const applied = [];
  const blocked = [];
  if (!parsed) return { applied, blocked, renamedTo: null };
  let data = { ...parsed.data };
  let content = parsed.content;
  let renamedTo = null;

  for (const issue of issues) {
    if (!issue.autofix || !issue.fix) continue;
    switch (issue.fix.kind) {
      case "strip": {
        for (const k of issue.fix.keys ?? []) delete data[k];
        applied.push(issue);
        break;
      }
      case "fill": {
        data[issue.fix.field] = issue.fix.value;
        applied.push(issue);
        break;
      }
      case "reorder": {
        applied.push(issue);
        break;
      }
      case "rename": {
        if (existsSync(issue.fix.toAbs)) {
          blocked.push({
            ...issue,
            autofix: false,
            message: `${issue.message}（目標已存在，需手動處理）`,
          });
          break;
        }
        renamedTo = issue.fix.toAbs;
        applied.push(issue);
        break;
      }
    }
  }

  data = reorderFields(data);

  const newRaw = matter.stringify(content, data, matterOptions);

  if (newRaw !== raw || renamedTo) {
    try {
      writeFileSync(absPath, newRaw, "utf8");
    } catch (e) {
      const reason = e?.message ?? String(e);
      const moved = applied.splice(0).map((i) => ({
        ...i,
        autofix: false,
        message: `${i.message}（寫入失敗：${reason}）`,
      }));
      blocked.push(...moved);
      return { applied, blocked, renamedTo: null };
    }
    if (renamedTo) {
      try {
        renameSync(absPath, renamedTo);
      } catch (e) {
        const reason = e?.message ?? String(e);
        const idx = applied.findIndex((i) => i.fix?.kind === "rename");
        if (idx >= 0) {
          const [renameIssue] = applied.splice(idx, 1);
          blocked.push({
            ...renameIssue,
            autofix: false,
            message: `${renameIssue.message}（重新命名失敗：${reason}）`,
          });
        }
        return { applied, blocked, renamedTo: null };
      }
    }
  }
  return { applied, blocked, renamedTo };
}

async function main() {
  const files = await listMarkdown();
  const allIssues = [];
  const allApplied = [];
  const blocked = [];

  const sensitive = [];
  for (const abs of files) {
    let currentAbs = abs;
    let raw;
    if (!isSchemaExempt(abs)) {
      const audit = auditFile(abs);
      raw = audit.raw;
      if (args.fix && audit.issues.length) {
        const result = applyFixes(abs, audit.issues, audit.parsed, audit.raw);
        allApplied.push(...result.applied);
        blocked.push(...result.blocked);
        if (result.renamedTo) currentAbs = result.renamedTo;
        // applyFixes 只處理 autofix=true 的 issue；剩下的（PARSE_ERROR 等）才推進 allIssues
        for (const i of audit.issues)
          if (!i.autofix || !i.fix) allIssues.push(i);
      } else {
        allIssues.push(...audit.issues);
      }
    } else {
      raw = readFileSync(abs, "utf8");
    }
    // 掃原 raw（fix 前）：fix 只動 frontmatter 結構不引入 token，掃原版若 strip 掉
    // 帶 token 的欄位還能留紀錄提醒；rename 不改內容，currentAbs 僅用於 report 顯示路徑。
    const sHits = scanSensitive(currentAbs, raw);
    if (sHits.length) {
      sensitive.push(...sHits);
      allIssues.push(...sHits);
    }
  }

  const byCode = {};
  for (const i of allIssues) byCode[i.code] = (byCode[i.code] ?? 0) + 1;

  const report = {
    summary: {
      total_files_scanned: files.length,
      total_issues: allIssues.length,
      by_category: byCode,
    },
    applied: args.fix ? allApplied : [],
    blocked,
    issues: args.fix ? [] : allIssues,
  };

  if (args.json) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    const mode = args.fix ? "修正" : "檢查";
    console.log(`# Vault ${mode}報告（硬規則）`);
    console.log(`- 掃描檔案：${files.length}`);
    console.log(`- 違規數：${allIssues.length}`);
    if (Object.keys(byCode).length) {
      const cats = Object.entries(byCode)
        .map(([k, v]) => `${codeLabel(k)}=${v}`)
        .join(", ");
      console.log(`- 分類：${cats}`);
    }

    if (args.fix) {
      console.log(`\n## 已修正（${allApplied.length}）`);
      for (const i of allApplied) {
        console.log(`- [${codeLabel(i.code)}] ${i.file} — ${i.message}`);
      }
      if (blocked.length) {
        console.log(`\n## 修正被阻擋（${blocked.length}，需手動處理）`);
        for (const i of blocked) {
          console.log(`- [${codeLabel(i.code)}] ${i.file} — ${i.message}`);
        }
      }
      const unhandled = allIssues.filter((i) => !sensitive.includes(i));
      if (unhandled.length) {
        console.log(`\n## 未自動處理（${unhandled.length}，需手動處理）`);
        for (const i of unhandled) {
          console.log(`- [${codeLabel(i.code)}] ${i.file} — ${i.message}`);
        }
      }
    } else if (allIssues.length) {
      console.log(`\n## 違規清單`);
      for (const i of allIssues) {
        console.log(`- [${codeLabel(i.code)}] ${i.file} — ${i.message}`);
      }
      console.log(
        `\n執行 \`node scripts/vault-check.mjs --fix\` 自動修可修項。`,
      );
    }

    if (sensitive.length) {
      console.log(
        `\n## ⚠ 疑似敏感資料（${sensitive.length}，high-precision 硬掃）`,
      );
      for (const i of sensitive) {
        console.log(`- ${i.file}:${i.line} [${i.kind}] ${i.match}`);
      }
      console.log(
        `\n請立即檢查並移除；此項不會自動修改，但會讓 exit code 為非零。`,
      );
    }

    console.log(
      `\n備註：完整語意層稽核（wikilink 斷鏈、tag 一致性、自然語言密碼 / 個資、缺 title/created/tags）由語意層稽核流程（/vault-check skill 內 audit reference）處理。`,
    );
  }

  const hardFail = sensitive.length > 0;
  const softFail = blocked.length > 0 || allIssues.length > 0;
  process.exit(hardFail || softFail ? 1 : 0);
}

main().catch((e) => {
  console.error(e);
  process.exit(2);
});
