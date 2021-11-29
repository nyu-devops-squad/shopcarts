"""
Models for shopcart

All of the models are stored in this module

Models
------
Shopcart
Attributes:
-----------
product_id - (TBD) from the product API
customer_id - (TBD) from the customer API
product_name - (TBD) from the product API
product_price - (TBD) from the product API
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
    customer_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(64), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return "<customer id=[%s]>,<product id=[%s]>" % (self.customer_id,self.product_id)

    def create(self):
        """
        Creates a shopcart to the database
        """
        logger.info("Creating customer_id: %s, product_id：%s", self.customer_id,self.product_id)
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
        logger.info("Deleting %s,%s", self.customer_id,self.product_id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a shopcart into a dictionary """
        return {
            "product_id": self.product_id,
            "customer_id": self.customer_id,
            "product_name": self.product_name,
            "product_price": self.product_price,
            "quantity":self.quantity
        }


    def deserialize(self, data):
        """
        Deserializes a shopcart from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.product_id = data["product_id"]
            self.customer_id = data["customer_id"]
            self.product_price = data["product_price"]
            self.quantity = data["quantity"]

            if isinstance(data["product_name"], str):
                self.product_name = data["product_name"]
            else:
                raise DataValidationError("Invalid type for string [product_name]: " + type(data["product_name"]))

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
    def find_by_customer_id(cls, customer_id):
        """Returns the shopcart with the given customer_id
        Args:
            customer_id (Integer): the customer_id that the shopcart matches
        """
        logger.info("Processing query for customer %s ...", customer_id)
        return cls.query.filter(cls.customer_id == customer_id)

    @classmethod
    def find_shopcart_items_price(cls, customer_id, price_threshold):
        """Returns the shopcart with the given customer_id
        Args:
            customer_id (Integer): the customer_id that the shopcart matches
        """
        logger.info("Processing query for customer %s ...", customer_id)
        return cls.query.filter(cls.customer_id == customer_id, cls.product_price >= price_threshold)

    # @classmethod
    # def find_or_404(cls, customer_id,product_id):
    #     """ Find a shopcart by it's compound key """
    #     logger.info("Processing lookup or 404 for customer %s with product %s ...", customer_id,product_id)
    #     return cls.query.get_or_404((customer_id,product_id))

    @classmethod
    def find_by_shopcart_item(cls, customer_id, product_id):
        """Returns the shopcart record with the given costomer_id and product_id

        Args:
            customer_id (Integer)
            product_id (Integer)
        """
        logger.info("Processing query for customer_id: %s ... and product_id: %s", customer_id, product_id)
        return cls.query.get((customer_id, product_id))

