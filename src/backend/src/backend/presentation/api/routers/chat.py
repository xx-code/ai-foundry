
import json
import logging

from langchain.messages import HumanMessage

from backend.app.services.dto.chat import AskModelDto
from backend.presentation.api.dependencies import ChatServiceDep, CurrentUserIdDep
from backend.presentation.api.schemas.chat import AskChatModelRequest, ChatModelResponse
from fastapi import APIRouter
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/models/{model_id}", tags=["chat models"])
logger = logging.getLogger(__name__)

@router.post("/chat")
def chat_model(model_id: str, request: AskChatModelRequest,  _: CurrentUserIdDep, service: ChatServiceDep) -> ChatModelResponse:
    # upgrade to handle multi mode or type message
    response = service.chat_model(AskModelDto(
        model_id=model_id,
        message=HumanMessage(request.message) ,
        session_id=request.session_id
    )).get_or_throw()

    return ChatModelResponse.from_service(response)

@router.post("/stream-chat", response_class=StreamingResponse)
def stream_chat_model(
    model_id: str,
    request: AskChatModelRequest,
    _: CurrentUserIdDep,
    service: ChatServiceDep,
) -> StreamingResponse:
    stream = service.stream_chat_with_model(AskModelDto(
        model_id=model_id,
        message=HumanMessage(content=request.message),
        session_id=request.session_id,
    ))

    def event_stream():
        try:
            for dto in stream:
                response = ChatModelResponse.from_service(dto)
                yield f"data: {response.model_dump_json()}\n\n"
        except Exception:
            logger.exception("Chat model stream failed")
            yield f'event: error\ndata: {json.dumps({"detail": "The model stream failed."})}\n\n'

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )