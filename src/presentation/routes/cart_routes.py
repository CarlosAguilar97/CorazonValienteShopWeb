from flask import Blueprint
from src.presentation.controllers.cart_controller import (
    get_cart, add_item, remove_item, clear_cart, checkout
)

cart_bp = Blueprint("cart", __name__, url_prefix="/api/cart")

cart_bp.route("/",                   methods=["GET"])(get_cart)
cart_bp.route("/add",                methods=["POST"])(add_item)
cart_bp.route("/remove/<int:index>", methods=["DELETE"])(remove_item)
cart_bp.route("/clear",              methods=["DELETE"])(clear_cart)
cart_bp.route("/checkout",           methods=["POST"])(checkout)
