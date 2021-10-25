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
from services import status  # HTTP Status Codes
from services.models import db
from services.routes import app, init_db
from .factories import ShopcartFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)
BASE_URL = "/shopcarts"

######################################################################
#  T E S T   C A S E S
######################################################################
class TestShopcartServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()


    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_shopcart(self, count):
        """Factory method to create shopcart"""
        shopcarts = []
        for _ in range(count):
            test_shopcart = ShopcartFactory()
            resp = self.app.post(BASE_URL, json=test_shopcart.serialize(), content_type="application/json")
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test shopcart"
            )
            new_shopcart = resp.get_json()
            test_shopcart.id = new_shopcart["id"]
            shopcarts.append(test_shopcart)
        return shopcarts


    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    
    def test_create_shopcart(self):
        """Create a new Shopcart"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(BASE_URL, json=test_shopcart.serialize(), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["customer_id"], test_shopcart.customer_id, "customer_id does not match")
        self.assertEqual(new_shopcart["product_id"], test_shopcart.product_id, "product_id does not match")
        self.assertEqual(new_shopcart["quantity"],test_shopcart.quantity, "quantity does not match")
        # Check that the location header was correct
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(
            new_shopcart["customer_id"], 
            test_shopcart.customer_id, "customer_id does not match"
        )
        self.assertEqual(
            new_shopcart["product_id"], 
            test_shopcart.product_id, "product_id does not match"
        )
        self.assertEqual(
            new_shopcart["quantity"],
            test_shopcart.quantity, "quantity does not match"
        )

    def test_update_shopcart(self):
        """Update an existing Shopcart"""
        # create a shopcart to update
        test_shopcart = ShopcartFactory()
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)        
        # update the shopcart
        new_shopcart = resp.get_json()
        logging.debug(new_shopcart)
        new_shopcart["quantity"] = 3
        resp = self.app.put(
            "{0}/{1}/{2}".format(BASE_URL, new_shopcart["customer_id"], new_shopcart["product_id"]),
            json=new_shopcart,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_shopcart = resp.get_json()
        self.assertEqual(updated_shopcart["quantity"], 3)

    def test_list_shopcarts(self):
        self._create_shopcart(5)
        repr = self.app.get(BASE_URL)
        self.assertEqual(repr.status_code, status.HTTP_200_OK)
        data = repr.get_json()
        self.assertEqual(len(data),5)

    def test_read_shopcart(self):
        """Read an existing shopcart"""
        test_shopcart = self._create_shopcart(1)[0]
        resp = self.app.get("{0}/{1}".format(BASE_URL, test_shopcart.customer_id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data[0]["product_id"], test_shopcart.product_id)

    def test_delete_shopcart(self):
        """Delete an existing shopcart"""
        test_shopcart = ShopcartFactory()
        resp = self.app.post(
            BASE_URL, json=test_shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        new_shopcart = resp.get_json()
        logging.debug(new_shopcart)

        resp = self.app.delete(
            "{0}/{1}".format(BASE_URL, new_shopcart["customer_id"]), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(resp.data), 0)

        # make sure they are deleted
        resp = self.app.get(
            "{0}/{1}".format(BASE_URL, test_shopcart.customer_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
