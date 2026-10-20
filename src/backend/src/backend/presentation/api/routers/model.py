from fastapi import APIRouter

from backend.app.services.dto.model import DeployModelDto
from backend.domain.enums.ai_provider import AiProvider
from backend.presentation.api.dependencies import CurrentUserIdDep, ModelServiceDep
from backend.presentation.api.schemas.base import CreatedResponse, ListResponse
from backend.presentation.api.schemas.model import AiProviderModelResponse, DeployModelRequest, ModelResponse


router = APIRouter(prefix="/models", tags=["models"])

@router.get("/providers/{provider_id}", response_model=ListResponse[AiProviderModelResponse])
def get_provider_models(provider_id: str, _: CurrentUserIdDep, service: ModelServiceDep) -> ListResponse[AiProviderModelResponse]:
    models = service.list_provier_model(provider_id=provider_id).get_or_throw()

    return ListResponse(
        items=[AiProviderModelResponse.from_service(item) for item in models.items],
        total=models.total
    )

@router.get("/", response_model=ListResponse[ModelResponse])
def get_models(user_id: CurrentUserIdDep, service: ModelServiceDep) -> ListResponse[ModelResponse]: 
    models = service.get_models(user_id).get_or_throw()

    return ListResponse(
        items=[ModelResponse.from_service(item) for item in models.items],
        total=models.total
    )

@router.get("/{model_id}", response_model=ModelResponse)
def get_model(model_id: str, _: CurrentUserIdDep, service: ModelServiceDep) -> ModelResponse:
    model = service.get_model(model_id).get_or_throw()

    return ModelResponse.from_service(model)

@router.post("/")
def deploy_model(request: DeployModelRequest, user_id: CurrentUserIdDep,  service: ModelServiceDep) -> CreatedResponse:
    created = service.deploy_model(input=request.to_domain(user_id)).get_or_throw()

    return CreatedResponse.from_service(created)