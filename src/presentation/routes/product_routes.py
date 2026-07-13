from flask import Blueprint
from src.presentation.controllers.product_controller import (
    get_products,
    get_product,
    create_product,
    delete_product,
)

product_bp = Blueprint("products", __name__, url_prefix="/api/products")

product_bp.route("/", methods=["GET"])(get_products)
product_bp.route("/<int:product_id>", methods=["GET"])(get_product)
product_bp.route("/", methods=["POST"])(create_product)
product_bp.route("/<int:product_id>", methods=["DELETE"])(delete_product)
