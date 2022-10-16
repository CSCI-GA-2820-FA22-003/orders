"""
Models for YourResourceModel

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy
from datetime import date

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass


class YourResourceModel(db.Model):
    """
    Class that represents a YourResourceModel
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))

    def __repr__(self):
        return "<YourResourceModel %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a YourResourceModel to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a YourResourceModel to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a YourResourceModel from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a YourResourceModel into a dictionary """
        return {"id": self.id, "name": self.name}

    def deserialize(self, data):
        """
        Deserializes a YourResourceModel from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid YourResourceModel: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid YourResourceModel: body of request contained bad or no data - "
                "Error message: " + error
            )
        return self


#  ORDER DB MODEL

class Order(db.Model):

    app = None

    # Order Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    address = db.Column(db.String(63), db.ForeignKey('customer.address'))
    date_created = db.Column(db.Date(), nullable=False, default=date.today())
    items = db.relationship("Item", backref="order", passive_deletes=True)

    def __repr__(self):
        return "<Order id=[%s]\t name=[%s]\t customer_id=[%s]\t address=[%s]\t date_created=[%s]\t items=[%s]>" % (self.id, self.name, self.customer_id, self.address, self.date_created, self.items)

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
            "customer_id": self.customer_id,
            "address": self.address,
            "date_created": self.date_joined.isoformat(),
            "items": [],
        }
        for item in self.items:
            order["items"].append(item.serialize())
        return order

    def deserialize(self, data):
        try:
            self.name = data["name"]
            self.customer_id = data["customer_id"]
            self.address = data.get("address")
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
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the YourResourceModels in the database """
        logger.info("Processing all YourResourceModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a YourResourceModel by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all YourResourceModels with the given name

        Args:
            name (string): the name of the YourResourceModels you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

