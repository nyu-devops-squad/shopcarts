"""
Models for shopcart

All of the models are stored in this module

Models
------
Shopcart
Attributes:
-----------
id - (integer) auto increment
product_id - (TBD) from the product API
customer_id - (TBD) from the customer API
quantity - (integer) quantity of the items
"""

import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Shopcart(db.Model):
    """
    Class that represents a shopcart
    """
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return "<shopcart id=[%s]>" % (self.id)

    def create(self):
        """
        Creates a shopcart to the database
        """
        logger.info("Creating %s", self.id)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a shopcart to the database
        """
        logger.info("Saving %s", self.customer_id)
        if not self.customer_id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes a shopcart from the data store """
        logger.info("Deleting %s", self.id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a shopcart into a dictionary """
        return {
            "id": self.id,
            "product_id": self.product_id,
            "customer_id": self.customer_id,
            "quantity":self.quantity
        }


    def deserialize(self, data):
        """
        Deserializes a shopcart from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.id = data["id"]
            self.product_id = data["product_id"]
            self.customer_id = data["customer_id"]
            self.quantity = data["quantity"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid shopcart: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid shopcart: body of request contained bad or no data"
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
        """ Returns all of the shopcarts in the database """
        logger.info("Processing all shopcarts")
        return cls.query.all()

    @classmethod
    def find_by_id(cls, by_id):
        """ Finds a shopcart by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_customer_id(cls, customer_id):
        """Returns the shopcart with the given customer_id
        Args:
            customer_id (Integer): the customer_id that the shopcart matches
        """
        logger.info("Processing name query for %s ...", customer_id)
        return cls.query.filter(cls.customer_id == customer_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a shopcart by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)
