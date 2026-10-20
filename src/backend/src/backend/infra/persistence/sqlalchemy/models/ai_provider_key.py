from __future__ import annotations
from datetime import datetime
import uuid

from sqlalchemy import DateTime, Enum, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.entities.ai_provider_key import AiProviderKey
from backend.domain.enums.ai_provider import AiProvider
from .base import Base


class AiProviderKeyModel(Base):
    __tablename__ = "ai_provider_keys"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    api_key: Mapped[str] = mapped_column(String(500))
    name: Mapped[str] = mapped_column(String(100))
    provider: Mapped[AiProvider] = mapped_column(Enum(AiProvider), index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def to_domain(self) -> AiProviderKey:
        return AiProviderKey(
            id=self.id,
            user_id=self.user_id,
            provider=self.provider,
            name=self.name,
            api_key=self.api_key,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @classmethod
    def from_domain(cls, entity: AiProviderKey) -> AiProviderKeyModel:
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            provider=entity.provider,
            name=entity.name,
            api_key=entity.api_key,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )