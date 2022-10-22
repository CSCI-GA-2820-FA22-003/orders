# Add an item to an order

Create an item in an order. User should provide product id, price, quantity and status of the item.

**URL** : `/orders/<int:order_id>/items`

**Method** : `POST`

**Auth required** : No

**Permissions required** : None

## Success Response

**Code** : `201 CREATED`

**Content examples**

For an order with order id `123` the below item is created

```json
{
    "product_id": 111, 
    "price": 7.5,
    "quantity" : 2,
    "status" : "active"
}
```

You would receive 201 as feedback. An id is automatically generated at back-end, with location of `/orders/<int:order_id>/items`.

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