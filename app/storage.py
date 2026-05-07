from datetime import datetime
from typing import Dict, List, Optional

from app.models import Task, TaskCreate, TaskUpdate


class TaskStorage:
    """Armazenamento in-memory de tarefas. Suficiente para o demo."""

    def __init__(self) -> None:
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def create(self, payload: TaskCreate) -> Task:
        task = Task(
            id=self._next_id,
            title=payload.title,
            description=payload.description,
            completed=False,
            created_at=datetime.utcnow(),
        )
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def list_all(self) -> List[Task]:
        return list(self._tasks.values())

    def get(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def update(self, task_id: int, payload: TaskUpdate) -> Optional[Task]:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        data = task.model_dump()
        for field, value in payload.model_dump(exclude_unset=True).items():
            data[field] = value
        updated = Task(**data)
        self._tasks[task_id] = updated
        return updated

    def delete(self, task_id: int) -> bool:
        return self._tasks.pop(task_id, None) is not None

    def reset(self) -> None:
        """Apenas para testes."""
        self._tasks.clear()
        self._next_id = 1


storage = TaskStorage()
