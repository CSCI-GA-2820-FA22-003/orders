"""
My Service

Describe what your service does here
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from .common import status  # HTTP Status Codes
from service.models import Item
from service.models import Order

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )

######################################################################
# LIST ALL ORDERS
######################################################################
@app.route("/orders", methods=["GET"])
def list_orders():
    """Returns all of the Orders"""
    app.logger.info("Request for order list")
    orders = Order.all()

    results = [o.serialize() for o in orders]
    app.logger.info("Returning %d items", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# RETRIEVE AN ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["GET"])
def get_orders(order_id):
    """
    Retrieve a single order

    This endpoint will return an Order based on it's id
    """
    app.logger.info("Request for order with id: %s", order_id)
    order = Item.find(order_id)
    if not order:
        abort(status.HTTP_404_NOT_FOUND, f"Item with id '{order_id}' was not found.")

    app.logger.info("Returning item: %s", order.name)
    return jsonify(order.serialize()), status.HTTP_200_OK


######################################################################
# ADD A NEW ORDER
######################################################################
@app.route("/order", methods=["POST"])
def create_orders():
    """
    Add a new order
    This endpoint will create an order based the data in the body that is posted
    """
    app.logger.info("Request to create an order")
    check_content_type("application/json")
    order = Order()
    order.deserialize(request.get_json())
    order.create()
    message = order.serialize()
    location_url = url_for("get_orders", order_id=order.id, _external=True)

    app.logger.info("Order with ID [%s] created.", order.id)

    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}

######################################################################
# UPDATE AN EXISTING ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_orders(order_id):
    """
    Update a Order
    This endpoint will update a Order based the body that is posted
    """
    app.logger.info("Request to update order with id: %s", order_id)
    check_content_type("application/json")

    order = Order.find(order_id)
    if not order:
        abort(status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found.")

    order.deserialize(request.get_json())
    order.id = order_id
    order.update()

    app.logger.info("Order with ID [%s] updated.", order.id)
    return jsonify(order.serialize()), status.HTTP_200_OK

######################################################################
# DELETE AN ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_orders(order_id):
    """
    Delete an Order
    This endpoint will delete an Order based the id specified in the path
    """
    app.logger.info("Request to delete pet with id: %s", order_id)
    pet = Order.find(order_id)
    if pet:
        pet.delete()

    app.logger.info("Pet with ID [%s] delete complete.", order_id)
    return "", status.HTTP_204_NO_CONTENT


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Item.init_db(app)
    Order.init_db(app)

def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )