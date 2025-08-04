from typing import List, Dict, Optional
from Database.repositories.run_system_repository import RunSystemRepository


class RunSystemService:
    def __init__(self):
        self.run_system_repository = RunSystemRepository()

    def create_data_base(self):
        data_base = self.run_system_repository.create_data_base()
        return data_base if True else False
