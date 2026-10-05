from datetime import datetime
from abc import ABC
import uuid


class Entity(ABC):

    def __init__(
        self,
        id: uuid.UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self._id = id or uuid.uuid1()
        self._created_at = created_at or datetime.now()
        self._updated_at = updated_at or self._created_at
        self._changed = False

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def has_changed(self) -> bool:
        return self._changed

    def _mark_changed(self):
        self._changed = True
        self._updated_at = datetime.now()

    def reset_change(self):
        self._changed = False