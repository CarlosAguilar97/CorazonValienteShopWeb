from dataclasses import dataclass
from typing import Optional


@dataclass
class CartItem:
    product_id: int
    product_name: str
    color: str
    size: str
    price: float
    quantity: int = 1
    image_url: Optional[str] = None

    @property
    def subtotal(self) -> float:
        return round(self.price * self.quantity, 2)
