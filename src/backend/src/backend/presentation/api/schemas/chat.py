from __future__ import annotations
from backend.app.services.dto.chat import ChatModelDto
from pydantic import BaseModel


class AskChatModelRequest(BaseModel):
    message: str
    session_id: str

class ChatModelResponse(BaseModel):
    response: str
    session_id: str

    @classmethod
    def from_service(cls, dto: ChatModelDto) -> ChatModelResponse:   
        return ChatModelResponse(
            response=dto.response,
            session_id=dto.session_id
        )