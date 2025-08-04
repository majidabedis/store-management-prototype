from typing import Dict, List, Optional
from Database.repositories.interface import IRepository
from Database.db.connection_manager import DatabaseManager


class Cart_Item_Repository(IRepository):
    def __init__(self):
        self.table_name = "cart_item"
        self.db = DatabaseManager()

    def get_by_cart_id_and_product_id(self, cart_id: int | None, product_id: int) -> Optional[Dict] | None:
        if cart_id:
            data = self.get_by_id(cart_id)
            return data
        elif product_id:
            data = self.get_by_id(product_id)
            return data
        else:
            return None

    def get_all(self) -> List[Dict]:
        return self.db.read_data(self.table_name)

    def get_by_id(self, cart_id: int) -> Optional[Dict]:
        result = self.db.read_data(self.table_name, condition=f"cart_id = {cart_id}")
        return result if result else None

    def add(self, data: Dict) -> Optional[int]:

        columns = list(data.keys())
        values = list(data.values())
        self.db.insert_data(self.table_name, columns, values)
        return self.db.get_last_insert_id()

    def update_cart(self, cart_item_id: int, updates: Dict) -> bool:
        condition = f"cart_item_id = {cart_item_id}"
        self.db.update_data(self.table_name, updates, condition)
        return True

    def update_cart_item(self, cart_item_id: int, updates: Dict) -> bool:
        condition = f"cart_item_id = {cart_item_id}"
        self.db.update_data(self.table_name, updates, condition)
        return True

    def remove(self, cart_id: int) -> bool:
        condition = f"cart_id = {cart_id}"
        self.db.delete_data(self.table_name, condition)
        return True

    def get_by_user_id(self, user_id: int) -> Optional[Dict]:
        result = self.db.read_data(self.table_name, condition=f"customer_id = {user_id}")
        return result[0] if result else None

    def get_by_cart_id(self, cart_id: int) -> Optional[Dict]:
        condition = f"cart_id = {cart_id}"
        result = self.db.read_data(self.table_name, "*", condition)
        return result if result else None

    def get_by_cart_stock_id(self, stock_id: int) -> Optional[Dict]:
        condition = f"stock_id = {stock_id}"
        result = self.db.read_data(self.table_name, "*", condition)
        return result if result else None

    def get_by_cart_item_id(self, cart_item_id):
        condition = f"cart_item_id = {cart_item_id}"
        result = self.db.read_data(self.table_name, "*", condition)
        return result if result else None

    def clear_cart(self, user_id: int) -> bool:
        cart = self.get_by_user_id(user_id)
        if cart:
            return self.update(cart['id'], {'items': []})
        return False

    def clear_cart_item(self, cart_item_id: int) -> bool:
        return self.db.delete_data(self.table_name, f"cart_item_id = {cart_item_id}") if cart_item_id else False
