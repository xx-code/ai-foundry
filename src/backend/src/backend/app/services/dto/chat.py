from dataclasses import dataclass
from typing import Any, Dict

from langchain.messages import HumanMessage, UsageMetadata

@dataclass
class AskModelDto:
    model_id: str
    message: HumanMessage
    session_id: str

@dataclass
class ChatModelDto:
    response: str | list[str | dict[Any, Any]]
    session_id: str
    usage_info: UsageMetadata | None