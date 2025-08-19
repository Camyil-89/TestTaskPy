# tinydb_adapter.py
from tinydb import TinyDB, Query
from typing import List, Dict, Any, Optional
from .db_interface import DatabaseInterface

'''
TinyDB - использовалось потому что нет необходимости в более тяжелых решениях как SQL или NoSQL базы такие как mongodb
'''
class TinyDBAdapter(DatabaseInterface):
    def __init__(self, db_path: str):
        self.db = TinyDB(db_path)
        self.query = Query()

    def insert(self, data: Dict[str, Any]) -> None:
        self.db.insert(data)  # data уже содержит 'id'

    def get(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.db.get(self.query.fragment(query))

    def all(self) -> List[Dict[str, Any]]:
        return self.db.all()

    def update(self, updates: Dict[str, Any], query: Dict[str, Any]) -> bool:
        count = self.db.update(updates, self.query.fragment(query))
        return len(count) > 0

    def delete(self, query: Dict[str, Any]) -> bool:
        count = self.db.remove(self.query.fragment(query))
        return len(count) > 0

    def close(self):
        self.db.close()