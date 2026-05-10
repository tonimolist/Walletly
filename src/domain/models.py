"""
--- EL PLÀNOL I L'ESTRUCTURA DE DADES ---

- La funció de models.py és definir la forma de les taules i com es connecten entre elles.
- És l'arxiu on "dibuixes" la base de dades: decideixes que un usuari té nom, email i contrasenya, i que les despeses tenen un import i una data.
- Si db.py és la canonada, models.py és el disseny de tota la xarxa de distribució.

# 2. Explicació clara del que fa el codi
    -- CREAR LES TAULES (CLASSES): Cada classe (User, Budget, Transaction...) es convertirà en una taula real a la base de dades.
        - Aquí especifiques el tipus de dada: si és un número (Integer), text (String) o diners (Numeric).
    -- CONFIGURAR LES RELACIONS (1:N): Defineix com les taules "parlen" entre elles.
        - Per exemple, diu que un Usuari pot tenir molts Pressupostos, però que cada Pressupost pertany només a un Usuari.
    -- ESTABLIR VINCLES (FOREIGN KEYS): Són les "claus" que lliguen una taula amb una altra per a que no hi hagi dades perdudes.
    -- DISSENYAR ETIQUETES (MANY-TO-MANY): Crea la taula "pont" (transaction_tag) per a que una despesa pugui tenir moltes etiquetes alhora.

- __tablename__: El nom que tindrà la taula dins del fitxer de la base de dades.
- Mapped / mapped_column: La manera de dir-li a Python: "Aquesta propietat s'ha de guardar a la base de dades".
- relationship: El connector que et permet saltar d'una dada a una altra (ex: d'una despesa directament al nom de l'usuari).
- Base.metadata.create_all: L'ordre final que agafa tots aquests plànols i construeix les taules de veritat.
"""

from .db import Base, engine
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from sqlalchemy import create_engine, Integer, String, Date, Boolean, ForeignKey, Numeric, Text, DateTime, func, Table, Column, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker, Session

# 1. TAULA ASSOCIATIVA (MANY-TO-MANY)
#Aquesta taula serveix per connectar "transactions" i "tags" ja que una transacció pot tenir múltiples tags i un tag pot estar associat a múltiples transacciones. 
transaction_tag = Table(
    "transaction_tag",
    Base.metadata,  
    Column("id_transaction", Integer, ForeignKey("transactions.id_transaction"), primary_key=True),
    Column("id_tag", Integer, ForeignKey("tag.id_tag"), primary_key=True)
)

# 2. MODELS DE DADES
class User(Base):
    """Informació personal i d'accés a l'usuari"""

    #Nom de la taula a la base de dades on es guardaran els usuaris
    __tablename__ = "users"

    #Definició de les columnes de la taula "users"
    #Descriu quina informació es guarda de cada usuari i com es relaciona amb altres taules
    id_user: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    last_update: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    #Relacions: Un usuari té un perfil financer i pot tenir múltiples pressupostos
    financial_profile: Mapped[Optional["FinancialProfile"]] = relationship(back_populates="user") 
    budget: Mapped[List["Budget"]] = relationship(back_populates="user")


class FinancialProfile(Base):
    """Configuració financera específica de cada usuari (sou, estalvi, etc)"""

    # Nom de la taula on es guarda el perfil financer de cada usuari
    __tablename__ = "financial_profile"

    #Definició de les columnes: identificador, sou, objectiu d'estalvi i moneda
    id_profile: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id_user"), unique=True, nullable=False)
    monthly_salary: Mapped[Decimal] = mapped_column(Numeric(10,2), default=0.00)
    savings_goal: Mapped[Decimal] = mapped_column(Numeric(10,2), default=0.00)
    currency: Mapped[str] = mapped_column(String(3), server_default="eur")
    risk_profile: Mapped[str] = mapped_column(String(20), nullable=True)
    last_update: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    #Relació: Enllaça aquest perfil amb la informació general de l'usuari
    user: Mapped["User"] = relationship(back_populates="financial_profile")


class Budget(Base):
    """Contenidor mensual / anual on s'agrupen les despeses"""
    
    #Nom de la taula que emmagatzema els pressupostos mensuals o anuals de cada usuari
    __tablename__ = "budget"

    #Definició de les columnes: usuari propietari, període (mes/any) i límits de despesa
    id_budget: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id_user"), nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    total_limit: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=True)
    last_update: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    #Relacions: Un pressupost pot tenir múltiples transaccions i està associat a un usuari. També té una relació amb les categories a través de "BudgetCategory"
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="budget")
    user: Mapped["User"] = relationship(back_populates="budget")
    budget_categories: Mapped[List["BudgetCategory"]] = relationship(back_populates="budget")
    
    
