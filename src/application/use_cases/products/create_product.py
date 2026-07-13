import re
from src.domain.entities.product import Product
from src.domain.repositories.product_repository import ProductRepository
from src.application.dto.product_dto import CreateProductDTO, ProductDTO


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text


class CreateProductUseCase:
    def __init__(self, repo: ProductRepository):
        self._repo = repo

    def execute(self, dto: CreateProductDTO) -> ProductDTO:
        product = Product(
            id=None,
            name=dto.name,
            description=dto.description,
            price=dto.price,
            original_price=dto.original_price,
            stock=dto.stock,
            colors=dto.colors,
            sizes=dto.sizes,
            images=dto.images,
            slug=_slugify(dto.name),
        )
        saved = self._repo.save(product)
        return ProductDTO(
            id=saved.id,
            name=saved.name,
            description=saved.description,
            price=saved.price,
            original_price=saved.original_price,
            stock=saved.stock,
            colors=saved.colors,
            sizes=saved.sizes,
            images=saved.images,
            is_active=saved.is_active,
            slug=saved.slug,
            discount_percentage=saved.discount_percentage(),
        )
