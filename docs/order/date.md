# Get an Order By Date

Get an order on the specific date.

**URL** : `/api/orders_date`

**Method** : `GET`

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `200 OK`

**Content examples**

For an order with name `Jeo`, and the address of `70 Washington Square S, New York, NY 10012`, created at `2022-10-17`


```json
{
    "address": "70 Washington Sqaure S, New York, NY 10012",
    "date_created": "2022-10-17",
    "id": 30,
    "name": "Jeo"
}
```

You send a request of `/orders_date/2022-10-17`, where date is in [ISO 8601-format](https://en.wikipedia.org/wiki/ISO_8601).

The response is exactly same as the above.

## Failure response

When you send an invalid date, you will get `400 BAD REQUEST` as a result. For example, `GET /orders_date/nonsense` is a bad request.

When there is no order at target date, you will receive `404 NOT FOUND`.