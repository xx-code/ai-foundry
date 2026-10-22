from __future__ import annotations

from pydantic import BaseModel

from backend.app.adapters.dto.mcp_client_tool import McpServerInfoDto
from backend.app.services.dto.user_mcp_tool import (
    AddUserMcpServerDto,
    UpdateUserMcpServerDto,
    UserMcpServerDto,
)
from backend.domain.enums.mcp_client import McpClientApp, McpClientAuthType


class AddUserMcpServerRequest(BaseModel):
    app: McpClientApp
    api_key: str | None = None

    def to_service(self, user_id: str) -> AddUserMcpServerDto:
        return AddUserMcpServerDto(
            user_id=user_id,
            app=self.app,
            api_key=self.api_key,
        )


class UpdateUserMcpServerRequest(BaseModel):
    api_key: str | None = None

    def to_service(self, mcp_id: str) -> UpdateUserMcpServerDto:
        return UpdateUserMcpServerDto(
            id=mcp_id,
            api_key=self.api_key,
        )


class UserMcpServerCredResponse(BaseModel):
    api_key: str | None


class UserMcpServerResponse(BaseModel):
    id: str
    app: McpClientApp
    cred: UserMcpServerCredResponse

    @classmethod
    def from_service(cls, dto: UserMcpServerDto) -> UserMcpServerResponse:
        return cls(
            id=dto.id,
            app=dto.app,
            cred=UserMcpServerCredResponse(api_key=dto.cred.api_key),
        )

class McpClientToolResponse(BaseModel):
    app: McpClientApp
    auth_Type: McpClientAuthType

    @classmethod
    def from_adapter(cls, dto: McpServerInfoDto) -> McpClientToolResponse:
        return McpClientToolResponse(
            app=dto.app,
            auth_Type=dto.auth_type
        )