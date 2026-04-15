---
title: Sora 2 API 使用指南
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-10-07
source: https://www.youtube.com/watch?v=YWvN7EvVQQU
---

## 基本影片生成

```python
from openai import OpenAI
client = OpenAI()

# 建立影片生成任務
job = client.videos.create(
    model="sora-2",
    prompt="your prompt here",
    size="720x1280",   # 縱向；橫向用 1280x720
    seconds=4          # 可選 4、8、12 秒
)
```

### 查詢狀態與下載

```python
import time

# 列出所有影片，取最新一筆
video_list = client.videos.list()
latest = video_list.data[0]

# 輪詢直到完成
while True:
    status = client.videos.retrieve(latest.id)
    print(f"Progress: {status.progress}%")
    if status.status == "completed":
        break
    time.sleep(2)

# 下載
with open("output/video.mp4", "wb") as f:
    f.write(status.content)
```

## Image-to-Video（參考圖片動畫化）

- 參考圖片尺寸必須與影片尺寸完全一致，否則報錯
- 可用 GPT-5 生成圖片，再用 Pillow resize 至正確尺寸
- 傳入 `input_reference` 參數指定圖片路徑

## Pro 模型

- 模型名稱改為 `sora-2-pro`，其他參數相同
- 畫質更高、生成更慢、費用更高
- 錄影當下（2025/10）Pro 模型有卡在 pending 的 bug

## 進階 Prompting

- OpenAI 提供完整 Sora prompting guide，可指定相機型號、鏡頭、打光、角色細節
- 建立 `SoraDirector` 類別：將模糊的主題描述自動轉成詳細 Sora prompt

```python
# 範例：Pixar 風格 director
class SoraDirector:
    def generate_sora_prompt(self, user_idea: str) -> str:
        # 用 GPT 將 user_idea 轉成帶有特定視覺風格的詳細 prompt
        ...
```

## Remix（影片再編輯）

```python
remixed = client.videos.remix(
    video_id=original_video_id,
    prompt="change the monster color to orange"
)
```

- 只能 remix 用 Sora 生成的影片，無法上傳外部影片
- 適合微調場景、顏色、動作

## 多鏡頭序列生成

1. 生成 shot 1（原始影片）
2. 用 remix 生成 shot 2，以 shot 1 為基礎並給新場景 prompt
3. 重複至所有鏡頭完成
4. 用 FFmpeg 拼接：

```python
import subprocess
# FFmpeg 合併多個 mp4 檔案
subprocess.run(["ffmpeg", "-f", "concat", "-i", "list.txt", "-c", "copy", "output.mp4"])
```

## 注意事項

- 內容審查較嚴，涉及真人臉部的 reference 圖片常被拒絕
- 多鏡頭角色一致性目前尚未完善，屬提示詞技巧問題
- 生成時間依長度與模型不同，通常 1-3 分鐘
