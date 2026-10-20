
from backend.app.services.chat import ChatService
from backend.app.services.dto.chat import AskModelDto
from backend.presentation.api.dependencies import CurrentUserIdDep
from backend.presentation.api.schemas.chat import AskChatModelRequest, ChatModelResponse
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from collections.abc import AsyncIterable


router = APIRouter(prefix="/models/{model_id}", tags=["chat models"])

@router.post("/chat")
def chat_model(model_id: str, request: AskChatModelRequest,  _: CurrentUserIdDep, service: ChatService) -> ChatModelResponse:
    response = service.chat_model(AskModelDto(
        message=request.message,
        session_id=request.session_id
    ))

    return ChatModelResponse.from_service(response)

@router.post("/stream-chat", response_class=StreamingResponse)
async def stream_chat_model(model_id: str, request: AskChatModelRequest, _: ChatModelResponse, service: ChatService) -> AsyncIterable[ChatModelResponse]:  
    return await service.stream_chat_with_model(AskModelDto(
        message=request.message,
        session_id=request.session_id,
    ), ChatModelResponse.from_service)