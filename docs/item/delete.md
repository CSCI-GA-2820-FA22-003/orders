# Update an order

Delete an item. This endpoint will delete an item based on the id specified in the path.

**URL** : `/orders/<int:order_id>/items/<int:item_id>`

**Method** : `DELETE`

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `204`

**Content examples**

Delete an item based on new information for an existing entry. For example, For an order with order id 123 there is an item with id 30:

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

To delete this item from the order send `DELETE` request to `/orders/123/items/30`.

The web server should return a 204 response with no message. When you try to get that order again with `GET /orders/123/items/30`, you would receive a 404 response:

```json
{
    "error": "Not Found",
    "message": "404 Not Found: Item with id '30' was not found.",
    "status": 404
}
```

## Note
If you delete an invalid item, your request would do nothing at back-end. The server would not explicitly return an error.