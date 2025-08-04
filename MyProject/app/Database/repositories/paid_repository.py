from typing import Dict, List, Optional
from Database.repositories.interface import IRepository
from Database.db.connection_manager import DatabaseManager


class PaidRepository(IRepository):
    def __init__(self):
        self.table_name = "payment"
        self.db = DatabaseManager()

    def get_all(self) -> List[Dict]:
        return self.db.read_data(self.table_name)

    def get_by_id(self, payment_id: int) -> List[Dict]:
        condition = f"payment_id = {payment_id}"
        result = self.db.read_data(self.table_name, "*", condition)
        return result if result else None

    def add(self, data: Dict) -> Optional[int]:
        columns = list(data.keys())
        values = list(data.values())
        last_id = self.db.insert_data(self.table_name, columns, values)
        return last_id if last_id else 0

    def update(self, payment_id: int, updates: Dict) -> bool:
        condition = f"id = {payment_id}"
        self.db.update_data(self.table_name, updates, condition)
        return True

    def delete(self, payment_id: int) -> bool:
        condition = f"id = {payment_id}"
        self.db.delete_data(self.table_name, condition)
        return True
