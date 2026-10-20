from backend.app.services.dto.chat import AskModelDto, ChatModelDto
from backend.app.services.model import ModelService
from collections.abc import AsyncIterable
from typing import Callable, Never


class ChatService:

    def __init__(
            self,
            model_service: ModelService
        ) -> None:
        self._model_service = model_service 

    def chat_model(self, ask: AskModelDto) -> ChatModelDto:...

    async def stream_chat_with_model[T](self, ask: AskModelDto, output: Callable[[ChatModelDto], T]) -> AsyncIterable[T]: ...