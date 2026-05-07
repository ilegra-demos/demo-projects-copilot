from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Payload para criar uma nova tarefa."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)


class TaskUpdate(BaseModel):
    """Payload para atualizar uma tarefa existente."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: Optional[bool] = None


class Task(BaseModel):
    """Representação completa de uma tarefa."""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime
