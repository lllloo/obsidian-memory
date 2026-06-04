---
title: Vue 的 JSDoc 型別註解
created: 2026-06-03
updated: 2026-06-04
tags:
  - vue
  - javascript
  - typescript
---

# Vue 的 JSDoc 型別註解

在 Vue 3 Composition API 中使用 JSDoc 為 `ref`、`computed`、`props`、`emit` 等加上型別註解，不需要寫 TypeScript 也能獲得完整的型別提示。

> 通用 JSDoc 語法請參閱 [JSDoc 型別註解](https://bugloop.com/notes/typescript/jsdoc)。

## ref

```ts
/** @type {import('vue').Ref<string>} */
const name = ref('')
```

物件型別：

```ts
/** @type {import('vue').Ref<{id: number, name: string}>} */
const user = ref({ id: 0, name: '' })
```

搭配型別斷言，常見於純 JS 專案中需要強制指定型別的情境：

```ts
/** @type any */
let x = ''
const y = ref(/** @type {string} */ x)
// y.value 型別會被推斷為 string
```

## reactive

```ts
/**
 * @type {import('vue').UnwrapNestedRefs<{count: number, items: string[]}>}
 */
const state = reactive({ count: 0, items: [] })
```

多數情況下 `reactive` 型別可由初始值自動推斷，需要 JSDoc 的場景通常是初始值無法精確表達型別時（如空陣列）。

## computed

```ts
/** @type {import('vue').ComputedRef<number>} */
const count = computed(() => 123)
```

物件型別：

```ts
/** @type {import('vue').ComputedRef<{id: number, name: string}>} */
const user = computed(() => ({ id: 1, name: 'Alice' }))
```

## defineProps

使用 `PropType` 標註複雜的 props 型別：

```ts
const props = defineProps({
  list: {
    /** @type {import('vue').PropType<{id: number, name: string}[]>} */
    type: Array,
    default: () => [],
  },
  status: {
    /** @type {import('vue').PropType<'active' | 'inactive'>} */
    type: String,
    default: 'active',
  },
})
```

## defineEmits

```ts
/** @type {(e: 'update', value: string) => void} */
const emit = defineEmits(['update'])
```

多個事件：

```ts
/**
 * @type {{
 *   (e: 'update', value: string): void
 *   (e: 'delete', id: number): void
 * }}
 */
const emit = defineEmits(['update', 'delete'])
```

## provide / inject

```ts
import { provide, inject } from 'vue'

/** @type {import('vue').InjectionKey<string>} */
const ThemeKey = Symbol('theme')

// 提供端
provide(ThemeKey, 'dark')

// 注入端
const theme = inject(ThemeKey)
// theme 型別為 string | undefined
```

## 參考資料

- [TypeScript with Composition API](https://vuejs.org/guide/typescript/composition-api.html)
- [TypeScript 官方 JSDoc 型別文件](https://www.typescriptlang.org/docs/handbook/jsdoc-supported-types.html)
