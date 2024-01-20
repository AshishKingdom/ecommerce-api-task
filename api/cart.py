from flask_restx import Resource, Namespace
from flask import request, jsonify
from app import db
from models.product import Product
from models.cart import Cart, CartItemListSchema

cart_api = Namespace("cart")


@cart_api.route("")
class AddItemToCart(Resource):
    def post(self):
        data = request.get_json()
        try:
            user_id = data["user_id"]
            product_id = data["product_id"]
            quantity = data["quantity"]

            product = Product.query.get(product_id)
            if not product:
                response = jsonify({"message": "No product with given id found"})
                response.status_code = 404
                return response
            if product.quantity < data["quantity"]:
                response = jsonify(
                    {"message": "Not enough quantity for the given product ID"}
                )
                response.status_code = 400
                return response

            existing_cart_item = Cart.query.filter_by(
                user_id=user_id, product_id=product_id
            ).first()
            if existing_cart_item:
                existing_cart_item.quantity += quantity
                product.quantity -= quantity
                db.session.commit()
                response = jsonify({"message": "Cart item updated successfully"})
                response.status_code = 200
                return response
            else:
                new_cart_item = Cart(
                    user_id=user_id, product_id=product_id, quantity=quantity
                )
                db.session.add(new_cart_item)
                product.quantity -= quantity
                db.session.commit()
                response = jsonify({"message": "cart item created successfully"})
                response.status_code = 201
                return response

        except KeyError:
            response = jsonify(
                {
                    "message": "Invalid data. Please provide user_id, product_id, and quantity"
                }
            )
            response.status_code = 400
            return response
        except Exception as e:
            response = jsonify({"message": "Error : " + str(e)})
            response.status_code = 400
            return response


@cart_api.route("/<int:user_id>")
class GetUserItems(Resource):
    def get(self, user_id):
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        if cart_items:
            cart_items_data = CartItemListSchema(many=True).dump(cart_items)
            response = jsonify(cart_items_data)
            response.status_code = 200
            return response
        else:
            response = jsonify({"message": "No cart items found for the given user id"})
            response.status_code = 404
            return response


@cart_api.route("/<int:user_id>/<int:product_id>")
class CRUDItems(Resource):
    def delete(self, user_id, product_id):
        product = Product.query.get(product_id)
        if not product:
            response = jsonify({"message": "No product with given id found"})
            response.status_code = 404
            return response

        cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item:
            product.quantity += cart_item.quantity
            db.session.delete(cart_item)
            db.session.commit()
            response = jsonify({"message": "Cart item deleted successfully"})
            response.status_code = 200
            return response
        else:
            response = jsonify(
                {"message": "No cart item with given user and product id found"}
            )
            response.status_code = 404
            return response

    def put(self, user_id, product_id):
        data = request.get_json()
        product = Product.query.get(product_id)
        if not product:
            response = jsonify({"message": "No product with given id found"})
            response.status_code = 404
            return response

        cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item:
            if data["quantity"] > cart_item.quantity:
                if product.quantity < data["quantity"] - cart_item.quantity:
                    response = jsonify({"message": "Not enough stock of product ID"})
                    response.status_code = 404
                    return response
                product.quantity -= data["quantity"] - cart_item.quantity
            else:
                product.quantity += cart_item.quantity - data["quantity"]

            cart_item.quantity = data["quantity"]
            db.session.commit()
            response = jsonify({"message": "Cart item updated successfully"})
            response.status_code = 200
            return response
        else:
            response = jsonify(
                {"message": "No cart item with given user and product id found"}
            )
            response.status_code = 404
            return response

    def get(self, user_id, product_id):
        data = (
            Cart.query.join(Product, Product.id == Cart.product_id)
            .with_entities(
                Cart.id,
                Cart.product_id,
                Cart.user_id,
                Cart.quantity,
                Product.name,
                Product.description,
                Product.price_per_item,
            )
            .filter(Cart.user_id == user_id, Cart.product_id == product_id)
            .first()
        )
        if data:
            cart_item_data = {
                "id": data[0],
                "product_id": data[1],
                "user_id": data[2],
                "quantity": data[3],
                "product_name": data[4],
                "product_desc": data[5],
                "price_per_item": data[6],
            }
            response = jsonify(cart_item_data)
            response.status_code = 200
            return response
        else:
            response = jsonify(
                {"message": "No cart item with given user and product id found"}
            )
            response.status_code = 404
            return response
