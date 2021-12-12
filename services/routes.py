"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_restx import Api, Resource, fields, reqparse, inputs
from . import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from services.models import Shopcart, DataValidationError, DatabaseConnectionError

# Import Flask applicationf
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return app.send_static_file("index.html")  # use GUI

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Shopcarts Demo REST API Service',
          description='This is a sample server Shopcarts server.',
          default='shopcarts',
          default_label='Shopcarts operations',
          doc='/apidocs', # default also could use doc='/apidocs/'
          prefix='/api'
         )

# Define the model so that the docs reflect what can be sent
shopcart_model = api.model('Shopcart', {
    'customer_id': fields.Integer(required=True,
                            description='The unique id for a customer or a shopcart'),
    'product_id': fields.Integer(required=True,
                          description='The unique id of the product'),
    'product_name': fields.String(required=True,
                              description='The name of the product'),
    'product_price': fields.Float(required=True,
                                description='The price of each product'),
    'quantity': fields.Integer(required=True, description='The number of products added in the shopcart')
})

# query string arguments
shopcart_args = reqparse.RequestParser()
shopcart_args.add_argument('price', type=float, required=False, help='List Products higher than the provided price')

######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST

@api.errorhandler(DatabaseConnectionError)
def database_connection_error(error):
    """ Handles Database Errors from connection attempts """
    message = str(error)
    app.logger.critical(message)
    return {
        'status_code': status.HTTP_503_SERVICE_UNAVAILABLE,
        'error': 'Service Unavailable',
        'message': message
    }, status.HTTP_503_SERVICE_UNAVAILABLE


######################################################################
#  PATH: /shopcarts/{id}
######################################################################
@api.route('/shopcarts/<customer_id>')
@api.param('customer_id', 'The Shopcart identifier')
class ShopcartResource(Resource):
    """
    ShopcartResource class
    Allows the manipulation of a single customer's shopcart
    GET /customer{id} - Returns a customer's shopcart with the id
    DELETE /customer{id} -  Deletes a customer's shopcart with the id
    """
    ######################################################################
    # READING A SHOPCART
    ######################################################################
    @api.doc('get_shopcarts')
    @api.response(404, 'Shopcart for the customer does not exist!')
    @api.marshal_with(shopcart_model)
    def get(self, customer_id):
        """
        Reads a shopcart
        """
        app.logger.info("Request to read a shopcart for customer " + customer_id)
        price_threshold = request.args.get('price')
        if price_threshold:
            shopcarts = Shopcart.find_shopcart_items_price_by_customer_id(customer_id, price_threshold)
        else:
            shopcarts = Shopcart.find_by_customer_id(customer_id).all()
        if not shopcarts:
            message = {"error": "Shopcart for the customer does not exist!"}
            return message, status.HTTP_404_NOT_FOUND

        message = [shopcart.serialize() for shopcart in shopcarts]
        return message, status.HTTP_200_OK

        
    ######################################################################
    # DELETE A SHOPCART
    ######################################################################
    @api.doc('delete_shopcart')
    @api.response(204, 'Shopcart deleted')
    def delete(self,customer_id):
        """
        Deletes a customer's shopcart
        """
        app.logger.info("Request to delete a shopcart for customer " + customer_id)
        shopcarts = Shopcart.find_by_customer_id(customer_id).all()

        message = [shopcart.serialize() for shopcart in shopcarts]
    
        for shopcart in shopcarts:
            shopcart.delete()
        
        return message, status.HTTP_204_NO_CONTENT
        

######################################################################
#  PATH: /shopcarts
######################################################################
@api.route('/shopcarts', strict_slashes=False)
class ShopcartCollection(Resource):
    """ Handles all interactions with collections of Shopcarts """
    #------------------------------------------------------------------
    # LIST ALL SHOPCARTS
    #------------------------------------------------------------------
    @api.doc('list_shopcarts')
    @api.expect(shopcart_args, validate=True)
    @api.marshal_list_with(shopcart_model)
    def get(self):
        """
        Return all of the shopcarts
        """
        app.logger.info("Request for shopcarts list")
        price_threshold = shopcart_args.parse_args().get('price')
        shopcarts=[]
        if price_threshold:
            shopcarts = Shopcart.find_shopcart_items_price(price_threshold)
        else:
            shopcarts = Shopcart.all()
        results=[shopcart.serialize() for shopcart in shopcarts]
        app.logger.info("Returning %d shopcarts", len(results))
        return results,status.HTTP_200_OK


