from Database.db.connection_manager import DatabaseManager
from typing import Dict, List, Optional
from Database.repositories.interface import IRepository


class RunSystemRepository(IRepository):
    def __init__(self):
        self.db = DatabaseManager()

    def create_data_base(self):
        data_base = self.db.create_database()
        return data_base if True else False
