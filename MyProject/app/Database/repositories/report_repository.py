from typing import Dict, List, Optional
from Database.repositories.interface import IRepository
from Database.db.connection_manager import DatabaseManager


class ReportRepository(IRepository):
    def __init__(self):
        self.db = DatabaseManager()

    def create_report(self, table: str = None, columns: list = None, joins: list = None, filters: list = None):
        return self.db.generic_sql_fetch(table, columns, joins, filters)
