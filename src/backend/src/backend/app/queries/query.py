from dataclasses import dataclass
from ..queries.sort import Sort
from .condition import Condition

@dataclass(frozen=True)
class Query:
    conditions: tuple[Condition, ...] = ()
    order_by: tuple[Sort, ...] = ()
    offset: int = 0
    limit: int | None = None

    def __post_init__(self) -> None:
        if self.offset < 0:
            raise ValueError("offset doit être >= 0")
        if self.limit is not None and self.limit < 0:
            raise ValueError("limit doit être >= 0")