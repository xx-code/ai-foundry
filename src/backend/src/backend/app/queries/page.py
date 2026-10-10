from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar('T')

@dataclass(frozen=True)
class Page(Generic[T]):
    items: tuple[T, ...]
    total: int
    offset: int
    limit: int|None