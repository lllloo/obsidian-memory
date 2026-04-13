---
title: Pydantic 完整入門課程
tags:
  - youtube
  - python
  - pydantic
  - ai-agent
created: 2026-04-13
updated: 2026-04-13
published: 2026-01-28
source: https://www.youtube.com/watch?v=PkQIREapb9o
---

## 為什麼需要 Pydantic

Python 是動態型別語言，變數可以在任何時候被設為任何型別，Python 不會報錯。這在快速實驗時很方便，但在生產系統中是噩夢：

- API 收到 `age = "unknown"` → 不會立刻報錯 → 等到計算年齡時才爆炸
- LLM 輸出的結構可能和預期不符 → 程式不報錯 → 資料庫存入垃圾資料

**Pydantic 的核心價值**：在資料進入系統的那一刻進行驗證，而不是等到使用時才出錯。

```
沒有 Pydantic：錯誤在生產環境深處才爆發
有 Pydantic：錯誤在進入點立刻被攔截
```

## 環境設定

```bash
uv sync           # 已包含 pydantic 在 pyproject.toml
# 或
pip install pydantic
pip install pydantic-settings  # 另外安裝
```

## 第一章：Python 型別提示（Type Hints）

型別提示是 Pydantic 的基礎，但本身**不強制執行**：

```python
name: str = "Dave"      # 只是文件，Python 不強制
age: int = "twenty"     # 不會報錯

# 函式型別提示
def create_user(name: str, email: str, age: int) -> dict:
    return {"name": name, "email": email, "age": age}
```

常用型別：
```python
# 基本型別
str, int, float, bool

# 容器型別
tags: list[str] = ["a", "b"]
scores: dict[str, int] = {"errors": 12}
status: tuple[str, int]

# Optional（兩種寫法等價）
from typing import Optional
middle_name: Optional[str] = None
middle_name: str | None = None

# Literal（限定可選值）
from typing import Literal
status: Literal["draft", "published", "archived"] = "draft"
```

## 第二章：建立第一個模型

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

# 建立實例（有驗證）
user = User(name="Dave", age=31, email="dave@example.com")
user.name   # "Dave"
user.age    # 31

# 錯誤會立刻拋出
user = User(name="Dave", age="invalid", email="dave@example.com")
# ValidationError: age - Input should be a valid integer
```

型別強制轉換（預設寬鬆模式）：
```python
User(name="Dave", age="25", email="...")  # "25" 自動轉為整數 25，不報錯
```

嚴格模式：
```python
from pydantic import ConfigDict

class StrictUser(BaseModel):
    model_config = ConfigDict(strict=True)
    name: str
    age: int
# 此時 age="25" 會報錯，必須傳入整數
```

## 第三章：驗證與 Field

### 基本欄位約束

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(gt=0, le=150)  # gt=大於, ge=大於等於, lt=小於, le=小於等於
    email: str = Field(default="none@example.com")  # 預設值
    bio: str = Field(description="用戶簡介，也會出現在 JSON schema 和 LLM prompt 中")
```

### 字串模式驗證（正規表達式）

```python
username: str = Field(pattern=r"^[a-zA-Z0-9_]+$")
```

### 自訂驗證器

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if " " in value:
            raise ValueError("username 不能包含空格")
        return value.lower()
```

### 內建特殊型別

```python
from pydantic import EmailStr, HttpUrl

class Contact(BaseModel):
    email: EmailStr   # 自動驗證 email 格式
    website: HttpUrl  # 自動驗證 URL 格式
```

### 清單約束

```python
items: list[str] = Field(min_length=1)  # 清單至少要有一個元素
```

## 第四章：資料轉換

```python
# Pydantic 模型 → 字典
user_dict = user.model_dump()          # Python dict
user_json = user.model_dump_json()     # JSON 字串

# 字典 → Pydantic 模型（兩種方式）
user = User(**data_dict)              # Python 解包
user = User.model_validate(data_dict) # 更多選項（strict, extra values 等）

# 取得 JSON Schema（API 文件用）
User.model_json_schema()
```

## 第五章：巢狀模型（Nested Models）

```python
class OrderItem(BaseModel):
    product_id: str
    name: str
    quantity: int
    price: float

