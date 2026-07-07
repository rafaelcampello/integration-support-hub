from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import TechnicalLog, User
from app.schemas import TechnicalLogRead

router = APIRouter(prefix="/logs", tags=["Logs técnicos"])


@router.get(
    "",
    response_model=list[TechnicalLogRead],
    summary="Consultar logs técnicos",
    description="Lista eventos importantes salvos no banco para apoiar troubleshooting de autenticação e integrações.",
)
def list_logs(
    level: str | None = Query(None, description="Filtra por INFO, WARNING ou ERROR."),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[TechnicalLog]:
    query = db.query(TechnicalLog)
    if level:
        query = query.filter(TechnicalLog.level == level.upper())
    return query.order_by(TechnicalLog.created_at.desc()).limit(limit).all()
