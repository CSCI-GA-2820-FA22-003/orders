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
        return "<Item id=[%s]\t product_id=[%s]\t cost=[%s]\t quantity=[%s]\t order_id=[%s]\t status=[%s]>" % (self.id, self.product_id, self.cost, self.quantity, self.order_id, self.status)

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
        return {"id": self.id, "product_id": self.product_id, "price": self.price, 'quantity': self.quantity, 'order': self.order_id}

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
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Item: body of request contained bad or no data - "
                "Error message: " + error
            )

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

    @classmethod
    def find_by_name(cls, name):
        """Returns all Item with the given name

        Args:
            name (string): the name of the Item you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)


class Order(db.Model):

    app = None

    # Order Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    address = db.Column(db.String(63), default="Invalid Address")
    date_created = db.Column(db.Date(), nullable=False, default=date.today())
    items = db.relationship("Item", backref="order", passive_deletes=True)

    def __repr__(self):
        return "<Order id=[%s]\t name=[%s]\t address=[%s]\t date_created=[%s]\t items=[%s]>" % (self.id, self.name, self.address, self.date_created, self.items)

    def create(self):
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        order = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "date_created": self.date_created.isoformat(),
            "items": [],
        }
        for item in self.items:
            order["items"].append(item.serialize())
        return order

    def deserialize(self, data):
        try:
            self.name = data["name"]
            self.address = data["address"]
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
        logger.info("Initializing database")
        cls.app = app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  

    @classmethod
    def all(cls):
        logger.info("Processing all YourResourceModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

