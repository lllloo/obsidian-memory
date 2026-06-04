---
title: TypeScript 工具型別 Utility Types
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/notes/typescript/utility-types
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

## 參考資料

- [TypeScript 官方文件：Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)
