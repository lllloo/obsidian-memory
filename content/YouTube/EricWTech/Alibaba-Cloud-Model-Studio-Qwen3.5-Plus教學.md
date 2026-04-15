---
title: Alibaba Cloud Model Studio 完整教學：用 Qwen3.5 Plus 建立 AI Agent
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-10
source: https://www.youtube.com/watch?v=QmB2qxcQx88
---

## 什麼是 Alibaba Cloud Model Studio

介於純 API（無任何工具）與精美 demo（不能轉成產品）之間的平台。提供 Qwen3.5 Plus 模型存取，並整合可用的工作流：實驗 prompt、建立 Agent、連接工具、處理多模態輸入（文字、圖片、影片），然後透過 OpenAI 相容 API 直接投入生產。

免費額度：**1M tokens for Qwen3.5 Plus**（可用來真正測試完整功能）。

## 設定步驟

1. 前往 Model Studio，登入 Alibaba Cloud 帳號
2. 啟用服務（Activate，幾秒完成）
3. API Keys → Create API key → 複製保存
4. 設定環境變數：

```bash
export DASHSCOPE_API_KEY="your_api_key_here"
```

## API 呼叫（OpenAI 相容）

Qwen3.5 Plus API 與 OpenAI SDK 完全相容，只需更換三個設定：

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"  # 使用對應區域 endpoint
)

response = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你的問題"}]
)
print(response.choices[0].message.content)
```

## 多模態輸入（同一模型）

不需切換模型，Qwen3.5 Plus 原生支援文字 + 圖片：

```python
messages = [{
    "role": "user",
    "content": [
        {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}},
        {"type": "text", "text": "這張圖片裡有什麼？"}
    ]
}]
```

同一個 chat completions endpoint，只是 content 變成 list。可在單一請求中傳入多張圖片，或與長指令結合。

## Thinking Mode（推理模式）

Qwen3.5 Plus 預設開啟 thinking mode — 先生成推理過程再輸出最終答案：

```python
# 關閉 thinking mode（直接回答）
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[...],
    extra_body={"enable_thinking": False}
)
```

Streaming 時會先收到 reasoning content，再收到最終答案。使用者介面通常隱藏推理層，只顯示最終答案；debug 或研究工具可以顯示完整推理過程。

## 建立 Agent（對話迴圈）

Agent 本質：維護對話歷史 + 系統 prompt + 決定何時繼續處理：

```python
messages = [{"role": "system", "content": "你是一個有幫助的技術助理，清晰解釋概念。"}]

while True:
    user_input = input("User: ")
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=messages
    )
    
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    print(f"Assistant: {reply}")
```

**Qwen3.5 Plus 的 context window 高達 1M tokens**，不需要頻繁截斷對話歷史。

## Console 功能

- **Model Debugging**：調整 temperature、thinking budget，即時看輸出變化
- **System prompt**：原型設計完直接複製進 code，概念完全一致
- **多模態測試**：在同一介面混合測試文字 / 圖片 / 多輪對話，不需換模型

## 適用情境

- 已有 OpenAI SDK 基礎，遷移成本極低
- 需要長 context window 的應用（RAG、長文件分析）
- 多模態應用（文件截圖、視覺 QA）
- 需要推理可見性的研究或內部工具
