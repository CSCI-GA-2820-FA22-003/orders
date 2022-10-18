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
from tests.factories import OrderFactory
from datetime import date

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/orders"
######################################################################
#  T E S T   C A S E S
######################################################################
class TestOrderServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Order.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
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
            response = self.client.post(BASE_URL, json=test_order.serialize())
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
        data = response.get_json()
        self.assertEqual(data["name"], "Order Demo REST API Service")

    def test_get_order_list(self):
        """It should Get a list of orders"""
        self._create_orders(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_get_order(self):
        """It should Get a single order"""
        # get the id of a order
        test_order = self._create_orders(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_order.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_order.name)

    def test_get_order_not_found(self):
        """It should not Get a order thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("Item with id '0' was not found.", data["message"])

    def test_create_order(self):
        """It should Create a new order"""
        test_order = OrderFactory()
        logging.debug("Test order: %s", test_order.serialize())
        response = self.client.post(BASE_URL, json=test_order.serialize())
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
        """It should Update an existing order"""
        # create a order to update
        test_order = OrderFactory()
        response = self.client.post(BASE_URL, json=test_order.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the order
        new_order = response.get_json()
        logging.debug(new_order)
        new_order["address"] = "Tandon Brooklyn downtown"
        response = self.client.put(f"{BASE_URL}/{new_order['id']}", json=new_order)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_order = response.get_json()
        self.assertEqual(updated_order["address"], "Tandon Brooklyn downtown")

    def test_update_order_not_found(self):
        """It should not Update a order thats not found"""
        # create a order to update
        test_order = OrderFactory()
        response = self.client.post(BASE_URL, json=test_order.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the order
        new_order = response.get_json()
        response = self.client.put(f"{BASE_URL}/1000", json=new_order)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("Order with id '1000' was not found.", data["message"])

    def test_delete_order(self):
        """It should Delete a order"""
        test_order = self._create_orders(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_order.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_order.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
