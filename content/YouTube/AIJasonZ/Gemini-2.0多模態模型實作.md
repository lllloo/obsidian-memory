---
title: Gemini 2.0 多模態模型實作
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-03-18
source: https://www.youtube.com/watch?v=HJa8G6e1oRw
---

## Gemini 2.0 的多模態能力

Gemini 2.0 experimental 是首個同時支援圖像理解與生成的多模態模型：
- 上傳圖片 + 文字指令 → 模型回傳修改後的圖片
- 可合成兩張圖片（服裝 + 模特兒）
- 連續生成多張圖片形成動畫 / GIF
- 成本比 GPT-4o 便宜約 96%

**使用注意：**對話越長，生成品質越低，建議在單一 session 中保持精簡的對話輪次。

## API 基礎使用（Python）

```python
import google.generativeai as genai

client = genai.GenerativeModel('gemini-2.0-flash-exp')

# 設定回應模態：同時包含 text 和 image
response = client.generate_content(
    contents=[{'role': 'user', 'parts': [{'text': 'Generate an image of a cat'}]}],
    generation_config={'response_modalities': ['TEXT', 'IMAGE']}
)

# 解析回應
for part in response.candidates[0].content.parts:
    if part.text:
        print(part.text)
    elif part.inline_data:
        with open('output.png', 'wb') as f:
            f.write(part.inline_data.data)
```

## 圖片輸入（本地檔案）

```python
import types

# 將上一張生成的圖片作為輸入
parts = [
    types.Part.from_bytes(data=open('generated_image.png', 'rb').read(), mime_type='image/png'),
    {'text': 'Change the hair color to red'}
]
```

## 圖片轉影片（Wan 2.1 via Replicate）

```python
import replicate

def generate_video(image_path: str, prompt: str) -> str:
    with open(image_path, 'rb') as f:
        output = replicate.run(
            'wan-ai/wan2.1-i2v-480p',
            input={'image': f, 'prompt': prompt}
        )
    # 儲存輸出影片
    video_path = 'output.mp4'
    with open(video_path, 'wb') as f:
        f.write(output.read())
    return video_path
```

## 完整應用：電商商品圖工作流

使用 Streamlit 快速建立 UI：

**流程：**
1. 使用者上傳商品照片
2. 透過 Chat 介面與 Gemini 2.0 對話，反覆調整 product shot（換背景、換模特兒膚色等）
3. 對滿意的圖片，切換到 Video Generation tab
4. 選取圖片 + 輸入動態描述，用 Wan 2.1 生成短影片

```bash
pip install google-generativeai replicate streamlit
streamlit run app.py
```

**架構：**
- `gemini_experimental.py`：Gemini 2.0 圖片生成函式
- `wan21.py`：Replicate 影片生成函式
- `utility.py`：儲存檔案、處理上傳圖片、去重等工具函式
- `app.py`：Streamlit 主程式（sidebar 上傳、Tab 1 聊天、Tab 2 影片）
