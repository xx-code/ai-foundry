from uuid import UUID

from backend.app.queries.comparator import Comparator
from backend.app.queries.condition import Condition
from backend.app.queries.page import Page
from backend.app.queries.query import Query
from backend.domain.entities.model import Model
from backend.domain.repositories.model_repository import ModelRepository
from backend.infra.persistence.sqlalchemy.models.model import ModelModel
from backend.infra.persistence.sqlalchemy.repositories.base import SqlAlchemyRepository


class SqlAlchemyModelRepository(SqlAlchemyRepository[Model, ModelModel], ModelRepository):
    model = ModelModel

    def get_by_user_id(self, user_id: UUID, query: Query | None = None) -> Page[Model]:
        query = Query(
            conditions=(
                Condition(field="user_id", operator=Comparator.EQUAL, value=user_id),
            ),
        )
        return self.get_all(query)
