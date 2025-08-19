import pytest
from fastapi.testclient import TestClient

# Импортируем приложение и зависимости
from main import app, db, manager


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_database():
    """Очищает TinyDB перед каждым тестом"""
    db.db.truncate()


@pytest.fixture
def sample_task_data():
    return {
        "title": "Test Task",
        "description": "A task for testing",
        "expires_at": "2025-12-31T10:00:00"
    }