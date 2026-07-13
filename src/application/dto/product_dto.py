from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ProductDTO:
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
    discount_percentage: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "original_price": self.original_price,
            "stock": self.stock,
            "colors": self.colors,
            "sizes": self.sizes,
            "images": self.images,
            "is_active": self.is_active,
            "slug": self.slug,
            "discount_percentage": self.discount_percentage,
        }


@dataclass
class CreateProductDTO:
    name: str
    description: str
    price: float
    stock: int
    original_price: Optional[float] = None
    colors: List[str] = field(default_factory=list)
    sizes: List[str] = field(default_factory=list)
    images: List[str] = field(default_factory=list)
