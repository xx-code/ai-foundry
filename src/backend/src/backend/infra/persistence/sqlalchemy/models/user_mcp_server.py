from __future__ import annotations

from typing import Any
import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.entities.user_mcp_server import UserMcpServer
from backend.domain.enums.mcp_client import McpClientApp
from backend.domain.value_objects.mcp_client import McpClientCred

from .base import Base


class UserMcpServerModel(Base):
    __tablename__ = "user_mcp_servers"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    server_app: Mapped[McpClientApp] = mapped_column(Enum(McpClientApp))
    client_cred: Mapped[dict[str, Any]] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def to_domain(self) -> UserMcpServer:
        return UserMcpServer(
            id=self.id,
            user_id=self.user_id,
            server_app=self.server_app,
            client_cred=McpClientCred(
                encrypt_api_key=self.client_cred.get("encrypt_api_key")
            ),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, entity: UserMcpServer) -> UserMcpServerModel:
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            server_app=entity.server_app,
            client_cred={
                "encrypt_api_key": (
                    entity.client_cred.encrypt_api_key
                    if entity.client_cred is not None
                    else None
                )
            },
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )