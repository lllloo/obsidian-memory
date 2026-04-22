import { z } from "zod"

export const FIELD_ORDER = [
  "title",
  "created",
  "updated",
  "source",
  "published",
  "parent",
  "last_sync_id",
  "draft",
  "tags",
]

export const REQUIRED_FIELDS = ["title", "created", "updated", "tags"]

/** 規則 code → 中文標籤（人類報告用；JSON 輸出仍保留原 code） */
export const CODE_LABELS = {
  FILENAME_HAS_SPACE: "檔名含空格",
  FRONTMATTER_PARSE_ERROR: "Frontmatter 解析失敗",
  MISSING_REQUIRED_FIELD: "缺必填欄位",
  INVALID_VALUE: "值格式錯誤",
  UNKNOWN_FIELD: "白名單外欄位",
  EMPTY_OPTIONAL_FIELD: "選填欄位為空",
  FIELD_ORDER: "欄位順序錯誤",
  // 尚未實作
  BROKEN_WIKILINK: "Wikilink 斷鏈",
  SENSITIVE_DATA: "敏感資料",
  MISPLACED_NOTE: "位置錯誤",
}

export const codeLabel = (code) => CODE_LABELS[code] ?? code

const DATE_RE = /^\d{4}-\d{2}-\d{2}$/
const WIKILINK_RE = /^\[\[[^\]]+\]\]$/

const dateString = z
  .string()
  .regex(DATE_RE, { message: "日期格式必須為 YYYY-MM-DD" })

const emptyToUndef = (v) => (v === "" || v === null ? undefined : v)
const optional = (schema) => z.preprocess(emptyToUndef, schema.optional())

export const frontmatterSchema = z
  .object({
    title: z.string().min(1),
    created: dateString,
    updated: dateString,
    source: optional(z.string().url()),
    published: optional(dateString),
    parent: optional(
      z
        .string()
        .regex(WIKILINK_RE, { message: "parent 必須為 wikilink 格式 [[...]]" }),
    ),
    last_sync_id: optional(z.string()),
    draft: optional(z.boolean()),
    tags: z.array(z.string().min(1)).min(1),
  })
  .strict()

export function validateFieldOrder(data) {
  const keys = Object.keys(data)
  const indexed = keys
    .map((k) => ({ key: k, order: FIELD_ORDER.indexOf(k) }))
    .filter((x) => x.order >= 0)
  for (let i = 1; i < indexed.length; i++) {
    if (indexed[i].order < indexed[i - 1].order) {
      return {
        ok: false,
        actual: indexed.map((x) => x.key),
        expected: indexed
          .slice()
          .sort((a, b) => a.order - b.order)
          .map((x) => x.key),
      }
    }
  }
  return { ok: true }
}

export function reorderFields(data) {
  const ordered = {}
  for (const key of FIELD_ORDER) {
    if (data[key] !== undefined) ordered[key] = data[key]
  }
  return ordered
}

export function stripUnknownFields(data) {
  const allowed = new Set(FIELD_ORDER)
  const stripped = []
  const clean = {}
  for (const [k, v] of Object.entries(data)) {
    if (allowed.has(k)) clean[k] = v
    else stripped.push(k)
  }
  return { clean, stripped }
}
