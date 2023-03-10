# Overview
A sushi order system based on Docker, FastAPI, SQLAlchemy and MySQL.

# Getting Started
## Run the application
```bash
docker-compose up --build
```

## Open the application
[http://localhost:8000/](http://localhost:8000/)

## API
- GET /menus
- GET /menus/sushi
- GET /menus/sushi?category_id=1
- GET /menus/drink
- POST /customers
- GET /customers/{customer_id}/orders
- POST /customers/{customer_id}/orders
- GET /admin/orders/new
- GET /admin/orders
- PUT /admin/order_details/{order_detail_id}
- POST /admin/menus/sushi
- PUT /admin/menus/sushi/{sushi_id}
- DELETE /admin/menus/sushi/{sushi_id}
- POST /admin/menus/drink
- PUT /admin/menus/drink/{drink_id}
- DELETE /admin/menus/drink/{drink_id}

## Status定義
```
- orders.status
    - 0: unpaid
    - 1: paid
- order_details.status
    - ~~0: in cart~~
    - 1: submitted（謝罪行く前も含む？）
    - 2: delivered
    - 3: cancelled_by_customer
    - 4: cancelled_by_staff
- item_type
    - 0: 寿司
    - 1: ドリンク
- topping
    - 0: マヨネーズ
    - 1: チリソース
    - 2: ネギ
    - 3: オリーブオイル
    - 4: ホイップクリーム
- size
    - 0: おつまみ（シャリなし）
    - 1: 少なめ
    - 2: 並
    - 3: 特大
```

## ER図
```
erDiagram
    customers{
        string customer_id
				int seat_id
    }
		
		seats{
				int seat_id
				boolean is_available
		}

    sushis{
        int sushi_id
        string name
        boolean has_wasabi
        decimal price
        int category_id
    }

    drinks{
        int drink_id
        string name
        decimal price
    }

    categories{
        int category_id
        string name
    }

    orders{
        int order_id
        string customer_id
        decimal total_price
				int status
    }

		order_details{
				int order_detail_id
				int order_id
				int item_type
				int item_id
				int topping
				int size
				int quantity
				boolean has_wasabi
				decimal price
				int status
				datetime ordered_at
		}

    stocks{
        int stock_id
        int item_type
        int item_id
        int quantity
    }

		customers ||--|{ orders: ""
		seats ||--|{ customers: ""
        sushis ||--|{ order_details: ""
		drinks ||--|{ order_details: ""
		orders ||--|{ order_details: ""
		categories ||--|{ sushis: ""
		sushis ||--|{ stocks: ""
		drinks ||--|{ stocks: ""


```

## シーケンス図
```
sequenceDiagram
	autonumber
	actor お客様

	お客様 ->> NativeApp: 来店、customer_idを発行する
	NativeApp ->> SushiOrderBackend: POST /customers, param: seat_id
	SushiOrderBackend ->> SushiOrderBackend: お客様のcustomer_id(UUID)を生成する
	SushiOrderBackend ->> SushiOrderDatabase: Customersテーブルに{customer_id, seat_id}を挿入する
	SushiOrderDatabase ->> SushiOrderBackend: ok/ng
	SushiOrderBackend ->> NativeApp: お客様のcustomer_id
	NativeApp ->> お客様: お客様のcustomer_id

	お客様 ->> NativeApp: メニュー一覧を取得する
    NativeApp ->> SushiOrderBackend: GET /menus
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
    SushiOrderDatabase ->> SushiOrderBackend: result list
	SushiOrderBackend ->> NativeApp: result list
	NativeApp ->> お客様: メニュー一覧

	お客様 ->> NativeApp: 寿司メニュー一覧を取得する
    NativeApp ->> SushiOrderBackend: GET /menus/sushi
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
    SushiOrderDatabase ->> SushiOrderBackend: result list
	SushiOrderBackend ->> NativeApp: result list of sushi menu
	NativeApp ->> お客様: 寿司メニュー一覧

	お客様 ->> NativeApp: カテゴリごとの寿司一覧を取得する
    NativeApp ->> SushiOrderBackend: GET /menus/sushi param:categorized=true
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
    SushiOrderDatabase ->> SushiOrderBackend: result list
	SushiOrderBackend ->> NativeApp: result list
	NativeApp ->> お客様: カテゴリごとの寿司一覧

	お客様 ->> NativeApp: ドリンクメニュー一覧を取得する
	NativeApp ->> SushiOrderBackend: GET /menus/drink
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
    SushiOrderDatabase ->> SushiOrderBackend: result list
	SushiOrderBackend ->> NativeApp: result list of drink menu
	NativeApp ->> お客様: ドリンクメニュー一覧

	お客様 ->> NativeApp: カートの追加、更新、削除
	NativeApp ->> お客様: カートの最新情報

	お客様 ->> NativeApp: カートに入ったメニューを注文する
	NativeApp ->> SushiOrderBackend: POST /customers/{customer_id}/orders
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
    SushiOrderDatabase ->> SushiOrderBackend: result
    activate SushiOrderBackend
    SushiOrderBackend ->> SUSYS: POST /recommended
    SUSYS ->> SushiOrderBackend: list of recommendations
    SushiOrderBackend ->> NativeApp: list of recommendations
	NativeApp ->> お客様: list of recommendations
    activate SUSYS
```

```
sequenceDiagram
	autonumber
	actor 従業員
	従業員 ->> NativeApp: 新規注文を閲覧する
  NativeApp ->> SushiOrderBackend: GET /admin/orders/new
	SushiOrderBackend ->> SushiOrderDatabase: SQL query: select all order_details with status=submitted
	SushiOrderDatabase ->> SushiOrderBackend: result
	SushiOrderBackend ->> NativeApp: result
	NativeApp ->> 従業員: 全ての新規注文

	従業員 ->> NativeApp: お客様の注文履歴を閲覧する
  NativeApp ->> SushiOrderBackend: GET /admin/orders, param: customer_id
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
	SushiOrderDatabase ->> SushiOrderBackend: result
	SushiOrderBackend ->> NativeApp: result
	NativeApp ->> 従業員: お客様の注文履歴

	従業員 ->> NativeApp: 注文の状態を更新する
	NativeApp ->> SushiOrderBackend: PUT /admin/order_details/{order_detail_id}
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
	SushiOrderDatabase ->> SushiOrderBackend: OK/NG
	SushiOrderBackend ->> NativeApp: OK/NG
	NativeApp ->> 従業員: 更新完了/エラー
	
	従業員 ->> NativeApp: お客様の注文履歴から注文を削除する
	NativeApp ->> SushiOrderBackend: PUT /admin/order_details/{order_detail_id}
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
	SushiOrderDatabase ->> SushiOrderBackend: OK/NG
	SushiOrderBackend ->> NativeApp: OK/NG
	NativeApp ->> 従業員: 削除完了/エラー

	従業員 ->> NativeApp: 注文を完了する（寿司を届ける）
	NativeApp ->> SushiOrderBackend: PUT /admin/order_details/{order_detail_id}
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
	SushiOrderDatabase ->> SushiOrderBackend: OK/NG
	SushiOrderBackend ->> NativeApp: OK/NG
	NativeApp ->> 従業員: 注文完了/エラー

	従業員 ->> NativeApp: 寿司メニューの一覧を取得する
    NativeApp ->> SushiOrderBackend: GET /menus/sushi
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
	SushiOrderDatabase ->> SushiOrderBackend: result
	SushiOrderBackend ->> NativeApp: result
	NativeApp ->> 従業員: 寿司メニューの一覧

	従業員 ->> NativeApp: 寿司メニューを追加する
    NativeApp ->> SushiOrderBackend: POST /admin/menus/sushi
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
	SushiOrderDatabase ->> SushiOrderBackend: OK/NG
	SushiOrderBackend ->> NativeApp: OK/NG
	NativeApp ->> 従業員: 追加完了/エラー

	従業員 ->> NativeApp: 寿司メニューを変更する
    NativeApp ->> SushiOrderBackend: PUT /admin/menus/sushi/{sushi_id}
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
	SushiOrderDatabase ->> SushiOrderBackend: OK/NG
	SushiOrderBackend ->> NativeApp: OK/NG
	NativeApp ->> 従業員: 変更完了/エラー

	従業員 ->> NativeApp: 寿司メニューを削除する
    NativeApp ->> SushiOrderBackend: DELETE /admin/menus/sushi/{sushi_id}
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
	SushiOrderDatabase ->> SushiOrderBackend: OK/NG
	SushiOrderBackend ->> NativeApp: OK/NG
	NativeApp ->> 従業員: 削除完了/エラー
	
	従業員 ->> NativeApp: ドリンクメニューの一覧を取得する
	NativeApp ->> SushiOrderBackend: GET /menus/drink
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
	SushiOrderDatabase ->> SushiOrderBackend: result
	SushiOrderBackend ->> NativeApp: result
	NativeApp ->> 従業員: ドリンクメニューの一覧

	従業員 ->> NativeApp: ドリンクメニューを追加する
	NativeApp ->> SushiOrderBackend: POST /admin/menus/drink
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
	SushiOrderDatabase ->> SushiOrderBackend: OK/NG
	SushiOrderBackend ->> NativeApp: OK/NG
	NativeApp ->> 従業員: 追加完了/エラー

	従業員 ->> NativeApp: ドリンクメニューを変更する
	NativeApp ->> SushiOrderBackend: PUT /admin/menus/drink/{drink_id}
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
	SushiOrderDatabase ->> SushiOrderBackend: OK/NG
	SushiOrderBackend ->> NativeApp: OK/NG
	NativeApp ->> 従業員: 変更完了/エラー

	従業員 ->> NativeApp: ドリンクメニューを削除する
	NativeApp ->> SushiOrderBackend: DELETE /admin/menus/drink/{drink_id}
	SushiOrderBackend ->> SushiOrderDatabase: SQL query
	SushiOrderDatabase ->> SushiOrderBackend: OK/NG
	SushiOrderBackend ->> NativeApp: OK/NG
	NativeApp ->> 従業員: 削除完了/エラー

```