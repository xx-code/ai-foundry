from dataclasses import dataclass

@dataclass
class AskModelDto:
    message: str
    session_id: str

@dataclass
class ChatModelDto:
    response: str
    session_id: str