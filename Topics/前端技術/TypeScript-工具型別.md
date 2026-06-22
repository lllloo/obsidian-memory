---
title: TypeScript 工具型別 Utility Types
created: 2026-06-03
updated: 2026-06-22
tags:
  - typescript
---

# TypeScript 工具型別 Utility Types

TypeScript 工具型別（Utility Types）是官方預設的一組泛型型別，能協助你靈活操作、轉換現有型別，減少重複程式碼並提升維護性。本文整理常用 Utility Types 說明與範例，適合 TypeScript 開發者參考。

## Partial 可選

將型別 T 的所有屬性變為可選 (optional)。

```ts
type Person = { name: string; age: number; gender: string }
type PartialPerson = Partial<Person> // { name?: string; age?: number; gender?: string }
```

## Required 必填

將型別 T 的所有屬性變為必填 (required)。

```ts
type Person = { name?: string; age?: number; gender?: string }
type RequiredPerson = Required<Person> // { name: string; age: number; gender: string }
```

## Readonly 唯讀

將型別 T 的所有屬性設為唯讀 (readonly)。

```ts
type Person = { name: string; age: number }
const p: Readonly<Person> = { name: 'Alice', age: 20 }
// p.age = 30 // 編譯錯誤，屬性不可修改
```

## Record 記錄<K, T>

建立一個以 K 為鍵、T 為值的物件型別。

```ts
type Score = Record<string, number>
// { [key: string]: number }
```

## Pick 挑選

從型別 T 中挑選指定屬性 K，組成新型別。

```ts
type Person = { name: string; age: number; gender: string }
type PersonName = Pick<Person, 'name'> // { name: string }
```

## Omit 忽略

從型別 T 中移除指定屬性 K，組成新型別。

```ts
type Person = { name: string; age: number; gender: string }
type PersonWithoutAge = Omit<Person, 'age'> // { name: string; gender: string }
```

## Exclude 排除

從聯集型別 T 中排除 U 型別。

```ts
type T = 'a' | 'b' | 'c'
type Excluded = Exclude<T, 'a'> // 'b' | 'c'
```

## Extract 提取

從聯集型別 T 中提取 U 型別。

```ts
type T = 'a' | 'b' | 'c'
type Extracted = Extract<T, 'a' | 'b'> // 'a' | 'b'
```

## NonNullable 移除(null 與 undefined)

移除型別中的 null 與 undefined。

```ts
type T = string | null | undefined
type NonNull = NonNullable<T> // string
```

## 常見場景選型

挑工具型別前先分清楚：要操作的是「物件的屬性」還是「聯集的成員」——兩類名字相似但作用層次不同。

- **改屬性可選性**：表單／PATCH 更新型別用 `Partial<T>`（欄位都可選傳）；反向把可選補成必填用 `Required<T>`。
- **取屬性子集**：要「只留某幾個」用 `Pick<T, K>`；要「去掉某幾個」用 `Omit<T, K>`。欄位多、只排除少數時 `Omit` 較省；只需少數欄位時 `Pick` 較清楚。
- **建字典／對照表**：`Record<K, V>` 取代手寫 index signature，`K` 用聯集字串可限定鍵範圍。
- **操作聯集成員**：從聯集「拿掉」某些成員用 `Exclude<U, M>`、「只留」某些用 `Extract<U, M>`。
- **收斂 null/undefined**：`NonNullable<T>`，常接在 API 回傳或可選鏈型別後。

> **關鍵分辨**：`Pick`／`Omit` 作用於「物件的鍵」，`Exclude`／`Extract` 作用於「聯集的成員」，別互相套用。

## 參考資料

- [TypeScript 官方文件：Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)
