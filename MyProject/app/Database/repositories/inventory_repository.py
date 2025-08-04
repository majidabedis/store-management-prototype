from typing import Dict, List, Optional
from Database.repositories.interface import IRepository
from Database.db.connection_manager import DatabaseManager


class InventoryRepository(IRepository):
    def __init__(self):
        self.db = DatabaseManager()

    pass
