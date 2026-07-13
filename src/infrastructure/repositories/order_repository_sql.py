from typing import List, Optional
from src.domain.entities.order import Order, OrderItem
from src.domain.repositories.order_repository import OrderRepository
from src.infrastructure.database.models.order_model import OrderModel, OrderItemModel
from src.main.config.database import db


def _to_entity(m: OrderModel) -> Order:
    return Order(
        id=m.id,
        name=m.name,
        address=m.address,
        notes=m.notes,
        total=float(m.total),
        voucher_url=m.voucher_url,
        status=m.status,
        created_at=m.created_at,
        items=[
            OrderItem(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product_name,
                color=item.color,
                size=item.size,
                price=float(item.price),
                quantity=item.quantity,
            )
            for item in m.items
        ],
    )


class OrderRepositorySQL(OrderRepository):

    def save(self, order: Order) -> Order:
        if order.id:
            m = OrderModel.query.get(order.id)
            if not m:
                raise ValueError(f"Pedido {order.id} no encontrado")
        else:
            m = OrderModel()
            db.session.add(m)

        m.name = order.name
        m.address = order.address
        m.notes = order.notes
        m.total = order.total
        m.voucher_url = order.voucher_url
        m.status = order.status

        if not order.id:
            db.session.flush()
            m.items = [
                OrderItemModel(
                    product_id=item.product_id,
                    product_name=item.product_name,
                    color=item.color,
                    size=item.size,
                    price=item.price,
                    quantity=item.quantity,
                )
                for item in order.items
            ]

        db.session.commit()
        db.session.refresh(m)
        return _to_entity(m)

    def find_all(self) -> List[Order]:
        orders = OrderModel.query.order_by(OrderModel.created_at.desc()).all()
        return [_to_entity(o) for o in orders]

    def find_by_id(self, order_id: int) -> Optional[Order]:
        m = OrderModel.query.get(order_id)
        return _to_entity(m) if m else None

    def delete(self, order_id: int) -> bool:
        m = OrderModel.query.get(order_id)
        if not m:
            return False
        db.session.delete(m)
        db.session.commit()
        return True
