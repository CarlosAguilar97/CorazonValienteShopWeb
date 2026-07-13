from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Inicia sesión para acceder al panel."


def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from src.infrastructure.database.models import product_model, user_model  # noqa

    # Cargar usuario para Flask-Login
    from src.infrastructure.database.models.user_model import UserModel

    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(int(user_id))

    return db
