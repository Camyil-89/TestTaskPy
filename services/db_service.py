# services/task_manager_service.py
from typing import List, Optional
from pydantic import BaseModel
from db.tasks_schemas import Task
from dto.createTask_dto import CreateTaskDTO
from db.db_interface import DatabaseInterface


class PaginatedResponse(BaseModel):
    items: List[Task]
    count: int

class TaskManagerService:
    def __init__(self, db: DatabaseInterface):
        self.db = db

    def add(self, task_dto: CreateTaskDTO) -> Task:
        # Создаём задачу — id генерируется автоматически
        task = Task(**task_dto.to_dict())
        # Сохраняем в БД
        self.db.insert(task.to_dict())
        return task

    def get_all(self) -> List[Task]:
        tasks_data = self.db.all()
        return [Task(**task) for task in tasks_data]

    def get_by_id(self, task_id: str) -> Task:
        task_data = self.db.get({"id": task_id})
        if not task_data:
            raise KeyError(f"Task with id {task_id} not found")
        return Task(**task_data)

    def update(self, task_id: str, task_dto: CreateTaskDTO) -> Task:
        if not self.db.get({"id": task_id}):
            raise KeyError(f"Task with id {task_id} not found")

        # Обновляем данные: сохраняем id, перезаписываем остальное
        updated_data = task_dto.to_dict()
        updated_data["id"] = task_id  # гарантируем, что id не потеряется

        success = self.db.update(updates=updated_data, query={"id": task_id})
        if not success:
            raise RuntimeError("Failed to update task")

        return Task(**updated_data)

    def delete(self, task_id: str) -> bool:
        if not self.db.get({"id": task_id}):
            raise KeyError(f"Task with id {task_id} not found")
        return self.db.delete({"id": task_id})

    def search(
            self,
            title: Optional[str] = None,
            limit: int = 10,
            offset: int = 0
    ) -> PaginatedResponse:
        all_tasks = self.db.all()
        # Фильтрация по названию
        filtered_tasks = all_tasks
        if title is not None and title.strip() != "":
            title_lower = title.lower().strip()
            filtered_tasks = [
                task for task in all_tasks
                if task.get("title") and title_lower in task["title"].lower()
            ]

        # Подсчёт общего количества
        total_count = len(filtered_tasks)

        # Пагинация
        start = offset
        end = offset + limit
        paginated_tasks = filtered_tasks[start:end]

        # Преобразуем в модели Task
        task_models = [Task(**task) for task in paginated_tasks]

        return PaginatedResponse(items=task_models, count=total_count)