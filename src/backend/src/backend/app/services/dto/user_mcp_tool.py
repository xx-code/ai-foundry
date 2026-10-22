from __future__ import annotations
from dataclasses import dataclass

from backend.app.adapters.crypto import Crypto
from backend.domain.entities.user_mcp_server import UserMcpServer
from backend.domain.enums.mcp_client import McpClientApp
from backend.domain.value_objects.mcp_client import McpClientCred


@dataclass
class AddUserMcpServerDto:
    user_id: str
    app: McpClientApp
    api_key: str | None = None

@dataclass
class UpdateUserMcpServerDto:
    id: str
    api_key: str | None = None

@dataclass
class UserMcpServerCredDto:
    api_key: str | None

    @classmethod
    def from_value_object(cls, obj: McpClientCred | None, crypto: Crypto) -> UserMcpServerCredDto:
        return UserMcpServerCredDto(
            api_key=(
                crypto.decrypt(obj.encrypt_api_key)
                if obj is not None and obj.encrypt_api_key is not None
                else None
            )
        )
    
@dataclass
class UserMcpServerDto:
    id: str
    app: McpClientApp
    cred: UserMcpServerCredDto

    @classmethod
    def from_model(cls, model: UserMcpServer, cred: UserMcpServerCredDto) -> UserMcpServerDto:
        return UserMcpServerDto(
            id=str(model.id),
            app=model.server_app,
            cred=cred
        )
        