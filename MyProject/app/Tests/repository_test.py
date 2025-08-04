# import os
# from utils.input_utils import get_common_fields
# from Domains.users.base_user import Customer, Seller, Employee
# from Application.services.user_service import UserService, AdminSercvice
# from Database.repositories.user_repository import UserRepository
# from Database.db.connection_manager import DatabaseManager
# employee = Employee()
# repo = UserRepository()
# service = UserService(repo)
# admin = AdminSercvice(repo)
# (employee.name, employee.family, employee.email, employee.password, employee.mobile, employee.birthday
#  , employee.address, gender) = get_common_fields()
# employee.status = employee.activate()
# employee.username = employee.email.split("@")[0]
# data = employee.to_dict()
# service.add_user(employee)
from typing import Dict, List

from Database.db.connection_manager import DatabaseManager
import mysql.connector

db = DatabaseManager()


# connection = db.connect()
# cursor = connection.cursor()


def get_all_products() -> List[Dict]:
    try:
        product_id = 1
        name = "mobile"
        condition = f"name = '{name}'"

        products = db.read_data("product", "*", condition)
        return products
    except Exception as e:
        print(f"خطا در دریافت لیست محصولات: {e}")
        return []


data = get_all_products()
print(data)
#
# def get_person(position: str, condition: str = None):
#     table = position.lower()
#     try:
#         result = db.read_data(table, '*', condition)
#         print(result)
#         return result
#     except mysql.connector.Error as err:
#         print(f"Error reading {position}: {err}")
#         return None
#
#
# position = "customer"
# get_person(position)
