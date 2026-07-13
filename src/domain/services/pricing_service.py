from typing import List
from src.domain.entities.cart_item import CartItem
from src.domain.value_objects.money import Money


class PricingService:
    """Calcula totales y aplica descuentos sobre el carrito."""

    def calculate_total(self, items: List[CartItem]) -> Money:
        total = sum(item.subtotal for item in items)
        return Money(round(total, 2))

    def apply_discount(self, total: Money, percent: float) -> Money:
        if not (0 < percent < 100):
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        discount = total.amount * (percent / 100)
        return Money(round(total.amount - discount, 2))
