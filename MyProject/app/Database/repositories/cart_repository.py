from typing import Dict, List, Optional
from Database.repositories.interface import IRepository
from Database.db.connection_manager import DatabaseManager


class CartRepository(IRepository):
    def __init__(self):
        self.table_name = "cart"
        self.db = DatabaseManager()

    def get_all(self) -> List[Dict]:
        return self.db.read_data(self.table_name)

    def get_by_id(self, user_id: int) -> Optional[Dict]:
        result = self.db.read_data(self.table_name, condition=f"customer_id = {user_id}")
        return result[0] if result else None

    def add(self, data: Dict) -> Optional[int]:
        columns = list(data.keys())
        values = list(data.values())
        self.db.insert_data(self.table_name, columns, values)
        return self.db.get_last_insert_id()

    def update(self, cart_id: int, updates: Dict) -> bool:
        condition = f"id = {cart_id}"
        self.db.update_data(self.table_name, updates, condition)
        return True

    def delete(self, cart_id: int) -> bool:
        condition = f"cart_id = {cart_id}"
        self.db.delete_data(self.table_name, condition)
        return True

    def get_by_user_id(self, user_id: int) -> Optional[Dict]:
        result = self.db.read_data(self.table_name, condition=f"customer_id = {user_id}")
        return result if result else None

    def clear_cart(self, user_id: int) -> bool:
        cart = self.get_by_user_id(user_id)
        if cart:
            return self.update(cart['id'], {'items': []})
        return False

    def join(self,  table: str, columns: list = None, joins: list = None, filters: list = None):
        data = self.db.generic_sql_fetch(table, columns, joins, filters)
        return data if data else None


