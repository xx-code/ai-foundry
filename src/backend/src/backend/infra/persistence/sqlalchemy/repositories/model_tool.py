from backend.domain.entities.model_tool import ModelTool
from backend.infra.persistence.sqlalchemy.models.model_tool import ModelToolModel
from backend.infra.persistence.sqlalchemy.repositories.base import SqlAlchemyRepository


class SqlAlchemyModelToolRepository(
    SqlAlchemyRepository[ModelTool, ModelToolModel]
):
    model = ModelToolModel