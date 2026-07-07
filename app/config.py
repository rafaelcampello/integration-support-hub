import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Centraliza configurações para facilitar testes e manutenção.

    Em um projeto real, estes valores viriam de um gerenciador de segredos.
    Aqui usamos variáveis de ambiente com defaults seguros apenas para estudo.
    """

    secret_key: str = os.getenv("SECRET_KEY", "change-this-secret-key-with-at-least-32-bytes")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./integration_support.db")


settings = Settings()
