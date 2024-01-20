from flask_restx import Resource, Namespace
from flask import request, jsonify
from app import db
from models.cart import Cart
from models.order import Order, UserOrdertem, OrderDetailSchema

order_api = Namespace("order")


@order_api.route("")
class CreateOrder(Resource):
    def post(self):
        data = request.get_json()

        user_id = data["user_id"]
        new_order = Order(status="shipping")
        db.session.add(new_order)
        for product_id in data["product_ids"]:
            item = Cart.query.filter(
                Cart.user_id == user_id, Cart.product_id == product_id
            ).first()
            if not item:
                response = jsonify({"message": "product ID not found in user cart"})
                response.status_code = 404
                return response
            new_order_item = UserOrdertem(
                order_id=new_order.id,
                user_id=user_id,
                product_id=item.product_id,
                quantity=item.quantity,
            )
            db.session.add(new_order_item)
            db.session.delete(item)

        db.session.commit()

        response = jsonify({"order_id": new_order.id, "status": new_order.status})
        response.status_code = 201
        return response

    def get(self):
        user_id = request.args.get("user_id", None, int)

        if not user_id:
            response = jsonify({"message": "user ID not passed"})
            response.status_code = 400
            return response

        user_orders = Order.query.filter(Order.user_id == user_id).all()
        count = len(user_orders)
        user_orders = OrderDetailSchema(many=True).dump(user_orders)

        response = jsonify({"count": count, "order": user_orders})
        response.status_code = 200
        return response


@order_api.route("/<int:order_id>")
class GetOrderDetail(Resource):
    def get(self, order_id: int):
        data = Order.query.get(order_id)

        if not data:
            response = jsonify({"message": "order ID not found"})
            response.status_code = 404
            return response

        order = OrderDetailSchema().dump(data)
        response = jsonify({"user_id": data.user_id, "order": order})
        response.status_code = 200
        return response
