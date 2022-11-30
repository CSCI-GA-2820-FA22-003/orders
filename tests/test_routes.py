"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import app
from service.models import Order, Item, db
from service.common import status  # HTTP Status Codes
from tests.factories import OrderFactory, ItemFactory
from datetime import date

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/orders"
######################################################################
#  T E S T   C A S E S
######################################################################
class TestRestApiServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        db.drop_all()
        Order.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Item).delete()  # clean up the last tests
        db.session.query(Order).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def _create_orders(self, count):
        """Factory method to create orders in bulk"""
        orders = []
        for _ in range(count):
            test_order = OrderFactory()
            response = self.client.post("/api/orders", json=test_order.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test order"
            )
            new_order = response.get_json()
            test_order.id = new_order["id"]
            orders.append(test_order)
        return orders

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order_list(self):
        """It should Get a list of orders"""
        self._create_orders(5)
        response = self.client.get("/api/orders")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_get_order(self):
        """It should Get a single order"""
        # get the id of a order
        test_order = self._create_orders(1)[0]
        response = self.client.get(f"api/orders/{test_order.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_order.name)

    def test_get_order_by_date(self):
        """It should get a single order by date"""
        # get the id of a order
        test_order = self._create_orders(1)[0]
        
        response = self.client.get(f"api/orders/{test_order.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_order.name)

        response = self.client.get(f"api/orders/date/{test_order.date_created}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], test_order.name)

    def test_get_order_not_found(self):
        """It should not Get a order thats not found"""
        response = self.client.get(f"api/orders/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("Order with id '0' was not found.", data["message"])

    def test_create_order(self):
        """It should Create a new order"""
        test_order = OrderFactory()
        logging.debug("Test order: %s", test_order.serialize())
        response = self.client.post("/api/orders", json=test_order.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_order = response.get_json()
        self.assertEqual(new_order["name"], test_order.name)
        self.assertEqual(new_order["address"], test_order.address)
        self.assertEqual(date.fromisoformat(new_order["date_created"]), test_order.date_created)

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_order = response.get_json()
        self.assertEqual(new_order["name"], test_order.name)
        self.assertEqual(new_order["address"], test_order.address)
        self.assertEqual(date.fromisoformat(new_order["date_created"]), test_order.date_created)

    def test_update_order(self):
        """It should update an existing order"""
        # create a order to update
        test_order = OrderFactory()
        response = self.client.post("/api/orders", json=test_order.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the order
        new_order = response.get_json()
        logging.debug(new_order)
        new_order["address"] = "Tandon Brooklyn downtown"
        response = self.client.put(f"/api/orders/{new_order['id']}", json=new_order)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_order = response.get_json()
        self.assertEqual(updated_order["address"], "Tandon Brooklyn downtown")

    def test_update_order_not_found(self):
        """It should not Update a order thats not found"""
        # create a order to update
        test_order = OrderFactory()
        response = self.client.post("/api/orders", json=test_order.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the order
        new_order = response.get_json()
        response = self.client.put(f"/api/orders/1000", json=new_order)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("Order with id '1000' was not found.", data["message"])

    def test_delete_order(self):
        """It should Delete a order"""
        test_order = self._create_orders(1)[0]
        response = self.client.delete(f"api/orders/{test_order.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"/api/orders/{test_order.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order_not_found(self):
        """It should not delete an order thats not found"""
        # create a order
        test_order = OrderFactory()
        response = self.client.post("/api/orders", json=test_order.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # try to delete order
        response = self.client.delete(f"api/orders/1000")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("Order with id '1000' was not found.", data["message"])

    def test_add_item(self):
        """It should Add an item to an order"""
        test_order = self._create_orders(1)[0]
        item = ItemFactory()
        response = self.client.post(
            f"/api/orders/{test_order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.get_json()
        # print(data)
        logging.debug(data)
        self.assertEqual(data["product_id"], item.product_id)
        self.assertEqual(data["price"], item.price)
        self.assertEqual(data["quantity"], item.quantity)
        self.assertEqual(data["status"], item.status)

    def test_get_item(self):
        """It should Get an item from an order"""
        # create an item
        test_order = self._create_orders(1)[0]
        item = ItemFactory()
        response = self.client.post(
            f"/api/orders/{test_order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.get_json()
        logging.debug(data)
        item_id = data["id"]

        # fetch it back
        response = self.client.get(
            f"/api/orders/{test_order.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        logging.debug(data)
        self.assertEqual(data["product_id"], item.product_id)
        self.assertEqual(data["price"], item.price)
        self.assertEqual(data["quantity"], item.quantity)
        self.assertEqual(data["status"], item.status)

    def test_get_item_list(self):
        """It should Get all Items of an Order"""
        test_order = self._create_orders(1)[0]
        item = ItemFactory()
        response = self.client.post(
            f"/api/orders/{test_order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            f"/api/orders/{test_order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # get the list back and make sure there are 2
        resp = self.client.get(f"/api/orders/{test_order.id}/items")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(len(data), 2)

    def test_get_item_with_order_not_exist(self):
        """It should not list item if order not exists"""
        test_order = self._create_orders(1)[0]
        item = ItemFactory()
        response = self.client.post(
            f"/api/orders/{test_order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )

        data = response.get_json()
        logging.debug(data)
        item_id = data["id"]

        # fetch it back
        response = self.client.get(
            f"/api/orders/10/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item(self):
        """It should Update an item in an order"""
        # create an item
        test_order = self._create_orders(1)[0]
        item = ItemFactory()
        response = self.client.post(
            f"/api/orders/{test_order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.get_json()
        logging.debug(data)
        item_id = data["id"]
        data["price"] = 3.75

        # send the update back
        response = self.client.put(
            f"/api/orders/{test_order.id}/items/{item_id}",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve it back
        response = self.client.get(
            f"/api/orders/{test_order.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        logging.debug(data)
        self.assertEqual(data["id"], item_id)
        self.assertEqual(data["price"], 3.75)

    def test_update_item_with_order_not_exist(self):
        """It should not update item if order not exists"""
        test_order = self._create_orders(1)[0]
        item = ItemFactory()
        response = self.client.post(
            f"/api/orders/{test_order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )

        data = response.get_json()
        logging.debug(data)
        item_id = data["id"]
        data["price"] = 3.75

        # try to update
        response = self.client.put(
            f"/api/orders/4533/items/{item_id}",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item(self):
        """It should Delete an item"""
        test_order = self._create_orders(1)[0]
        item = ItemFactory()
        response = self.client.post(
            f"/api/orders/{test_order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.get_json()
        logging.debug(data)
        item_id = data["id"]

        # send delete request
        response = self.client.delete(
            f"/api/orders/{test_order.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # retrieve it back and make sure item is not there
        response = self.client.get(
            f"/api/orders/{test_order.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order_with_item(self):
        """It should delete Order and its items"""
        test_order = self._create_orders(1)[0]
        item = ItemFactory()
        response = self.client.post(
            f"/api/orders/{test_order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.get_json()
        logging.debug(data)
        item_id = data["id"]

        # delete item
        response = self.client.delete(
            f"/api/orders/{test_order.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # check item is not there
        response = self.client.get(
            f"/api/orders/{test_order.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        #delete order
        response = self.client.delete(f"api/orders/{test_order.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)

        # check they are deleted
        response = self.client.get(f"api/orders/{test_order.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item_with_order_not_exist(self):
        """It should not delete item if order not exists"""
        test_order = self._create_orders(1)[0]
        item = ItemFactory()
        response = self.client.post(
            f"/api/orders/{test_order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )

        data = response.get_json()
        logging.debug(data)
        item_id = data["id"]

        # fetch it back
        response = self.client.delete(
            f"/api/orders/10/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_check_content_type_with_wrong_type(self):
        """It should not receive data except json"""
        test_order = self._create_orders(1)[0]
        item = ItemFactory()
        response = self.client.post(
            f"/api/orders/{test_order.id}/items",
            json=item.serialize(),
            content_type="application/txt",
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_check_content_type_with_no_context(self):
        """It should not receive data with no content type"""
        test_order = self._create_orders(1)[0]
        response = self.client.post(
            f"/api/orders/{test_order.id}/items",
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_method_not_allowed(self):
        """It should not allow an illegal method call"""
        test_order = self._create_orders(1)[0]
        response = self.client.delete(
            f"/api/orders/{test_order.id}/items",
            json={"method": "invalid"},
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_items_price_min_max(self):
        """It should get all Items of an Order that are between max and min price"""
        test_order = self._create_orders(5)
        item = ItemFactory()
        response = self.client.post(
            f"/api/orders/{test_order[0].id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.get_json()
        logging.debug(data)
        item_id = data["id"]
        data["price"] = 3.75

        # send the update back
        response = self.client.put(
            f"/api/orders/{test_order[0].id}/items/{item_id}",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            f"/api/orders/{test_order[1].id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.get_json()
        logging.debug(data)
        item_id = data["id"]
        data["price"] = 4.75

        # send the update backIt should find
        response = self.client.put(
            f"/api/orders/{test_order[1].id}/items/{item_id}",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # retrieve it back
        response = self.client.post(
            f"/api/orders/prices",
            json={'max_price': 5.0, 'min_price': 3.0},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 2)
