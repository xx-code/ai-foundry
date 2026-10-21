from __future__ import annotations
from dataclasses import dataclass

from backend.domain.entities.user_mcp_server import UserMcpServer


@dataclass
class AddUserMcpServerDto:
    user_id: str
    hostname: str
    api_key: str | None = None

@dataclass
class UpdateUserMcpServerDto:
    id: str
    hostname: str | None = None
    api_key: str | None = None
    
@dataclass
class UserMcpServerDto:
    id: str
    hostname: str
    api_key: str|None

    @classmethod
    def from_model(cls, model: UserMcpServer, api_key: str | None) -> UserMcpServerDto:
        return UserMcpServerDto(
            id=str(model.id),
            hostname=model.hostname,
            api_key=api_key
        )
        