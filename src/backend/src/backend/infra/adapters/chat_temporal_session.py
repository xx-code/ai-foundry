import uuid

from cachetools import TTLCache
from langchain.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from backend.app.adapters.chat_temporal_session import ChatTemporalSession

class ChatTemporalSessionTTLCache(ChatTemporalSession):
    def __init__(
        self,
        session_cache: TTLCache):
        self._session_cache = session_cache

    def get_conversation_session(self, session_id: str) -> list[HumanMessage | AIMessage | SystemMessage | ToolMessage]:
        session_id = session_id.strip() if session_id else ""
        if not session_id:
            return []

        conversation = self._session_cache.get(session_id)
        return list(conversation) if conversation is not None else []

    def save_session(self, session_id: str, conversation: list[HumanMessage | AIMessage | SystemMessage | ToolMessage]) -> str:
        session_id = session_id.strip() if session_id else ""
        if not session_id or session_id not in self._session_cache:
            session_id = str(uuid.uuid4())

        self._session_cache[session_id] = conversation
        return session_id


