from dataclasses import dataclass


@dataclass(frozen=True)
class Sort:
    field: str
    descending: bool = False

