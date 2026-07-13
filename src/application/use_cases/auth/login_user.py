from src.infrastructure.database.models.user_model import UserModel


class LoginUserUseCase:
    def execute(self, email: str, password: str):
        """
        Retorna el UserModel si las credenciales son válidas, None si no.
        """
        user = UserModel.query.filter_by(email=email.lower().strip()).first()
        if not user or not user.check_password(password):
            return None
        if not user.is_active:
            return None
        return user
