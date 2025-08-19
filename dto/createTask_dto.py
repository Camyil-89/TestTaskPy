from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class CreateTaskDTO(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = datetime.now()
    expires_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Преобразует модель в словарь для сохранения в БД"""
        return self.model_dump(mode='json')  # mode='json' — гарантирует, что datetime станет строкой

    @classmethod
    def from_dict(cls, data: dict) -> 'CreateTaskDTO':
        """Создаёт экземпляр Task из словаря (например, из БД)"""
        return cls(**data)  # Pydantic сам преобразует ISO-строки в datetime!