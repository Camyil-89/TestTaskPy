# models.py
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import uuid


class Task(BaseModel):
    title: str
    id: str = f"{uuid.uuid4()}"
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = datetime.now()
    expires_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return self.model_dump(mode='json')  # mode='json' — гарантирует, что datetime станет строкой

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        return cls(**data)
