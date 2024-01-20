from app import db, ma
from datetime import datetime


class Cart(db.Model):
    __tablename__ = "user_cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class CartItemListSchema(ma.Schema):
    class Meta:
        fields = ("id", "product_id", "user_id", "quantity")
