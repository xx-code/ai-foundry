from fastapi import APIRouter

from backend.app.services.dto.model import AddModelToolDto, DeployModelDto
from backend.domain.enums.ai_provider import AiProvider
from backend.presentation.api.dependencies import CurrentUserIdDep, ModelServiceDep
from backend.presentation.api.schemas.base import CreatedResponse, ListResponse
from backend.presentation.api.schemas.model import AddModelToolRequest, AiProviderModelResponse, DeployModelRequest, ModelResponse


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

@router.put("/{id}/tool")
def add_tool(_: CurrentUserIdDep, id: str, request: AddModelToolRequest, service: ModelServiceDep):
    service.add_tool(AddModelToolDto(
        model_id=id,
        tool_id=request.tool_id,
        type=request.tool_type
    )).get_or_throw()


@router.delete("/{id}/model/{model_tool_id}")
def remove_tool(__: CurrentUserIdDep, id: str, model_tool_id: str, service: ModelServiceDep):
    service.remove_tool(model_tool_id).get_or_throw()