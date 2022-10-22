# Retrieve an Item

Retrieve an item in an order. This endpoint will return an item based on it's id

**URL** : `/orders/<int:order_id>/items/<int:item_id>`

**Method** : `GET`

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `200 OK`

**Content examples**

For an item created with `/orders/<int:order_id>/items/<int:item_id>` POST request. Use the item id to retrieve the item in an order, You would get an item json with format like this:

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

## Failure Response

If the order item with `/orders/<int:order_id>/items/<int:item_id>` does not exists, it would return a 404 back. For example of `/orders/123/items/30` that is a invalid id:

```json
{
    "error": "Not Found",
    "message": "404 Not Found: Item with id '30' was not found.",
    "status": 404
}
```