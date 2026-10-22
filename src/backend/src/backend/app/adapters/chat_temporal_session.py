from typing import Protocol
from langchain.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage

class ChatTemporalSession(Protocol):
    def get_conversation_session(self, session_id: str) -> list[HumanMessage | AIMessage | SystemMessage | ToolMessage]:
        """Return conversation history, or an empty list for a new or expired session."""
        ...

    def save_session(self, session_id: str, conversation: list[HumanMessage | AIMessage | SystemMessage | ToolMessage]) -> str:
        """Save the conversation and return its ID, creating one when the supplied ID is absent or unknown."""
        ...


