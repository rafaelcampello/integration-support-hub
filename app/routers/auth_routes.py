import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import authenticate_user, create_access_token, get_current_user
from app.database import get_db
from app.models import User
from app.schemas import LoginRequest, TokenResponse, UserRead
from app.services.troubleshooting_service import register_event

router = APIRouter(prefix="/auth", tags=["Autenticação"])
logger = logging.getLogger(__name__)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Realizar login e obter JWT",
    description="Autentica o usuário de demonstração e retorna um Bearer Token para acessar endpoints protegidos.",
)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = authenticate_user(db, payload.username, payload.password)
    if user is None:
        register_event(db, level="warning", event_type="auth_failed", message=f"Falha de login para '{payload.username}'.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos.")

    register_event(db, level="info", event_type="auth_success", message=f"Login bem-sucedido para '{user.username}'.")
    token = create_access_token(subject=user.username, role=user.role)
    return TokenResponse(access_token=token)


@router.get(
    "/me",
    response_model=UserRead,
    summary="Consultar usuário autenticado",
    description="Endpoint simples para validar se o token JWT está funcionando.",
)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
