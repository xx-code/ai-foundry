from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class CreatedResponse(BaseModel):
    id: str


class ListResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int