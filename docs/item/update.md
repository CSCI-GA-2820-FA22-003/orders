# Update an item

Updates an item in an order.

**URL** : `/api/orders/<int:order_id>/items/<int:item_id>`

**Method** : `PUT`

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `200 OK`

**Content examples**

Update an item based on new information for an existing entry. For an order with order id 123 there is an item with id 30:

```json
{
    "product_id": 111, 
    "price": 7.5,
    "quantity" : 2,
    "id" : 30,
    "order_id" : 123,
    "status" : "active",
}
```

I would like to change price of "7.5" into "4.5" at that moment. Send `PUT` request to `/api/orders/123/items/30` with body of:

```json
{
    "product_id": 111, 
    "price": 4.5,
    "quantity" : 2,
    "status" : "active",
}
```

The web server should return a 200 response:
```json
{
    "product_id": 111, 
    "price": 4.5,
    "quantity" : 2,
    "id" : 30,
    "order_id" : 123,
    "status" : "active",
}
```

## Failure Response

If id is invalid, you would receive a 404 response like:

```json
{
    "error": "Not Found",
    "message": "404 Not Found: Order with id '30' was not found.",
    "status": 404
}
```