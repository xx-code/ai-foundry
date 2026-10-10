from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Uuid, Boolean, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column

from backend.domain.entities.audit import Audit
from backend.domain.enums.audit import AuditAction

from .base import Base


class AuditModel(Base):
    __tablename__ = "audits"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(100), unique=True)
    entity_id: Mapped[str] = mapped_column(String(100), unique=True)
    action: Mapped[AuditAction] = mapped_column(Enum(AuditAction), index=True)
    changes: Mapped[dict[str, str]|None] = mapped_column(JSON, nullable=True)
    is_fail: Mapped[bool] = mapped_column(Boolean, default=False)
    actor_id: Mapped[uuid.UUID|None] = mapped_column(Uuid, index=True)

    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def to_domain(self) -> Audit:
        return Audit(
            action=self.action,
            entity_type=self.entity_type,
            entity_id=self.entity_id,
            changes=self.changes,
            is_fail=self.is_fail,
            actor_id=self.actor_id,
            id=self.id,
            occurred_at=self.occurred_at
        )

    @classmethod
    def from_domain(cls, entity: Audit) -> AuditModel:
        return cls(
            id=entity.id,
            entity_type=entity.entity_type,
            entity_id=entity.entity_id,
            action=entity.action,
            changes=entity.changes,
            is_fail=entity.is_fail,
            actor_id=entity.actor_id,
            occurred_at=entity.occurred_at
        )