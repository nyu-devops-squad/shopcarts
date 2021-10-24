"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from services.models import Shopcart, DataValidationError

# Import Flask application
from . import app


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


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """

    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Shopcarts REST API Service",
            version="1.0",
            # paths=url_for("list_shopcarts", _external=True),
        ),
        status.HTTP_200_OK,
    )

######################################################################
# CREATE A NEW SHOPCART
######################################################################
@app.route("/shopcart", methods=["POST"])
def create_shopcart():
    """
    Creates a shopcart
    """
    app.logger.info("Request to create a shopcart")
    check_content_type("application/json")
    shopcart = Shopcart()
    shopcart.deserialize(request.get_json())

    shopcart.create()
    message = shopcart.serialize()
    location_url = url_for("create_shopcart", id=shopcart.id, _external=True)
    app.logger.info("Shorpcart for customer ID [%s] created.", shopcart.customer_id)

    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# READING A SHOPCART
######################################################################
@app.route("/shopcart/<customer_id>", methods=["GET"])
def read_shopcart(customer_id):
    """
    Reads a shopcart
    """
    app.logger.info("Request to read a shopcart for customer " + customer_id)
    shopcart = Shopcart.find_by_customer_id(customer_id).first()
    message = shopcart.serialize()
    location_url = url_for("read_shopcart", id=shopcart.id, customer_id=shopcart.customer_id, _external=True)
    
    return make_response(
        jsonify(message), status.HTTP_200_OK, {"Location": location_url}
    )

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Shopcart.init_db(app)

    
    
