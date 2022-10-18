"""
Models for YourResourceModel

All of the models are stored in this module
"""
from datetime import date
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Item(db.Model):
    """
    Class that represents a Item belongs to an order with a specific product

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    app = None

    # Schema
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable = False)
    quantity = db.Column(db.Integer, nullable = False, default = 1)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    status = db.Column(db.String, nullable = False)

    # Remark: Remove constructor according to consistent implementation with:
    #         https://github.com/nyu-devops/lab-flask-tdd/blob/master/service/models.py
    #         Since it is redundant with serialize method

    def __repr__(self):
        return f"<Item id=[{self.id}]\t product_id=[{self.product_id}]\t price=[{self.price}]\t quantity=[{self.quantity}]\t order_id=[{self.order_id}]\t status=[{self.status}]>"

    def create(self):
        """
        Creates an Item to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates an Item to the database
        """
        logger.info("Saving %s", self.id)
        db.session.commit()

    def delete(self):
        """ Removes an Item from the data store """
        logger.info("Deleting %s", self.id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Item into a dictionary """
        return {"id": self.id, "product_id": self.product_id, "price": self.price, 'quantity': self.quantity, 'order_id': self.order_id}

    def deserialize(self, data):
        """
        Deserializes a YourResourceModel from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.id = data["id"]
            self.product_id = data['product_id']
            self.price = data['price']
            self.quantity = data['quantity']
        except KeyError as error:
            raise DataValidationError(
                "Invalid Item: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Item: body of request contained bad or no data - "
                "Error message: " + error
            ) from error

        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing Item database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Item in the database """
        logger.info("Processing all ItemsModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Item by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    # @classmethod
    # def find_by_name(cls, name):
    #     """Returns all Item with the given name

    #     Args:
    #         name (string): the name of the Item you want to match
    #     """
    #     logger.info("Processing name query for %s ...", name)
    #     return cls.query.filter(cls.name == name)


class Order(db.Model):
    '''
    Class that represent an order contains multiple Items.

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    '''

    app = None

    # Order Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    # user_id = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(63), default="Invalid Address")
    date_created = db.Column(db.Date(), nullable=False, default=date.today())

    def __repr__(self):
        return f"<Order id=[{self.id}]\t name=[{self.name}]\t address=[{self.address}]\t date_created=[{self.date_created}]]>"

    def create(self):
        """
        create an Order to database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        update an Order to database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """
        Removes an Order from the data store
        """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """
        Serializes an Order into a dictionary
        """
        order = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "date_created": self.date_created.isoformat(),
        }
        return order

    def deserialize(self, data):
        """
        Deserializes a Order from a dictionary
        Args:
            data (dict): A dictionary containing the Order data
        """
        try:
            self.name = data["name"]
            self.address = data["address"]
            if "date_created" in data.keys():
                self.date_created = date.fromisoformat(data["date_created"])
            order_list = data.get("items")
            for json_item in order_list:
                item = Item() #Item db-model
                item.deserialize(json_item)
                self.items.append(item)
        except KeyError as error:
            raise DataValidationError("Invalid order: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid order: body of request contained "
                "bad or no data - " + error.args[0]
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session

        :param app: the Flask app
        :type data: Flask

        """
        logger.info("Initializing database")
        cls.app = app
        db.init_app(app)
        app.app_context().push()
        db.create_all()

    @classmethod
    def all(cls):
        """
        Returns all of the Orders in the database
        """
        logger.info("Processing all orders")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Order by it's ID

        :param order_id: the id of the Order to find
        :type order_id: int

        :return: an instance with the order_id, or None if not found
        :rtype: Pet
        """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Orders with the given name

        :param name: the name of the Pets you want to match
        :type name: str

        :return: a collection of Orders with that name
        :rtype: list

        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
