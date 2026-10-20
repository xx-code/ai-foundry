from fastapi import APIRouter

from backend.domain.enums.ai_provider import AiProvider
from backend.presentation.api.dependencies import CurrentUserIdDep, ModelServiceDep
from backend.presentation.api.schemas.base import ListResponse
from backend.presentation.api.schemas.model import ModelResponse


router = APIRouter(prefix="/models", tags=["models"])

@router.get("/providers/{provider_id}")
def get_models(provider_id: str, _: CurrentUserIdDep, service: ModelServiceDep) -> ListResponse[ModelResponse]:
    models = service.list_model(provider_id=provider_id).get_or_throw()

    return ListResponse(
        items=[ModelResponse.from_service(item) for item in models.items],
        total=models.total
    )
