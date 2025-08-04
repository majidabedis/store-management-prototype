from typing import Dict, List, Optional
from Database.repositories.interface import IRepository
from Database.db.connection_manager import DatabaseManager


class OrderRepository(IRepository):
    def __init__(self):
        self.table_name = "orders"
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
        condition = f"order_id = {order_id}"
        self.db.update_data(self.table_name, updates, condition)
        return True

    def delete(self, order_id: int) -> bool:
        condition = f"order_id = {order_id}"
        self.db.delete_data(self.table_name, condition)
        return True

    def get_by_user_id(self, user_id: int) -> List[Dict]:
        return self.db.read_data(self.table_name, condition=f"customer_id = {user_id}")

    def get_by_status(self, status: str) -> List[Dict]:
        return self.db.read_data(self.table_name, condition=f"status = '{status}'")

    def get_seller_orders(self, stock_id) -> List[Dict]:
        return self.db.read_data(self.table_name, condition=f"stock_id = '{stock_id}'")

    def get_pending_orders(self) -> List[Dict]:
        return self.get_by_status('pending')

    def get_paid_orders(self) -> List[Dict]:
        return self.get_by_status('paid')

    def get_shipping_orders(self) -> List[Dict]:
        return self.get_by_status('shipping')

    def get_delivered_orders(self) -> List[Dict]:
        return self.get_by_status('delivered')

    def get_cancelled_orders(self) -> List[Dict]:
        return self.get_by_status('cancelled')
