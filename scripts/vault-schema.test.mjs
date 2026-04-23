import { describe, it } from "node:test";
import assert from "node:assert/strict";
import {
  FIELD_ORDER,
  REQUIRED_FIELDS,
  SENSITIVE_PATTERNS,
  WIKILINK_RE,
  codeLabel,
  frontmatterSchema,
  reorderFields,
  scanSensitive,
  stripCodeForLinkScan,
  stripUnknownFields,
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

describe("codeLabel", () => {
  it("已知 code 回中文", () => {
    assert.equal(codeLabel("FIELD_ORDER"), "欄位順序錯誤");
  });

  it("未知 code 回原字串", () => {
    assert.equal(codeLabel("NOT_A_CODE"), "NOT_A_CODE");
  });
});

describe("scanSensitive", () => {
  it("偵測 OpenAI key（不漏 prefix）", () => {
    const hits = scanSensitive("token is sk-abcdefghij1234567890ABCD done");
    assert.equal(hits.length, 1);
    assert.equal(hits[0].name, "OpenAI API key");
    assert.equal(hits[0].line, 1);
  });

  it("偵測 Anthropic key", () => {
    const hits = scanSensitive("sk-ant-api03-abcdefghij1234567890XYZ");
    assert.ok(hits.some((h) => h.name === "Anthropic API key"));
  });

  it("偵測 GitHub token", () => {
    const hits = scanSensitive("key=ghp_abcdefghij1234567890ABCDEFGHIJKLMNOP");
    assert.ok(hits.some((h) => h.name === "GitHub token"));
  });

  it("偵測 AWS access key", () => {
    const hits = scanSensitive("AKIAIOSFODNN7EXAMPLE");
    assert.ok(hits.some((h) => h.name === "AWS access key"));
  });

  it("偵測 private key header", () => {
    const hits = scanSensitive("-----BEGIN RSA PRIVATE KEY-----\n...");
    assert.ok(hits.some((h) => h.name === "Private key header"));
  });

  it("不誤報一般文字", () => {
    const hits = scanSensitive("這是正常的中文筆記，沒有任何敏感資料");
    assert.equal(hits.length, 0);
  });

  it("多行正確回報行號", () => {
    const text = "line1\nline2 sk-abcdefghij1234567890ABCD\nline3";
    const hits = scanSensitive(text);
    assert.equal(hits[0].line, 2);
  });

  it("多次呼叫結果一致（regex lastIndex 正確重置）", () => {
    const text = "sk-abcdefghij1234567890ABCD";
    const first = scanSensitive(text).length;
    const second = scanSensitive(text).length;
    assert.equal(first, second);
    assert.equal(SENSITIVE_PATTERNS.length > 0, true);
  });
});

describe("stripCodeForLinkScan", () => {
  it("fenced code block 內容被空白化（保留換行）", () => {
    const input = "before\n```\n[[InsideCode]]\n```\nafter";
    const out = stripCodeForLinkScan(input);
    assert.ok(!out.includes("[[InsideCode]]"));
    assert.equal(out.split("\n").length, input.split("\n").length);
  });

  it("inline code 內容被空白化", () => {
    const input = "see `[[X]]` here";
    const out = stripCodeForLinkScan(input);
    assert.ok(!out.includes("[[X]]"));
  });

  it("非 code 區塊的 wikilink 保留", () => {
    const input = "這是 [[RealLink]] 不是程式";
    const out = stripCodeForLinkScan(input);
    assert.ok(out.includes("[[RealLink]]"));
  });
});

describe("WIKILINK_RE", () => {
  const extractAll = (text) => {
    WIKILINK_RE.lastIndex = 0;
    const out = [];
    let m;
    while ((m = WIKILINK_RE.exec(text)) !== null) {
      out.push(m[1]);
    }
    return out;
  };

  it("擷取純 wikilink", () => {
    assert.deepEqual(extractAll("see [[Foo]] and [[Bar]]"), ["Foo", "Bar"]);
  });

  it("擷取 wikilink 含 alias", () => {
    assert.deepEqual(extractAll("[[Foo|顯示名]]"), ["Foo"]);
  });

  it("擷取 embed", () => {
    assert.deepEqual(extractAll("![[image.png]]"), ["image.png"]);
  });

  it("純 anchor 無 target", () => {
    WIKILINK_RE.lastIndex = 0;
    const m = WIKILINK_RE.exec("[[#heading]]");
    assert.equal(m[1], undefined);
  });
});
