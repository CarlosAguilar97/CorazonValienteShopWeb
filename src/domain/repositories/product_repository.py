from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.product import Product


class ProductRepository(ABC):

    @abstractmethod
    def find_all(self, only_active: bool = True) -> List[Product]:
        ...

    @abstractmethod
    def find_by_id(self, product_id: int) -> Optional[Product]:
        ...

    @abstractmethod
    def find_by_slug(self, slug: str) -> Optional[Product]:
        ...

    @abstractmethod
    def save(self, product: Product) -> Product:
        ...

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        ...
