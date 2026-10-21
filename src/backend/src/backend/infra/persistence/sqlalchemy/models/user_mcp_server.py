from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.entities.user_mcp_server import UserMcpServer

from .base import Base


class UserMcpServerModel(Base):
    __tablename__ = "user_mcp_servers"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    hostname: Mapped[str] = mapped_column(String(253))
    encrypt_api_key: Mapped[str | None] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def to_domain(self) -> UserMcpServer:
        return UserMcpServer(
            id=self.id,
            user_id=self.user_id,
            hostname=self.hostname,
            encrypt_api_key=self.encrypt_api_key,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, entity: UserMcpServer) -> UserMcpServerModel:
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            hostname=entity.hostname,
            encrypt_api_key=entity.encrypt_api_key,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )