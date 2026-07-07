from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str = Field(..., examples=["admin"])
    password: str = Field(..., examples=["admin123"])


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str


class IntegrationCreate(BaseModel):
    name: str = Field(..., min_length=3, examples=["Consulta de cliente"])
    type: Literal["REST", "SOAP"] = Field(..., examples=["REST"])
    url: HttpUrl = Field(..., examples=["https://api.exemplo.local/clientes"])
    status: Literal["ativa", "inativa"] = "ativa"
    description: str | None = Field(None, examples=["Integração usada para demonstrar troubleshooting."])
    failure_mode: Literal["bad_request", "forbidden", "server_error", "timeout"] | None = Field(
        None,
        description="Cenário controlado para simular incidentes durante o teste.",
    )


class IntegrationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    url: str
    status: str
    description: str | None
    failure_mode: str | None
    created_at: datetime


class IntegrationTestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    integration_id: int
    status_code: int
    success: bool
    request_payload: str | None
    response_payload: str | None
    error_message: str | None
    duration_ms: int
    created_at: datetime


class IntegrationTestResult(BaseModel):
    integration_id: int
    integration_type: str
    status_code: int
    success: bool
    duration_ms: int
    request_payload: str | None
    response_payload: dict | str | None
    error_message: str | None = None


class TechnicalLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    level: str
    event_type: str
    message: str
    integration_id: int | None
    created_at: datetime
