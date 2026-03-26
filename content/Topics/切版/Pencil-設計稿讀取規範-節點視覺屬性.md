---
title: Pencil 設計稿讀取規範 - 節點視覺屬性
tags:
  - 切版
  - frontend
  - css
created: 2026-03-25
updated: 2026-03-25
---

## 核心原則

**每個節點都必須讀，每個屬性都有意義。**

讀取任何 Node 時，遞迴到所有葉節點，逐一確認下列屬性。容器沒有 `fill` 不代表沒有背景，背景可能定義在子元素上。

---

### 每個節點需確認的屬性

#### `fill`（背景）

- 字串 `"#rrggbbaa"` → 實色（8 位含透明度）
- `{ type: "gradient" }` → 漸層
- `{ type: "image" }` → 圖片
- `[]` 或不存在 → 透明
- `{ enabled: false }` → 停用，視為透明

> ref 元件的 fill 可能定義在 component 層，不在 instance 的 descendants 裡。

#### `stroke`（線條）

- `thickness` 可以是數字（四邊）或 `{ top, right, bottom, left }`（單邊）
- `align`：`inside` / `center` / `outside`，影響實際佔用空間
- `fill`：線條顏色，可含透明度（8 位 hex 最後兩碼）
- `dashPattern`：虛線，例如 `[4, 2]`

#### `cornerRadius`（圓弧）

- 數字 → 四角統一
- `[topLeft, topRight, bottomRight, bottomLeft]` → 各角獨立
- 不存在 → 無圓角（0）

#### `opacity`（節點透明度）

- 作用在整個節點，包含 fill、stroke、子元件
- `fill` 有值但 `opacity: 0` → 整體仍透明
- 不存在 → 預設 1（完全不透明）

---

### 常見漏掉的情況

- 只看容器就停止，沒往下讀子元件的 `fill` / `stroke`
- `fill: { enabled: false }` 有值但停用，誤以為有背景
- `stroke.thickness: { bottom: 1 }` 只有底線，誤以為四邊都有
- `cornerRadius` 是數字以為四角一樣，沒注意到可能是陣列（各角獨立）
- `opacity` 沒讀，`fill` 有色但節點透明
