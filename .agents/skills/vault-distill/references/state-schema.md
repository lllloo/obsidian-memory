# Distill 狀態檔 Schema

跨 session 保存每個 MOC 的整合進度。檔案路徑：`.vault-distill/state.json`（gitignored）。

## 讀寫規則

- **狀態偵測時**：先嘗試讀取 `.vault-distill/state.json`，取出 `mocs` 清單補充 moc tag 掃描結果（解決 Topics/ 掃描漏洞之外，也補充跨 session 的輪數資訊）
- **每個步驟完成後**：更新對應 MOC 的 state 欄位
- **不存在時**：靜默建立（`{}` 空物件）；不阻斷流程

## Schema

```json
{
  "mocs": {
    "<Cards/主題.md 或 Topics/.../主題.md 的相對路徑>": {
      "last_step": "A|B|C|D|E",
      "round": 1,
      "candidates": [
        "content/Cards/原筆記-1.md",
        "content/Inbox/YouTube/頻道/影片.md"
      ],
      "last_review": "第 1 輪：5 項（必改 2 / 應改 2 / 可選 1）",
      "fact_check_urls": [
        "https://docs.example.com/...",
        "https://github.com/..."
      ],
      "updated_at": "2026-05-10"
    }
  }
}
```

## 欄位說明

| 欄位 | 用途 |
|------|------|
| `last_step` | 最後完成的步驟，供狀態偵測判斷「進行中」 |
| `round` | 累計 review 輪數（傳給 reviewer prompt 的 `<第 N 輪>`） |
| `candidates` | Step A 的原筆記候選清單（Step E 優先從這裡取，不重跑 A1） |
| `last_review` | 最後一輪 reviewer 回報摘要（傳給 reviewer 的 `<前幾輪摘要>`） |
| `fact_check_urls` | Step D 事實校正取得的官方 URL（傳給 reviewer 的 docs 欄位） |
| `updated_at` | 最後更新日期 |

## 讀寫流程

### 讀取（狀態偵測）

```bash
# 狀態偵測時附加讀取
[ -f ".vault-distill/state.json" ] && cat .vault-distill/state.json
```

取出 `mocs` 鍵清單，補充 moc tag 掃描結果（去重）。`round` 欄位直接傳給 reviewer prompt，不再靠對話上下文推算。

### 寫入（步驟完成後）

每個步驟完成後，主 agent 更新對應欄位：

- Step A 完成 → 寫 `last_step: "A"` + `candidates`
- Step B 完成 → 寫 `last_step: "B"` + `round +1` + `last_review`
- Step C 完成 → 寫 `last_step: "C"` + `last_review`（round 不遞增，C 是 fix 不是新 review）
- Step D 完成 → 寫 `last_step: "D"` + `fact_check_urls`
- Step E 完成 → 刪除對應 MOC 鍵（原筆記已處置，整合完成）

## 舊狀態清理

執行 F 推薦模式時，順帶清除 `.vault-distill/state.json` 中指向已不存在檔案的 MOC 鍵。
