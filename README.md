# NYU DevOps  - Orders Team

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Pylint](https://github.com/CSCI-GA-2820-FA22-003/orders/actions/workflows/pylint.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA22-003/orders/actions/workflows/pylint.yml)
[![TestCasesTDD](https://github.com/CSCI-GA-2820-FA22-003/orders/actions/workflows/tdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA22-003/orders/actions/workflows/tdd.yml)
[![BDD Tests](https://github.com/CSCI-GA-2820-FA22-003/orders/actions/workflows/bdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA22-003/orders/actions/workflows/bdd.yml)

## Overview

![](docs/logo-order.png)

A collection of order items created from products and quantity. Logo made by [NovelAI](https://novelai.net/).

## Docs

### Basic Order Operations

| Description     | Endpoint                        | Docs |
| --------------- | ------------------------------- | ---- |
| Delete an order | DELETE `/api/orders/{int:order_id}` | [link](docs/order/delete.md)     |
| Get an order   | GET `/api/orders/{int:order_id}`    | [link](docs/order/get.md)     |
| Update an order | PUT `/api/orders/{int: order_id}/`  | [link](docs/order/update.md)     |
| Create an order | POST `/api/order/`                  | [link](docs/order/create.md)     |
| List orders     | GET `/api/orders/`                  | [link](docs/order/list.md)    |

### Basic Item Operations

| Description                | Endpoint                                    | Docs |
| -------------------------- | ------------------------------------------- | ---- |
| Delete an item in an order | DELETE `/api/orders/{order_id}/items/{item_id}` | [link](docs/item/delete.md)  |
| Add an item to an order    | POST `/api/orders/{order_id}/items`             | [link](docs/item/create.md)  |
| Get the detail of an item  | GET `/api/orders/{order_id}/items/{item_id}`    | [link](docs/item/get.md)  |
| Update an item in an order | PUT `/api/orders/{order_id}/items/{item_id}`    | [link](docs/item/update.md)  |

### Advanced Operations

| Description                       | Endpoint                      | Issue |
| --------------------------------- | ----------------------------- | ----- |
| Read order based on price range   | GET `/api/orders_date/{date}` | [link](docs/order/price.md)      |
| Read order based on item quantity | POST `/api/orders/orders_prices/`    | [link](docs/order/date.md)      |

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
