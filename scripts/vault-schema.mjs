/**
 * Vault Frontmatter Schema — 真實來源
 *
 * 此檔為 vault 筆記 frontmatter 的機器驗證真實來源。
 * 新增／修改欄位、改順序、改必填、改型別皆在此修改。
 *
 * content/CLAUDE.md 的「欄位說明」表格只記人類語意（作用、出現情境），
 * 不複述欄位清單或順序。兩者分工：schema 管機械，CLAUDE.md 管語意。
 *
 * /vault-check 的兩段（scripts/vault-check.mjs 硬規則自動修 + 語意層稽核
 * 流程，即 /vault-check skill 內 audit reference）皆讀取此檔。
 */
import { z } from "zod";

export const FIELD_ORDER = [
  "title",
  "created",
  "updated",
  "source",
  "published",
  "parent",
  "extracted_to",
  "last_sync_id",
  "draft",
  "tags",
];

export const REQUIRED_FIELDS = ["title", "created", "updated", "tags"];

/** 規則 code → 中文標籤（人類報告用；JSON 輸出仍保留原 code）
 *
 * 列 script 會自動修的硬規則，外加 SENSITIVE_DATA 與 PARSE_ERROR（script 做
 * high-precision 偵測 + flag 不修，作為 CI 最後一道防線；完整語意層稽核仍由
 * 語意層稽核流程（audit reference）處理）。其餘語意層問題（BROKEN_WIKILINK /
 * 缺 title-created-tags / tag 一致性）仍全由 audit reference 處理。
 */
export const CODE_LABELS = {
  FILENAME_HAS_SPACE: "檔名含空格",
  MISSING_REQUIRED_FIELD: "缺必填欄位",
  INVALID_VALUE: "值格式錯誤",
  UNKNOWN_FIELD: "白名單外欄位",
  EMPTY_OPTIONAL_FIELD: "選填欄位為空",
  FIELD_ORDER: "欄位順序錯誤",
  SENSITIVE_DATA: "敏感資料（硬掃）",
  PARSE_ERROR: "frontmatter 解析失敗",
};

export const codeLabel = (code) => CODE_LABELS[code] ?? code;

const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
const WIKILINK_VALUE_RE = /^\[\[[^\]]+\]\]$/;

/** YYYY[/.-]M[/.-]D（月/日可 1-2 位）— 接受 `/`、`.`、`-` 分隔 */
const DATE_NORMALIZE_RE = /^(\d{4})[\/.\-](\d{1,2})[\/.\-](\d{1,2})$/;

/**
 * 嘗試把常見變體日期 normalize 為 `YYYY-MM-DD`。
 * 支援：`YYYY/MM/DD`、`YYYY.MM.DD`、`YYYY-M-D` 等分隔/零填充變體。
 * 不支援：英文月份、`DD/MM/YYYY` 類（兩端無法判別）、非字串。
 * 回 null 表示無法安全推斷。
 */
export function tryNormalizeDate(value) {
  if (typeof value !== "string") return null;
  const m = DATE_NORMALIZE_RE.exec(value.trim());
  if (!m) return null;
  const [, y, mo, d] = m;
  const monthNum = Number(mo);
  const dayNum = Number(d);
  const mm = String(monthNum).padStart(2, "0");
  const dd = String(dayNum).padStart(2, "0");
  const norm = `${y}-${mm}-${dd}`;
  const date = new Date(`${norm}T00:00:00Z`);
  if (
    Number.isNaN(date.getTime()) ||
    date.getUTCFullYear() !== Number(y) ||
    date.getUTCMonth() !== monthNum - 1 ||
    date.getUTCDate() !== dayNum
  ) {
    return null;
  }
  if (norm === value) return null;
  return norm;
}

/** 接受 date normalize 的欄位白名單 */
export const DATE_FIELDS = new Set(["created", "updated", "published"]);

const dateString = z
  .string()
  .regex(DATE_RE, { message: "日期格式必須為 YYYY-MM-DD" });

const emptyToUndef = (v) => (v === "" || v === null ? undefined : v);
const optional = (schema) => z.preprocess(emptyToUndef, schema.optional());

export const frontmatterSchema = z
  .object({
    title: z.string().min(1),
    created: dateString,
    updated: dateString,
    source: optional(z.string().url()),
    published: optional(dateString),
    parent: optional(
      z.string().regex(WIKILINK_VALUE_RE, {
        message: "parent 必須為 wikilink 格式 [[...]]",
      }),
    ),
    extracted_to: optional(
      z.string().regex(WIKILINK_VALUE_RE, {
        message: "extracted_to 必須為 wikilink 格式 [[...]]",
      }),
    ),
    last_sync_id: optional(z.string()),
    draft: optional(z.boolean()),
    tags: z.array(z.string().min(1)).min(1),
  })
  .strict();

export function validateFieldOrder(data) {
  const keys = Object.keys(data);
  const indexed = keys
    .map((k) => ({ key: k, order: FIELD_ORDER.indexOf(k) }))
    .filter((x) => x.order >= 0);
  for (let i = 1; i < indexed.length; i++) {
    if (indexed[i].order < indexed[i - 1].order) {
      return {
        ok: false,
        actual: indexed.map((x) => x.key),
        expected: indexed
          .slice()
          .sort((a, b) => a.order - b.order)
          .map((x) => x.key),
      };
    }
  }
  return { ok: true };
}

export function reorderFields(data) {
  const ordered = {};
  for (const key of FIELD_ORDER) {
    if (data[key] !== undefined) ordered[key] = data[key];
  }
  return ordered;
}

export function stripUnknownFields(data) {
  const allowed = new Set(FIELD_ORDER);
  const stripped = [];
  const clean = {};
  for (const [k, v] of Object.entries(data)) {
    if (allowed.has(k)) clean[k] = v;
    else stripped.push(k);
  }
  return { clean, stripped };
}