class Category(Base):
    """Diccionari de categories (ex: Alimentació, Oci, Transport, etc.)"""

    #Nom de la taula on es defineixen les categories de despesa (Oci, Menjar, Lloguer, etc.)
    __tablename__ = "category"

    #Definició de les columnes: identificador, nom, descripció i si és una despesa vital
    id_category: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    is_essential: Mapped[bool] = mapped_column(Boolean, server_default="false", default=False)
    last_update: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    #Relacions: Connecta la categoria amb totes les seves transaccions i amb els límits dels pressupostos
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="category")
    budget_categories: Mapped[List["BudgetCategory"]] = relationship(back_populates="category")
    

class BudgetCategory(Base):
    """Estableix un límit de despesa per a una categoria dins d'un pressupost específic"""

    #Taula que defineix quant es pot gastar en cada categoria dins d'un pressupost concret
    __tablename__ = "budget_category"

    #Definició de columnes: enllaç pressupost-categoria, import màxim i llindar d'alerta
    id_budget: Mapped[int] = mapped_column(ForeignKey("budget.id_budget"), primary_key=True)
    id_category: Mapped[int] = mapped_column(ForeignKey("category.id_category"), primary_key=True)
    max_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    alert_threshold: Mapped[Decimal] = mapped_column(Numeric(5, 2), server_default="0.80", default=0.80)
    last_update: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    #Relacions: Enllaça amb els objectes complets de pressupost i categoria
    budget: Mapped["Budget"] = relationship(back_populates="budget_categories")
    category: Mapped["Category"] = relationship(back_populates="budget_categories")


class PaymentMethod(Base):
    """Mètodes de pagament (ex: Targeta de crèdit, PayPal, etc.)"""

    #Nom de la taula on es defineixen les formes de pagament (Efectiu, Targeta, etc.)
    __tablename__ = "payment_method"

    #Definició de les columnes: identificador, nom del mètode i l'entitat o proveïdor
    id_method: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=True)
    last_update: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    #Relació: Un mètode de pagament pot aparèixer en moltes transaccions diferents
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="payment_method")


class TransactionType(Base):
    """Defineix si el moviment és 'Ingrés' o 'Despesa'"""

    #Nom de la taula que classifica si el moviment és un "Ingrés" o una "Despesa"
    __tablename__ = "transaction_type"

    #Definició de les columnes: identificador i el nom del tipus de transacció
    id_type: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_update: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    #Relació: Un tipus (per exemple, "Despesa") s'assigna a múltiples transaccions
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="transaction_type")


class Transaction(Base):
    """Registre de cada moviment econòmic realitzat"""

    #Nom de la taula principal on es registren tots els moviments (despeses/ingressos)
    __tablename__ = "transactions"
    
    #Definició de columnes: claus alienes (links), import, data i si és un pagament recurrent
    id_transaction: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_budget: Mapped[int] = mapped_column(ForeignKey("budget.id_budget"), nullable=True)
    id_method: Mapped[int] = mapped_column(ForeignKey("payment_method.id_method"), nullable=True)
    id_type: Mapped[int] = mapped_column(ForeignKey("transaction_type.id_type"), nullable=True)
    id_category: Mapped[int] = mapped_column(ForeignKey("category.id_category"), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    transaction_date: Mapped[date] = mapped_column("date", Date, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    is_recurring: Mapped[bool] = mapped_column(Boolean, server_default="false", default=False)
    last_update: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    #Relacions: Permet saber fàcilment la categoria, mètode de pagament, tipus i etiquetes del moviment
    category: Mapped["Category"] = relationship(back_populates="transactions")
    budget: Mapped["Budget"] = relationship(back_populates="transactions")
    payment_method: Mapped["PaymentMethod"] = relationship(back_populates="transactions")
    transaction_type: Mapped["TransactionType"] = relationship(back_populates="transactions")

    #Relació Many-to-Many amb Tag a través de la taula associativa "transaction_tag"
    tags: Mapped[List["Tag"]] = relationship(
        secondary=transaction_tag,
        back_populates="transactions" 
    )


class Tag(Base):
    """Etiquetes lliures per a l'usuari (ex: "Vacances", "Regal", etc.)"""

    #Nom de la taula on es guarden les etiquetes personalitzades
    __tablename__ = "tag"
    
    #Definició de columnes: identificador, nom de l'etiqueta (únic) i color visual
    id_tag: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    color_code: Mapped[str] = mapped_column(String(7), nullable=True)
    last_update: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    #Relació: Una etiqueta pot estar present en moltes transaccions diferents
    transactions: Mapped[List["Transaction"]] = relationship(
        secondary="transaction_tag",
        back_populates="tags"
    )