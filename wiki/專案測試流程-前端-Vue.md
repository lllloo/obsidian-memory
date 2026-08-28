---
title: 專案測試流程 前端 Vue
description: Vue 端測試落地：判斷從 script setup 抽到 utils 與 composable、需不需掛載的分界、元件測試該測互動而非樣板
created: 2026-08-08
updated: 2026-08-28
parent: "[[wiki/01.index]]"
tags:
  - testing
  - vue
  - coding-agent
---

> [[專案測試流程|總覽]] ｜ **前端 Vue** ｜ [[專案測試流程-後端-Laravel|後端 Laravel]]

本頁是 [[專案測試流程]] 在 Vue 端的落地。分層原則、斷言紀律、覆蓋率的停止條件都在總頁，這裡只講**Vue 專屬的做法與坑**。後端對應的一頁是 [[專案測試流程-後端-Laravel]]。

## 第一層：單元測試

### 判斷長在元件裡，就沒有單元可以測

```vue
<!-- ❌ 折扣計算埋在 script setup 裡 -->
<script setup>
const total = computed(() => {
  let sum = items.value.reduce((a, i) => a + i.price * i.qty, 0)
  if (sum >= 1000) sum = sum * 0.9
  return Math.round(sum)
})
</script>
```

要驗證那條「滿 1000 打九折」，得先 `mount()` 整個元件、準備 props、可能還要 stub 掉子元件。慢、脆，而且失敗時不會告訴你是哪一段錯了。

抽出來，讓它脫離 Vue：

```js
// ✅ src/utils/pricing.js — 純函式，不 import 任何 Vue 的東西
export function calcTotal(items) {
  const sum = items.reduce((a, i) => a + i.price * i.qty, 0)
  return Math.round(sum >= 1000 ? sum * 0.9 : sum)
}
```

```vue
<script setup>
import { calcTotal } from '@/utils/pricing'
// 元件這側只剩「把資料交出去、把結果拿回來」
const total = computed(() => calcTotal(items.value))
</script>
```

測試變成幾行、毫秒級，不需要 Vue、不需要 DOM：

```js
// src/utils/__tests__/pricing.spec.js
import { describe, it, expect } from 'vitest'
import { calcTotal } from '../pricing'

describe('calcTotal', () => {
  it('未滿門檻不打折', () => {
    expect(calcTotal([{ price: 100, qty: 2 }])).toBe(200)
  })
  it('剛好滿 1000 就打折', () => {
    expect(calcTotal([{ price: 500, qty: 2 }])).toBe(900)
  })
  it('空清單為 0', () => {
    expect(calcTotal([])).toBe(0)
  })
})
```

**`import { ref } from 'vue'` 出現在測試檔裡不是問題，`mount()` 出現才是。** 前者只是用了響應式基本型，後者代表你需要整個元件實例——那是第二層。

### composable 分兩種，只有一種屬於第一層

這是 Vue 端最容易搞混的地方。同樣叫 composable，可測性差很多：

| 類型 | 特徵 | 屬於 |
|---|---|---|
| **純計算型** | 只用 `ref`／`computed` 做資料轉換，不碰生命週期、不發請求 | **第 1 層**，直接呼叫就能測 |
| **有生命週期／副作用型** | 用了 `onMounted`、`watch` 副作用、`fetch`、路由、`provide/inject` | 第 2 層，需要掛載環境 |

純計算型直接當函式呼叫即可，不必掛載任何東西：

```js
// src/composables/useCart.js
export function useCart(items) {
  const total = computed(() => calcTotal(items.value))
  const isEmpty = computed(() => items.value.length === 0)
  return { total, isEmpty }
}
```

```js
// 測試：直接呼叫，不需要元件
import { ref } from 'vue'
import { useCart } from '../useCart'

it('購物車為空時 isEmpty 為 true', () => {
  const { isEmpty } = useCart(ref([]))
  expect(isEmpty.value).toBe(true)
})

it('items 變動時 total 跟著重算', () => {
  const items = ref([{ price: 100, qty: 1 }])
  const { total } = useCart(items)
  expect(total.value).toBe(100)
  items.value = [{ price: 100, qty: 3 }]   // 響應式在此可直接驗
  expect(total.value).toBe(300)
})
```

若一個 composable 因為用了 `onMounted` 而測不動，那是設計訊號而非測試問題：**把裡面的判斷再抽一層成純函式**，剩下的生命週期外殼留給第二層。

### 該測什麼、不該測什麼

第一層的射程：

- `utils/` 的格式化、計算、驗證函式——金額、日期、字串處理
- 純計算型 composable
- 表單驗證規則
- Pinia store 裡的 getter 與純粹的 action（不發請求那些）

不測的：

- **框架本身的行為**——`computed` 會不會重算、`ref` 的響應式是否運作，那是 Vue 的測試不是你的
- **元件的渲染結果**——需要 `mount()`，屬第二層
- **`axios` 能不能發請求**——那是套件的責任；你該測的是「回來的資料怎麼轉換」，而那應該已經被你抽成純函式了

### 怎麼跑

```bash
npm run test:unit
```

用 Vitest（Vue 官方測試指南推薦的 runner，與 Vite 共用同一份設定，不必再維護第二套 transform 設定）。專案若用 `create-vue` 建立並勾選單元測試，這個指令與設定檔已經備妥。

檔案落點把第一層與第二層的分界畫出來，值得刻意維持：

