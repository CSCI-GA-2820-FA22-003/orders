"""
Test cases for Order and Item Model

"""
import os
import logging
import unittest
from service.models import Order, Item, db
from service import app
from datetime import date
from tests.factories import OrderFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  O r d e r   M O D E L   T E S T   C A S E S
######################################################################
class TestOrderModel(unittest.TestCase):
    """ Test Cases for YourResourceModel Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Order.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Order).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_create_a_order(self):
        """It should Create a order and assert that it exists"""
        order = Order(name="Devops order", address="383 LAFAYETTE ST, NEW YORK", date_created=date.today())
        # self.assertEqual(str(order), f"<Order id=[{self.id}]\t name=[{self.name}]\t address=[{self.address}]\t date_created=[{self.date_created}]\t items=[{self.items}]>")
        self.assertTrue(order is not None)
        self.assertEqual(order.id, None)
        self.assertEqual(order.name, "Devops order")
        # self.assertEqual(order.user_id, 123456)
        self.assertEqual(order.address, "383 LAFAYETTE ST, NEW YORK")
        self.assertEqual(order.date_created, date.today())
    
    def test_add_a_order(self):
        """It should Create a order and add it to the database"""
        orders = Order.all()
        self.assertEqual(orders, [])
        order = Order(name="Devops order", address="383 LAFAYETTE ST, NEW YORK", date_created=date.today())
        self.assertTrue(order is not None)
        self.assertEqual(order.id, None)
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        orders = order.all()
        self.assertEqual(len(orders), 1)

    def test_read_a_order(self):
        """It should Read a Order"""
        order = OrderFactory()
        logging.debug(order)
        order.id = None
        order.create()
        self.assertIsNotNone(order.id)
        # Fetch it back
        found_order = Order.find(order.id)
        self.assertEqual(found_order.id, order.id)
        self.assertEqual(found_order.name, order.name)
        self.assertEqual(found_order.address, order.address)


######################################################################
#  I T E M   M O D E L   T E S T   C A S E S
######################################################################
class TestItemModel(unittest.TestCase):
    """ Test Cases for YourResourceModel Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Order.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Item).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_XXXX(self):
        """ It should always be true """
        self.assertTrue(True)
        