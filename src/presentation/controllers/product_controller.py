from flask import jsonify, request, abort
from src.application.use_cases.products.list_products import ListProductsUseCase
from src.application.dto.product_dto import CreateProductDTO
from src.domain.entities.product import Product
from src.infrastructure.repositories.product_repository_sql import ProductRepositorySQL


def _repo():
    return ProductRepositorySQL()


def get_products():
    use_case = ListProductsUseCase(_repo())
    products = use_case.execute()
    return jsonify([p.to_dict() for p in products]), 200


def get_product(product_id: int):
    product = _repo().find_by_id(product_id)
    if not product:
        abort(404, description="Producto no encontrado")
    return jsonify(Product(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        original_price=product.original_price,
        stock=product.stock,
        colors=product.colors,
        sizes=product.sizes,
        images=product.images,
        is_active=product.is_active,
        slug=product.slug,
    ).__dict__), 200


def create_product():
    data = request.get_json()
    dto = CreateProductDTO(
        name=data["name"],
        description=data.get("description", ""),
        price=float(data["price"]),
        stock=int(data.get("stock", 0)),
        original_price=float(data["original_price"]) if data.get("original_price") else None,
        colors=data.get("colors", []),
        sizes=data.get("sizes", ["S", "M", "L", "XL"]),
        images=data.get("images", []),
    )
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
    )
    saved = _repo().save(product)
    return jsonify(saved.__dict__), 201


def delete_product(product_id: int):
    deleted = _repo().delete(product_id)
    if not deleted:
        abort(404, description="Producto no encontrado")
    return jsonify({"message": "Producto eliminado"}), 200
