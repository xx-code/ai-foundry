
import uuid

from backend.app.adapters.key_hasher import KeyHasher
from backend.app.adapters.model_adapter import ProviderAiModelRepository
from backend.app.services.dto.base import Result
from backend.app.services.dto.provider_key import AddOnlineProviderKeyDto
from backend.domain.entities.ai_provider_key import AiProviderKey
from backend.domain.exception import NotFoundException
from backend.domain.repositories.repository import Repository
from backend.domain.repositories.unit_of_work import UnitOfWork
from backend.domain.repositories.user_repository import UserRepository


class AiProviderKeyService:

    def __init__(
            self,
            model_adapter: ProviderAiModelRepository,
            ai_provider_key_repo: Repository[AiProviderKey],
            key_hasher: KeyHasher,
            user_repo: UserRepository,
            uow: UnitOfWork
        ) -> None:
        self._user_repo = user_repo
        self._key_hasher = key_hasher 
        self._model_adapter = model_adapter
        self._ai_provider_key_repo = ai_provider_key_repo
        self._uow = uow

    def add_api_key(self, input: AddOnlineProviderKeyDto) -> Result[None]:
        try:
            user = self._user_repo.get(uuid.UUID(input.user_id))
            if user == None: 
                raise NotFoundException("USER_NOT_FOUND", "l'utilisateur est introuvable")

            memo = "generate memo"
            encrypt_value = self._key_hasher.encrypt(input.api_key, memo)

            self._ai_provider_key_repo.create(AiProviderKey(
                user_id=user.id,
                provider=input.provider,
                api_key=encrypt_value,
                name=input.name,
                memo_key=memo
            ))

            return Result.success(None)
        except Exception as e:
            return Result.fail(e)