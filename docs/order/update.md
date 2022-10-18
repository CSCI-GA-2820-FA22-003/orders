# Update an order

Returns all of the orders.

**URL** : `/orders/<int:order_id>`

**Method** : `PUT`

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `200 OK`

**Content examples**

Update an order based on new information for an existing entry. For example, such order with id 30 exists:

```json
{
    "address": "70 Washington Sqaure S, New York, NY 10012",
    "date_created": "2022-10-17",
    "id": 30,
    "name": "Jeo"
}
```

I would like to change name of "Jeo" into "David" at that moment. Send `PUT` request to `/orders/30` with body of:

```json
{
    "address": "70 Washington Sqaure S, New York, NY 10012",
    "name": "David"
}
```

The web server should return a 200 response:
```json
{
    "address": "70 Washington Sqaure S, New York, NY 10012",
    "date_created": "2022-10-17",
    "id": 30,
    "name": "David"
}
```

## Failure Response

If order id is invalid, you would receive a 404 response like:

```json
{
    "error": "Not Found",
    "message": "404 Not Found: Order with id '31' was not found.",
    "status": 404
}
```