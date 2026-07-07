from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth import get_current_user, require_admin
from app.database import get_db
from app.models import Integration, IntegrationTest, User
from app.schemas import IntegrationCreate, IntegrationRead, IntegrationTestRead, IntegrationTestResult
from app.services.integration_service import create_integration, execute_integration_test, get_integration_or_404

router = APIRouter(prefix="/integrations", tags=["Integrações"])


@router.get(
    "/admin/forbidden-demo",
    summary="Demonstrar autorização 403",
    description="Endpoint didático que exige usuário admin. Útil para estudar diferença entre 401 e 403.",
)
def forbidden_demo(_: User = Depends(require_admin)) -> dict:
    return {"message": "Acesso administrativo autorizado."}


@router.post(
    "",
    response_model=IntegrationRead,
    status_code=201,
    summary="Criar integração",
    description="Cadastra uma integração REST ou SOAP simulada. O campo failure_mode permite criar cenários de incidente.",
)
def create(
    payload: IntegrationCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Integration:
    return create_integration(db, payload)


@router.get(
    "",
    response_model=list[IntegrationRead],
    summary="Listar integrações",
    description="Lista integrações cadastradas para análise e execução de testes.",
)
def list_integrations(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Integration]:
    return db.query(Integration).order_by(Integration.created_at.desc()).all()


@router.get(
    "/{integration_id}",
    response_model=IntegrationRead,
    summary="Consultar integração por ID",
    description="Busca os detalhes de uma integração específica ou retorna 404 quando não existe.",
)
def get_by_id(
    integration_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Integration:
    return get_integration_or_404(db, integration_id)


@router.get(
    "/{integration_id}/test",
    response_model=IntegrationTestResult,
    summary="Executar teste de integração",
    description="Executa um teste REST ou SOAP. Integrações SOAP retornam XML convertido para JSON.",
)
def test_integration(
    integration_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> IntegrationTestResult:
    return execute_integration_test(db, integration_id)


@router.get(
    "/{integration_id}/tests",
    response_model=list[IntegrationTestRead],
    summary="Consultar histórico de testes",
    description="Mostra execuções anteriores para apoiar troubleshooting e análise de incidentes.",
)
def list_tests(
    integration_id: int,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[IntegrationTest]:
    get_integration_or_404(db, integration_id)
    return (
        db.query(IntegrationTest)
        .filter(IntegrationTest.integration_id == integration_id)
        .order_by(IntegrationTest.created_at.desc())
        .limit(limit)
        .all()
    )

