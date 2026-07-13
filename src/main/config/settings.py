import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Flask
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_key")
    FLASK_ENV: str = os.getenv("FLASK_ENV", "development")
    DEBUG: bool = os.getenv("FLASK_DEBUG", "1") == "1"

    # MySQL — SQLAlchemy URI
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "corazon_valiente")
    MYSQL_SSL_CA: str = os.getenv("MYSQL_SSL_CA", "")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        direct_url = os.getenv("DATABASE_URL")
        if direct_url:
            if direct_url.startswith("mysql://"):
                direct_url = direct_url.replace("mysql://", "mysql+pymysql://", 1)
            
            # Limpiar parámetros incompatibles (como ssl-mode) de la URL
            import urllib.parse
            parsed = urllib.parse.urlparse(direct_url)
            query_params = urllib.parse.parse_qs(parsed.query)
            query_params.pop("ssl-mode", None)
            query_params.pop("ssl_mode", None)
            new_query = urllib.parse.urlencode(query_params, doseq=True)
            parsed = parsed._replace(query=new_query)
            return urllib.parse.urlunparse(parsed)

        import urllib.parse
        encoded_password = urllib.parse.quote_plus(self.MYSQL_PASSWORD)
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{encoded_password}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False

    # WhatsApp
    WHATSAPP_PHONE: str = os.getenv("WHATSAPP_PHONE", "51999999999")

    # Cloudinary
    CLOUDINARY_URL: str = os.getenv("CLOUDINARY_URL", "")

    # Servidor
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "5000"))

    def __init__(self):
        # Block default insecure SECRET_KEY in production
        if self.FLASK_ENV == "production" and self.SECRET_KEY in ["dev_secret_key", "", None]:
            raise ValueError(
                "ERROR CRÍTICO DE SEGURIDAD: La variable de entorno 'SECRET_KEY' "
                "debe estar configurada con una clave secreta fuerte y aleatoria en producción."
            )


settings = Settings()
