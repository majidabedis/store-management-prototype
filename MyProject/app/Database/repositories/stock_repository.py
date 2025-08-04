from typing import Dict, List, Optional
from Database.repositories.interface import IRepository
from Database.db.connection_manager import DatabaseManager


class StockRepository(IRepository):
    def __init__(self):
        self.table_name = "stock"
        self.db = DatabaseManager()

    def get_all(self) -> List[Dict]:
        return self.db.read_data(self.table_name)

    def get_by_product_id(self, product_id: int) -> Optional[Dict]:
        result = self.db.read_data(self.table_name, condition=f"product_id = {product_id}")
        return result if result else None

    def get_by_seller_id(self, seller_id: int) -> Optional[Dict]:
        result = self.db.read_data(self.table_name, condition=f"seller_id = {seller_id}")
        return result if result else None

    def add(self, data: Dict) -> Optional[int]:
        columns = list(data.keys())
        values = list(data.values())
        self.db.insert_data(self.table_name, columns, values)
        return self.db.get_last_insert_id()

    def update(self, stock_id: int, updates: Dict ) -> bool:
        condition = f"stock_id = {stock_id} "
        self.db.update_data(self.table_name, updates, condition)
        return True

    def delete(self, stock_id: int) -> bool:
        condition = f"stock_id = {stock_id}"
        self.db.delete_data(self.table_name, condition)
        return True

    def get_by_stock_id(self, stock_id: int) -> List[Dict]:
        return self.db.read_data(self.table_name, condition=f"stock_id = {stock_id}")

    def update_stock(self, warehouse_id=None, product_id=None, seller_id=None, updates: dict = None) -> None:
        return self.db.update_data(warehouse_id, product_id, seller_id, updates)
