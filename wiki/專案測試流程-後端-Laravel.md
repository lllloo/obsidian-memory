---
title: 專案測試流程 後端 Laravel
description: Laravel 端測試落地：判斷從 Controller 抽到 Service、Unit／Feature 兩個 testsuite 的分界與陷阱、整合測試該覆蓋到哪
created: 2026-08-08
updated: 2026-08-28
parent: "[[wiki/01.index]]"
tags:
  - testing
  - laravel
  - coding-agent
---

> [[專案測試流程|總覽]] ｜ [[專案測試流程-前端-Vue|前端 Vue]] ｜ **後端 Laravel**

本頁是 [[專案測試流程]] 在 Laravel 端的落地。分層原則、斷言紀律、覆蓋率的停止條件都在總頁，這裡只講**Laravel 專屬的做法與坑**。前端對應的一頁是 [[專案測試流程-前端-Vue]]。

## 第一層：單元測試

### 判斷長在 Controller 裡，就沒有單元可以測

```php
// ❌ 折扣規則埋在 Controller
public function store(Request $request)
{
    $sum = collect($request->items)->sum(fn ($i) => $i['price'] * $i['qty']);
    if ($sum >= 1000) { $sum = $sum * 0.9; }
    return response()->json(['total' => round($sum)]);
}
```

要驗證那條「滿 1000 打九折」，得發一個 HTTP request、通過 middleware、可能還要有資料庫與登入使用者。

抽出來，讓它脫離框架：

```php
// ✅ app/Services/PricingService.php — 不碰 Request、不碰 Model
class PricingService
{
    public function calcTotal(array $items): int
    {
        $sum = collect($items)->sum(fn ($i) => $i['price'] * $i['qty']);
        return (int) round($sum >= 1000 ? $sum * 0.9 : $sum);
    }
}
```

Controller 這側只剩接收與交出，沒有判斷：

```php
public function store(StoreOrderRequest $request, PricingService $pricing)
{
    // StoreOrderRequest 是 FormRequest——validated() 只存在於 FormRequest，基礎 Request 沒有
    return response()->json([
        'total' => $pricing->calcTotal($request->validated()['items']),
    ]);
}
```

### 陷阱：`tests/Unit` 裡繼承錯 TestCase，框架就被啟動了

這是 Laravel 端最容易無聲踩到的坑。專案裡有兩個名字很像的 `TestCase`：

| 繼承的類別 | 會發生什麼 | 屬於 |
|---|---|---|
| `PHPUnit\Framework\TestCase` | 什麼都不做，純 PHP | **第 1 層** |
| `Tests\TestCase` | 啟動整個 Laravel application、載入設定與服務容器 | 第 2 層 |

Laravel 骨架預設就把這個分界做好了——`tests/Unit/ExampleTest.php` 繼承前者、`tests/Feature/ExampleTest.php` 繼承後者。問題是**放在 `tests/Unit/` 底下的檔案改成繼承 `Tests\TestCase` 也完全能跑**，測試照樣是綠的，只是每一條都悄悄付了啟動框架的成本。目錄名稱不構成保證。

真正的第一層測試長這樣，不繼承 Laravel 的東西、不加 `RefreshDatabase`：

```php
// tests/Unit/PricingServiceTest.php
namespace Tests\Unit;

use App\Services\PricingService;
use PHPUnit\Framework\TestCase;   // ← 不是 Tests\TestCase

class PricingServiceTest extends TestCase
{
    public function test_未滿門檻不打折(): void
    {
        $this->assertSame(200, (new PricingService)->calcTotal([
            ['price' => 100, 'qty' => 2],
        ]));
    }

    public function test_剛好滿_1000_就打折(): void
    {
        $this->assertSame(900, (new PricingService)->calcTotal([
            ['price' => 500, 'qty' => 2],
        ]));
    }
}
```

`assertSame()` 優先於 `assertEquals()`——後者不比較型別，`"900"` 會等於 `900`，那正是總頁講的弱斷言。

> 專案若用 Pest，語法是 `it('剛好滿 1000 就打折', fn () => expect(...)->toBe(900))`，底層仍是 PHPUnit，上面的分層與繼承規則完全相同。

### 該測什麼、不該測什麼

第一層的射程：

- **Service 類別**裡的業務規則——計價、折扣、額度、狀態轉換
- **Value Object / DTO** 的建構驗證與轉換
- **Enum 上的方法**、權限判斷這類純函式
- 純粹的字串／日期／金額處理

不測的：

- **Eloquent 能不能存進資料庫**——那是框架的責任，而且需要 DB，屬第二層
- **route 有沒有正確回應**——那是 `Feature` 測試
- **`FormRequest` 的驗證規則**——它需要框架容器解析，屬第二層

**遇到規則寫在 Model 裡怎麼辦**：Eloquent Model 綁著資料庫，難以留在第一層。做法不是硬測 Model，而是把規則再往外抽一層——判斷進 Service 或純方法，Model 只留欄位與關聯。

### 怎麼跑

```bash
php artisan test --testsuite=Unit
```

`phpunit.xml` 預設就把 `Unit` 與 `Feature` 分成兩個 testsuite，第一層只跑前者。

```
tests/
  Unit/
    PricingServiceTest.php     ◀ 第 1 層：extends PHPUnit\Framework\TestCase
    DiscountRuleTest.php          無 RefreshDatabase、不碰容器
  Feature/
    OrderApiTest.php           ◀ 第 2 層：extends Tests\TestCase
                                  打 route、碰 DB
```

