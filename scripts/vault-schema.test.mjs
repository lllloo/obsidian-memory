import { describe, it } from "node:test";
import assert from "node:assert/strict";
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

describe("frontmatterSchema", () => {
  const minimal = {
    title: "t",
    created: "2026-04-01",
    updated: "2026-04-23",
    tags: ["x"],
  };

  it("接受最小合法 frontmatter", () => {
    const r = frontmatterSchema.safeParse(minimal);
    assert.equal(r.success, true);
  });

  it("拒絕缺 title", () => {
    const r = frontmatterSchema.safeParse({ ...minimal, title: undefined });
    assert.equal(r.success, false);
  });

  it("拒絕非 YYYY-MM-DD 日期", () => {
    const r = frontmatterSchema.safeParse({
      ...minimal,
      created: "2026/04/01",
    });
    assert.equal(r.success, false);
  });

  it("拒絕空 tags 陣列", () => {
    const r = frontmatterSchema.safeParse({ ...minimal, tags: [] });
    assert.equal(r.success, false);
  });

  it("拒絕非陣列 tags", () => {
    const r = frontmatterSchema.safeParse({ ...minimal, tags: "x" });
    assert.equal(r.success, false);
  });

  it("拒絕未白名單欄位", () => {
    const r = frontmatterSchema.safeParse({ ...minimal, author: "Roy" });
    assert.equal(r.success, false);
    const codes = r.error.issues.map((i) => i.code);
    assert.ok(codes.includes("unrecognized_keys"));
  });

  it("source 必須為合法 URL", () => {
    const ok = frontmatterSchema.safeParse({
      ...minimal,
      source: "https://example.com",
    });
    const bad = frontmatterSchema.safeParse({ ...minimal, source: "notaurl" });
    assert.equal(ok.success, true);
    assert.equal(bad.success, false);
  });

  it("source / published 的空字串會被視為 undefined（選填）", () => {
    const r = frontmatterSchema.safeParse({
      ...minimal,
      source: "",
      published: "",
    });
    assert.equal(r.success, true);
  });

  it("parent 必須為 [[wikilink]] 格式", () => {
    const ok = frontmatterSchema.safeParse({
      ...minimal,
      parent: "[[01.index]]",
    });
    const bad = frontmatterSchema.safeParse({ ...minimal, parent: "01.index" });
    assert.equal(ok.success, true);
    assert.equal(bad.success, false);
  });

  it("extracted_to 必須為 [[wikilink]] 格式", () => {
    const ok = frontmatterSchema.safeParse({
      ...minimal,
      extracted_to: "[[Claude-Design-全景評估]]",
    });
    const bad = frontmatterSchema.safeParse({
      ...minimal,
      extracted_to: "Claude-Design-全景評估",
    });
    assert.equal(ok.success, true);
    assert.equal(bad.success, false);
  });
});

describe("validateFieldOrder / reorderFields", () => {
  it("合法順序回 ok", () => {
    const ok = validateFieldOrder({
      title: "t",
      created: "2026-01-01",
      updated: "2026-01-02",
      tags: ["x"],
    });
    assert.equal(ok.ok, true);
  });

  it("tags 放最前會被抓出錯誤", () => {
    const r = validateFieldOrder({
      tags: ["x"],
      title: "t",
      created: "2026-01-01",
      updated: "2026-01-02",
    });
    assert.equal(r.ok, false);
  });

  it("reorderFields 把欄位排回 FIELD_ORDER 順序", () => {
    const data = {
      tags: ["a"],
      title: "t",
      updated: "2026-01-02",
      created: "2026-01-01",
    };
    const ordered = reorderFields(data);
    assert.deepEqual(Object.keys(ordered), [
      "title",
      "created",
      "updated",
      "tags",
    ]);
  });

  it("reorderFields 冪等", () => {
    const data = {
      title: "t",
      tags: ["a"],
      created: "2026-01-01",
      updated: "2026-01-02",
    };
    const once = reorderFields(data);
    const twice = reorderFields(once);
    assert.deepEqual(Object.keys(twice), Object.keys(once));
  });
});

describe("stripUnknownFields", () => {
  it("移除非白名單欄位並回報", () => {
    const { clean, stripped } = stripUnknownFields({
      title: "t",
      author: "Roy",
      cover: "x.png",
    });
    assert.deepEqual(Object.keys(clean), ["title"]);
    assert.deepEqual(stripped.sort(), ["author", "cover"]);
  });
});

describe("REQUIRED_FIELDS / FIELD_ORDER 一致性", () => {
  it("REQUIRED 全部在 FIELD_ORDER 裡", () => {
    for (const k of REQUIRED_FIELDS) {
      assert.ok(FIELD_ORDER.includes(k), `${k} 不在 FIELD_ORDER`);
    }
  });
});

describe("tryNormalizeDate", () => {
  it("slash 分隔轉 dash", () => {
    assert.equal(tryNormalizeDate("2026/04/01"), "2026-04-01");
  });

  it("dot 分隔轉 dash", () => {
    assert.equal(tryNormalizeDate("2026.04.01"), "2026-04-01");
  });

  it("月/日未零填充也能 normalize", () => {
    assert.equal(tryNormalizeDate("2026/4/1"), "2026-04-01");
    assert.equal(tryNormalizeDate("2026-4-1"), "2026-04-01");
  });

  it("已是合法 YYYY-MM-DD 回 null（不需修）", () => {
    assert.equal(tryNormalizeDate("2026-04-01"), null);
  });

  it("非字串回 null", () => {
    assert.equal(tryNormalizeDate(null), null);
    assert.equal(tryNormalizeDate(undefined), null);
    assert.equal(tryNormalizeDate(20260401), null);
    assert.equal(tryNormalizeDate(new Date()), null);
  });

  it("非法日期（月份超出、日期超出）回 null", () => {
    assert.equal(tryNormalizeDate("2026/13/01"), null);
    assert.equal(tryNormalizeDate("2026/02/30"), null);
    assert.equal(tryNormalizeDate("2026/00/01"), null);
  });

  it("英文月份、`YYYY年M月D日`、`MM/DD/YYYY` 不支援", () => {
    assert.equal(tryNormalizeDate("Apr 1, 2026"), null);
    assert.equal(tryNormalizeDate("2026年4月1日"), null);
    assert.equal(tryNormalizeDate("04/01/2026"), null);
  });

  it("DATE_FIELDS 涵蓋所有 date 欄位", () => {
    assert.ok(DATE_FIELDS.has("created"));
    assert.ok(DATE_FIELDS.has("updated"));
    assert.ok(DATE_FIELDS.has("published"));
  });
});

describe("codeLabel", () => {
  it("已知 code 回中文", () => {
    assert.equal(codeLabel("FIELD_ORDER"), "欄位順序錯誤");
  });

  it("未知 code 回原字串", () => {
    assert.equal(codeLabel("NOT_A_CODE"), "NOT_A_CODE");
  });

  it("語意層 code 不在 label 表（已交 audit reference）", () => {
    assert.equal(codeLabel("BROKEN_WIKILINK"), "BROKEN_WIKILINK");
  });
});
