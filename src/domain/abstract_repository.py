import abc
from typing import Generic, TypeVar, Sequence

T = TypeVar("T")
ID = TypeVar("ID")

class AbstractRepository(Generic[T, ID], abc.ABC):
    @abc.abstractmethod
    def add(self, entity: T) -> None:
        pass

    @abc.abstractmethod
    def update(self, entity: T) -> None:
        pass

    @abc.abstractmethod
    def get(self, entity_id: ID) -> T | None:
        pass

    @abc.abstractmethod
    def get_all(self) -> Sequence[T]:
        pass

    @abc.abstractmethod
    def delete(self, entity: T) -> None:
        pass
