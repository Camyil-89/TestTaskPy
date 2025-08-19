from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class DatabaseInterface(ABC):
    @abstractmethod
    def insert(self, data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def all(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def update(self, updates: Dict[str, Any], query: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def delete(self, query: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def close(self):
        pass