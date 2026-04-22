#!/usr/bin/env node
import { readFileSync, writeFileSync, renameSync, existsSync } from "node:fs"
import { basename, dirname, join, parse, relative, resolve } from "node:path"
import { globby } from "globby"
import matter from "gray-matter"
import yaml from "js-yaml"
import { parseArgs } from "node:util"

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
}
const matterOptions = { engines: { yaml: yamlEngine } }
import {
  FIELD_ORDER,
  REQUIRED_FIELDS,
  codeLabel,
  frontmatterSchema,
  reorderFields,
  stripUnknownFields,
  validateFieldOrder,
} from "./vault-schema.mjs"

const REQUIRED_SET = new Set(REQUIRED_FIELDS)

const REPO_ROOT = resolve(import.meta.dirname, "..")
const CONTENT_DIR = join(REPO_ROOT, "content")
const EXCLUDED = new Set([
  "content/index.md",
  "content/master-index.md",
  "content/CLAUDE.md",
])

const { values: args } = parseArgs({
  options: {
    fix: { type: "boolean", default: false },
    json: { type: "boolean", default: false },
    help: { type: "boolean", short: "h", default: false },
  },
})

if (args.help) {
  console.log(`Usage: node scripts/vault-check.mjs [--fix] [--json]

掃描 content/ 下所有 .md 的 frontmatter 與檔名，依 Zod schema 驗證。

  --fix    自動修可修項目（欄位順序、白名單外欄位、補 updated、檔名空格）
  --json   以 JSON 輸出（預設為人類可讀）`)
  process.exit(0)
}

const today = new Date().toISOString().slice(0, 10)

/** 將路徑轉成 repo-relative、forward-slash 形式 */
function rel(p) {
  return relative(REPO_ROOT, p).replaceAll("\\", "/")
}

async function listMarkdown() {
  const patterns = ["content/**/*.md", "!content/.obsidian/**"]
  const files = await globby(patterns, { cwd: REPO_ROOT, absolute: true })
  return files.filter((f) => !EXCLUDED.has(rel(f)))
}

/** 檢查檔名是否含空格；回傳建議的新檔名（若需要） */
function checkFilename(absPath) {
  const name = basename(absPath)
  if (!name.includes(" ")) return null
  const dir = dirname(absPath)
  const { name: stem, ext } = parse(name)
  const normalizedStem = stem
    .replaceAll(/\s+/g, "-")
    .replaceAll(/-+/g, "-")
    .replace(/^-+|-+$/g, "")
  if (!normalizedStem) return null
  const renamed = normalizedStem + ext
  if (renamed === name) return null
  return { dir, from: name, to: renamed, toAbs: join(dir, renamed) }
}

/** 對單一檔案做稽核，回傳 issues 陣列 */
function auditFile(absPath) {
  const issues = []
  const relPath = rel(absPath)
  const raw = readFileSync(absPath, "utf8")

  let parsed
  try {
    parsed = matter(raw, matterOptions)
  } catch (e) {
    issues.push({
      code: "FRONTMATTER_PARSE_ERROR",
      severity: "error",
      file: relPath,
      message: `frontmatter 解析失敗：${e.message}`,
      autofix: false,
    })
    return { issues, parsed: null, raw }
  }

  const data = parsed.data ?? {}

  const fnIssue = checkFilename(absPath)
  if (fnIssue) {
    issues.push({
      code: "FILENAME_HAS_SPACE",
      severity: "error",
      file: relPath,
      message: `檔名含空格：'${fnIssue.from}' → '${fnIssue.to}'`,
      autofix: true,
      fix: { kind: "rename", ...fnIssue },
    })
  }

  for (const [k, v] of Object.entries(data)) {
    if (REQUIRED_SET.has(k)) continue
    if (v === "" || v === null) {
      issues.push({
        code: "EMPTY_OPTIONAL_FIELD",
        severity: "warn",
        file: relPath,
        field: k,
        message: `選填欄位 ${k} 為空值（${v === null ? "null" : "空字串"}），應刪除`,
        autofix: true,
        fix: { kind: "strip", keys: [k] },
      })
    }
  }

  const schemaResult = frontmatterSchema.safeParse(data)
  if (!schemaResult.success) {
    for (const iss of schemaResult.error.issues) {
      const field = iss.path.join(".") || "(root)"
      const unknown = iss.code === "unrecognized_keys"
      const missing =
        iss.code === "invalid_type" && data[iss.path[0]] === undefined
      const code = unknown
        ? "UNKNOWN_FIELD"
        : missing
          ? "MISSING_REQUIRED_FIELD"
          : "INVALID_VALUE"
      issues.push({
        code,
        severity: "error",
        file: relPath,
        field,
        message: unknown
          ? `白名單外欄位：${iss.keys.join(", ")}`
          : missing
            ? `缺必填欄位：${field}`
            : `${field}: ${iss.message}`,
        autofix: unknown || (missing && field === "updated"),
        fix: unknown
          ? { kind: "strip", keys: iss.keys }
          : missing && field === "updated"
            ? { kind: "fill", field: "updated", value: today }
            : undefined,
      })
    }
  }

  const orderCheck = validateFieldOrder(data)
  if (!orderCheck.ok) {
    issues.push({
      code: "FIELD_ORDER",
      severity: "warn",
      file: relPath,
      message: `欄位順序錯誤：實際 [${orderCheck.actual.join(", ")}]，應為 [${orderCheck.expected.join(", ")}]`,
      autofix: true,
      fix: { kind: "reorder" },
    })
  }

  return { issues, parsed, raw }
}

