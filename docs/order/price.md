# Get an Order By Price Range

Get an order with item at target price range.

For example, if you would like filter out the laptop you bought, from 1000$ to 2000$, then this API would help you.

**URL** : `/api/orders_prices`

**Method** : `POST`

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `200 OK`

**Content examples**

The goal of this API is to get an order of item within the price range.

For an order like:

```json
{
    "id": 1,
    "name": "Joe",
    "address": "New York University",
    "date_created": "2022-12-14",
    "items": [
        {
            "id": 1,
            "product_id": 250124,
            "price": 20.0,
            "quantity": 2.0,
            "order_id": 1,
            "status": "shipped"
        }
    ]
}
```

You send a request of `/orders_prices/` with message

```json
{
    "max_price": 40,
    "min_price": 20
}
```

Then you would get that order back.

## Failure response

When you send invalid price, you will get `400 BAD REQUEST` as a result. For example, following json is a bad request

```json
{
    "max_price": "xx",
    "min_price": "yy"
}
```

When there is no order at target date, you will receive `404 NOT FOUND`.