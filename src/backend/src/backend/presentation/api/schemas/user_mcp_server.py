from __future__ import annotations

from pydantic import BaseModel

from backend.app.services.dto.user_mcp_tool import (
    AddUserMcpServerDto,
    UpdateUserMcpServerDto,
    UserMcpServerDto,
)


class AddUserMcpServerRequest(BaseModel):
    hostname: str
    api_key: str | None = None

    def to_service(self, user_id: str) -> AddUserMcpServerDto:
        return AddUserMcpServerDto(
            user_id=user_id,
            hostname=self.hostname,
            api_key=self.api_key,
        )


class UpdateUserMcpServerRequest(BaseModel):
    hostname: str | None = None
    api_key: str | None = None

    def to_service(self, mcp_id: str) -> UpdateUserMcpServerDto:
        return UpdateUserMcpServerDto(
            id=mcp_id,
            hostname=self.hostname,
            api_key=self.api_key,
        )


class UserMcpServerResponse(BaseModel):
    id: str
    hostname: str
    api_key: str | None

    @classmethod
    def from_service(cls, dto: UserMcpServerDto) -> UserMcpServerResponse:
        return cls(
            id=dto.id,
            hostname=dto.hostname,
            api_key=dto.api_key,
        )