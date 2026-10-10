from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.entities.user_password import UserPassword

from .base import Base


class UserPasswordModel(Base):
    __tablename__ = "user_passwords"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
    )
    hashed_pwd: Mapped[str] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def to_domain(self) -> UserPassword:
        return UserPassword(
            id=self.id,  # plus de uuid.UUID(...) : la colonne renvoie déjà un UUID
            user_id=self.user_id,
            hashed_pwd=self.hashed_pwd,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, entity: UserPassword) -> UserPasswordModel:
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            hashed_pwd=entity.hashed_pwd,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )