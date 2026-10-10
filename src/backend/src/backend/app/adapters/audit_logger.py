from typing import Protocol
from backend.domain.entities.audit import Audit


class AuditLogger(Protocol):
    def log(self, audit: Audit):...
