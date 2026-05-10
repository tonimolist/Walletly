"""
--- EL SELECTOR D'ENTORNS ---

- La funció de config.py és dir-li a l'aplicació on ha d'anar a buscar les dades segons el que estiguis fent.
- És com un interruptor: si estàs provant coses, fa servir una base de dades de "mentida"; si estàs treballant seriosament, fa servir la de "veritat".
- Serveix per a que no hagis de canviar rutes a mà cada vegada que mous el projecte de lloc.

# 2. Explicació clara del que fa el codi
    -- LLEGIR EL FITXER SECRET (.env): La funció load_dotenv() obre un fitxer on guardem les adreces de les bases de dades per a que ningú les vegi.
    -- SABER ON SOM: La variable ENVIRONMENT mira si estem a l'ordinador de programar (development) o en un servidor real (production).
    -- TRIAR LA CARRETERA CORRECTA: Segons l'entorn, DB_URL agafa l'adreça que toca. Així no barregem dades de prova amb dades reals.
    -- PROTEGIR LA INFORMACIÓ: Com que les rutes no estan escrites directament aquí, el teu codi és més segur i net.

- ENVIRONMENT: El nom de l'escenari on estem treballant ara mateix.
- load_dotenv: El mètode que llegeix el fitxer de configuració externa.
- os.getenv: L'eina que busca una dada concreta (com l'adreça de la base de dades) dins del sistema.
- DB_URL: El resultat final; la ruta exacta que l'app farà servir per connectar-se.
"""

import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

DB_URL = {
    "development": os.getenv("DB_URL_DEVELOPMENT"),
    "test": os.getenv("DB_URL_TEST"),
    "production": os.getenv("DB_URL_PRODUCTION")
}.get(ENVIRONMENT)

