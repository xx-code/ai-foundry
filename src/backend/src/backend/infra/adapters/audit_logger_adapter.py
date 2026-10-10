from backend.app.adapters.audit_logger import AuditLogger
from backend.domain.entities.audit import Audit
from backend.domain.repositories.repository import Repository


class AuditLoggerAdapter(AuditLogger):
    def __init__(self, audit_repository: Repository[Audit]) -> None:
        self._audit_repo = audit_repository

    def log(self, audit: Audit):
        self._audit_repo.create(audit)

