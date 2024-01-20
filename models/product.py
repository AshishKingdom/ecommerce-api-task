from app import db, ma
from datetime import datetime


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    price_per_item = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class ProductListSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "price_per_item", "quantity")
