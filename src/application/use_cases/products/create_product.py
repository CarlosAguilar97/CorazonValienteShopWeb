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
        # Validar nombre
        if not dto.name or not dto.name.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")

        # Validar precios
        if dto.price < 0:
            raise ValueError("El precio no puede ser negativo.")
        if dto.original_price is not None:
            if dto.original_price < 0:
                raise ValueError("El precio original no puede ser negativo.")
            if dto.original_price <= dto.price:
                raise ValueError("El precio original debe ser mayor que el precio de venta.")

        # Validar stock
        if dto.stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        # Verificar unicidad del slug
        slug = _slugify(dto.name)
        existing = self._repo.find_by_slug(slug)
        if existing:
            raise ValueError(f"Ya existe un producto con el nombre '{dto.name}' o similar.")

        product = Product(
            id=None,
            name=dto.name.strip(),
            description=dto.description,
            price=dto.price,
            original_price=dto.original_price,
            stock=dto.stock,
            colors=dto.colors,
            sizes=dto.sizes,
            images=dto.images,
            slug=slug,
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
