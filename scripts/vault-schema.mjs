import { z } from "zod";

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
];

export const REQUIRED_FIELDS = ["title", "created", "updated", "tags"];

/** 規則 code → 中文標籤（人類報告用；JSON 輸出仍保留原 code） */
export const CODE_LABELS = {
  FILENAME_HAS_SPACE: "檔名含空格",
  FRONTMATTER_PARSE_ERROR: "Frontmatter 解析失敗",
  MISSING_REQUIRED_FIELD: "缺必填欄位",
  INVALID_VALUE: "值格式錯誤",
  UNKNOWN_FIELD: "白名單外欄位",
  EMPTY_OPTIONAL_FIELD: "選填欄位為空",
  FIELD_ORDER: "欄位順序錯誤",
  BROKEN_WIKILINK: "Wikilink 斷鏈",
  SENSITIVE_DATA: "敏感資料",
  // 尚未實作
  MISPLACED_NOTE: "位置錯誤",
};

export const codeLabel = (code) => CODE_LABELS[code] ?? code;

const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
const WIKILINK_VALUE_RE = /^\[\[[^\]]+\]\]$/;

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

/**
 * Wikilink 偵測 regex — 與 Quartz `ofm.ts` 同步，含 embed、anchor、alias。
 * Group 1 = target（路徑，可能含資料夾）
 */
export const WIKILINK_RE =
  /!?\[\[([^\[\]\|\#\\]+)?(#+[^\[\]\|\#\\]+)?(\\?\|[^\[\]\#]*)?\]\]/g;

/**
 * 以「行為保留換行」的方式，把 fenced code block 與 inline code 變空白。
 * 目的：避免 wikilink 掃描把程式碼範例裡的 `[[X]]` 當作真連結。
 */
export function stripCodeForLinkScan(text) {
  const blank = (m) => m.replace(/[^\n]/g, " ");
  return text.replace(/```[\s\S]*?```/g, blank).replace(/`[^`\n]+`/g, blank);
}

/**
 * 敏感資料 regex（掃描筆記正文與 frontmatter 值）
 *
 * 參考 content/CLAUDE.md：API key / token / 密碼 / 私人 IP。
 * 故意偏向 high-precision（可能漏，但少誤報）— 誤報反而會讓用戶忽略告警。
 *
 * 加新規則前請思考：會不會對一般技術筆記誤報？
 */
export const SENSITIVE_PATTERNS = [
  {
    name: "OpenAI API key",
    re: /\bsk-[a-zA-Z0-9_-]{20,}\b/g,
  },
  {
    name: "Anthropic API key",
    re: /\bsk-ant-[a-zA-Z0-9_-]{20,}\b/g,
  },
  {
    name: "GitHub token",
    re: /\b(ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{30,}\b/g,
  },
  {
    name: "AWS access key",
    re: /\bAKIA[0-9A-Z]{16}\b/g,
  },
  {
    name: "Google API key",
    re: /\bAIza[0-9A-Za-z_-]{35}\b/g,
  },
  {
    name: "Slack token",
    re: /\bxox[baprs]-[a-zA-Z0-9-]{10,}\b/g,
  },
  {
    name: "JWT token",
    re: /\beyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\b/g,
  },
  {
    name: "Private key header",
    re: /-----BEGIN (RSA |DSA |EC |OPENSSH |PGP )?PRIVATE KEY-----/g,
  },
];

/**
 * 掃描文字內所有敏感資料命中。
 * 回傳 [{ name, match, line }]，line 從 1 起算。
 */
export function scanSensitive(text) {
  const hits = [];
  const lines = text.split(/\r?\n/);
  for (const { name, re } of SENSITIVE_PATTERNS) {
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      re.lastIndex = 0;
      let m;
      while ((m = re.exec(line)) !== null) {
        hits.push({ name, match: m[0], line: i + 1 });
      }
    }
  }
  return hits;
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
