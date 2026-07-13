from flask import Blueprint
from src.presentation.controllers.admin_controller import (
    dashboard,
    product_new_get,
    product_new_post,
    product_edit_get,
    product_edit_post,
    product_delete,
    order_update_status,
)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

admin_bp.route("/",                              methods=["GET"])(dashboard)
admin_bp.route("/products/new",                  methods=["GET"])(product_new_get)
admin_bp.route("/products/new",                  methods=["POST"])(product_new_post)
admin_bp.route("/products/<int:product_id>/edit", methods=["GET"])(product_edit_get)
admin_bp.route("/products/<int:product_id>/edit", methods=["POST"])(product_edit_post)
admin_bp.route("/products/<int:product_id>/delete", methods=["POST"])(product_delete)
admin_bp.route("/orders/<int:order_id>/status",  methods=["POST"])(order_update_status)
