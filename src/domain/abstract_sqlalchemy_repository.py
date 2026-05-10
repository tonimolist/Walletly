from typing import Generic, Optional, Sequence, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import Session
from .abstract_repository import AbstractRepository

T = TypeVar("T")
ID = TypeVar("ID")


class SqlAlchemyRepository(AbstractRepository[T, ID], Generic[T, ID]):
    def __init__(self, session: Session, model_class: type[T]):
        self.model_class = model_class
        self.session = session

    def add(self, entity: T) -> None:
        self.session.add(entity)

    def get(self, entity_id: ID) -> Optional[T]:
        return self.session.get(self.model_class, entity_id)

    def get_all(self) -> Sequence[T]:
        stmt = select(self.model_class)
        return self.session.scalars(stmt).all()

    def update(self, entity: T) -> None:
        self.session.merge(entity)

    def delete(self, entity: T) -> None:
        self.session.delete(entity)
