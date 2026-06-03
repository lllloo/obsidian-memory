---
title: FullCalendar 教學
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/notes/library/fullcalendar
tags:
  - library
  - javascript
  - vue
  - frontend
---

# FullCalendar 教學

FullCalendar 是一個強大的 JavaScript 日曆元件，常用於網頁上顯示行事曆、活動排程等。支援多種視圖、互動功能，並可與 Vue 等前端框架整合。

---

## Vue 版本安裝與使用

### 安裝方式

請先執行下列指令安裝相關套件：

```bash
npm install --save \
  @fullcalendar/core \
  @fullcalendar/vue3
```

### 基本範例

以下為 Vue 3 組件整合範例：

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

```javascript
const calendarOptions = {
  // plugins：啟用功能插件，決定日曆支援哪些視圖與互動
  //   - dayGridPlugin：月視圖（格狀）
  //   - timeGridPlugin：週/日視圖（時間軸）
  //   - interactionPlugin：支援點擊、拖曳等互動
  //   可依需求增減，例如只要月視圖可只留 dayGridPlugin
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],

  // initialView：預設載入時的日曆視圖
  //   - 'dayGridMonth'：月視圖
  //   - 'timeGridWeek'：週視圖
  //   - 'timeGridDay'：日視圖
  //   也可用 'listWeek'、'listDay'（需額外插件）
  initialView: 'dayGridMonth',

  // initialDate：預設顯示的日期（字串格式 'YYYY-MM-DD'）
  //   此值可為任何能被 Date 解析的格式，例如 ISO8601 字串 '2014-02-01'
  initialDate: '2023-01-01',

  // allDayContent：自訂「全天」欄位顯示文字（僅 timeGridPlugin 有效）
  //   預設為 'All-day'，可改成任何字串
  allDayContent: '全天',

  slotLabelContent: (date) => {
    return date.toLocaleDateString('zh-TW', { weekday: 'long' })
  },

  // editable：是否允許拖曳、編輯事件（需 interactionPlugin）
  //   true 可拖曳、調整事件時間；
  //   false 禁止編輯
  editable: false,

  // selectable：是否允許使用者框選日期區間（需 interactionPlugin）
  //   true 可用滑鼠或觸控選取多天，false 禁止選取
  selectable: false,

  // longPressDelay：長按觸發拖曳或選取的延遲毫秒數（需 interactionPlugin）
  //   僅在觸控螢幕裝置上使用行事曆時適用，否則沒有延遲
  //   預設 1000，設 0 代表點擊立即觸發拖曳/選取
  longPressDelay: 0,

  // dayMaxEventRows：每一天最多顯示幾行事件（超過會摺疊成「更多」）
  //   預設 false（不限制），可設數字如 6
  dayMaxEventRows: 6,

  // eventMaxStack：每一天最多堆疊幾個事件（僅 dayGridMonth 有效）
  //   超過會顯示「更多」連結
  eventMaxStack: 6,

  // dayMaxEvents：是否啟用「更多」事件顯示（true 則超過自動摺疊）
  //   若設為 true，事件數量會根據日單元格高度自動限制，超過則顯示「更多」
  dayMaxEvents: true,

  // events：事件資料來源
  //   格式如 [{ title: '會議', start: '2023-01-02' }]
  events: [],

  // eventClick：事件被點擊時的回呼
  //   參數 eventInfo，內含事件資料
  eventClick: (eventInfo) => {
    console.log('事件被點擊:', eventInfo)
  },

  // dateClick：日期被點擊時的回呼
  //   參數 dateInfo，內含日期資訊
  dateClick: (dateInfo) => {
    console.log('日期被點擊:', dateInfo)
  },

  // 日期範圍變更時的回呼
  datesSet: (dateInfo) => {
    const { start, end } = dateInfo
    console.log('日期範圍變更:', start, end)
  },
}
```

## 自訂事件內容

```vue
<template>
  <FullCalendar>
    <template v-slot:eventContent="arg">
      <b>{{ arg.event.title }}</b>
    </template>
  </FullCalendar>
</template>
```

## 取得 FullCalendar 實例與操作 API

```vue
<template>
  <FullCalendar ref="fullCalendar" />
</template>

<script setup>
const fullCalendar = ref(null)
let calendarApi = fullCalendar.value.getApi()
calendarApi.next()
</script>
```

---

## 參考資料

- [FullCalendar 官方文件](https://fullcalendar.io/docs)
- [Vue 3 版本官方教學](https://fullcalendar.io/docs/vue)
