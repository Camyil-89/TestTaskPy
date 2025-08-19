import pytest
from datetime import datetime


def test_create_task(client, sample_task_data):
    """Тест: создание задачи"""
    response = client.post("/tasks/", json=sample_task_data)

    assert response.status_code == 201
    data = response.json()

    assert data["title"] == sample_task_data["title"]
    assert data["description"] == sample_task_data["description"]
    assert "id" in data
    assert "created_at" in data
    # Проверим, что expires_at корректно распарсился
    if sample_task_data["expires_at"]:
        assert data["expires_at"] == sample_task_data["expires_at"]


def test_create_task_missing_title(client):
    """Тест: ошибка при отсутствии title"""
    response = client.post("/tasks/", json={"description": "No title"})
    assert response.status_code == 422  # Validation Error
    assert "title" in str(response.json())


def test_get_task_by_id(client, sample_task_data):
    """Тест: получение задачи по ID"""
    # Сначала создаём
    create_response = client.post("/tasks/", json=sample_task_data)
    task_id = create_response.json()["id"]

    # Получаем по ID
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == sample_task_data["title"]


def test_get_task_not_found(client):
    """Тест: задача не найдена"""
    response = client.get("/tasks/nonexistent-id")
    assert response.status_code == 404


def test_update_task(client, sample_task_data):
    """Тест: обновление задачи"""
    create_response = client.post("/tasks/", json=sample_task_data)
    task_id = create_response.json()["id"]

    updated_data = {
        "title": "Updated Task",
        "description": "Updated description"
    }

    response = client.put(f"/tasks/{task_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated description"


def test_update_task_not_found(client):
    """Тест: обновление несуществующей задачи"""
    response = client.put("/tasks/unknown-id", json={"title": "New"})
    assert response.status_code == 404


def test_delete_task(client, sample_task_data):
    """Тест: удаление задачи"""
    create_response = client.post("/tasks/", json=sample_task_data)
    task_id = create_response.json()["id"]

    # Удаляем
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    # Проверяем, что больше не существует
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    """Тест: удаление несуществующей задачи"""
    response = client.delete("/tasks/unknown-id")
    assert response.status_code == 404


def test_search_tasks(client, sample_task_data):
    """Тест: поиск задач по названию"""
    client.post("/tasks/", json=sample_task_data)
    client.post("/tasks/", json={"title": "Another task"})

    # Поиск по "Test"
    response = client.get("/tasks/?title=Test")

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert len(data["items"]) == 1
    assert "Test" in data["items"][0]["title"]

    # Поиск по "task" — должно быть 2
    response = client.get("/tasks/?title=task")
    data = response.json()
    assert data["count"] == 2

    # Поиск по "xyz" — 0
    response = client.get("/tasks/?title=xyz")
    data = response.json()
    assert data["count"] == 0
    assert len(data["items"]) == 0


def test_search_with_pagination(client):
    """Тест: пагинация в поиске"""
    # Создаём 5 задач
    for i in range(5):
        client.post("/tasks/", json={"title": f"Task {i}"})

    # Лимит 2, смещение 0
    response = client.get("/tasks/?limit=2&offset=0")
    data = response.json()

    assert len(data["items"]) == 2
    assert data["count"] == 5

    # Лимит 2, смещение 2
    response = client.get("/tasks/?limit=2&offset=2")
    data = response.json()
    assert len(data["items"]) == 2
    assert data["items"][0]["title"] == "Task 2"