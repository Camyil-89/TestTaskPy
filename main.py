# main.py
from fastapi import FastAPI, HTTPException, Query
from db.tasks_schemas import Task
from dto.createTask_dto import CreateTaskDTO
from typing import List
from services.db_service import TaskManagerService
from db.db_provider import TinyDBAdapter
from services.db_service import PaginatedResponse

app = FastAPI()

# Инициализация
db = TinyDBAdapter(db_path="./db/tinydb.db")
manager = TaskManagerService(db)


@app.post("/tasks/", response_model=Task, status_code=201)
def create_task(task_dto: CreateTaskDTO):
    """Создать новую задачу."""
    try:
        task = manager.add(task_dto)
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании задачи: {str(e)}")


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    """Получить задачу по ID."""
    try:
        return manager.get_by_id(task_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении задачи: {str(e)}")


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task_dto: CreateTaskDTO):
    """Обновить задачу по ID."""
    try:
        return manager.update(task_id, task_dto)
    except KeyError:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении: {str(e)}")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):
    """Удалить задачу по ID."""
    try:
        manager.delete(task_id)
        return  # 204 No Content
    except KeyError:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {str(e)}")


@app.get("/tasks/", response_model=PaginatedResponse)
def search_tasks(
    title: str = Query(None, description="Поиск по названию (частичное совпадение)"),
    limit: int = Query(10, ge=1, le=100, description="Количество задач на странице"),
    offset: int = Query(0, ge=0, description="Смещение (пагинация)")
):
    """
    Поиск задач по названию с пагинацией.
    """
    try:
        return manager.search(title=title, limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при поиске: {str(e)}")
