from typing import Protocol
from uuid import UUID

from backend.app.queries.page import Page
from backend.app.queries.query import Query
from backend.domain.entities.model import Model
from backend.domain.repositories.repository import Repository


class ModelRepository(Repository[Model], Protocol):
    def get_by_user_id(self, user_id: UUID, query: Query | None = None) -> Page[Model]: ...