from typing import List
from src.domain.repositories.product_repository import ProductRepository
from src.application.dto.product_dto import ProductDTO


class ListProductsUseCase:
    def __init__(self, repo: ProductRepository):
        self._repo = repo

    def execute(self, only_active: bool = True) -> List[ProductDTO]:
        products = self._repo.find_all(only_active=only_active)
        return [
            ProductDTO(
                id=p.id,
                name=p.name,
                description=p.description,
                price=p.price,
                original_price=p.original_price,
                stock=p.stock,
                colors=p.colors,
                sizes=p.sizes,
                images=p.images,
                is_active=p.is_active,
                slug=p.slug,
                discount_percentage=p.discount_percentage(),
            )
            for p in products
        ]