```
src/
  utils/
    pricing.js
    __tests__/
      pricing.spec.js          ◀ 第 1 層：純函式，不 import vue 的元件 API
  composables/
    useCart.js
    __tests__/
      useCart.spec.js          ◀ 第 1 層：純計算型，直接呼叫
  components/
    CartSummary.vue
    __tests__/
      CartSummary.spec.js      ◀ 第 2 層：需要 mount()
```

**訊號**：測試檔裡出現 `mount()` 或 `shallowMount()`，它就不屬於第一層。這是個好用的 grep 判準——`grep -rli "mount(" src/utils src/composables` 應該永遠是空的。`-i` 不可省，否則 `shallowMount(` 這一半漏掉；加了也不會誤傷 `onMounted(`（它後面接的是 `ed(` 而非 `(`）。

### 這一層完成的樣子

1. 業務規則已從 `script setup` 抽成不 import Vue 元件 API 的函式
2. 每個純計算型 composable 至少有一條測試，且沒有用到 `mount()`
3. `npm run test:unit` 一個指令跑完、全綠，並寫進 `README.md`
4. `src/utils` 與 `src/composables` 底下的測試以 `grep -i` 找不到 `mount(`

### 什麼時候該停

停止條件見 [[專案測試流程]] 的「不追覆蓋率數字」。Vue 端有一個特有的過度工程紅線：**不要為了提高覆蓋率而去測元件的樣板輸出**（斷言某個 `div` 的 class、某段文字有沒有出現）。那類測試在改版面時會整批壞掉，但它們壞掉不代表功能壞了——這是最典型的「測試變成阻力」。

## 第二層：元件測試

**尚未實作，以下為做法設計**（2026-08-28 談定，未在本專案驗證）。

對外叫 **component test**。第二層絕大多數是元件測試，但不全是——Pinia store 的 action 串接、用了 `onMounted`／`watch` 的 composable 也在這層，它們說 integration test 更精確。判準始終是**「啟動框架、但沒跨 HTTP」**，不是「有沒有元件」。

### 射程：互動與狀態流轉

```js
it('點擊送出會 emit 訂單內容', async () => {
  const wrapper = mount(OrderForm, { props: { items } })
  await wrapper.get('[data-testid="submit"]').trigger('click')
  expect(wrapper.emitted('submit')[0][0]).toEqual({ items, total: 900 })
})
```

測的是：點擊 → emit 什麼、props 變了 → 渲染哪個分支、表單填錯 → 出現哪個錯誤狀態、載入中 → 顯示什麼。

**選元素用 `data-testid` 或 role，不要用 CSS class**——class 是樣式的東西，拿它當測試的抓手，改樣式就會弄壞測試。

### API 一律 mock，這是定義不是偷懶

```js
// 做法 A：mock 掉 API 模組
vi.mock('@/api/order', () => ({
  fetchOrder: () => Promise.resolve({ total: 900 })   // ← 形狀是自己手寫的
}))

// 做法 B：攔截網路層（MSW）
http.get('/api/orders/1', () => HttpResponse.json({ total: 900 }))
```

一旦真的打後端，就要後端服務跑著、資料庫備好資料、每次跑測試都等網路來回，而且後端壞了前端測試會跟著紅——那已經是 E2E，不是元件測試。第二層的判準本來就是「不跨 HTTP」。

**代價要知道**：那份 mock 的形狀是手寫的，與後端無關。所以這層測得到「拿到這樣的資料，元件行為對不對」，測不到「後端實際回不回這個形狀」。這條縫的處置見 [[專案測試流程]] 的契約測試一節。

實務建議：**把手寫的 mock 形狀集中放**（例如 `src/test/fixtures/`），不要散在各測試檔裡。它們是你對後端的隱含契約，集中之後才有可能跟後端實際回應對照，日後要接型別產生也是現成的起點。

### 紅線：不要斷言樣板細節

某個 `div` 的 class、某段文字出現在第幾個位置——改版面就整批紅，但功能沒壞。這是第一層那條紅線在第二層的延續，機制說明見 [[用測試約束-AI-產碼]] 第一節。

### 這一層完成的樣子

1. **每個有互動的元件至少兩條**：主要互動 + 一個錯誤狀態
2. 選元素不依賴 CSS class
3. `npm run test` 一個指令跑完、全綠（含元件測試）
4. mock 的回應形狀集中在一處，不散落

執行時間從第一層的毫秒級掉到分鐘級是正常的。

### 這一層是前端的價值重心

後端的 bug 多在判斷邏輯裡（第一層射得到），**前端的 bug 多在互動與狀態流轉裡，只有這層射得到**。所以前端第一層做完就該往這裡走，不要在第一層加深度（例如急著上 mutation）——理由見 [[測試手段的優先序與成本]]。

## 關聯

- [[專案測試流程]] — 總頁：三層射程（2026-08-28 由四層改制，契約層不採）、一個測試該歸哪一層的判準，以及兩端共通的斷言紀律與停止條件。本頁只補 Vue 專屬的部分。
- [[專案測試流程-後端-Laravel]] — 對照組。兩端卡的是同一個坑（判斷長在框架內部），但訊號不同：這裡是測試檔出現 `mount()`，那邊是 `--testsuite=Unit` 跑起來很慢。
- [[測試手段的優先序與成本]] — 本頁「第二層是前端價值重心」的完整理由在該頁：Stryker 不支援 Vitest browser mode，加上前端可掃的純函式面積本來就小，所以前端第一層做完該往廣度走而非深度。
- [[用測試約束-AI-產碼]] — 上面「不該測什麼」那節要避開的東西，在該頁第一節有機制說明：AI 產測試最常見的失效正是過度 mock 與斷言樣板細節，兩者都讓測試變成實作的鏡子。