######################################################################
#  PATH: /shopcarts/<customer_id>/products/<product_id>
######################################################################
@api.route('/shopcarts/<customer_id>/products/<product_id>', strict_slashes=False)
@api.param('customer_id', 'The Shopcart identifier')
@api.param('product_id', 'The Product identifier')
class ProductResource(Resource):
    """
    ProductResource class
    Allows the manipulation of a single customer's shopcart
    GET - Returns a customer's shopcart's product with the respective ids
    PUT - Updates the quantity for a customer's shopcart's product with the respective ids
    DELETE -  Deletes a customer's shopcart product with the respective ids
    """
    ######################################################################
    # READ A PRODUCT FROM THE SHOPCART
    ######################################################################
    @api.doc('get_product_from_shopcart')
    @api.response(404, 'Product in shopcart not found')
    @api.marshal_with(shopcart_model)
    def get(self, customer_id,product_id):
        """
        Read a product from a shopcart
        """
        app.logger.info("Request to get a product from {}'s shopcart. ".format(customer_id))
        product = Shopcart.find_by_shopcart_item(customer_id,product_id)
        if not product:
            message = {"error": "The product does not exist!"}
            return message, status.HTTP_404_NOT_FOUND
        target_product = product
        app.logger.info("Returning product with id: %s", product_id)
        return target_product.serialize(), status.HTTP_200_OK

    ######################################################################
    # UPDATE A SHOPCART 
    ######################################################################
    @api.doc('update_product_in_shopcart')
    @api.response(404, 'Product not found')
    @api.response(400, 'The posted shopcart data was not valid')
    @api.expect(shopcart_model)
    @api.marshal_with(shopcart_model)
    def put(self, customer_id, product_id):
        """
        Update the quantity of an item in a Shopcart
        This endpoint will update a Shopcart based the body that is posted
        """
        app.logger.info("Request to update Shopcart for costomer_id: %s", customer_id)
        check_content_type("application/json")
        shopcart = Shopcart.find_by_shopcart_item(customer_id, product_id)
        if not shopcart:
            raise NotFound("ShopCart item for customer_id '{}' was not found.".format(customer_id))
        logging.debug(shopcart)
        shopcart.deserialize(api.payload)
        shopcart.update()
        app.logger.info("Shopcart with custoemr_id [%s] updated.", shopcart.customer_id)
        return shopcart.serialize(), status.HTTP_200_OK

    ######################################################################
    # DELETE A PRODUCT FROM THE SHOPCART
    ######################################################################
    @api.doc('delete_product_in_shopcart')
    @api.response(204, 'Product deleted')
    def delete(self, customer_id, product_id):
        """
        Delete a product from a shopcart
        """
        app.logger.info("Request to delete a product from {}'s shopcart. ".format(customer_id))
        product = Shopcart.find_by_shopcart_item(customer_id,product_id)
        if product:
            product.delete()

        app.logger.info("Product with id {} in {}'s shopcart delete completely".format(product_id,customer_id))
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /shopcarts/<customer_id>/products/
######################################################################
@api.route('/shopcarts/<customer_id>/products/', strict_slashes=False)
@api.param('customer_id', 'The Shopcart identifier')
class ProductCollection(Resource):
    """ Handles all interactions with collections of Products """

    ######################################################################
    # ADD A PRODUCT
    ######################################################################
    @api.doc('add_product_in_shopcart')
    @api.response(400, 'The posted data was not valid')
    @api.expect(shopcart_model)
    @api.marshal_with(shopcart_model, code=201)
    def post(self, customer_id):
            """
            Add a product into the shopcart
            """
            app.logger.info("Request to add a product into the shopcart")
            check_content_type("application/json")
            shopcart = Shopcart()
            shopcart.deserialize(api.payload)
            product = shopcart.find_by_shopcart_item(customer_id,shopcart.product_id)
            if product:
                message = {"error": "Product already exist!"}
                return message,status.HTTP_400_BAD_REQUEST
            shopcart.create()
            message = shopcart.serialize()
            app.logger.info("Product with id [%s] added in to the customer: [%s]'s shopcart.",shopcart.product_id, shopcart.customer_id)

            return message, status.HTTP_201_CREATED


######################################################################
#  PATH: /shopcarts/{id}/checkout
######################################################################
@api.route('/shopcarts/<customer_id>/checkout')
@api.param('customer_id', 'The Shopcart identifier')
class CheckoutResource(Resource):
    ######################################################################
    # ACTION: CUSTOMER CHECKOUT
    ######################################################################
    @api.doc('checkout_customer')
    @api.response(404, 'Customer not found')
    def put(self, customer_id):
        """
        Checkout a customer
        """
        app.logger.info("Request to create a checkout event for customer {0}.".format(customer_id))
        shopcarts = Shopcart.find_by_customer_id(customer_id).all()
        
        if not shopcarts:
            abort(status.HTTP_404_NOT_FOUND, 'Shopcart with id [{}] was not found.'.format(customer_id))
       
        message = [shopcart.serialize() for shopcart in shopcarts]
        
        for shopcart in shopcarts:
            shopcart.delete()
        return message, status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Shopcart.init_db(app)

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )
