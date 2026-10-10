from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.entities.user import User

from .base import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    user_name: Mapped[str] = mapped_column(String(30), unique=True)
    external_id: Mapped[str] = mapped_column(String(100), index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def to_domain(self) -> User:
        return User(
            id=self.id,  # la colonne Uuid renvoie déjà un UUID
            email=self.email,
            user_name=self.user_name,
            external_id=self.external_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, entity: User) -> UserModel:
        return cls(
            id=entity.id,
            email=entity.email,
            user_name=entity.user_name,
            external_id=entity.external_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )