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
  stripUnknownFields,
  tryNormalizeDate,
  validateFieldOrder,
} from "./vault-schema.mjs";

const REQUIRED_SET = new Set(REQUIRED_FIELDS);

const REPO_ROOT = resolve(import.meta.dirname, "..");
const CONTENT_DIR = join(REPO_ROOT, "content");
const EXCLUDED = new Set([
  "content/index.md",
  "content/master-index.md",
  "content/CLAUDE.md",
]);

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
語意層稽核（wikilink 斷鏈、敏感資料、misplaced、tag 一致性、缺 title/created/tags、parse error）
由 vault-auditor subagent 處理，不在此 script。

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
 * 不可推斷的 INVALID_VALUE）一律跳過交 vault-auditor subagent 處理。
 */
function auditFile(absPath) {
  const issues = [];
  const relPath = rel(absPath);
  const raw = readFileSync(absPath, "utf8");

  let parsed;
  try {
    parsed = matter(raw, matterOptions);
  } catch {
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

/** 套用自動修正到單一檔案，回傳 { applied, blocked } */
function applyFixes(absPath, issues, parsed, raw) {
  const applied = [];
  const blocked = [];
  if (!parsed) return { applied, blocked };
  let data = { ...parsed.data };
  let content = parsed.content;
  let renamedTo = null;

  for (const issue of issues) {
    if (!issue.autofix || !issue.fix) continue;
    switch (issue.fix.kind) {
      case "strip": {
        for (const k of issue.fix.keys ?? []) delete data[k];
        const { clean } = stripUnknownFields(data);
        data = clean;
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
    writeFileSync(absPath, newRaw, "utf8");
    if (renamedTo) {
      renameSync(absPath, renamedTo);
    }
  }
  return { applied, blocked };
}

async function main() {
  const files = await listMarkdown();
  const allIssues = [];
  const allApplied = [];
  const blocked = [];

  for (const abs of files) {
    const { issues, parsed, raw } = auditFile(abs);
    allIssues.push(...issues);
    if (args.fix && issues.length) {
      const result = applyFixes(abs, issues, parsed, raw);
      allApplied.push(...result.applied);
      blocked.push(...result.blocked);
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
    } else if (allIssues.length) {
      console.log(`\n## 違規清單`);
      for (const i of allIssues) {
        console.log(`- [${codeLabel(i.code)}] ${i.file} — ${i.message}`);
      }
      console.log(
        `\n執行 \`node scripts/vault-check.mjs --fix\` 自動修可修項。`,
      );
    }

    console.log(
      `\n備註：語意層稽核（wikilink 斷鏈、敏感資料、misplaced、tag 一致性、缺 title/created/tags、parse error）由 vault-auditor subagent 處理。`,
    );
  }

  const failed = args.fix ? blocked.length > 0 : allIssues.length > 0;
  process.exit(failed ? 1 : 0);
}

main().catch((e) => {
  console.error(e);
  process.exit(2);
});