/** 套用自動修正到單一檔案，回傳 { applied, blocked } */
function applyFixes(absPath, issues, parsed, raw) {
  const applied = []
  const blocked = []
  if (!parsed) return { applied, blocked }
  let data = { ...parsed.data }
  let content = parsed.content
  let renamedTo = null

  for (const issue of issues) {
    if (!issue.autofix || !issue.fix) continue
    switch (issue.fix.kind) {
      case "strip": {
        for (const k of issue.fix.keys ?? []) delete data[k]
        const { clean } = stripUnknownFields(data)
        data = clean
        applied.push(issue)
        break
      }
      case "fill": {
        data[issue.fix.field] = issue.fix.value
        applied.push(issue)
        break
      }
      case "reorder": {
        // 稍後統一 reorder
        applied.push(issue)
        break
      }
      case "rename": {
        if (existsSync(issue.fix.toAbs)) {
          blocked.push({
            ...issue,
            autofix: false,
            message: `${issue.message}（目標已存在，需手動處理）`,
          })
          break
        }
        renamedTo = issue.fix.toAbs
        applied.push(issue)
        break
      }
    }
  }

  // 統一最後 reorder（修過欄位後順序可能亂掉）
  data = reorderFields(data)

  const newRaw = matter.stringify(content, data, matterOptions)

  if (newRaw !== raw || renamedTo) {
    writeFileSync(absPath, newRaw, "utf8")
    if (renamedTo) {
      renameSync(absPath, renamedTo)
    }
  }
  return { applied, blocked }
}

async function main() {
  const files = await listMarkdown()
  const allIssues = []
  const allApplied = []
  const skipped = []

  for (const abs of files) {
    const { issues, parsed, raw } = auditFile(abs)
    allIssues.push(...issues)
    if (args.fix && issues.some((i) => i.autofix)) {
      const { applied, blocked } = applyFixes(abs, issues, parsed, raw)
      allApplied.push(...applied)
      skipped.push(...blocked)
    }
    for (const iss of issues) {
      if (!iss.autofix) skipped.push(iss)
    }
  }

  const byCode = {}
  for (const i of allIssues) byCode[i.code] = (byCode[i.code] ?? 0) + 1

  const report = {
    summary: {
      total_files_scanned: files.length,
      total_issues: allIssues.length,
      by_category: byCode,
    },
    applied: args.fix ? allApplied : [],
    skipped,
    issues: args.fix ? [] : allIssues,
  }

  if (args.json) {
    console.log(JSON.stringify(report, null, 2))
  } else {
    const mode = args.fix ? "修正" : "檢查"
    console.log(`# Vault ${mode}報告`)
    console.log(`- 掃描檔案：${files.length}`)
    console.log(`- 違規數：${allIssues.length}`)
    if (Object.keys(byCode).length) {
      const cats = Object.entries(byCode)
        .map(([k, v]) => `${codeLabel(k)}=${v}`)
        .join(", ")
      console.log(`- 分類：${cats}`)
    }

    if (args.fix) {
      console.log(`\n## 已修正（${allApplied.length}）`)
      for (const i of allApplied) {
        console.log(`- [${codeLabel(i.code)}] ${i.file} — ${i.message}`)
      }
      if (skipped.length) {
        console.log(`\n## 無法自動修（${skipped.length}，需手動處理）`)
        for (const i of skipped) {
          console.log(`- [${codeLabel(i.code)}] ${i.file} — ${i.message}`)
        }
      }
    } else if (allIssues.length) {
      console.log(`\n## 違規清單`)
      for (const i of allIssues) {
        const tag = i.autofix ? "可自動修" : "手動"
        console.log(`- [${codeLabel(i.code)}/${tag}] ${i.file} — ${i.message}`)
      }
      console.log(`\n執行 \`node scripts/vault-check.mjs --fix\` 自動修可修項。`)
    }
  }

  const failed = args.fix ? skipped.length > 0 : allIssues.length > 0
  process.exit(failed ? 1 : 0)
}

main().catch((e) => {
  console.error(e)
  process.exit(2)
})
