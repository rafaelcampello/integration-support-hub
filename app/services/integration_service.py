import json
import time

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Integration, IntegrationTest
from app.schemas import IntegrationCreate, IntegrationTestResult
from app.services.soap_service import call_simulated_soap_service
from app.services.troubleshooting_service import register_event


def create_integration(db: Session, integration_in: IntegrationCreate) -> Integration:
    integration = Integration(
        name=integration_in.name,
        type=integration_in.type,
        url=str(integration_in.url),
        status=integration_in.status,
        description=integration_in.description,
        failure_mode=integration_in.failure_mode,
    )
    db.add(integration)
    db.commit()
    db.refresh(integration)
    register_event(
        db,
        level="info",
        event_type="integration_created",
        message=f"Integração '{integration.name}' criada com tipo {integration.type}.",
        integration_id=integration.id,
    )
    return integration


def get_integration_or_404(db: Session, integration_id: int) -> Integration:
    integration = db.get(Integration, integration_id)
    if integration is None:
        register_event(
            db,
            level="warning",
            event_type="integration_not_found",
            message=f"Tentativa de consultar integração inexistente: {integration_id}.",
            integration_id=integration_id,
        )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Integração não encontrada.")
    return integration


def _simulate_failure(integration: Integration) -> None:
    """Gera falhas controladas para treinar análise de incidentes."""

    if integration.failure_mode == "bad_request":
        raise HTTPException(status_code=400, detail="Payload inválido na integração simulada.")
    if integration.failure_mode == "forbidden":
        raise HTTPException(status_code=403, detail="Usuário sem permissão para executar esta integração.")
    if integration.failure_mode == "server_error":
        raise HTTPException(status_code=500, detail="Falha interna simulada no provedor.")
    if integration.failure_mode == "timeout":
        time.sleep(0.2)
        raise HTTPException(status_code=504, detail="Timeout simulado ao chamar o provedor.")


def execute_integration_test(db: Session, integration_id: int) -> IntegrationTestResult:
    integration = get_integration_or_404(db, integration_id)
    started_at = time.perf_counter()
    request_payload: str | None = None
    response_payload: dict | str | None = None

    try:
        if integration.status != "ativa":
            raise HTTPException(status_code=400, detail="Integração inativa não pode ser testada.")

        _simulate_failure(integration)

        if integration.type == "SOAP":
            request_payload, response_payload = call_simulated_soap_service()
        else:
            request_payload = json.dumps({"ping": "healthcheck", "target": integration.url}, ensure_ascii=False)
            response_payload = {
                "message": "Integração REST simulada com sucesso.",
                "target": integration.url,
                "provider_status": "available",
            }

        duration_ms = int((time.perf_counter() - started_at) * 1000)
        record = IntegrationTest(
            integration_id=integration.id,
            status_code=200,
            success=True,
            request_payload=request_payload,
            response_payload=json.dumps(response_payload, ensure_ascii=False),
            duration_ms=duration_ms,
        )
        db.add(record)
        db.commit()
        register_event(
            db,
            level="info",
            event_type="integration_test_success",
            message=f"Teste da integração {integration.id} concluído com sucesso.",
            integration_id=integration.id,
        )
        return IntegrationTestResult(
            integration_id=integration.id,
            integration_type=integration.type,
            status_code=200,
            success=True,
            duration_ms=duration_ms,
            request_payload=request_payload,
            response_payload=response_payload,
        )

    except HTTPException as exc:
        duration_ms = int((time.perf_counter() - started_at) * 1000)
        record = IntegrationTest(
            integration_id=integration.id,
            status_code=exc.status_code,
            success=False,
            request_payload=request_payload,
            response_payload=None,
            error_message=str(exc.detail),
            duration_ms=duration_ms,
        )
        db.add(record)
        db.commit()
        event_type = "timeout" if exc.status_code == 504 else "integration_test_error"
        register_event(
            db,
            level="error",
            event_type=event_type,
            message=f"Teste da integração {integration.id} falhou: {exc.detail}",
            integration_id=integration.id,
        )
        raise
