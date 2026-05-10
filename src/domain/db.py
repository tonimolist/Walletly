"""
--- COR DE LA CONNEXIÓ A LA BASE DE DADES ---

- La funció de db.py és establir i configurar la connexió amb la base de dades.
- És l'arxiu que "obre la canonada" entre el teu codi Python i el fitxer on es desaran els teus estalvis, despeses i usuaris.
- El models.py defineix que guardem, db.py defineix com ens connectem a la base de dades

# 2. Explicació clara del que fa el codi
    -- IMPORTAR LA CONFIGURACIÓ (DB_URL) i les eines de SQLAlchemy per connectar-se a la base de dades i gestionar les sessions.
    -- CREAR UN MOTOR DE BASE DE DADES: create_engine(DB_URL) és com configurar el "motor" que s'encarregarà de gestionar la connexió amb la base de dades.
        - És la peça que sap com empènyer les dades cap al fitxer. Tu li parles en Python, i el motor s'encarrega de traduir-ho.
            al "llenguatge de base de dades" (SQL) per a que el fitxer l'entengui.
    -- CONFIGURAR LES SESSIONS: sessionmaker(bind=engine) crea una fàbrica de sessions que utilitzaràs per interactuar amb la base de dades.
        - Les sessions són com "converses" que tens amb la base de dades. Cada vegada que vols llegir o escriure dades, obres una sessió, fas les teves preguntes o ordres, i després tanques la sessió.
    -- DEFINIR LA BASE DE DADES: La classe Base(DeclarativeBase) és la classe base que utilitzaràs per definir les teves taules (models) a models.py.

- DB_URL: On és la base de dades?
- engine: Com hi arribo?
- Session: Com hi interactuo ara mateix?
- Base: Com s'han de construir les meves taules per ser compatibles? 
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import DB_URL

assert DB_URL is not None, f"DB_URL no configurada per a l'entorn actual. Comprova el fitxer .env"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    ...

