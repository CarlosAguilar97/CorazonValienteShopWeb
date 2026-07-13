import json
from datetime import datetime
from src.main.config.database import db


class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text, default="")
    price = db.Column(db.Numeric(10, 2), nullable=False)
    original_price = db.Column(db.Numeric(10, 2), nullable=True)
    stock = db.Column(db.Integer, default=0)
    # Almacenados como JSON string: '["Negro","Hueso"]'
    colors_json = db.Column(db.Text, default="[]")
    sizes_json = db.Column(db.Text, default='["S","M","L","XL"]')
    images_json = db.Column(db.Text, default="[]")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def colors(self):
        return json.loads(self.colors_json or "[]")

    @colors.setter
    def colors(self, value):
        self.colors_json = json.dumps(value)

    @property
    def sizes(self):
        return json.loads(self.sizes_json or "[]")

    @sizes.setter
    def sizes(self, value):
        self.sizes_json = json.dumps(value)

    @property
    def images(self):
        return json.loads(self.images_json or "[]")

    @images.setter
    def images(self, value):
        self.images_json = json.dumps(value)

    def __repr__(self):
        return f"<Product {self.name}>"
