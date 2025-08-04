# from Database.db.connection_manager import DatabaseManager
# import mysql.connector
# from typing import List, Dict, Optional
# from Application.services.product_service import ProductService
# from Database.repositories.product_repository import ProductRepository
#
# product_service = ProductService()
# product_repository = ProductRepository()
#
#
# def get_product_by_id(product_id: int, category) -> Optional[Dict]:
#     """get product by idه"""
#     try:
#         # for category in ["camera", "mobile", "laptop"]:
#         products = product_repository.read_product(
#             category, f"{category}_id = {product_id}"
#         )
#         if products:
#             return products[0]
#         return None
#     except Exception as e:
#         print(f"خطا در دریافت محصول: {e}")
#         return None
#
# no = 60000001//1_000_000
# print(no)
# # id = get_product_by_id(96000001, "camera")
# # print(id)
# #
# from Database.db.connection_manager import DatabaseManager
# db = DatabaseManager()
# db.connect()
import mysql.connector

# اتصال به دیتابیس
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="majid6175",
    database="erp"
)

cursor = conn.cursor()

# گرفتن لیست جدول‌ها
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

# گرفتن کوئری ساخت هر جدول
with open("create_tables.sql", "w", encoding="utf-8") as f:
    for (table_name,) in tables:
        cursor.execute(f"SHOW CREATE TABLE {table_name}")
        result = cursor.fetchone()
        create_stmt = result[1]
        print(f"-- Table: {table_name}\n{create_stmt}\n")
        f.write(f"-- Table: {table_name}\n{create_stmt};\n\n")

cursor.close()
conn.close()
