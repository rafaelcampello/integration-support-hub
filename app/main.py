from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.database import SessionLocal, create_database
from app.logging_config import setup_logging
from app.models import User
from app.routers import auth_routes, integration_routes, log_routes
from app.services.troubleshooting_service import register_event


def seed_default_user(db: Session) -> None:
    """Cria o usuário demo para reduzir fricção na avaliação do projeto."""

    existing_user = db.query(User).filter(User.username == "admin").first()
    if existing_user is None:
        db.add(User(username="admin", password_hash=hash_password("admin123"), role="admin"))
        db.commit()
        register_event(db, level="info", event_type="seed_user", message="Usuário padrão 'admin' criado.")


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Inicialização da aplicação: logs, banco e usuário padrão."""

    setup_logging()
    create_database()
    db = SessionLocal()
    try:
        seed_default_user(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Integration Support Hub",
    description=(
        "Plataforma educacional para diagnóstico de integrações REST/SOAP com JWT, "
        "Swagger, SQLite, logs técnicos e histórico de testes."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth_routes.router)
app.include_router(integration_routes.router)
app.include_router(log_routes.router)


@app.get(
    "/health",
    tags=["Monitoramento"],
    summary="Verificar saúde da API",
    description="Endpoint público para confirmar que a aplicação está em execução.",
)
def health_check() -> dict:
    return {"status": "ok", "service": "Integration Support Hub"}
