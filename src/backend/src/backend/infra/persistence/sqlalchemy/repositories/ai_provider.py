from backend.domain.entities.ai_provider_key import AiProviderKey
from backend.infra.persistence.sqlalchemy.models.ai_provider_key import AiProviderKeyModel
from backend.infra.persistence.sqlalchemy.repositories.base import SqlAlchemyRepository


class SqlAlchemyAiProviderkeyRepository(SqlAlchemyRepository[AiProviderKey, AiProviderKeyModel]):
    model=AiProviderKeyModel
