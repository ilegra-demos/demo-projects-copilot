import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import storage


@pytest.fixture(autouse=True)
def reset_storage():
    """Garante storage limpo entre testes."""
    storage.reset()
    yield
    storage.reset()


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    response = client.post(
        "/tasks",
        json={"title": "Comprar pão", "description": "Padaria da esquina"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Comprar pão"
    assert body["description"] == "Padaria da esquina"
    assert body["completed"] is False
    assert "created_at" in body


def test_list_tasks_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_after_create():
    client.post("/tasks", json={"title": "Tarefa 1"})
    client.post("/tasks", json={"title": "Tarefa 2"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task():
    create = client.post("/tasks", json={"title": "Tarefa específica"})
    task_id = create.json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Tarefa específica"


def test_get_task_not_found():
    response = client.get("/tasks/9999")
    assert response.status_code == 404


def test_update_task():
    create = client.post("/tasks", json={"title": "Original"})
    task_id = create.json()["id"]
    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Atualizada", "completed": True},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Atualizada"
    assert body["completed"] is True


def test_delete_task():
    create = client.post("/tasks", json={"title": "Para deletar"})
    task_id = create.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_create_task_validation():
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422
