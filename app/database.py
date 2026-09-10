import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# On lit l'URL de connexion depuis une variable d'environnement.
# C'est LA pratique clé pour Docker : jamais d'URL en dur dans le code,
# car l'adresse de la DB change entre "en local" et "dans un conteneur".
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db") # Si la variable d'environnement n'est pas définie, on utilise une base SQLite locale par défaut.

engine = create_engine(DATABASE_URL) # connecte SQLAlchemy à la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # crée une session pour interagir avec la base de données
Base = declarative_base() # crée la classe de base pour les modèles


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()