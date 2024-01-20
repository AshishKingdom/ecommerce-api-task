from app import db, ma
from datetime import datetime
from marshmallow import fields


class UserOrdertem(db.Model):
    __tablename__ = "order_item"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer)


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    status = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    items = db.relationship(UserOrdertem, backref="order", lazy=True)


class OrderDetailItemSchema(ma.Schema):
    class Meta:
        model = UserOrdertem
        include_fk = True
        fields = ("id", "order_id", "product_id", "quantity")


class OrderDetailSchema(ma.Schema):
    class Meta:
        model = Order
        fields = ("id", "items")

    items = fields.Nested(OrderDetailItemSchema, many=True)
