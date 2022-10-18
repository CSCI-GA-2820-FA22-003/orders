# Update an order

Delete an Order. This endpoint will delete an Order based the id specified in the path.

**URL** : `/orders/<int:order_id>`

**Method** : `DELETE`

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `204`

**Content examples**

Delete an order based on new information for an existing entry. For example, such order with id 30 exists:

```json
{
    "address": "70 Washington Square S, New York, NY 10012",
    "date_created": "2022-10-17",
    "id": 30,
    "name": "Jeo"
}
```

I would like to delete that order at that moment. Send `DELETE` request to `/orders/30`.

The web server should return a 204 response with no message. When you try to get that order again with `GET /order/30`, you would receive a 404 response:

```json
{
    "error": "Not Found",
    "message": "404 Not Found: Item with id '30' was not found.",
    "status": 404
}
```

## Note
If you delete an invalid order (order id does not exist), your request would do nothing at back-end. The server would not explicitly return an error.