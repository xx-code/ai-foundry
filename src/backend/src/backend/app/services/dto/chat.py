from dataclasses import dataclass

@dataclass
class AskModelDto:
    model_id: str
    message: str
    session_id: str

@dataclass
class ChatModelDto:
    response: str
    session_id: str