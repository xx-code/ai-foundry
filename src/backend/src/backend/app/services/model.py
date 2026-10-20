import uuid

from backend.app.adapters.crypto import Crypto
from backend.app.adapters.dto.model_adapter import AiProviderModelDto, ListAiProviderModelDto
from backend.app.adapters.model_adapter import ProviderAiModelRepository
from backend.app.services.dto.base import CreatedDto, ListDto, Result
from backend.app.services.dto.model import DeployModelDto, ModelDto, UpdateModelDto
from backend.domain.entities.ai_provider_key import AiProviderKey
from backend.domain.entities.model import Model
from backend.domain.exception import NotFoundException, ValidationException
from backend.domain.repositories.model_repository import ModelRepository
from backend.domain.repositories.repository import Repository
from backend.domain.repositories.unit_of_work import UnitOfWork
from backend.domain.repositories.user_repository import UserRepository
from backend.domain.value_objects.model_params import ModelParams


class ModelService:
    def __init__(
            self,
            model_adapter: ProviderAiModelRepository,
            ai_provider_key_repo: Repository[AiProviderKey],
            model_repo: ModelRepository,
            crypto: Crypto,
            user_repo: UserRepository,
            uow: UnitOfWork 
        ) -> None:
        self._ai_provider_key_repo = ai_provider_key_repo
        self._crypto = crypto
        self._user_repo = user_repo
        self._model_adapter = model_adapter
        self._model_repo = model_repo
        self._uow = uow

    def list_provier_model(self, provider_id: str) -> Result[ListDto[AiProviderModelDto]]:
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

    def deploy_model(self, input: DeployModelDto) -> Result[CreatedDto]:
        try:
            user_id = uuid.UUID(input.user_id)
            user = self._user_repo.get(user_id)
            if user == None: 
                raise NotFoundException("USER_NOT_FOUND", "l'utilisateur est introuvable")

            # check provider and return avaible model
            provider_models = self.list_provier_model(input.provider_key_id).get_or_throw()
            provider_model_ids = [item.model_id for item in provider_models.items]

            # check if model selected exist in provider_models
            try:
                provider_model_ids.index(input.provider_model_id) 
            except ValueError:
                raise ValidationException("PROVIDER_MODEL_NOT_DISPONIBLE_BELONG_THE_PROVIDER", "Le models choisi n'exist")

            # deploy model
            instruction = ""
            if input.default_instruction is not None:
                instruction = input.default_instruction

            params = ModelParams()
            if input.params is not None:
                params = input.params

            model = Model(
                user_id=user_id,
                default_instruction=instruction,
                provider_model_id=input.provider_model_id,                
                provider_key_id=uuid.UUID(input.provider_key_id),
                name=input.name,
                params=params
            )
            self._model_repo.create(model)
            self._uow.commit()

            return Result.success(CreatedDto(str(model.id)))
        except Exception as e:
            return Result.fail(e)

    def update_model(self, input: UpdateModelDto) -> Result[None]:
        try:
            model = self._model_repo.get(uuid.UUID(input.model_id))
            if model is  None:
                raise NotFoundException("MODEL_NOT_FOUND", "le model est introuvable")

            if input.name is not None:
                model.set_name(input.name) 

            if input.params is not None:
                model.set_params(input.params)

            if model.has_changed: 
                self._model_repo.update(model)
                self._uow.commit()

            return Result.success(None)
        except Exception as e:
            return Result.fail(e)

    def get_models(self, user_id: str) -> Result[ListDto[ModelDto]]:
        try:
            models = self._model_repo.get_by_user_id(uuid.UUID(user_id))

            return Result.success(
                ListDto(
                    items=[ModelDto.from_model(item) for item in models.items],
                    total=models.total
                )
            )
        except Exception as e:
            return Result.fail(e)
        

    def get_model(self, id: str) -> Result[ModelDto]:
        try:
            model = self._model_repo.get(uuid.UUID(id))
            if model is None: 
                raise NotFoundException("MODEL_NOT_FOUND", "modele est introuvable")

            return Result.success(ModelDto.from_model(model))
        except Exception as e:
            return Result.fail(e)