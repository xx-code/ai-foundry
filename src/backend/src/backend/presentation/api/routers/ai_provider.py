
from fastapi import APIRouter, status

from backend.app.services.dto.provider_key import AddProviderKeyDto
from backend.presentation.api.dependencies import AiProviderKeyServiceDep, CurrentUserIdDep
from backend.presentation.api.schemas.ai_provider_key import AddAiProviderKeyRequest, AiProviderKeyResponse
from backend.presentation.api.schemas.base import CreatedResponse


router = APIRouter(prefix="/ai-provider-keys", tags=["Ai Provider"])

@router.post("/add-key", response_model=CreatedResponse, status_code=status.HTTP_201_CREATED)
def add_key(request: AddAiProviderKeyRequest, user_id: CurrentUserIdDep, service: AiProviderKeyServiceDep) -> CreatedResponse:
    created = service.add_api_key(AddProviderKeyDto(
        user_id=user_id,
        provider=request.provider,
        name=request.name,
        api_key=request.api_key
    )).get_or_throw()

    return CreatedResponse(id=created.id)

@router.get("/{provider_id}")
def get_provider_key(provider_id: str, _: CurrentUserIdDep, service: AiProviderKeyServiceDep) -> AiProviderKeyResponse:
    provider_key = service.get_api_key(provider_id=provider_id).get_or_throw()

    return AiProviderKeyResponse.from_service(provider_key) 