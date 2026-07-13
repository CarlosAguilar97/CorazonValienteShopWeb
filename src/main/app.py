import sys
import os
import click

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from flask import Flask, render_template
from flask_cors import CORS

from src.main.config.settings import settings
from src.main.config.database import init_db, db
from src.main.config.logger import logger

from src.presentation.routes.product_routes import product_bp
from src.presentation.routes.cart_routes import cart_bp
from src.presentation.routes.auth_routes import auth_bp
from src.presentation.routes.admin_routes import admin_bp
from src.presentation.middlewares.error_handler import register_error_handlers

# Import database models to ensure SQLAlchemy registers them for db.create_all()
from src.infrastructure.database.models.order_model import OrderModel, OrderItemModel
from src.infrastructure.database.models.product_model import ProductModel
from src.infrastructure.database.models.user_model import UserModel


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "../presentation/views"),
        static_folder=os.path.join(os.path.dirname(__file__), "../presentation/static"),
    )

    # ── Config ────────────────────────────────────────────────
    app.secret_key = settings.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"]        = settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ── Extensiones ───────────────────────────────────────────
    CORS(app)
    init_db(app)

    # ── Blueprints ────────────────────────────────────────────
    app.register_blueprint(product_bp)   # /api/products
    app.register_blueprint(cart_bp)      # /api/cart
    app.register_blueprint(auth_bp)      # /admin/login  /admin/logout
    app.register_blueprint(admin_bp)     # /admin/

    # ── Errores ───────────────────────────────────────────────
    register_error_handlers(app)

    # ── CSRF Protection ───────────────────────────────────────
    import secrets
    from flask import session, request, abort

    @app.before_request
    def manage_csrf():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_hex(32)

    @app.context_processor
    def inject_csrf():
        return dict(csrf_token=session.get("csrf_token", ""))

    @app.before_request
    def validate_csrf():
        # Validate CSRF for all modifying requests under /admin/
        if request.path.startswith("/admin/") and request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            token = request.form.get("csrf_token") or request.headers.get("X-CSRF-Token")
            if not token or token != session.get("csrf_token"):
                abort(400, description="Token CSRF inválido o ausente.")

    # ── Ruta pública ──────────────────────────────────────────
    @app.route("/")
    def index():
        return render_template("index.html")

    # ── Crear tablas ──────────────────────────────────────────
    with app.app_context():
        db.create_all()
        logger.info("Base de datos lista ✓")

    # ── Comando CLI: crear usuario admin ──────────────────────
    @app.cli.command("create-admin")
    @click.option("--email",    prompt="Email")
    @click.option("--name",     prompt="Nombre")
    @click.option("--password", prompt="Contraseña", hide_input=True, confirmation_prompt=True)
    def create_admin(email, name, password):
        """Crea un usuario administrador."""
        from src.infrastructure.database.models.user_model import UserModel
        existing = UserModel.query.filter_by(email=email.lower()).first()
        if existing:
            click.echo("⚠️  Ya existe un usuario con ese email.")
            return
        user = UserModel(email=email.lower(), name=name, role="admin")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"✅ Admin creado: {email}")

    return app

app = create_app()

if __name__ == "__main__":
    logger.info(f"🚀 http://{settings.APP_HOST}:{settings.APP_PORT}")
    app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.DEBUG)
