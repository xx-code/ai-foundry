from backend.domain.entities.audit import Audit
from backend.infra.persistence.sqlalchemy.models.audit import AuditModel
from backend.infra.persistence.sqlalchemy.repositories.base import SqlAlchemyRepository


class SqlAlchemyAuditRepository(SqlAlchemyRepository[Audit, AuditModel]):
    model=AuditModel