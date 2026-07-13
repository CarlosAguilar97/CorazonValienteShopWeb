import re
from typing import List, Optional
from src.domain.entities.product import Product
from src.domain.repositories.product_repository import ProductRepository
from src.infrastructure.database.models.product_model import ProductModel
from src.main.config.database import db


def _to_entity(m: ProductModel) -> Product:
    return Product(
        id=m.id,
        name=m.name,
        description=m.description or "",
        price=float(m.price),
        original_price=float(m.original_price) if m.original_price else None,
        stock=m.stock,
        colors=m.colors,
        sizes=m.sizes,
        images=m.images,
        is_active=m.is_active,
        slug=m.slug,
    )


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text


class ProductRepositorySQL(ProductRepository):

    def find_all(self, only_active: bool = True) -> List[Product]:
        q = ProductModel.query
        if only_active:
            q = q.filter_by(is_active=True)
        return [_to_entity(m) for m in q.all()]

    def find_by_id(self, product_id: int) -> Optional[Product]:
        m = ProductModel.query.get(product_id)
        return _to_entity(m) if m else None

    def find_by_slug(self, slug: str) -> Optional[Product]:
        m = ProductModel.query.filter_by(slug=slug).first()
        return _to_entity(m) if m else None

    def save(self, product: Product) -> Product:
        if product.id:
            m = ProductModel.query.get(product.id)
            if not m:
                raise ValueError(f"Producto {product.id} no encontrado")
        else:
            m = ProductModel()
            db.session.add(m)

        m.name = product.name
        m.slug = product.slug or _slugify(product.name)
        m.description = product.description
        m.price = product.price
        m.original_price = product.original_price
        m.stock = product.stock
        m.colors = product.colors
        m.sizes = product.sizes
        m.images = product.images
        m.is_active = product.is_active

        db.session.commit()
        db.session.refresh(m)
        return _to_entity(m)

    def delete(self, product_id: int) -> bool:
        m = ProductModel.query.get(product_id)
        if not m:
            return False
        db.session.delete(m)
        db.session.commit()
        return True
