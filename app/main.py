from typing import List

from fastapi import FastAPI, HTTPException, status

from app.models import Task, TaskCreate, TaskUpdate
from app.storage import storage

app = FastAPI(
    title="API de Tarefas",
    description="API simples de gestão de tarefas. Demo de fluxo AI-First com agentes.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
    return storage.create(payload)


@app.get("/tasks", response_model=List[Task])
def list_tasks() -> List[Task]:
    return storage.list_all()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    task = storage.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return task


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate) -> Task:
    task = storage.update(task_id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> None:
    if not storage.delete(task_id):
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
