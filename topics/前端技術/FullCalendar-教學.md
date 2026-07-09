---
title: FullCalendar 教學
created: 2026-06-03
updated: 2026-06-22
tags:
  - library
  - javascript
  - vue
  - frontend
---

# FullCalendar 教學

FullCalendar 是功能完整的 JavaScript 日曆元件，用於顯示行事曆、活動排程，支援月/週/日視圖與拖曳互動，並提供 Vue 3 整合套件。

## Vue 版本安裝與使用

### 安裝

```bash
npm install --save \
  @fullcalendar/core \
  @fullcalendar/vue3
```

### 基本範例

```vue
<template>
  <FullCalendar :options="calendarOptions" />
</template>

<script setup>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import zhTWLocale from '@fullcalendar/core/locales/zh-tw'

const calendarOptions = {
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  locale: zhTWLocale,
}
</script>
```

## 常用設定

功能由 plugins 決定（要哪個視圖／互動就引哪個 plugin），其餘多為開關與回呼。完整選項查官方文件，這裡只列日常最常動的：

```javascript
const calendarOptions = {
  // 功能插件：dayGrid=月視圖、timeGrid=週/日視圖、interaction=點擊/拖曳
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],

  initialView: 'dayGridMonth', // 也可 'timeGridWeek' / 'timeGridDay'
  locale: zhTWLocale,

  editable: false,    // 允許拖曳調整事件（需 interactionPlugin）
  selectable: false,  // 允許框選日期區間（需 interactionPlugin）
  dayMaxEvents: true, // 月視圖事件過多時自動摺疊成「更多」

  events: [{ title: '會議', start: '2023-01-02' }],

  eventClick: (info) => console.log('事件被點擊:', info.event),
  dateClick: (info) => console.log('日期被點擊:', info.dateStr),
  datesSet: ({ start, end }) => console.log('日期範圍變更:', start, end),
}
```

> 其他細項（`slotLabelContent` 時間軸刻度、`dayMaxEventRows`／`eventMaxStack` 堆疊上限、`longPressDelay` 觸控長按、`dayHeaderFormat` 表頭格式…）較少動，需要時查官方文件即可。

## 自訂事件內容

用具名插槽 `eventContent` 覆寫事件的渲染：

```vue
<template>
  <FullCalendar :options="calendarOptions">
    <template v-slot:eventContent="arg">
      <b>{{ arg.event.title }}</b>
    </template>
  </FullCalendar>
</template>
```

## 取得實例與操作 API

透過 `ref` 拿到元件，再用 `getApi()` 取得日曆實例呼叫 `next()`、`gotoDate()` 等方法：

```vue
<template>
  <FullCalendar ref="fullCalendar" :options="calendarOptions" />
  <button @click="goNext">下一個</button>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const fullCalendar = ref(null)

function goNext() {
  fullCalendar.value.getApi().next()
}

onMounted(() => {
  fullCalendar.value.getApi() // 掛載後即可操作，如 .gotoDate(...)
})
</script>
```

> **⚠️ `getApi()` 的呼叫時機**
>
> `getApi()` 只能在元件掛載後（`onMounted` 或使用者事件觸發的方法內）呼叫。在 `<script setup>` 頂層同步執行時 `fullCalendar.value` 仍為 `null`，會拋 `Cannot read properties of null`。

## 參考資料

- [FullCalendar 官方文件](https://fullcalendar.io/docs)
- [Vue 3 版本官方教學](https://fullcalendar.io/docs/vue)