**訊號：如果 `--testsuite=Unit` 跑起來很慢，那批測試就有問題。** 真正的第一層應該是毫秒級、幾百條也在一兩秒內跑完；一旦明顯變慢，代表有測試繼承了 `Tests\TestCase` 或偷偷連了資料庫。這個訊號比人工 review 可靠，因為它不需要有人記得去檢查。

### 這一層完成的樣子

1. 業務規則已從 Controller 抽成不依賴 `Request`／Model 的 Service 或純方法
2. `tests/Unit` 底下沒有任何一條繼承 `Tests\TestCase`，也沒有 `RefreshDatabase`
3. `php artisan test --testsuite=Unit` 一個指令跑完、全綠，並寫進 `README.md`
4. 那個指令的執行時間是**秒級以內**——這是第 2 點的自動化證明

### 什麼時候該停

停止條件見 [[專案測試流程]] 的「不追覆蓋率數字」。Laravel 端有一個特有的過度工程紅線：**不要為了覆蓋率去測 Model 的 `$fillable`、關聯宣告或 accessor 的直接回傳**。那些是設定不是邏輯，測了只會在改欄位時多一批要跟著改的檔案。

## 第二層：整合測試

**尚未實作，以下為做法設計**（2026-08-28 談定，未在本專案驗證）。

對外一律叫 **integration test**。Laravel 的 `Feature` 是框架專有命名，跟別的生態溝通時說 Feature 多半會被理解成 BDD 的驗收測試。

### 射程：判斷被接進框架之後還對不對

同一條「滿 1000 打九折」，第一層問「算得對嗎」，第二層問「打 API 進來、走完 middleware 與驗證、經過 Model，回出去的還是那個數字嗎」。

```php
// tests/Feature/OrderApiTest.php
class OrderApiTest extends TestCase   // ← Tests\TestCase，不是 PHPUnit 的
{
    use RefreshDatabase;

    public function test_滿門檻的訂單回九折後金額(): void
    {
        $user = User::factory()->create();

        $this->actingAs($user)
            ->postJson('/api/orders', ['items' => [['price' => 500, 'qty' => 2]]])
            ->assertCreated()
            ->assertJsonPath('data.total', 900);
    }
}
```

這層才碰得到的四種東西，第一層全部射不到：

| | 為什麼第一層射不到 |
|---|---|
| route 與 middleware | 需要真的發請求 |
| `FormRequest` 驗證規則 | 需要框架容器解析 |
| 權限與登入態 | `actingAs` 是框架能力 |
| Eloquent 持久化與關聯 | 需要 DB |

`RefreshDatabase` 把每條測試包在交易裡跑完退回——**這招到第三層就失效**，因為請求由另一個進程處理，測試端的交易包不住它（見 [[E2E-測試的資料庫隔離]]）。

### 紅線：不要重測第一層測過的規則

最常見的浪費：Service 已有 20 條測試釘死折扣規則，Feature 測試再把 20 種金額組合打一遍。**第二層只需要一條確認「規則有被正確接上」**，剩下的組合留在毫秒級的第一層跑。

判準：如果一條 Feature 測試改的是輸入的**數值**而不是**路徑或狀態**，它多半該退回第一層。

### 這一層完成的樣子

1. **每個 endpoint 至少兩條**：成功路徑（200/201，資料結構與關鍵欄位對）+ 驗證失敗（422，錯誤結構對）
2. 有權限控制的 endpoint 再加一條 403
3. `php artisan test --testsuite=Feature` 一個指令跑完、全綠
4. 測試用 database 獨立於開發用的

30 個 endpoint 大約 60–90 條測試、分鐘級跑完，是合理規模。執行時間從第一層的秒級掉到分鐘級是**正常的，不是訊號**。

### 這一層的職責邊界

**後端 API 本身對不對，完全由這層負責，而且要全覆蓋。** E2E 不承擔這件事——它只驗少數關鍵路徑的串接，用它來「多驗幾個 endpoint」是把便宜的事做貴了。

這層做紮實之後，後端唯一剩下的缺口是「前端以為的形狀跟實際回的一不一致」，那不是測試層的問題，處置見 [[專案測試流程]] 的契約測試一節。

## 關聯

- [[專案測試流程]] — 總頁：三層射程（2026-08-28 由四層改制，契約層不採）、一個測試該歸哪一層的判準，以及兩端共通的斷言紀律與停止條件。本頁只補 Laravel 專屬的部分。
- [[專案測試流程-前端-Vue]] — 對照組。兩端卡的是同一個坑（判斷長在框架內部），但訊號不同：這裡是 `--testsuite=Unit` 跑起來很慢，那邊是測試檔出現 `mount()`。
- [[E2E-測試的資料庫隔離]] — 本頁第 2 層靠 `RefreshDatabase` 的交易回滾做隔離，那個機制到第 3 層就失效（請求由另一個進程處理，包不進測試端的交易），因此 E2E 得改用獨立 database 加固定 fixture。
- [[測試手段的優先序與成本]] — 本頁第一層完成後的下一件事在該頁：對 `app/Services` 跑一次 mutation 基線（Pest `--mutate` 或 Infection），以及為何後端值得深挖 mutation 而前端不值得。
- [[用測試約束-AI-產碼]] — 上面「繼承錯 TestCase」屬於該頁講的一類病徵：測試看起來是綠的，但綠的理由不對。同節並記錄 AI 產測試最高頻的弱斷言問題，對應本頁 `assertSame` 與 `assertEquals` 的取捨。
