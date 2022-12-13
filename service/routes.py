"""
My Service

The orders resource is a collection of order items where each item represents a
product id, its quantity, and its price.
We also implement a subordinate REST API to add order items to the order collection
(e.g., /orders/{id}/items) and associate the order with a customer preferably through
its customer id. A good action for the order API is to be able to cancel an order.

"""

from flask import abort, request, render_template, make_response, jsonify
from service.models import Item, Order
from service.models import db
from flask_restx import Resource, fields

# Import Flask application
from . import app, api
from .common import status  # HTTP Status Codes

create_item_model = api.model('Item', {
    'product_id': fields.Integer(required=True, description='The ID of the product'),
    'price': fields.Float(required=True, description='The price of the product'),
    'quantity': fields.Float(required=True, description='The quantity of product(s)'),
    'order_id': fields.Integer(required=True, description='The ID of the order where the product(s) in'),
    'status': fields.String(required=True, description='The status(comment) of the product')
})

item_model = api.inherit(
    'ItemModel',
    create_item_model,
    {'id': fields.Integer(readOnly=True, description='The unique id assigned internally by service'), }
)

# Define the model so that the docs reflect what can be sent
create_model = api.model('Order', {
    'name': fields.String(required=True, description='The name of the Order'),
    'address': fields.String(
        required=True,
        description='The address of the order(e.g.: 9609 Helen Rd. Wisconsin Rapids, WI 54494).'
        ),
    'date_created': fields.Date(description='The date order created'),
    'items': fields.List(fields.Nested(item_model, description='List of items that order contains'))
})

order_model = api.inherit(
    'OrderModel',
    create_model,
    {'id': fields.Integer(readOnly=True, description='The unique id assigned internally by service'), }
)


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return render_template("index.html")


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def healthcheck():
    """Let them know our heart is still beating"""
    return make_response(jsonify(status=200, message="OK"), status.HTTP_200_OK)


@app.route("/reset")
def reset():
    """Reset the database"""
    app.logger.info("Resetting the database...")
    db.session.commit()
    db.drop_all()
    db.create_all()
    db.session.commit()
    app.logger.info("Reset succeed!")
    return make_response(jsonify(status=200, message="Reset"), status.HTTP_200_OK)


######################################################################
#  PATH: /orders
######################################################################
@api.route('/orders', strict_slashes=False)
class OrderCollection(Resource):
    """ Handles all interactions with collections of Orders """
    # ------------------------------------------------------------------
    # LIST ALL ORDERS
    # ------------------------------------------------------------------
    @api.doc('list_orders')
    @api.marshal_list_with(order_model)
    def get(self):
        """ Returns all of the Orders """
        app.logger.info('Request to list Pets...')

        orders = Order.all()

        app.logger.info('[%s] Orders returned', len(orders))
        results = [order.serialize() for order in orders]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW ORDER
    # ------------------------------------------------------------------
    @api.doc('create_orders')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(order_model, code=201)
    def post(self):
        """
        Creates a Order
        This endpoint will create an Order based the data in the body that is posted
        """
        app.logger.info('Request to Create a Order')
        check_content_type("application/json")
        order = Order()
        app.logger.debug('Payload = %s', api.payload)
        order.deserialize(api.payload)
        order.create()
        app.logger.info('Order with new id [%s] created!', order.id)
        location_url = api.url_for(OrderResource, order_id=order.id, _external=True)
        return order.serialize(), status.HTTP_201_CREATED, {'Location': location_url}


