from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    """Base declarativa usada por todos os modelos SQLAlchemy."""


# check_same_thread=False permite que o TestClient do FastAPI use SQLite nos testes.
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Entrega uma sessão por requisição e garante fechamento correto."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_database() -> None:
    """Cria as tabelas quando a aplicação inicia.

    Para portfólio e estudo, isso reduz atrito. Em produção, migrations com Alembic
    seriam a escolha mais adequada.
    """

    Base.metadata.create_all(bind=engine)
