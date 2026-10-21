from dataclasses import dataclass

from backend.domain.enums.ai_tool import AiToolType


@dataclass
class ToolSelectionDto:
    tool_id: str
    tool_type: AiToolType