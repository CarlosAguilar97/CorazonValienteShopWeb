from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Product:
    id: Optional[int]
    name: str
    description: str
    price: float
    original_price: Optional[float]
    stock: int
    colors: List[str] = field(default_factory=list)
    sizes: List[str] = field(default_factory=list)
    images: List[str] = field(default_factory=list)
    is_active: bool = True
    slug: str = ""

    def is_available(self) -> bool:
        return self.is_active and self.stock > 0

    def discount_percentage(self) -> Optional[int]:
        if self.original_price and self.original_price > self.price:
            return round((1 - self.price / self.original_price) * 100)
        return None
