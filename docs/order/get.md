# Retrieve an Order

Retrieve a single order. This endpoint will return an Order based on it's id

**URL** : `/api/order/<int:order_id>`

**Method** : `GET`

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `200 OK`

**Content examples**

For an order created with `/order` POST request. You would get an order json with format like this:

```json
{
    "address": "70 Washington Sqaure S, New York, NY 10012",
    "date_created": "2022-10-17",
    "id": 30,
    "name": "Jeo"
}
```

Use the id to retrieve the order, you would get exactly the same thing as above if it is not updated by other requests.

## Failure Response

If the order with `<int:order_id>` does not exists, it would return a 404 back. For example of `/order/31` that is a invalid id:

```json
{
    "error": "Not Found",
    "message": "404 Not Found: Item with id '31' was not found.",
    "status": 404
}
```