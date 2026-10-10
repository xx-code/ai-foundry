from collections.abc import Callable, Sequence
from typing import Any

from sqlalchemy import ColumnElement, inspect

from backend.app.queries.comparator import Comparator
from backend.app.queries.condition import Condition
from backend.app.queries.sort import Sort

_OPERATORS: dict[Comparator, Callable[[Any, Any], ColumnElement[bool]]] = {
    Comparator.EQUAL: lambda c, v: c == v,
    Comparator.NOT_EQUAL: lambda c, v: c != v,
    Comparator.IN: lambda c, v: c.in_(v),
    Comparator.NOT_IN: lambda c, v: c.not_in(v),
    Comparator.GREATER_THAN: lambda c, v: c > v,
    Comparator.GREATER_THAN_OR_EQUAL: lambda c, v: c >= v,
    Comparator.LESS_THAN: lambda c, v: c < v,
    Comparator.LESS_THAN_OR_EQUAL: lambda c, v: c <= v,
    # autoescape: un "%" ou "_" saisi par l'utilisateur est traité littéralement
    Comparator.CONTAINS: lambda c, v: c.contains(v, autoescape=True),
    Comparator.STARTS_WITH: lambda c, v: c.startswith(v, autoescape=True),
    Comparator.ENDS_WITH: lambda c, v: c.endswith(v, autoescape=True),
    Comparator.IS_NULL: lambda c, _: c.is_(None),
    Comparator.IS_NOT_NULL: lambda c, _: c.is_not(None),
}


def _column(model: type, field: str) -> Any:
    # Whitelist : on n'expose que les colonnes mappées, jamais un getattr libre
    if field not in inspect(model).column_attrs.keys(): # type: ignore
        raise ValueError(f"Champ inconnu pour {model.__name__}: {field!r}")
    return getattr(model, field)


def build_where(model: type, conditions: Sequence[Condition]) -> list[ColumnElement[bool]]:
    return [_OPERATORS[c.operator](_column(model, c.field), c.value) for c in conditions]


def build_order_by(model: type, sorts: Sequence[Sort]) -> list[ColumnElement[Any]]:
    clauses = []
    for s in sorts:
        col = _column(model, s.field)
        clauses.append(col.desc() if s.descending else col.asc()) # type: ignore
    return clauses # type: ignore