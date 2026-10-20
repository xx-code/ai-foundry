import uuid

from backend.app.adapters.crypto import Crypto
from backend.app.adapters.dto.model_adapter import AiProviderModelDto, ListAiProviderModelDto
from backend.app.adapters.model_adapter import ProviderAiModelRepository
from backend.app.services.dto.base import ListDto, Result
from backend.domain.entities.ai_provider_key import AiProviderKey
from backend.domain.exception import NotFoundException
from backend.domain.repositories.repository import Repository
from backend.domain.repositories.unit_of_work import UnitOfWork
from backend.domain.repositories.user_repository import UserRepository


class ModelService:
    def __init__(
            self,
            model_adapter: ProviderAiModelRepository,
            ai_provider_key_repo: Repository[AiProviderKey],
            crypto: Crypto,
            user_repo: UserRepository,
            uow: UnitOfWork 
        ) -> None:
        self._ai_provider_key_repo = ai_provider_key_repo
        self._crypto = crypto
        self._user_repo = user_repo
        self._model_adapter = model_adapter
        self._uow = uow

    def list_model(self, provider_id: str) -> Result[ListDto[AiProviderModelDto]]:
        try:
            provider_key = self._ai_provider_key_repo.get(uuid.UUID(provider_id))
            if provider_key == None:
                raise NotFoundException("AI_PROVIDER_ID_NOT_FOUND", "Ai provideur key est introuvable")

            api_key = self._crypto.decrypt(provider_key.api_key)

            list_model = self._model_adapter.list_model(ListAiProviderModelDto(
                provider=provider_key.provider,
                api_key=api_key
            ))

            return Result.success(list_model)
        except Exception as e:
            return Result.fail(e) 