from flask_restx import Resource, Namespace
from logger import logger
from flask import request, jsonify
from app import db
from models.product import Product, ProductListSchema
from sqlalchemy import cast, desc, asc, String


product_api = Namespace("product")


@product_api.route("/")
class ProductList(Resource):
    def get(self):
        # parsing request query url
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)

        search = request.args.get("search", None, type=str)
        search = eval(search) if search else {}

        sort = request.args.get("sort", None, type=str)
        sort = eval(sort) if sort else {}

        # get the products
        try:
            product_list = Product.query.with_entities(
                Product.id,
                Product.name,
                Product.description,
                Product.price_per_item,
                Product.quantity,
            )
            label_mapping = {
                "id": cast(Product.id, String),
                "name": Product.name,
                "description": Product.description,
                "price_per_item": Product.price_per_item,
                "quantity": Product.quantity,
            }
            # searching
            for search_param, search_value in search.items():
                if search_param in ["id", "name", "description"]:
                    product_list = product_list.filter(
                        label_mapping[search_param].ilike(f"%{search_value}%")
                    )
            label_mapping["id"] = Product.id
            # sorting
            for sort_param, sort_order in sort.items():
                if sort_param in label_mapping.keys():
                    if sort_order == "asc":
                        product_list = product_list.order_by(
                            asc(label_mapping[sort_param])
                        )
                    elif sort_order == "desc":
                        product_list = product_list.order_by(
                            desc(label_mapping[sort_param])
                        )
            product_count = product_list.count()
            product_list = product_list.paginate(page=page, per_page=limit)
        except Exception as e:
            logger.error(f"Exception during product_list query: {str(e)}")
            response = jsonify({"message": "No products found"})
            response.status_code = 404
            return response

        if not product_list or len(product_list.items) == 0:
            response = jsonify({"message": "No products found"})
            response.status_code = 404
            return response

        # return the products
        product_list = ProductListSchema().dump(product_list.items, many=True)
        response = jsonify(
            {
                "page": page,
                "limit": limit,
                "count": product_count,
                "products": product_list,
            }
        )
        response.status_code = 200
        return response

    def post(self):
        data = request.get_json()
        try:
            product = Product(
                name=data["name"],
                description=data["description"],
                quantity=data["quantity"],
                price_per_item=data["price_per_item"],
            )
            db.session.add(product)
            db.session.commit()
            response = jsonify({"message": "product created"})
            response.status_code = 201
            return response
        except Exception as e:
            response = jsonify({"message": f"Error : " + str(e)})
            response.status_code = 400
            return response


@product_api.route("/<int:product_id>/")
class ProductItem(Resource):
    def get(self, product_id: int):
        product = (
            Product.query.with_entities(
                Product.id,
                Product.name,
                Product.description,
                Product.price_per_item,
                Product.quantity,
            )
            .filter(Product.id == product_id)
            .all()
        )
        if product:
            product = ProductListSchema().dump(product[0])
            respose = jsonify(product)
            respose.status_code = 200
            return respose
        else:
            response = jsonify({"message": "No product with given id found"})
            response.status_code = 404
            return response

    def delete(self, product_id: int):
        product = Product.query.filter(Product.id == product_id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            response = jsonify({"message": "Product deleted successfully"})
            response.status_code = 200
            return response
        else:
            response = jsonify({"message": "No product with given id found"})
            response.status_code = 404
            return response

    def put(self, product_id: int):
        product = Product.query.filter(Product.id == product_id).first()
        if product:
            # Assuming you have a ProductSchema for incoming data
            data = request.get_json()
            try:
                product = Product.query.filter(Product.id == product_id).first()

                product.name = data["name"]
                product.description = data["description"]
                product.price_per_item = data["price_per_item"]
                product.quantity = data["quantity"]

                db.session.commit()

                response = jsonify({"message": f"product with ID {product_id} updated"})
                response.status_code = 200
                return response
            except Exception as e:
                response = jsonify({"message": "error : " + str(e)})
                response.status_code = 400
                return response
        else:
            response = jsonify({"message": "No product with given id found"})
            response.status_code = 404
            return response
