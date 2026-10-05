from dataclasses import dataclass
from .comparator import Comparator


@dataclass(frozen=True)
class Condition:
    field: str
    operator: Comparator
    value: object | None = None