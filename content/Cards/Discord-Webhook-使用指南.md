---
title: Discord Webhook 使用指南
tags:
  - api
  - discord
  - workflow
created: 2026-04-07
updated: 2026-04-07
---

## 什麼是 Discord Webhook

Webhook 是一個 URL，讓外部服務可以直接傳送訊息到 Discord 頻道，不需要 Bot token，適合單向通知場景（CI/CD 通知、監控警報、表單通知等）。

## 建立 Webhook

1. 進入 Discord 頻道設定 → **整合** → **Webhook**
2. 點「建立 Webhook」，設定名稱與頭像
3. 複製 Webhook URL，格式為：
   ```
   https://discord.com/api/webhooks/{webhook.id}/{webhook.token}
   ```

## 發送訊息

### 最簡單：純文字

```bash
curl -X POST "{WEBHOOK_URL}"   -H "Content-Type: application/json"   -d '{"content": "Hello from webhook!"}'
```

### 使用 Embed（卡片樣式）

```bash
curl -X POST "{WEBHOOK_URL}"   -H "Content-Type: application/json"   -d '{
    "embeds": [{
      "title": "部署通知",
      "description": "production 部署成功",
      "color": 5763719,
      "fields": [
        {"name": "Branch", "value": "main", "inline": true},
        {"name": "版本", "value": "v1.2.3", "inline": true}
      ],
      "timestamp": "2026-04-07T00:00:00.000Z"
    }]
  }'
```

### 用 Python 發送

```python
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN"

payload = {
    "content": "這是一則通知",
    "username": "My Bot",          # 覆寫顯示名稱（可選）
    "avatar_url": "https://..."    # 覆寫頭像（可選）
}

response = requests.post(WEBHOOK_URL, json=payload)
print(response.status_code)  # 204 = 成功
```

### 用 Node.js 發送

```javascript
const webhookUrl = 'https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN';

await fetch(webhookUrl, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    content: '這是一則通知',
    embeds: [{
      title: '標題',
      description: '內文',
      color: 0x57F287  // 綠色
    }]
  })
});
```

## Embed color 常用色碼

| 顏色 | Hex | 十進位 |
|------|-----|--------|
| 綠（成功） | #57F287 | 5763719 |
| 紅（失敗） | #ED4245 | 15548997 |
| 黃（警告） | #FEE75C | 16705372 |
| 藍（資訊） | #5865F2 | 5793266 |

## 限制

- 每個 Webhook 每秒最多 **5 則**訊息（rate limit）
-  最長 **2000** 字元
- 每個請求最多 **10 個** embeds
- Webhook URL 是機密，不要公開（任何人都能用它發訊息）

## 常見應用場景

- GitHub Actions 部署完成通知
- 伺服器監控警報（Uptime Kuma、Grafana）
- 表單填寫通知
- 爬蟲任務完成回報