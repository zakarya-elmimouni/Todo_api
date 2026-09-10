from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, crud
from app.database import engine, get_db

# Crée les tables dans la base au démarrage, si elles n'existent pas déjà.
# Équivalent d'exécuter "CREATE TABLE IF NOT EXISTS ..." pour chaque modèle défini dans models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API")


@app.get("/")
def root():
    return {"message": "Todo API is running"}


@app.get("/tasks", response_model=List[schemas.TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    updated = crud.update_task(db, task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return None