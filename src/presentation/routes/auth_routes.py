from flask import Blueprint
from src.presentation.controllers.auth_controller import login_get, login_post, logout

auth_bp = Blueprint("auth", __name__, url_prefix="/admin")

# El endpoint debe llamarse "login" para que Flask-Login lo resuelva con login_view = "auth.login"
auth_bp.add_url_rule("/login",  endpoint="login", view_func=login_get,  methods=["GET"])
auth_bp.add_url_rule("/login",  endpoint="login_post", view_func=login_post, methods=["POST"])
auth_bp.add_url_rule("/logout", endpoint="logout", view_func=logout,    methods=["GET"])
