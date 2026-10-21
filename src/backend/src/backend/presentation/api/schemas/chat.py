from __future__ import annotations
from typing import Any, Dict
from backend.app.services.dto.chat import ChatModelDto
from pydantic import BaseModel


class AskChatModelRequest(BaseModel):
    message: str
    session_id: str

class ChatModelResponse(BaseModel):
    response: Any
    usage_metadata: Any
    session_id: str
    tool_usage: Any = None

    @classmethod
    def from_service(cls, dto: ChatModelDto) -> ChatModelResponse:   
        return ChatModelResponse(
            response=dto.response,
            usage_metadata=dto.usage_info,
            session_id=dto.session_id,
            tool_usage=dto.tool_usage,
        )