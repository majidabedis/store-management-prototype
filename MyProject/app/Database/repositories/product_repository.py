from Database.db.connection_manager import DatabaseManager
import mysql.connector
from typing import List, Dict, Optional
from Database.repositories.interface import IRepository


class ProductRepository(IRepository):
    def __init__(self):
        self.db = DatabaseManager
        self.table = 'product'
        self.temp_table = 'product_temp'

    def add_product(self, data: dict):
        try:
            self.db.insert_data(self.table, data.keys(), tuple(data.values()))
            return self.db.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error inserting product: {err}")
            if self.db.connection:
                self.db.connection.rollback()
            return None

    def add_product_temp(self, data: dict):
        try:
            self.db.insert_data(self.temp_table, data.keys(), tuple(data.values()))
            return self.db.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error inserting product: {err}")
            if self.db.connection:
                self.db.connection.rollback()
            return None

    def read_product(self, condition: str = None) -> List[dict]:
        return self.db.read_data(self.table, "*", condition)

    def read_product_temp(self, condition: str = None) -> List[dict]:
        return self.db.read_data(self.temp_table, "*", condition)

    def update_product(self, update_values: dict, condition: str):
        try:
            self.db.update_data(self.table, update_values, condition)
            return True
        except mysql.connector.Error as err:
            print(f"Error updating product: {err}")
            return False

    def update_product_temp(self, update_values: dict, condition: str):
        try:
            self.db.update_data(self.temp_table, update_values, condition)
            return True
        except mysql.connector.Error as err:
            print(f"Error updating product: {err}")
            return False

    def delete_product(self, condition: str):

        try:
            self.db.delete_data(self.table, condition)
            return True
        except mysql.connector.Error as err:
            print(f"Error deleting product: {err}")
            return False

    def delete_product_temp(self, condition: str):
        try:
            self.db.delete_data(self.temp_table, condition)
            return True
        except mysql.connector.Error as err:
            print(f"Error deleting product: {err}")
            return False