######################################################################
#  PATH: /orders/{id}
######################################################################
@api.route('/orders/<order_id>')
@api.param('order_id', 'The Order identifier')
class OrderResource(Resource):
    """
    OrderResource class
    Allows the manipulation of an single order
    GET /order/{id} - Returns an Order with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A ORDER
    # ------------------------------------------------------------------
    @api.doc('get_order')
    @api.response(404, 'Order not found')
    @api.marshal_with(order_model)
    def get(self, order_id):
        """
        Retrieve a single Order
        This endpoint will return an Order based on it's id
        """
        app.logger.info("Request to Retrieve a order with id [%s]", order_id)
        order = Order.find(order_id)
        if not order:
            abort(status.HTTP_404_NOT_FOUND, "Order with id '{}' was not found.".format(order_id))
        return order.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING ORDER
    # ------------------------------------------------------------------
    @api.doc('update_orders')
    @api.response(404, 'Order not found')
    @api.response(400, 'The posted Order data was not valid')
    @api.expect(order_model)
    @api.marshal_with(order_model)
    def put(self, order_id):
        """
        Update an order
        This endpoint will update an order based the body that is posted
        """
        app.logger.info('Request to Update an order with id [%s]', order_id)
        try:
            int(order_id)
        except ValueError:
            abort(status.HTTP_404_NOT_FOUND, "Order with id '{}' was not found.".format(order_id))

        order = Order.find(order_id)
        if not order:
            abort(status.HTTP_404_NOT_FOUND, "Order with id '{}' was not found.".format(order_id))
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        order.deserialize(data)
        order.id = order_id
        order.update()
        return order.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN ORDER
    # ------------------------------------------------------------------
    @api.doc('delete_orders')
    @api.response(204, 'Order deleted')
    @api.response(404, 'Order not found')
    def delete(self, order_id):
        """
        Delete an order
        This endpoint will delete an Order based the id specified in the path
        """
        app.logger.info('Request to Delete an order with id [%s]', order_id)
        order = Order.find(order_id)
        if order:
            items_retrieve = Item.find_by_order_id(order_id)
            if items_retrieve:
                items_retrieve.delete()
            order.delete()
            app.logger.info('Order with id [%s] was deleted', order_id)
        else:
            abort(status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found.")

        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /orders/<order_id>/items/
######################################################################
@api.route('/orders/<order_id>/items/', strict_slashes=False)
@api.param('order_id', 'The Order identifier')
class ItemCollection(Resource):
    """ Handles all interactions with collections of Items"""
    # ------------------------------------------------------------------
    # LIST ALL ITEM
    # ------------------------------------------------------------------
    @api.doc('list_items')
    @api.marshal_list_with(item_model)
    def get(self, order_id):
        """ Returns all of the Orders """
        app.logger.info("Request for all Items for Order with id: %s", order_id)
        order = Order.find(order_id)
        if not order:
            abort(status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found.")

        results = [item.serialize() for item in order.items]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW ITEM
    # ------------------------------------------------------------------
    @api.doc('create_items')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_item_model)
    @api.marshal_with(item_model, code=201)
    def post(self, order_id):
        """
        Creates an item
        This endpoint will create an Item based the data in the body that is posted
        """
        app.logger.info("Request to create an item for order")
        check_content_type("application/json")

        order = Order.find(order_id)
        if not order:
            abort(status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found.")

        data = request.get_json()

        app.logger.debug("Payload = %s", data)
        item = Item()
        item.deserialize(data)
        item.order_id = order_id
        item.create()

        location_url = api.url_for(ItemResource, item_id=item.id, order_id=order.id, _external=True)
        app.logger.info("Item for order ID [%s] created.", id)

        return item.serialize(), status.HTTP_201_CREATED, {'Location': location_url}


######################################################################
#  PATH: /orders/<order_id>/items/<item_id>
######################################################################
@api.route('/orders/<order_id>/items/<item_id>')
@api.param('order_id', 'The Order identifier')
@api.param('item_id', 'The Item identifier')
class ItemResource(Resource):
    """
    ItemResource class
    Allows the manipulation of an single order
    """

    # ------------------------------------------------------------------
    # RETRIEVE A ITEM
    # ------------------------------------------------------------------
    @api.doc('get_item')
    @api.response(404, 'Item not found')
    @api.marshal_with(item_model)
    def get(self, order_id, item_id):
        """
        Retrieve a single Order
        This endpoint will return an Order based on it's id
        """
        app.logger.info("Request for item with id [%s]", item_id)
        order = Order.find(order_id)
        if not order:
            abort(status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found.")
        app.logger.info(item_id)
        item = Item.find(item_id)
        if not item:
            abort(status.HTTP_404_NOT_FOUND, f"Item with id '{item_id}' was not found.")

        app.logger.info("Get item details successful")
        return item.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING ITEM
    # ------------------------------------------------------------------
    @api.doc('update_item')
    @api.response(404, 'Item not found')
    @api.response(400, 'The posted Item data was not valid')
    @api.expect(item_model)
    @api.marshal_with(item_model)
    def put(self, order_id, item_id):
        """
        Update an item
        This endpoint will update an item based the body that is posted
        """
        app.logger.info(
            "Request to update Order %s for Item id: %s", (item_id, order_id)
        )
        check_content_type("application/json")
        order = Order.find(order_id)
        if not order:
            abort(status.HTTP_404_NOT_FOUND, f"Item with id '{order_id}' was not found.")

        # See if the item exists and abort if it doesn't
        item = Item.find(item_id)
        if not item:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Order with id '{item_id}' could not be found.",
            )

        # Update from the json in the body of the request
        item.deserialize(api.payload)
        item.id = item_id
        item.update()

        return item.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN ITEM
    # ------------------------------------------------------------------
    @api.doc('delete_items')
    @api.response(204, 'Item deleted')
    @api.response(404, 'Order not found')
    def delete(self, order_id, item_id):
        """
        Delete an item
        This endpoint will delete an Order based the id specified in the path
        """

        app.logger.info(
            "Request to delete item with order_id [%s] and item_id [%s]", order_id, item_id)

        order = Order.find(order_id)
        if not order:
            abort(status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found.")
        item = Item.find(item_id)
        if item:
            item.delete()
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /orders_date/<date_iso>
######################################################################
@api.route('/orders_date/<date_iso>', strict_slashes=False)
@api.param('date_iso', 'The date in ISO format')
class DateQuery(Resource):
    """ Handles all interactions with dates"""
    # ------------------------------------------------------------------
    # ORDER QUERY BASED ON DATE
    # ------------------------------------------------------------------
    @api.doc('order_retrieve_based_on_date')
    @api.marshal_list_with(order_model)
    def get(self, date_iso):
        """ Returns all of the Orders """
        app.logger.info(
            "Request to retrieve Orders based on date %s", (date_iso)
        )
        # check_content_type("application/json")

        order_list = list(Order.find_by_date(date_iso))

        if not order_list:
            abort(status.HTTP_404_NOT_FOUND, f"No order was found for date '{date_iso}'")

        ret = []
        for order in order_list:
            ret.append(order.serialize())
        return ret, status.HTTP_200_OK


######################################################################
#  PATH: /orders_prices
######################################################################
@api.route('/orders_prices', strict_slashes=False)
class PriceQuery(Resource):
    """ Handles all interactions with prices"""
    # ------------------------------------------------------------------
    # LIST ALL ITEMS IN ORDER IN PRICE RANGE
    # ------------------------------------------------------------------
    @api.doc('list_all_items_prices')
    @api.marshal_list_with(order_model)
    def post(self):
        """ Returns all of the Orders """
        app.logger.info("Request for all Orders in the price range")

        data = request.get_json()
        max_price = data['max_price']
        min_price = data['min_price']

        try:
            int(max_price)
            int(min_price)
        except ValueError as e:
            abort(status.HTTP_400_BAD_REQUEST, "Invalid price: {}".format(e))

        item_list = Item.find_by_price(max_price, min_price)
        if not item_list:
            abort(status.HTTP_404_NOT_FOUND, "Items not found")

        results = [item.serialize() for item in item_list]
        list_order_id = {}
        for order_id in results:
            list_order_id.setdefault(order_id["order_id"], []).append(order_id)
        order_final = []
        for key, value in list_order_id.items():
            res = {}
            order = Order.find(key)
            res["id"] = order.id
            res["name"] = order.name
            res["address"] = order.address
            res["date_created"] = order.date_created.isoformat()
            res["items"] = value
            order_final.append(order.serialize())
        return order_final, status.HTTP_200_OK


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

    app.logger.error("Invalid Content-Type: %s",
                     request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
