import abc
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import sessionmaker
from collections.abc import Sequence
from sqlalchemy import select
from typing import Optional, List
from .models import (
    Category,
    User,
    Budget,
    BudgetCategory,
    FinancialProfile,
    PaymentMethod,
    Transaction,
    TransactionType,
    Tag
)
from .abstract_sqlalchemy_repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository[User, int]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def get_by_email(self, email: str) -> Optional[User]:
        """Consulta específica: obtenir usuari per email"""
        stmt = select(User).where(User.email == email)
        return self.session.scalars(stmt).first()

    def add_budget_to_user(self, user_id: int, budget: Budget) -> None:
        """Operació de domini concreta: afegir un pressupost a un usuari existent"""
        user = self.get(user_id)
        if user:
            user.budget.append(budget)
            # No cal cridar update, SQLAlchemy ho detecta automàticament
            self.session.add(budget)


class FinancialProfileRepository(SqlAlchemyRepository[FinancialProfile, int]):
    def __init__(self, session: Session):
        super().__init__(session, FinancialProfile)


class BudgetRepository(SqlAlchemyRepository[Budget, int]):
    def __init__(self, session: Session):
        super().__init__(session, Budget)


class BudgetCategoryRepository(SqlAlchemyRepository[BudgetCategory, tuple]):
    def __init__(self, session: Session):
        super().__init__(session, BudgetCategory)

    def get(self, entity_id: tuple) -> Optional[BudgetCategory]:
        """Obté un BudgetCategory per clau composta (id_budget, id_category)"""
        id_budget, id_category = entity_id
        stmt = select(BudgetCategory).where(
            BudgetCategory.id_budget == id_budget,
            BudgetCategory.id_category == id_category
        )
        return self.session.scalars(stmt).first()

    def get_by_budget(self, budget_id: int) -> Sequence[BudgetCategory]:
        """Consulta específica: obtenir tots els límits de categoria d'un pressupost"""
        stmt = select(BudgetCategory).where(BudgetCategory.id_budget == budget_id)
        return self.session.scalars(stmt).all()


class CategoryRepository(SqlAlchemyRepository[Category, int]):
    def __init__(self, session: Session):
        super().__init__(session, Category)

    def get_essential_categories(self) -> Sequence[Category]:
        """Consulta específica: obtenir només les categories vitals"""
        stmt = select(Category).where(Category.is_essential == True)
        return self.session.scalars(stmt).all()


class PaymentMethodRepository(SqlAlchemyRepository[PaymentMethod, int]):
    def __init__(self, session: Session):
        super().__init__(session, PaymentMethod)


class TransactionTypeRepository(SqlAlchemyRepository[TransactionType, int]):
    def __init__(self, session: Session):
        super().__init__(session, TransactionType)


class TransactionRepository(SqlAlchemyRepository[Transaction, int]):
    def __init__(self, session: Session):
        super().__init__(session, Transaction)

    def get_by_category(self, category_id: int) -> Sequence[Transaction]:
        """Consulta específica: filtar transaccions per categoria"""
        stmt = select(Transaction).where(Transaction.id_category == category_id)
        return self.session.scalars(stmt).all()

    def get_paginated(self, page: int, page_size: int) -> Sequence[Transaction]:
        """Paginació per a la taula amb més dades esperades"""
        offset = (page - 1) * page_size
        stmt = select(Transaction).limit(page_size).offset(offset)
        return self.session.scalars(stmt).all()

    def add_tag_to_transaction(self, transaction_id: int, tag: Tag) -> None:
        """Operació de domini concreta: relacionar un tag amb una transacció"""
        transaction = self.get(transaction_id)
        if transaction and tag not in transaction.tags:
            transaction.tags.append(tag)
            # SQLAlchemy ho detectarà abans del commit


class TagRepository(SqlAlchemyRepository[Tag, int]):
    def __init__(self, session: Session):
        super().__init__(session, Tag)


class AbstractUnitOfWork(abc.ABC):
    users: UserRepository
    financial_profiles: FinancialProfileRepository
    budgets: BudgetRepository
    budget_categories: BudgetCategoryRepository
    categories: CategoryRepository
    payment_methods: PaymentMethodRepository
    transaction_types: TransactionTypeRepository
    transactions: TransactionRepository
    tags: TagRepository

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            self.rollback()
        self.close()

    @abc.abstractmethod
    def commit(self):
        pass

    @abc.abstractmethod
    def rollback(self):
        pass

    @abc.abstractmethod
    def close(self):
        pass


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: sessionmaker[Session]):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()

        # Inicialitzem els repositoris injectant-los la sessió d'aquest UoW
        self.users = UserRepository(self.session)
        self.financial_profiles = FinancialProfileRepository(self.session)
        self.budgets = BudgetRepository(self.session)
        self.budget_categories = BudgetCategoryRepository(self.session)
        self.categories = CategoryRepository(self.session)
        self.payment_methods = PaymentMethodRepository(self.session)
        self.transaction_types = TransactionTypeRepository(self.session)
        self.transactions = TransactionRepository(self.session)
        self.tags = TagRepository(self.session)

        return super().__enter__()

    def __exit__(self, exc_type, exc_val, traceback):
        # super().__exit__ ja crida self.close(), no cal tancar la sessió aquí
        super().__exit__(exc_type, exc_val, traceback)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        self.session.close()