"""
Test cases for Order and Item Model

"""
from itertools import product
import os
import logging
import unittest
from service.models import Order, Item, db, DataValidationError
from service import app
from datetime import date
from tests.factories import OrderFactory, ItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  O r d e r   M O D E L   T E S T   C A S E S
######################################################################
class TestOrderModel(unittest.TestCase):
    """ Test Cases for Order Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        db.drop_all()
        Order.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Order).delete()  # clean up the last tests
        db.session.query(Item).delete()  # clean up the last tests
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

    def test_update_a_order(self):
        """It should Update a Order"""
        order = OrderFactory()
        logging.debug(order)
        order.id = None
        order.create()
        logging.debug(order)
        self.assertIsNotNone(order.id)
        # Change it an save it
        order.address = "Tandon Brooklyn downtown"
        original_id = order.id
        order.update()
        self.assertEqual(order.id, original_id)
        self.assertEqual(order.address, "Tandon Brooklyn downtown")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        orders = Order.all()
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].id, original_id)
        self.assertEqual(order.address, "Tandon Brooklyn downtown")

    def test_delete_a_order(self):
        """It should Delete a order"""
        order = OrderFactory()
        order.create()
        self.assertEqual(len(Order.all()), 1)
        # delete the order and make sure it isn't in the database
        order.delete()
        self.assertEqual(len(Order.all()), 0)

    def test_list_all_orders(self):
        """It should List all orders in the database"""
        orders = Order.all()
        self.assertEqual(orders, [])
        # Create 5 orders
        for _ in range(5):
            order = OrderFactory()
            order.create()
        # See if we get back 5 orders
        orders = order.all()
        self.assertEqual(len(orders), 5)

    def test_serialize_a_order(self):
        """It should serialize a order"""
        order = OrderFactory()
        data = order.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], order.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], order.name)
        self.assertIn("address", data)
        self.assertEqual(data["address"], order.address)
        self.assertIn("date_created", data)
        self.assertEqual(date.fromisoformat(data["date_created"]), order.date_created)

    def test_deserialize_a_order(self):
        """It should de-serialize a order"""
        data = OrderFactory().serialize()
        order = Order()
        order.deserialize(data)
        self.assertNotEqual(order, None)
        self.assertEqual(order.id, None)
        self.assertEqual(order.name, data["name"])
        self.assertEqual(order.address, data["address"])
        self.assertEqual(order.date_created, date.fromisoformat(data["date_created"]))

    def test_deserialize_no_address(self):
        """It should not deserialize a order with no address"""
        data = {"name":"ZeQian"}
        order = Order()
        self.assertRaises(DataValidationError, order.deserialize, data)

    def test_deserialize_with_wrong_data_type(self):
        """It should not deserialize a order with wrong data type"""
        data = ["ZeQian"]
        order = Order()
        self.assertRaises(DataValidationError, order.deserialize, data)

    def test_find_order_by_id(self):
        """It should Find a order by ID"""
        orders = OrderFactory.create_batch(5)
        for order in orders:
            order.create()
        logging.debug(orders)
        # make sure they got saved
        self.assertEqual(len(Order.all()), 5)
        # find the 2nd order in the list
        order = Order.find(orders[1].id)
        self.assertIsNot(order, None)
        self.assertEqual(order.id, orders[1].id)
        self.assertEqual(order.name, orders[1].name)
        self.assertEqual(order.address, orders[1].address)
        self.assertEqual(order.date_created, orders[1].date_created)

    def test_find_order_by_name(self):
        """It should Find a order by name"""
        order1 = OrderFactory()
        order1.name = "ZeQian"
        order1.create()
        order2 = OrderFactory()
        order2.name = "ZeQian"
        order2.create()
        order_list = list(Order.find_by_name(order1.name))
        self.assertEqual(len(order_list), 2)
        # self.assertEqual(order1.address, order_list[])


######################################################################
#  I T E M   M O D E L   T E S T   C A S E S
######################################################################
class TestItemModel(unittest.TestCase):
    """ Test Cases for Item Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        db.drop_all()
        Order.init_db(app)
        Item.init_db(app)

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

    def test_deserialize_a_item(self):
        """It should de-serialize a item"""
        data = ItemFactory().serialize()
        item = Item()
        item.deserialize(data)
        self.assertNotEqual(item, None)
        self.assertEqual(item.product_id, data["product_id"])

    def test_deserialize_a_item_no_product_id(self):
        """It should not de-serialize a item with no product_id """
        data = ItemFactory().serialize()
        del data["product_id"]
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, data)

    # def test_deserialize_with_wrong_data_type(self):
    #     """It should not deserialize a item with wrong data type"""
    #     data = ["ZeQian"]
    #     item = Item()
    #     self.assertRaises(DataValidationError, item.deserialize, data)

    def test_add_order_item(self):
        """It should Create an order with an item and add it to the database"""
        # Make new order & item, bind item to the order
        order = OrderFactory()
        order.create()

        item = ItemFactory(order_id=order.id)
        item.create()

        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

        # Retrieve the item from order
        item_retrieve = Item.find_by_order_id(order.id)
        self.assertEqual(item_retrieve.count(), 1)

    def test_update_order_item(self):
        """It should Update an order's item"""
        len_orders_old = len(Order.all())

        order = OrderFactory()
        order.create()

        item = ItemFactory(order_id=order.id)
        item.create()

        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders) - len_orders_old, 1)

        # Fetch it back
        i = list(Item.find_by_order_id(order.id))[0]
        print("%r", i)
        self.assertEqual(i.price, item.price)
        # Change the price
        i.price = "10.75"
        order.update()

        # Fetch it back again
        i = list(Item.find_by_order_id(order.id))[0]
        self.assertEqual(i.price, 10.75)

    def test_delete_order_item(self):
        """It should Delete an order's item"""
        len_orders_old = len(Order.all())

        order = OrderFactory()
        order.create()
        item = ItemFactory(order_id=order.id)
        item.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders) - len_orders_old, 1)

        # Fetch it back
        item = list(Item.find_by_order_id(order.id))[0]
        item.delete()

        # Check whether has been deleted
        items = Item.find_by_order_id(order.id)
        self.assertEqual(items.count(), 0)

    def test_find_item_by_product_id(self):
        """It should Find orders by product id"""
        len_orders_old = len(Order.all())
        len_items_old = len(Item.all())
        order1 = OrderFactory()
        order1.create()
        order2 = OrderFactory()
        order2.create()
        item1 = ItemFactory(order_id=order1.id, product_id=12345)
        item1.create()
        item2 = ItemFactory(order_id=order2.id, product_id=12345)
        item2.create()
        # logging.debug(item1)
        # make sure they got saved
        self.assertEqual(len(Order.all()), 2+len_orders_old)
        self.assertEqual(len(Item.all()), 2+len_items_old)
        # find the 2nd order in the list
        item_list = Item.find_by_product_id(item1.product_id)
        self.assertEqual(len(list(item_list)), 2)

    def test_find_item_by_price_max_min(self):
        """It should Find items in orders within the price range"""
        order1 = OrderFactory()
        order1.create()
        order2 = OrderFactory()
        order2.create()
        item1 = ItemFactory(order_id=order1.id, product_id=12345, price=3.75)
        item1.create()
        item2 = ItemFactory(order_id=order2.id, product_id=2345, price=4.50)
        item2.create()
        item3 = ItemFactory(order_id=order2.id, product_id=54345, price=8.75)
        item3.create()
        item_list = Item.find_by_price(5, 3)
        self.assertEqual(len(list(item_list)), 2)
