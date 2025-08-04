from typing import List, Dict, Optional
from Database.repositories.warehouse_repository import WarehouseRepository


class WarehouseService:
    def __init__(self):
        self.warehouse_repository = WarehouseRepository()

    def create_warehouse(self, data: Dict) -> None:
        self.warehouse_repository.add(data)

    def update_warehouse(self, warehouse_id: int, updates) -> bool:
        return self.warehouse_repository.update(warehouse_id, updates)

    def delete_warehouse(self, warehouse_id) -> bool:
        return self.warehouse_repository.delete(warehouse_id)

    def get_all_warehouse(self) -> List[Dict]:
        return self.warehouse_repository.get_all()

    def get_warehouse_by_id(self, warehouse_id: int) -> Optional[Dict] | None:

        data = self.warehouse_repository.get_by_id(warehouse_id)
        if data is None:
            print("آیدی انبار مورد نظر وجود ندارد")
            return
        return data
