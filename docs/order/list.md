# List all orders

Returns all of the orders.

**URL** : `/api/orders`

**Method** : `GET`

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `200 OK`

**Content examples**

For a database with 30 entries, you would get a list of json like this:

```json
[
    {
        "address": "Test Address",
        "date_created": "2022-10-17",
        "id": 2,
        "name": "Test Order"
    },
    {
        "address": "Test Address",
        "date_created": "2022-10-17",
        "id": 3,
        "name": "Test Order"
    },
    {
        "address": "Test Address",
        "date_created": "2022-10-17",
        "id": 4,
        "name": "Test Order"
    },
    ... (omit 30 entries)
]
```

## Failure Response

It is supposed to be successful if database works. Otherwise, you would get a 500 return.