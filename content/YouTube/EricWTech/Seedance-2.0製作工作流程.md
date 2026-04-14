---
title: Seedance 2.0 製作工作流程：前期到成品
tags:
  - youtube
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-13
source: https://www.youtube.com/watch?v=GE9cT81SbfY
---

## 工具組合

四步驟工作流程：
1. **Higgsfield Soul Cinema** — 生成關鍵影格（keyframe）
2. **NanoBanana Pro** — 精修角色/場景圖像，維持視覺一致性
3. **Claude** — 根據關鍵影格生成 Seedance 2.0 prompt
4. **Higgsfield Seedance 2.0** — 輸出最終影片片段

平台：[Hexn.ai](https://higgsfield.ai)（Higgsfield 旗下平台）

## 前製（Pre-Production）

### 角色一致性設定

1. 用 Soul Cinema 生成角色設計圖（character sheet）：批次生成 4 張，選出喜歡的下載
2. 上傳至 NanoBanana Pro，加上 prompt，生成「專業角色參考表」（含多角度視圖）
3. 道具（如口琴）：同樣用角色 keyframe 做參考，在 Soul Cinema 生成道具參考圖，保持風格一致

### 場景一致性設定

- Soul Cinema 不接受參考圖 → 用 Soul Cinema 生成「風格錨定圖」（style anchor），決定整體視覺風格
- 再用 NanoBanana Pro + style anchor 圖，對所有場景（最多 5 個）批次生成位置參考圖（保持一致風格）
- 每個場景額外生成「位置參考表」（含左視/右視/前視等多角度），供後續 Seedance 使用

## 正式製作（Scene-by-Scene Production）

### 場景生成流程

1. **合成場景 keyframe**：NanoBanana Pro 同時上傳角色圖 + 場景圖，生成「角色在場景中」的組合圖
2. **生成 Seedance prompt**：Claude 輸入提示格式如下：
   - 上傳：場景 keyframe、角色參考表、道具表、位置參考表
   - Claude 輸出精細化的 Seedance 2.0 prompt
3. **上傳至 Seedance 2.0（Hexn）**：
   - 貼上 Claude 生成的 prompt
   - 按順序上傳圖片：場景 keyframe → 角色參考 → 道具表 → 場景位置參考表
   - 設定：15 秒片長、選擇長寬比、最高 720p
   - 點 Generate

### 注意事項

- Soul Cinema 不支援參考圖輸入（限制），需先用 Soul Cinema 定風格，再交給 NanoBanana Pro 精修
- 每個場景各生成 4 張備選圖，選一張作為最終 keyframe
- 提示詞（prompt）預計放在影片說明欄 + 社群（School）下載

## 成果特點

- 跨場景角色、道具、場景風格高度一致
- 不需要動態背景或動態設計，純靠 AI 流程產出動畫短片
- 整套工作流程文件（空白模板）可在 EricWTech 的 School 社群下載
