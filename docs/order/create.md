# Create an Order

Create an order that does not include any item. User should provide name, address of the order. An ISO time tag is optional.

**URL** : `/order`

**Method** : `POST`

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `201 CREATED`

**Content examples**

For an order with name `Jeo`, and the address of `70 Washington Square S, New York, NY 10012`

```json
{
    "name": "Jeo", 
    "address": "70 Washington Square S, New York, NY 10012",
}
```

You would receive 201 as feedback. A date and id is automatically generated at back-end, with location of `/orders/<int:order_id>`.

```json
{
    "address": "70 Washington Sqaure S, New York, NY 10012",
    "date_created": "2022-10-17",
    "id": 30,
    "name": "Jeo"
}
```

The date is optional, but you could specified in [ISO 8601-format](https://en.wikipedia.org/wiki/ISO_8601).

```json
{
    "name": "Jeo", 
    "address": "70 Washington Square S, New York, NY 10012",
    "date_created": "2022-10-17"
}
```

## Notes

- To retrieve the information of an order, reach endpoint of `/orders/<int:order_id>` for help.