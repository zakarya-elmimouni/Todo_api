from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Task(Base): # task hérite de Base, la classe Task devient officiellement un modèle SQLAlchemy
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False) # nullable=False → cette colonne est obligatoire, on ne peut pas créer une tâche sans titre.
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)