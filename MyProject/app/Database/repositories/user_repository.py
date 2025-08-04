import json
import logging
from Domains.users import User, customer, seller, Employee
from Database.repositories.interface import IRepository
import os
from Database.db.connection_manager import DatabaseManager

logging.basicConfig(level=logging.INFO)


class UserRepository(IRepository):
    def __init__(self):
        self._user_classes = {
            "customer": customer,
            "seller": seller,
            "Employee": Employee
        }
        self.db = DatabaseManager()

        # ********************  USER MANAGE REPOSITORY  *****************

    def add_person(self, data: dict):
        category_mapping = {
            "customer": " customer",
            "seller": "seller",
            "employee": "employee"
        }
        table = category_mapping.get(data.get("position"))
        if not table:
            print("خطا : دسته بندی وجود ندارد ")
            return None
        try:
            return self.db.insert_data(table, data.keys(), tuple(data.values()))

        except Exception as e:
            print("error")
            print(f"Error inserting product: {e}")
            if self.db.connection:
                self.db.connection.rollback()
            return None

    def get_person(self, position: str, condition: str = None):
        table = position.lower()
        try:
            result = self.db.read_data(table, '*', condition)
            return result
        except Exception as e:
            print(f"Error reading {position}: {e}")
            return None

    def update_person(self, position: str, update_values: dict, condition: str):
        table = position.lower()
        try:
            self.db.update_data(table, update_values, condition)
            return True
        except Exception as e:
            print(f"Error updating {position}: {e}")
            if self.db.connection:
                self.db.connection.rollback()
            return False

    def delete_person(self, position: str, condition: str):
        table = position.lower()
        try:
            self.db.delete_data(table, condition)
            return True
        except Exception as e:
            print(f"Error deleting {position}: {e}")
            if self.db.connection:
                self.db.connection.rollback()
            return False

    def _create_user_from_dict(self, user_data):
        position = user_data.get("position")
        user_class = self._user_classes.get(position)
        if not user_class:
            logging.error(f"Invalid user position: {position}")
            return None
        user = user_class()
        user.id = user_data.get("id")
        username = user_data.get("username")
        email = user_data.get("email")
        if not username and not email:
            logging.error("Both username and email are missing")
            return None
        user.username = username if username else email
        user.email = email if email else username
        user.status = user_data.get("status", user.STATUS_PENDING)
        print(user.__dict__)
        return user

    # def update_user(self, user_id, data):
    #     connection = self.db.connect()
    #     cursor = connection.cursor()
    #     update_query = "UPDATE users SET " + ", ".join(f"{key} = %s" for key in data.keys()) + " WHERE id = %s"
    #     values = list(data.values()) + [user_id]
    #     cursor.execute(update_query, values)
    #     connection.commit()
    #     cursor.close()
    #     connection.close()
