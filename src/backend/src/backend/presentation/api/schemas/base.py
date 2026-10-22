from __future__ import annotations
from typing import Generic, TypeVar
from pydantic import BaseModel

from backend.app.services.dto.base import CreatedDto

T = TypeVar("T")


class CreatedResponse(BaseModel):
    id: str

    @classmethod
    def from_service(cls, dto: CreatedDto) -> CreatedResponse:
        return CreatedResponse(
            id =dto.id
        )

class ListResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
