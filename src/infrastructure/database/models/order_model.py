from datetime import datetime
from src.main.config.database import db


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    voucher_url = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), default="Pendiente")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación uno a muchos
    items = db.relationship("OrderItemModel", backref="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order {self.id} - {self.name}>"


class OrderItemModel(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(100), nullable=True)
    size = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<OrderItem {self.id} - {self.product_name}>"
