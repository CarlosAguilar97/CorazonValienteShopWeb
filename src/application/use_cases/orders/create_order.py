from typing import List
from src.domain.entities.order import Order, OrderItem
from src.domain.repositories.order_repository import OrderRepository


class CreateOrderUseCase:

    def __init__(self, repo: OrderRepository):
        self._repo = repo

    def execute(
        self,
        name: str,
        address: str,
        notes: str,
        total: float,
        voucher_url: str,
        items_data: List[dict],
    ) -> Order:
        order_items = [
            OrderItem(
                id=None,
                product_id=item["product_id"],
                product_name=item["product_name"],
                color=item.get("color"),
                size=item.get("size"),
                price=float(item["price"]),
                quantity=int(item["quantity"]),
            )
            for item in items_data
        ]

        order = Order(
            id=None,
            name=name,
            address=address,
            notes=notes,
            total=total,
            voucher_url=voucher_url,
            items=order_items,
        )

        return self._repo.save(order)
