from langchain_core.language_models import LanguageModelInput
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool

from backend.app.adapters.chat_temporal_session import ChatTemporalSession
from backend.app.adapters.crypto import Crypto
from backend.app.services.ai_provider_key import AiProviderKeyService
from backend.app.services.ai_tool import AiToolService
from backend.app.services.dto.ai_tool import ToolSelectionDto
from backend.app.services.dto.base import Result
from backend.app.services.dto.chat import AskModelDto, ChatModelDto
from backend.app.services.model import ModelService
from collections.abc import Generator, Iterator
from typing import cast
from langchain.chat_models import BaseChatModel, init_chat_model
from langchain.messages import AIMessage, AIMessageChunk, HumanMessage, SystemMessage, ToolMessage


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
            ai_tool_service: AiToolService,
            uow: UnitOfWork
        ) -> None:
        self._ai_provider_key_service = ai_provider_key_service
        self._model_service = model_service 
        self._chat_temporal_session = chat_temporal_session
        self._ai_tool_service = ai_tool_service
        self._uow = uow

    def _init_chat_model(self, model_id: str) -> tuple[BaseChatModel | Runnable[LanguageModelInput, AIMessage], str, dict[str, BaseTool] | None, BaseChatModel]:
        model = self._model_service.get_model(model_id).get_or_throw()
        ai_provider_key = self._ai_provider_key_service.get_api_key(model.provider_id).get_or_throw()

        reasoning = None
        if model.params.reasoning != ModelReasoning.NONE:
            reasoning = model.params.reasoning 

        list_tools = None

        if len(model.tools) > 0:
            list_tools = self._ai_tool_service.list_tools([
                ToolSelectionDto(
                    tool_type=model_tool.tool_type,
                    tool_id=model_tool.tool_id
                ) for model_tool in model.tools
            ]).get_or_throw()

        chat_model = init_chat_model(
            model=model.provider_model_id,
            api_key=ai_provider_key.api_key,
            temperature=model.params.temperature,
            timeout=model.params.timeout,
            max_tokens=model.params.max_tokens,
            reasoning_effort=reasoning,
        )

        chat_model_with_tool = chat_model
        tools_by_name = None 
        if list_tools is not None:
            chat_model_with_tool = chat_model_with_tool.bind_tools(list_tools)
            tools_by_name = {tool.name: tool for tool in list_tools}

        return (
            chat_model_with_tool,
            model.default_instruction,
            tools_by_name,
            chat_model,
        )

    def _stream_response(
        self,
        chat_model: BaseChatModel | Runnable[LanguageModelInput, AIMessage],
        conversation: list,
        session_id: str,
    ) -> Generator[ChatModelDto, None, AIMessageChunk | None]:
        full: AIMessageChunk | None = None
        for chunk in chat_model.stream(conversation):
            full = cast(AIMessageChunk, chunk if full is None else full + chunk)
            yield ChatModelDto(
                response=chunk.content,
                session_id=session_id,
                usage_info=chunk.usage_metadata,
            )
        return full

    def chat_model(self, ask: AskModelDto) -> Result[ChatModelDto] : 
        try:
            (chat_model_with_tool, default_instruction, tools_by_name, chat_model) = self._init_chat_model(ask.model_id)
            # get history of conversation if empty setup system message
            conversation = self._chat_temporal_session.get_conversation_session(ask.session_id)
            if len(conversation) == 0 and  len(default_instruction.strip()) > 0:
                conversation.append(SystemMessage(default_instruction))


            conversation.append(ask.message)

            response = chat_model_with_tool.invoke(conversation)
            tool_steps = 0
            tool_usage = []
            while tools_by_name and response.tool_calls and tool_steps < 3:
                conversation.append(response)
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool = tools_by_name.get(tool_name)
                    tool_usage.append({
                        "tool_name": tool_name,
                        "arguments": tool_call["args"],
                        "status": "started",
                    })
                    result = (
                        tool.invoke(tool_call["args"])
                        if tool
                        else f"Unknown tool: {tool_name}"
                    )
                    result_text = str(result)
                    tool_usage.append({
                        "tool_name": tool_name,
                        "result": result_text,
                        "status": "completed",
                    })
                    conversation.append(
                        ToolMessage(content=result_text, tool_call_id=tool_call["id"])
                    )

                response = chat_model_with_tool.invoke(conversation)
                tool_steps += 1

            if response.tool_calls and tool_steps == 3:
                response = AIMessage(content=response.content)
            conversation.append(response)

            if not response.content:
                explanation_prompt = HumanMessage(
                    content=(
                        "Your previous response was empty. Based on the "
                        "conversation and tool results, explain why you could "
                        "not find a result. Do not call tools. Respond in the "
                        "same language as the user's request."
                    )
                )
                conversation.append(explanation_prompt)
                response = chat_model.invoke(conversation)
                if not response.content:
                    response = AIMessage(
                        content=(
                            "I could not find a result, and the model did not "
                            "provide an explanation."
                        )
                    )
                conversation.append(response)

            session_id = self._chat_temporal_session.save_session(ask.session_id, conversation)

            return Result.success(ChatModelDto(
                response=response.content,
                session_id=session_id,
                usage_info=response.usage_metadata,
                tool_usage=tool_usage or None,
            ))
        except Exception as e:
            return Result.fail(e) 
        

    def stream_chat_with_model(self, ask: AskModelDto) -> Iterator[ChatModelDto]:
        (chat_model_with_tool, default_instruction, tools_by_name, chat_model) = self._init_chat_model(ask.model_id)
        # get history of conversation if empty setup system message
        conversation = self._chat_temporal_session.get_conversation_session(ask.session_id)
        session_id = self._chat_temporal_session.save_session(ask.session_id, conversation)

        if len(conversation) == 0 and  len(default_instruction.strip()) > 0:
            conversation.append(SystemMessage(default_instruction)) 

        conversation.append(ask.message)

        yield ChatModelDto(response="", session_id=session_id, usage_info=None)

        tool_steps = 0
        while True:
            response = yield from self._stream_response(
                chat_model_with_tool,
                conversation,
                session_id,
            )
            if response is None:
                response = AIMessageChunk(content="")

            if response.tool_calls and tools_by_name:
                if tool_steps >= 3:
                    conversation.append(AIMessage(content=response.content))
                    conversation.append(HumanMessage(
                        content=(
                            "You could not provide a result after three tool "
                            "steps. Based on the conversation and tool results, "
                            "explain why you found nothing. Do not call tools. "
                            "Respond in the same language as the user's request."
                        )
                    ))
                    explanation = yield from self._stream_response(
                        chat_model,
                        conversation,
                        session_id,
                    )
                    if explanation is None or not explanation.content:
                        explanation = AIMessageChunk(
                            content=(
                                "I could not find a result, and the model did "
                                "not provide an explanation."
                            )
                        )
                        yield ChatModelDto(
                            response=explanation.content,
                            session_id=session_id,
                            usage_info=explanation.usage_metadata,
                        )
                    conversation.append(AIMessage(content=explanation.content))
                    break

                conversation.append(response)
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool = tools_by_name.get(tool_name)
                    yield ChatModelDto(
                        response="",
                        session_id=session_id,
                        usage_info=None,
                        tool_usage={
                            "tool_name": tool_name,
                            "arguments": tool_call["args"],
                            "status": "started",
                        },
                    )
                    result = (
                        tool.invoke(tool_call["args"])
                        if tool
                        else f"Unknown tool: {tool_name}"
                    )
                    result_text = str(result)
                    conversation.append(ToolMessage(
                        content=result_text,
                        tool_call_id=tool_call["id"],
                    ))
                    yield ChatModelDto(
                        response="",
                        session_id=session_id,
                        usage_info=None,
                        tool_usage={
                            "tool_name": tool_name,
                            "result": result_text,
                            "status": "completed",
                        },
                    )
                tool_steps += 1
                continue

            conversation.append(AIMessage(content=response.content))
            if not response.content:
                conversation.append(HumanMessage(
                    content=(
                        "Your previous response was empty. Based on the "
                        "conversation and tool results, explain why you found "
                        "nothing. Do not call tools. Respond in the same "
                        "language as the user's request."
                    )
                ))
                explanation = yield from self._stream_response(
                    chat_model,
                    conversation,
                    session_id,
                )
                if explanation is None or not explanation.content:
                    explanation = AIMessageChunk(
                        content=(
                            "I could not find a result, and the model did not "
                            "provide an explanation."
                        )
                    )
                    yield ChatModelDto(
                        response=explanation.content,
                        session_id=session_id,
                        usage_info=explanation.usage_metadata,
                    )
                conversation.append(AIMessage(content=explanation.content))
            break

        self._chat_temporal_session.save_session(session_id, conversation)
