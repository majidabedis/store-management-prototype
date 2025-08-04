from typing import Dict, List, Optional
from Database.repositories.interface import IRepository
from Database.db.connection_manager import DatabaseManager


class OrderItemRepository(IRepository):
    def __init__(self):
        self.table_name = "order_item"
        self.db = DatabaseManager()

    def get_all(self) -> List[Dict]:
        return self.db.read_data(self.table_name)

    def get_by_id(self, order_id: int) -> Optional[Dict]:
        result = self.db.read_data(self.table_name, condition=f"order_id = {order_id}")
        return result[0] if result else None

    def add(self, data: Dict) -> Optional[int]:
        columns = list(data.keys())
        values = list(data.values())
        self.db.insert_data(self.table_name, columns, values)
        return self.db.get_last_insert_id()

    def update(self, order_id: int, updates: Dict) -> bool:
        condition = f"id = {order_id}"
        self.db.update_data(self.table_name, updates, condition)
        return True

    def delete(self, order_id: int) -> bool:
        condition = f"id = {order_id}"
        self.db.delete_data(self.table_name, condition)
        return True
    def get_seller_orders(self, stock_id) -> List[Dict]:
        return self.db.read_data(self.table_name, condition=f"stock_id = '{stock_id}'")
