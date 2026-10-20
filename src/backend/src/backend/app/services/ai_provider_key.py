
import uuid

from backend.app.adapters.dto.model_adapter import AiProviderModelDto, ListAiProviderModelDto
from backend.app.adapters.crypto import Crypto
from backend.app.adapters.model_adapter import ProviderAiModelRepository
from backend.app.services.dto.base import CreatedDto, ListDto, Result
from backend.app.services.dto.provider_key import AddProviderKeyDto, AiProviderKeyDto
from backend.domain.entities.ai_provider_key import AiProviderKey
from backend.domain.exception import NotFoundException
from backend.domain.repositories.repository import Repository
from backend.domain.repositories.unit_of_work import UnitOfWork
from backend.domain.repositories.user_repository import UserRepository


class AiProviderKeyService:

    def __init__(
            self,
            ai_provider_key_repo: Repository[AiProviderKey],
            crypto: Crypto,
            user_repo: UserRepository,
            uow: UnitOfWork
        ) -> None:
        self._user_repo = user_repo
        self._crypto = crypto 
        self._ai_provider_key_repo = ai_provider_key_repo
        self._uow = uow

    def add_api_key(self, input: AddProviderKeyDto) -> Result[CreatedDto]:
        try:
            user = self._user_repo.get(uuid.UUID(input.user_id))
            if user == None: 
                raise NotFoundException("USER_NOT_FOUND", "l'utilisateur est introuvable")

            encrypt_value = self._crypto.encrypt(input.api_key)

            new_ai_provider_key = AiProviderKey(
                user_id=user.id,
                provider=input.provider,
                api_key=encrypt_value,
                name=input.name
            )

            self._ai_provider_key_repo.create(new_ai_provider_key)

            self._uow.commit()

            return Result.success(CreatedDto(str(new_ai_provider_key.id)))
        except Exception as e:
            return Result.fail(e)

    def get_api_key(self, provider_id: str) -> Result[AiProviderKeyDto]:
        try:
            provider_key = self._ai_provider_key_repo.get(uuid.UUID(provider_id))
            if provider_key == None:
                raise NotFoundException("AI_PROVIDER_ID_NOT_FOUND", "Ai provideur key est introuvable")

            api_key = self._crypto.decrypt(provider_key.api_key)
    

            return Result.success(AiProviderKeyDto(
                provider_id=provider_id,
                provider=provider_key.provider,
                api_key=api_key,
                name=provider_key.name
            ))
        except Exception as e:
            return Result.fail(e)