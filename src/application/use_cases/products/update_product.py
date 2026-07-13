from src.domain.repositories.product_repository import ProductRepository
from src.application.dto.product_dto import ProductDTO


class UpdateProductUseCase:
    def __init__(self, repo: ProductRepository):
        self._repo = repo

    def execute(self, product_id: int, data: dict) -> ProductDTO:
        product = self._repo.find_by_id(product_id)
        if not product:
            raise ValueError(f"Producto {product_id} no encontrado")

        product.name        = data.get("name", product.name)
        product.description = data.get("description", product.description)
        product.price       = float(data.get("price", product.price))
        product.original_price = float(data["original_price"]) if data.get("original_price") else product.original_price
        product.stock       = int(data.get("stock", product.stock))
        product.colors      = data.get("colors", product.colors)
        product.sizes       = data.get("sizes", product.sizes)
        product.images      = data.get("images", product.images)
        product.is_active   = data.get("is_active", product.is_active)

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
