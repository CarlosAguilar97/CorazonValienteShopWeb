from src.domain.repositories.product_repository import ProductRepository
from src.application.dto.product_dto import ProductDTO


class UpdateProductUseCase:
    def __init__(self, repo: ProductRepository):
        self._repo = repo

    def execute(self, product_id: int, data: dict) -> ProductDTO:
        import re
        def _slugify(text: str) -> str:
            text = text.lower().strip()
            text = re.sub(r"[^\w\s-]", "", text)
            text = re.sub(r"[\s_-]+", "-", text)
            return text

        product = self._repo.find_by_id(product_id)
        if not product:
            raise ValueError(f"Producto {product_id} no encontrado")

        new_name = data.get("name", product.name)
        if not new_name or not new_name.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        new_name = new_name.strip()

        # Validar precios
        new_price = float(data.get("price", product.price))
        if new_price < 0:
            raise ValueError("El precio no puede ser negativo.")

        raw_original = data.get("original_price")
        new_original_price = None
        if raw_original is not None and str(raw_original).strip() != "":
            new_original_price = float(raw_original)
            if new_original_price < 0:
                raise ValueError("El precio original no puede ser negativo.")
            if new_original_price <= new_price:
                raise ValueError("El precio original debe ser mayor que el precio de venta.")

        # Validar stock
        new_stock = int(data.get("stock", product.stock))
        if new_stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        # Verificar unicidad del slug excluyendo este producto
        new_slug = _slugify(new_name)
        existing = self._repo.find_by_slug(new_slug)
        if existing and existing.id != product_id:
            raise ValueError(f"Ya existe un producto con el nombre '{new_name}' o similar.")

        product.name = new_name
        product.slug = new_slug
        product.description = data.get("description", product.description)
        product.price = new_price
        product.original_price = new_original_price
        product.stock = new_stock
        product.colors = data.get("colors", product.colors)
        product.sizes = data.get("sizes", product.sizes)
        product.images = data.get("images", product.images)
        product.is_active = data.get("is_active", product.is_active)

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
