from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import Never


@dataclass
class CreatedDto:
    id: str


@dataclass
class ListDto[L]:
    items: list[L]
    total: int


class Result[T](ABC):
    """Représentation fonctionnelle d'un résultat : Success ou Failure."""

    @property
    @abstractmethod
    def is_success(self) -> bool: ...

    @property
    def is_failure(self) -> bool:
        return not self.is_success

    @abstractmethod
    def get_or_null(self) -> T | None: ...

    @abstractmethod
    def exception_or_null(self) -> Exception | None: ...

    @abstractmethod
    def get_or_throw(self) -> T: ...

    @abstractmethod
    def map[U](self, fn: Callable[[T], U]) -> "Result[U]": ...

    @staticmethod
    def success[U](data: U) -> "Result[U]":
        return Success(data)

    @staticmethod
    def fail(error: Exception) -> "Result[Never]":
        return Failure(error)


@dataclass(frozen=True, slots=True)
class Success[T](Result[T]):
    data: T

    @property
    def is_success(self) -> bool:
        return True

    def get_or_null(self) -> T:
        return self.data

    def exception_or_null(self) -> None:
        return None

    def get_or_throw(self) -> T:
        return self.data

    def map[U](self, fn: Callable[[T], U]) -> Result[U]:
        return Success(fn(self.data))


@dataclass(frozen=True, slots=True)
class Failure(Result[Never]):
    error: Exception

    @property
    def is_success(self) -> bool:
        return False

    def get_or_null(self) -> None:
        return None

    def exception_or_null(self) -> Exception:
        return self.error

    def get_or_throw(self) -> Never:
        raise self.error

    def map[U](self, fn: Callable[[Never], U]) -> Result[Never]:
        return self