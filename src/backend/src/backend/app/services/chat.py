from backend.app.adapters.crypto import Crypto
from backend.app.services.ai_provider_key import AiProviderKeyService
from backend.app.services.dto.base import Result
from backend.app.services.dto.chat import AskModelDto, ChatModelDto
from backend.app.services.model import ModelService
from collections.abc import AsyncIterable
from typing import Callable
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage


from backend.domain.entities.ai_provider_key import AiProviderKey
from backend.domain.enums.model_reasoning import ModelReasoning
from backend.domain.repositories.repository import Repository
from backend.domain.repositories.unit_of_work import UnitOfWork


class ChatService:

    def __init__(
            self,
            model_service: ModelService,
            ai_provider_key_service: AiProviderKeyService,
            uow: UnitOfWork
        ) -> None:
        self._ai_provider_key_service = ai_provider_key_service
        self._model_service = model_service 
        self._uow = uow

    def chat_model(self, ask: AskModelDto) -> Result[ChatModelDto] : 
        try:
            model = self._model_service.get_model(ask.model_id).get_or_throw()
            ai_provider_key = self._ai_provider_key_service.get_api_key(model.provider_id).get_or_throw()

            reasoning = None
            if model.params.reasoning != ModelReasoning.NONE:
                reasoning = model.params.reasoning 

            chat_model = init_chat_model(
                model=model.provider_model_id,
                api_key=ai_provider_key.api_key,
                temperature=model.params.temperature,
                timeout=model.params.timeout,
                max_tokens=model.params.max_tokens,
                reasoning_effort=reasoning
            )

            conversation: list[SystemMessage|AIMessage|HumanMessage] = []

            if len(model.default_instruction.strip()) > 0:
                conversation = [
                    SystemMessage(model.default_instruction)
                ]
            
            conversation.append(HumanMessage(ask.message))

            response = chat_model.invoke(conversation)

            return Result.success(ChatModelDto(
                response=str(response.content),
                session_id=""
            ))
        except Exception as e:
            return Result.fail(e) 
        

    def stream_chat_with_model[T](self, ask: AskModelDto, output: Callable[[ChatModelDto], T]) -> AsyncIterable[T]: ...