class Order(BaseModel):
    order_id: str
    customer_email: str
    item: OrderItem         # 單個巢狀模型
    items: list[OrderItem]  # 多個巢狀模型
    discount: Discount | None = None  # 可選的巢狀模型

# 使用
order = Order(
    order_id="001",
    customer_email="dave@example.com",
    item=OrderItem(product_id="p1", name="Widget", quantity=2, price=9.99),
    items=[...]
)
order.item.name  # "Widget"
```

可以無限巢狀：Customer → Address → Order → Items → Product

## 第六章：Pydantic Settings

用於環境變數和設定管理（需額外安裝）：

```bash
uv add pydantic-settings
```

```python
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    api_key: str               # 必填
    model: str = "gpt-4o"     # 預設值
    max_tokens: int = 1000
    debug: bool = False

# 啟動時立刻驗證，而非等到使用時才報錯
settings = Settings()
# 若 .env 中沒有 api_key → 立刻 ValidationError
```

`.env` 範例：
```
API_KEY=sk-xxxxx
MODEL=gpt-4o
MAX_TOKENS=2000
```

### 進階功能

```python
# 前綴
model_config = ConfigDict(env_prefix="MYAPP_")  # 讀取 MYAPP_API_KEY

# 隱藏敏感值
from pydantic import SecretStr
api_key: SecretStr  # print 時顯示 *** 而非實際值
```

## 第七章：Structured Output 與 LLM 整合

這是 Pydantic 在 AI 應用中最重要的角色。

### 基本範例（OpenAI SDK）

```python
from pydantic import BaseModel
from openai import OpenAI

class ProductInfo(BaseModel):
    name: str
    price: float
    category: str
    in_stock: bool

client = OpenAI()
response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "user", "content": "The new MacBook Pro is now $1999..."}],
    response_format=ProductInfo,
)
product = response.choices[0].message.parsed
product.name    # "MacBook Pro"
product.price   # 1999.0
```

底層機制：Pydantic 模型 → JSON Schema → 注入到 prompt → LLM 強制輸出符合格式 → 若格式不對，自動 retry 並將錯誤訊息回饋給 LLM 自我修正。

### Literal 用於 LLM 路由

```python
from typing import Literal
from pydantic import BaseModel

class TicketClassification(BaseModel):
    text: str
    sentiment: Literal["positive", "negative", "neutral"]
    category: Literal["billing", "technical", "general"]
    needs_human: bool

# LLM 的輸出被限定在這些選項中
# 可用於工作流路由：positive → 謝謝訊息；negative → 人工升級
```

### 生產案例（客服系統）

真實架構：工單進入 → 分類+情感分析（Pydantic 結構化輸出）→ 路由到對應處理流程。

```python
class SupportTicket(BaseModel):
    category: TicketCategory  # Enum 或 Literal
    sentiment: Literal["positive", "negative", "neutral"]
    is_order_related: bool
    needs_tracking: bool
    missing_info: list[str]   # 需要追問客戶的資訊
```

### Field descriptions 的力量

```python
class InvoiceData(BaseModel):
    vendor_name: str = Field(description="發票上的供應商名稱，可能在右上角或左上角")
    total_amount: float = Field(description="稅後總金額，單位為台幣")
    is_paid: bool = Field(description="是否已付款，根據是否有收款章或已付款字樣判斷")
```

`description` 會被注入到給 LLM 的 prompt 中，等同於 prompting——這是調整 LLM 輸出可靠性的重要工具。

## 快速參考

```python
from pydantic import BaseModel, Field, field_validator, EmailStr
from pydantic_settings import BaseSettings
from typing import Literal, Optional

class MyModel(BaseModel):
    # 必填
    name: str

    # 有預設值
    status: Literal["active", "inactive"] = "active"

    # 可選
    bio: str | None = None

    # 有約束
    age: int = Field(gt=0, lt=150)

    # 自訂驗證
    @field_validator("name")
    @classmethod
    def check_name(cls, v):
        if len(v) < 2:
            raise ValueError("名字太短")
        return v.strip()

# 常用操作
obj = MyModel(name="Dave", age=31)
obj.model_dump()           # → dict
obj.model_dump_json()      # → JSON 字串
MyModel.model_validate(d)  # dict → 模型
MyModel.model_json_schema() # → JSON Schema
```
