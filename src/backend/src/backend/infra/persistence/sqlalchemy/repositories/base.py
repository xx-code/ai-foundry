from collections.abc import Collection, Sequence
from typing import Any, Protocol, Self
from uuid import UUID

from sqlalchemy import delete, exists, func, select
from sqlalchemy.orm import Mapped, Session

from backend.app.queries.page import Page
from backend.app.queries.query import Query
from backend.domain.repositories.repository import Repository
from .query_translator import build_order_by, build_where


class DomainModel[E](Protocol):
    id: Mapped[UUID]

    def to_domain(self) -> E: ...

    @classmethod
    def from_domain(cls, entity: E) -> Self: ...


class SqlAlchemyRepository[E, M: DomainModel[Any]](Repository[E]):
    """Repository générique. Les sous-classes définissent `model`."""

    model: type[M]

    def __init__(self, session: Session) -> None:
        super().__init__()
        self._session = session
 

    def create(self, entity: E) -> str:
        model = self.model.from_domain(entity)
        self._session.add(model)
        self._session.flush()  # fait remonter les erreurs d'intégrité tout de suite
        return str(model.id)

    def create_many(self, entities: Sequence[E]) -> Sequence[E]:
        models = [self.model.from_domain(e) for e in entities]
        self._session.add_all(models)
        self._session.flush()
        return [m.to_domain() for m in models]

    def get(self, id: UUID) -> E | None:
        model = self._session.get(self.model, id)
        return model.to_domain() if model else None

    def get_many_by_ids(self, ids: Collection[str]) -> list[E]:
        stmt = select(self.model).where(self.model.id.in_([UUID(i) for i in ids]))
        return [m.to_domain() for m in self._session.scalars(stmt)]

    def get_all(self, query: Query | None = None) -> Page[E]:
        query = query or Query()
        where = build_where(self.model, query.conditions)

        total = self._session.scalar(
            select(func.count()).select_from(self.model).where(*where)
        ) or 0

        # Tie-breaker sur l'id : sans ordre total, offset/limit donnent
        # des pages instables (doublons ou éléments manquants entre deux appels)
        order = [*build_order_by(self.model, query.order_by), self.model.id.asc()] # type: ignore

        stmt = select(self.model).where(*where).order_by(*order).offset(query.offset) # type: ignore
        if query.limit is not None:
            stmt = stmt.limit(query.limit)

        items = tuple(m.to_domain() for m in self._session.scalars(stmt))
        return Page(items=items, total=total, offset=query.offset, limit=query.limit)


    def update(self, entity: E) -> E:
        merged = self._session.merge(self.model.from_domain(entity))
        self._session.flush()
        return merged.to_domain()

    def delete(self, id: str) -> None:
        self._session.execute(delete(self.model).where(self.model.id == UUID(id)))

    def delete_many_by_ids(self, ids: Collection[str]) -> None:
        self._session.execute(
            delete(self.model).where(self.model.id.in_([UUID(i) for i in ids]))
        )

    def exists(self, query: Query) -> bool:
        where = build_where(self.model, query.conditions)
        return bool(self._session.scalar(select(exists().where(*where).select_from(self.model))))


    def delete_by(self, query: Query) -> int:
        if not query.conditions:
            raise ValueError("delete_by sans condition supprimerait toute la table")
        where = build_where(self.model, query.conditions)
        result = self._session.execute(delete(self.model).where(*where))
        return result.rowcount # type: ignore