import logging

from sqlalchemy.orm import Session

from app.models import TechnicalLog

logger = logging.getLogger(__name__)


def register_event(
    db: Session,
    *,
    level: str,
    event_type: str,
    message: str,
    integration_id: int | None = None,
) -> TechnicalLog:
    """Registra eventos em arquivo e banco.

    Manter os dois registros ajuda a demonstrar uma rotina real de investigação:
    logs em arquivo dão contexto técnico, enquanto a tabela facilita filtros via API.
    """

    level_upper = level.upper()
    getattr(logger, level.lower(), logger.info)("%s | integration_id=%s", message, integration_id)
    event = TechnicalLog(
        level=level_upper,
        event_type=event_type,
        message=message,
        integration_id=integration_id,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
