import uuid

from backend.app.adapters.crypto import Crypto
from backend.app.adapters.dto.model_adapter import AiProviderModelDto, ListAiProviderModelDto
from backend.app.adapters.model_adapter import ProviderAiModelRepository
from backend.app.queries.comparator import Comparator
from backend.app.queries.condition import Condition
from backend.app.queries.query import Query
from backend.app.services.dto.base import CreatedDto, ListDto, Result
from backend.app.services.dto.model import AddModelToolDto, DeployModelDto, ModelDto, UpdateModelDto
from backend.app.services.user_mcp_tool import UserMcpToolServerService
from backend.domain.entities.ai_provider_key import AiProviderKey
from backend.domain.entities.model import Model
from backend.domain.entities.model_tool import ModelTool
from backend.domain.enums.ai_tool import AiToolType
from backend.domain.exception import ForbiddenException, NotFoundException, ValidationException
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
            model_tool_repo: Repository[ModelTool],
            user_mcp_tool_service: UserMcpToolServerService,
            crypto: Crypto,
            user_repo: UserRepository,
            uow: UnitOfWork 
        ) -> None:
        self._ai_provider_key_repo = ai_provider_key_repo
        self._crypto = crypto
        self._user_repo = user_repo
        self._user_mcp_tool_service = user_mcp_tool_service
        self._model_adapter = model_adapter
        self._model_repo = model_repo
        self._model_tool_repo = model_tool_repo
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

            # check name already exist

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

    def update_model(
            self, 
            input: UpdateModelDto, 
            user_id: str | None = None) -> Result[None]:
        try:
            model = self._model_repo.get(uuid.UUID(input.model_id))

            if model is  None:
                raise NotFoundException("MODEL_NOT_FOUND", "le model est introuvable")

            if user_id is not None and model.user_id != uuid.UUID(user_id):
                raise ForbiddenException("MODEL_USER_FORBIDDEN")

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
    
    def down_model(
            self, 
            id: str,
            user_id: str|None = None) -> Result[None]:
        try:
            model_id = uuid.UUID(id)
            model = self._model_repo.get(model_id) 
            if model is None: 
                raise NotFoundException("MODEL_NOT_FOUND", "modele est introuvable")

            if user_id is not None and model.user_id != uuid.UUID(user_id):
                raise ForbiddenException("MODEL_USER_FORBIDDEN")

            self._model_repo.delete(id)
            self._uow.commit()

            return Result.success(None)
        except Exception as e:
            return Result.fail(e)
    

    def add_tool(
            self, 
            input: AddModelToolDto,
            user_id: str | None = None
        ) -> Result[None]:
        try:
            model_id = uuid.UUID(input.model_id)
            model = self._model_repo.get(model_id) 
            if model is None: 
                raise NotFoundException("MODEL_NOT_FOUND", "modele est introuvable")

            if user_id is not None and model.user_id != uuid.UUID(user_id):
                raise ForbiddenException("MODEL_USER_FORBIDDEN")

            tool = ModelTool(
                model_id=model_id,
                tool_id="",
                tool_type=AiToolType.WEB_SEARCH
            )
            if input.type == AiToolType.CODE_INTERPRETOR or input.type == AiToolType.WEB_SEARCH:
                tool = ModelTool(
                    model_id=tool.model_id,
                    tool_id=input.type.value,
                    tool_type=input.type
                )
            else:
                mcp_server = self._user_mcp_tool_service.get_user_mcp_server(input.tool_id).get_or_throw()
                tool = ModelTool(
                    model_id=tool.model_id,
                    tool_id=str(mcp_server.id),
                    tool_type=AiToolType.MCP_SERVER
                )

            self._model_tool_repo.create(tool)
            self._uow.commit()

            return Result.success(None)
        except Exception as e:
            return Result.fail(e)

    def remove_tool(
            self, 
            model_id: str,
            id: str,
            user_id: str | None = None
        ) -> Result[None]:
        try:
            model = self._model_repo.get(uuid.UUID(model_id)) 
            if model is None: 
                raise NotFoundException("MODEL_NOT_FOUND", "modele est introuvable")

            if user_id is not None and model.user_id != uuid.UUID(user_id):
                raise ForbiddenException("MODEL_USER_FORBIDDEN")

            tool = self._model_tool_repo.get(uuid.UUID(id))
            if tool is None:
                raise NotFoundException("MODEL_TOOL_NOT_FOUND", "le tool du model est introuvable")

            if tool.model_id == uuid.UUID(model_id):
                raise ForbiddenException("DELETE_TOOL_MODEL_FORBIDDEN", "the tool is not bellow the model")

            self._model_tool_repo.delete(id)
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
        

    def get_model(
            self, 
            id: str,
            user_id: str | None = None
        ) -> Result[ModelDto]:
        try:
            model = self._model_repo.get(uuid.UUID(id)) 
            if model is None: 
                raise NotFoundException("MODEL_NOT_FOUND", "modele est introuvable")

            if user_id is not None and model.user_id != uuid.UUID(user_id):
                raise NotFoundException("MODEL_TOOL_NOT_FOUND", "le tool du model est introuvable")

            query = Query(
                conditions=(
                    Condition(field="model_id", operator=Comparator.EQUAL, value=model.id),
                ),
            )

            model_tools = list(self._model_tool_repo.get_all(query).items)

            return Result.success(ModelDto.from_model(model, model_tools))
        except Exception as e:
            return Result.fail(e)