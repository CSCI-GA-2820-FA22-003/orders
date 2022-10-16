"""
Models for YourResourceModel

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

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


class Item(db.Model):
    app = None

    # Schema
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable = False)
    quantity = db.Column(db.Integer, nullable = False, default = 1)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    status = db.Column(db.String, nullable = False)

    def __init__(self, args):
        self.id = args.get('id', None)
        self.product_id = args['product_id']
        self.price = args['price']
        self.quantity = args['quantity']
        self.order_id = args['order_id']
        self.status = args['status']

    def __repr__(self):
        return "<Item id=[%s]\t product_id=[%s]\t cost=[%s]\t quantity=[%s]\t order_id=[%s]\t status=[%s]>" % (self.id, self.product_id, self.cost, self.quantity, self.order_id, self.status)

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
    