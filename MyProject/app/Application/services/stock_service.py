from typing import List, Dict, Optional
from Database.repositories.stock_repository import StockRepository
from Domains.FieldValidatorMixin import FieldValidatorMixin


class StockService:
    def __init__(self):
        self.stock_repository = StockRepository()

    def add_stock(self, data: Dict) -> None:
        if data is None:
            print("data is None in warehouse service")
        self.stock_repository.add(data)

    def update_stock(self, stock_id: int = None, updates: dict = None) -> bool:
        return self.stock_repository.update(stock_id, updates)

    def delete_stock(self, warehouse_id) -> bool:
        return self.stock_repository.delete(warehouse_id)

    def get_all_stock(self) -> List[Dict]:
        return self.stock_repository.get_all()

    def get_stock_by_id(self, stock_id: int) -> Optional[Dict] | None:
        data = self.stock_repository.get_by_stock_id(stock_id)
        return data if data else None

    def get_stock_by_product(self, product_id: int) -> Optional[Dict]:
        data = self.stock_repository.get_by_product_id(product_id)
        return data if data else None

    def get_stock_by_seller_id(self, seller_id: int) -> Optional[Dict]:
        data = self.stock_repository.get_by_seller_id(seller_id)
        return data if data else None

