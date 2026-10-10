from uuid import UUID
from datetime import datetime

from backend.domain.entities.entity import Entity
from backend.domain.enums.audit import AuditAction


class Audit(Entity):
    def __init__(self, 
                action: AuditAction,
                entity_type: str,
                entity_id: str,
                changes: dict[str, str] | None = None,
                is_fail: bool = False,
                actor_id: UUID | None = None,
                id: UUID | None = None, 
                occurred_at: datetime | None = None,
            ):
        super().__init__(id, occurred_at, occurred_at)

        self._action = action
        self._entity_type = entity_type
        self._entity_id = entity_id
        self._actor_id = actor_id
        self._changes = changes
        self._is_fail = is_fail

    @property
    def action(self) -> AuditAction:
        return self._action

    @property
    def is_fail(self) -> bool:
        return self._is_fail

    @property
    def changes(self) -> dict[str, str] | None:
        return self._changes

    @property
    def entity_id(self) -> str:
        return self._entity_id

    @property
    def entity_type(self):
        return self._entity_type

    @property
    def actor_id(self) -> UUID | None:
        return self._actor_id

    @property
    def occurred_at(self) -> datetime:
        return self.created_at