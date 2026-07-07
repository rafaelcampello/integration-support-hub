from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utc_now() -> datetime:
    """Retorna data/hora UTC com timezone para evitar ambiguidades em logs."""

    return datetime.now(timezone.utc)


class IntegrationType(str, Enum):
    REST = "REST"
    SOAP = "SOAP"


class IntegrationStatus(str, Enum):
    ACTIVE = "ativa"
    INACTIVE = "inativa"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String(40), default="support")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class Integration(Base):
    __tablename__ = "integrations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    type: Mapped[IntegrationType] = mapped_column(String(10))
    url: Mapped[str] = mapped_column(String(255))
    status: Mapped[IntegrationStatus] = mapped_column(String(20), default=IntegrationStatus.ACTIVE.value)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    failure_mode: Mapped[str | None] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    tests: Mapped[list["IntegrationTest"]] = relationship(back_populates="integration")


class IntegrationTest(Base):
    __tablename__ = "integration_tests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    integration_id: Mapped[int] = mapped_column(ForeignKey("integrations.id"))
    status_code: Mapped[int] = mapped_column()
    success: Mapped[bool] = mapped_column(Boolean, default=False)
    request_payload: Mapped[str | None] = mapped_column(Text, nullable=True)
    response_payload: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_ms: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    integration: Mapped[Integration] = relationship(back_populates="tests")


class TechnicalLog(Base):
    __tablename__ = "technical_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    level: Mapped[str] = mapped_column(String(20), index=True)
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    message: Mapped[str] = mapped_column(Text)
    integration_id: Mapped[int | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
