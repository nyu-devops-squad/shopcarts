"""
Test cases for YourResourceModel Model

"""
import logging
import unittest
import os
from services.models import Shopcart, DataValidationError, db
from tests.factories import ShopcartFactory
from services import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  S H O P C A R T   M O D E L   T E S T   C A S E S
######################################################################
class TestShopcart(unittest.TestCase):
    """ Test Cases for Shopcart Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Shopcart.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        # db.session.close()
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_shopcart(self):
        """ Test create shopcart """
        fake_shopcart = ShopcartFactory()
        shopcart = Shopcart(
            customer_id = fake_shopcart.customer_id,
            product_id = fake_shopcart.product_id,
            quantity = fake_shopcart.quantity
            )
        self.assertTrue(shopcart != None)
        self.assertEqual(shopcart.id, None)
        self.assertEqual(shopcart.customer_id, fake_shopcart.customer_id)
        self.assertEqual(shopcart.product_id, fake_shopcart.product_id)
        self.assertEqual(shopcart.quantity, fake_shopcart.quantity)
        # self.assertTrue(True)

    def test_update_a_shopcart(self):
        """Update a Shopcart"""
        shopcart = ShopcartFactory()
        logging.debug(shopcart)
        shopcart.create()
        logging.debug(shopcart)
        self.assertEqual(shopcart.id, 1)
        # Change it an save it
        shopcart.quantity=3
        original_id = shopcart.id
        shopcart.update()
        self.assertEqual(shopcart.id, original_id)
        self.assertEqual(shopcart.quantity, 3)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)
        self.assertEqual(shopcarts[0].id, 1)
        self.assertEqual(shopcart.quantity, 3)

    def test_delete_shopcart(self):
        fake_shopcart = ShopcartFactory()
        logging.debug(fake_shopcart)
        fake_shopcart.create()
        logging.debug(fake_shopcart)
        self.assertEqual(len(fake_shopcart.all()), 1)
        # delete the shopcart and make sure it isn't in the database
        fake_shopcart.delete()
        self.assertEqual(len(fake_shopcart.all()), 0)

    def test_serialize_shopcart(self):
        """ Test serialization of a Shopcart """
        shopcart = ShopcartFactory()
        data = shopcart.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], shopcart.id)
        self.assertIn("customer_id", data)
        self.assertEqual(data["customer_id"], shopcart.customer_id)
        self.assertIn("product_id", data)
        self.assertEqual(data["product_id"], shopcart.product_id)
        self.assertIn("quantity", data)
        self.assertEqual(data["quantity"], shopcart.quantity)

    def test_deserialize_shopcart(self):
        """ Test deserialization of a Shopcart """
        data = {
            "id": 1,
            "customer_id": 123,
            "product_id": 321,
            "quantity": 2
        }
        shopcart = Shopcart()
        shopcart.deserialize(data)
        self.assertNotEqual(shopcart, None)
        self.assertEqual(shopcart.id, data['id'])
        self.assertEqual(shopcart.customer_id, 123)
        self.assertEqual(shopcart.product_id, 321)
        self.assertEqual(shopcart.quantity, 2)



