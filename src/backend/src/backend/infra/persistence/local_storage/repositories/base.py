from collections.abc import Callable, Collection, Sequence
from copy import deepcopy
from typing import Any, Protocol
from uuid import UUID

from backend.app.queries.comparator import Comparator
from backend.app.queries.condition import Condition
from backend.app.queries.page import Page
from backend.app.queries.query import Query
from backend.domain.repositories.repository import Repository


class HasId(Protocol):
    id: UUID


_OPERATORS: dict[Comparator, Callable[[Any, Any], bool]] = {
    Comparator.EQUAL: lambda f, v: f == v,
    Comparator.NOT_EQUAL: lambda f, v: f != v,
    Comparator.IN: lambda f, v: f in v,
    Comparator.NOT_IN: lambda f, v: f not in v,
    Comparator.GREATER_THAN: lambda f, v: f is not None and f > v,
    Comparator.GREATER_THAN_OR_EQUAL: lambda f, v: f is not None and f >= v,
    Comparator.LESS_THAN: lambda f, v: f is not None and f < v,
    Comparator.LESS_THAN_OR_EQUAL: lambda f, v: f is not None and f <= v,
    Comparator.CONTAINS: lambda f, v: f is not None and v in f,
    Comparator.STARTS_WITH: lambda f, v: f is not None and f.startswith(v),
    Comparator.ENDS_WITH: lambda f, v: f is not None and f.endswith(v),
    Comparator.IS_NULL: lambda f, _: f is None,
    Comparator.IS_NOT_NULL: lambda f, _: f is not None,
}


class LocalStorageRepository[T: HasId](Repository[T]):
    """Repository en mémoire, pour tests rapides. Rien n'est persisté."""

    def __init__(self) -> None:
        self._db: dict[str, T] = {}

    # --- helpers -----------------------------------------------------------

    @staticmethod
    def _key(id: UUID | str) -> str:
        return str(id)

    def _matches(self, entity: T, conditions: Sequence[Condition]) -> bool:
        for c in conditions:
            if not hasattr(entity, c.field):
                raise ValueError(f"Champ inconnu pour {type(entity).__name__}: {c.field!r}")
            if not _OPERATORS[c.operator](getattr(entity, c.field), c.value):
                return False
        return True

    def _filter(self, query: Query) -> list[T]:
        return [e for e in self._db.values() if self._matches(e, query.conditions)]

    # --- écriture ----------------------------------------------------------

    def create(self, entity: T) -> str:
        key = self._key(entity.id)
        if key in self._db:
            raise ValueError(f"id déjà existant: {key}")
        self._db[key] = deepcopy(entity)  # copie : simule une vraie persistance
        return key

    def create_many(self, entities: Sequence[T]) -> Sequence[T]:
        keys = [self._key(e.id) for e in entities]
        if len(set(keys)) != len(keys) or any(k in self._db for k in keys):
            raise ValueError("ids dupliqués")  # tout ou rien, comme une transaction
        for key, entity in zip(keys, entities):
            self._db[key] = deepcopy(entity)
        return list(entities)

    def update(self, entity: T) -> T:
        key = self._key(entity.id)
        if key not in self._db:
            raise KeyError(f"entité introuvable: {key}")
        self._db[key] = deepcopy(entity)
        return entity

    def delete(self, id: str) -> None:
        self._db.pop(self._key(id), None)

    def delete_many_by_ids(self, ids: Collection[str]) -> None:
        for id in ids:
            self._db.pop(self._key(id), None)

    def delete_by(self, query: Query) -> int:
        if not query.conditions:
            raise ValueError("delete_by sans condition supprimerait tout")
        to_delete = [self._key(e.id) for e in self._filter(query)]
        for key in to_delete:
            del self._db[key]
        return len(to_delete)

    # --- lecture -----------------------------------------------------------

    def get(self, id: UUID) -> T | None:
        entity = self._db.get(self._key(id))
        return deepcopy(entity) if entity is not None else None

    def get_many_by_ids(self, ids: Collection[str]) -> list[T]:
        return [deepcopy(self._db[k]) for i in ids if (k := self._key(i)) in self._db]

    def get_all(self, query: Query | None = None) -> Page[T]:
        query = query or Query()
        items = self._filter(query)
        total = len(items)

        # Tri stable : on applique les critères du moins au plus prioritaire.
        # Tie-breaker sur l'id, comme dans la version SQL.
        items.sort(key=lambda e: str(e.id))
        for sort in reversed(query.order_by):
            items.sort(
                key=lambda e, f=sort.field: (getattr(e, f) is None, getattr(e, f)),
                reverse=sort.descending,
            )

        end = None if query.limit is None else query.offset + query.limit
        page_items = tuple(deepcopy(e) for e in items[query.offset:end])
        return Page(items=page_items, total=total, offset=query.offset, limit=query.limit)

    def exists(self, query: Query) -> bool:
        return any(self._matches(e, query.conditions) for e in self._db.values())