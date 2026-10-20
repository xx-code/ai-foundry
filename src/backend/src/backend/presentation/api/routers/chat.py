
from backend.app.services.dto.chat import AskModelDto
from backend.presentation.api.dependencies import ChatServiceDep, CurrentUserIdDep
from backend.presentation.api.schemas.chat import AskChatModelRequest, ChatModelResponse
from fastapi import APIRouter
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/models/{model_id}", tags=["chat models"])

@router.post("/chat")
def chat_model(model_id: str, request: AskChatModelRequest,  _: CurrentUserIdDep, service: ChatServiceDep) -> ChatModelResponse:
    response = service.chat_model(AskModelDto(
        model_id=model_id,
        message=request.message,
        session_id=request.session_id
    )).get_or_throw()

    return ChatModelResponse.from_service(response)

# @router.post("/stream-chat", response_class=StreamingResponse)
# async def stream_chat_model(model_id: str, request: AskChatModelRequest, _: CurrentUserIdDep, service: ChatServiceDep) -> StreamingResponse:
#     stream = service.stream_chat_with_model(AskModelDto(
#         model_id=model_id,
#         message=request.message,
#         session_id=request.session_id,
#     ), ChatModelResponse.from_service)

#     return StreamingResponse(stream, media_type="text/event-stream")