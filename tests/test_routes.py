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
from services.models import db,DataValidationError
from services.routes import app, init_db
from .factories import ShopcartFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)
BASE_URL = "/api/shopcarts"

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
        duplicate = set()
        for _ in range(count):
            test_shopcart = ShopcartFactory()
            key = str(test_shopcart.customer_id)+"_"+str(test_shopcart.product_id)
            if key not in duplicate:
                duplicate.add(key)
                resp = self.app.post(
                    "{0}/{1}/products/".format(BASE_URL, test_shopcart.customer_id), 
                    json=test_shopcart.serialize(), content_type="application/json")
                self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test shopcart"
                )
                shopcarts.append(test_shopcart)

        return shopcarts


    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    
    def test_add_product(self):
        """Add a new Product"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post("{0}/{1}/products/".format(BASE_URL, test_shopcart.customer_id), 
                            json=test_shopcart.serialize(), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)   

        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["customer_id"], test_shopcart.customer_id, "customer_id does not match")
        self.assertEqual(new_shopcart["product_id"], test_shopcart.product_id, "product_id does not match")
        self.assertEqual(new_shopcart["product_name"], test_shopcart.product_name, "product_name does not match")
        self.assertEqual(new_shopcart["product_price"], test_shopcart.product_price, "product_price does not match")
        self.assertEqual(new_shopcart["quantity"],test_shopcart.quantity, "quantity does not match")

        self.assertEqual(
            new_shopcart["customer_id"], 
            test_shopcart.customer_id, "customer_id does not match"
        )
        self.assertEqual(
            new_shopcart["product_id"], 
            test_shopcart.product_id, "product_id does not match"
        )
        self.assertEqual(
            new_shopcart["product_name"], 
            test_shopcart.product_name, "product_name does not match"
        )
        self.assertEqual(
            new_shopcart["product_price"], 
            test_shopcart.product_price, "product_price does not match"
        )
        self.assertEqual(
            new_shopcart["quantity"],
            test_shopcart.quantity, "quantity does not match"
        )

    def test_add_same_product(self):
        """Add a new Product that already exists in the shopcart"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post("{0}/{1}/products/".format(BASE_URL, test_shopcart.customer_id), 
                            json=test_shopcart.serialize(), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        resp = self.app.post("{0}/{1}/products/".format(BASE_URL, test_shopcart.customer_id), 
                            json=test_shopcart.serialize(), content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_shopcart(self):
        """Update an existing Shopcart"""
        # create a shopcart to update
        test_shopcart = ShopcartFactory()
        resp = self.app.post(
            "{0}/{1}/products/".format(BASE_URL, test_shopcart.customer_id),
            json=test_shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)        
        # update the shopcart
        new_shopcart = resp.get_json()
        logging.debug(new_shopcart)
        new_shopcart["quantity"] = 3
        resp = self.app.put(
            "{0}/{1}/products/{2}".format(BASE_URL, new_shopcart["customer_id"],new_shopcart["product_id"]),
            json=new_shopcart,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_shopcart = resp.get_json()
        self.assertEqual(updated_shopcart["quantity"], 3)

    def test_list_shopcarts(self):
        created_data = self._create_shopcart(5)
        resp = self.app.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(created_data))

    def test_read_shopcart(self):
        """Read an existing shopcart"""
        test_shopcart = self._create_shopcart(1)[0]
        resp = self.app.get("{0}/{1}".format(BASE_URL, test_shopcart.customer_id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data[0]["product_id"], test_shopcart.product_id)

    def test_read_product(self):
        """Read a product form a shopcart"""
        test_shopcart = self._create_shopcart(1)[0]
        resp = self.app.get("{}/{}/products/{}".format(BASE_URL, test_shopcart.customer_id,test_shopcart.product_id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["quantity"], test_shopcart.quantity)

    def test_read_nonexist_product(self):
        """Read a product form a shopcart that not exist"""
        test_shopcart = ShopcartFactory()
        resp = self.app.post(
            "{0}/{1}/products/".format(BASE_URL, test_shopcart.customer_id), json=test_shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        new_shopcart = resp.get_json()
        logging.debug(new_shopcart)

        resp = self.app.get("{}/{}/products/{}".format(BASE_URL, new_shopcart["customer_id"],new_shopcart["product_id"]+1))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_product(self):
        """Delete a Product"""
        test_shopcart = ShopcartFactory()
        resp = self.app.post(
            "{0}/{1}/products/".format(BASE_URL, test_shopcart.customer_id), 
            json=test_shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        new_shopcart = resp.get_json()
        logging.debug(new_shopcart)

        resp = self.app.delete(
            "{0}/{1}/products/{2}".format(BASE_URL, test_shopcart.customer_id,test_shopcart.product_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "{0}/{1}/products/{2}".format(BASE_URL, test_shopcart.customer_id,test_shopcart.product_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_shopcart(self):
        """Delete an existing shopcart"""
        test_shopcart = ShopcartFactory()
        resp = self.app.post(
            "{0}/{1}/products/".format(BASE_URL, test_shopcart.customer_id), 
            json=test_shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        new_shopcart = resp.get_json()
        logging.debug(new_shopcart)

        resp = self.app.delete(
            "{0}/{1}".format(BASE_URL, new_shopcart["customer_id"]), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)

        # make sure they are deleted
        resp = self.app.get(
            "{0}/{1}".format(BASE_URL, test_shopcart.customer_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
   
    def test_create_shopcart_no_content_type(self):
        """ Create a shopcart item with no content type """
        test_shopcart = ShopcartFactory()
        resp = self.app.post("{0}/{1}/products/".format(BASE_URL, test_shopcart.customer_id))
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_get_shopcart_not_found(self):
        """Get a Shopcart thats not found"""
        resp = self.app.get("{}/0".format(BASE_URL))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_allowed(self):
        """ Test method not allowed """
        resp = self.app.put(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('services.routes.Shopcart.find_by_customer_id')
    def test_bad_request(self, bad_request_mock):
        """ Test a Bad Request error from Find By customer_id """
        bad_request_mock.side_effect = DataValidationError()
        resp = self.app.get("{}/1000".format(BASE_URL))
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_shopcart_by_price_by_customer_id(self):
        """Read an existing shopcart with items above a price threshold for a customer"""
        test_shopcart = self._create_shopcart(15)
        test_customer_id = test_shopcart[0].customer_id
        products = []
        for shopcart_items in test_shopcart:
            if shopcart_items.customer_id == test_customer_id and shopcart_items.product_price >= 100:
                products.append(shopcart_items)

        resp = self.app.get("{0}/{1}?price={2}".format(BASE_URL, test_customer_id, 100))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(products))
    
    def test_read_shopcart_by_price(self):
        """Read an existing shopcart with items above a price threshold"""
        test_shopcart = self._create_shopcart(15)
        products = []
        for shopcart_items in test_shopcart:
            if shopcart_items.product_price >= 100:
                products.append(shopcart_items)

        resp = self.app.get("{0}?price={1}".format(BASE_URL, 100))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(products))

    def test_checkout_customer(self):
        """Checkout customer"""

        test_shopcart = ShopcartFactory()
        resp = self.app.post(
            "{0}/{1}/products/".format(BASE_URL, test_shopcart.customer_id), 
            json=test_shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        new_shopcart = resp.get_json()
        logging.debug(new_shopcart)

        resp = self.app.put(
            "{0}/{1}/checkout".format(BASE_URL, new_shopcart["customer_id"]), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(resp.data), 0)

        # make sure they are deleted
        resp = self.app.get(
            "{0}/{1}".format(BASE_URL, test_shopcart.customer_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
