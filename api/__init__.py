from flask import Blueprint
from flask_restx import Api
from api.product import product_api
from api.cart import cart_api
from api.order import order_api


blueprint = Blueprint("api", "e-commerce task api")
api = Api(blueprint, title="Apis", version="1.0", description="Api")

api.add_namespace(product_api)
api.add_namespace(cart_api)
api.add_namespace(order_api)
