from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    id: int
    completed: bool

    class Config:
        from_attributes = True  #c'est ce qui permet à Pydantic de lire directement un objet
        #SQLAlchemy (ex: task.title, task.id) et de le convertir en JSON, au lieu d'exiger un dictionnaire.
        #  Sans ça, FastAPI ne saurait pas transformer l'objet Task (venant de la base) en réponse JSON.