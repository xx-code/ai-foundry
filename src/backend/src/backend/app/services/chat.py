from backend.app.adapters.chat_temporal_session import ChatTemporalSession
from backend.app.adapters.crypto import Crypto
from backend.app.services.ai_provider_key import AiProviderKeyService
from backend.app.services.dto.base import Result
from backend.app.services.dto.chat import AskModelDto, ChatModelDto
from backend.app.services.model import ModelService
from collections.abc import Iterator
from langchain.chat_models import BaseChatModel, init_chat_model
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
            chat_temporal_session: ChatTemporalSession,
            uow: UnitOfWork
        ) -> None:
        self._ai_provider_key_service = ai_provider_key_service
        self._model_service = model_service 
        self._chat_temporal_session = chat_temporal_session
        self._uow = uow

    def _init_chat_model(self, model_id: str) -> tuple[BaseChatModel, str]:
        model = self._model_service.get_model(model_id).get_or_throw()
        ai_provider_key = self._ai_provider_key_service.get_api_key(model.provider_id).get_or_throw()

        reasoning = None
        if model.params.reasoning != ModelReasoning.NONE:
            reasoning = model.params.reasoning 

        return (
            init_chat_model(
            model=model.provider_model_id,
            api_key=ai_provider_key.api_key,
            temperature=model.params.temperature,
            timeout=model.params.timeout,
            max_tokens=model.params.max_tokens,
            reasoning_effort=reasoning
            ),
            model.default_instruction
        )

    def chat_model(self, ask: AskModelDto) -> Result[ChatModelDto] : 
        try:
            (chat_model, default_instruction) = self._init_chat_model(ask.model_id)
            # get history of conversation if empty setup system message
            conversation = self._chat_temporal_session.get_conversation_session(ask.session_id)
            if len(conversation) == 0 and  len(default_instruction.strip()) > 0:
                conversation.append(SystemMessage(default_instruction))
            
            conversation.append(ask.message)

            response = chat_model.invoke(conversation)

            conversation.append(response)

            session_id = self._chat_temporal_session.save_session(ask.session_id, conversation)

            return Result.success(ChatModelDto(
                response=response.content,
                session_id=session_id,
                usage_info=response.usage_metadata
            ))
        except Exception as e:
            return Result.fail(e) 
        

    def stream_chat_with_model(self, ask: AskModelDto) -> Iterator[ChatModelDto]:
        (chat_model, default_instruction) = self._init_chat_model(ask.model_id)
        # get history of conversation if empty setup system message
        conversation = self._chat_temporal_session.get_conversation_session(ask.session_id)
        session_id = self._chat_temporal_session.save_session(ask.session_id, conversation)

        if len(conversation) == 0 and  len(default_instruction.strip()) > 0:
            conversation.append(SystemMessage(default_instruction))

        conversation.append(ask.message)

        full = None
        yield ChatModelDto(response="", session_id=session_id, usage_info=None)

        for chunk in chat_model.stream(conversation):
            full = chunk if full is None else full + chunk
            yield ChatModelDto(
                response=chunk.content,
                session_id=session_id,
                usage_info=chunk.usage_metadata,
            )

        if full is not None:
            conversation.append(AIMessage(content=full.content))

        self._chat_temporal_session.save_session(session_id, conversation)
