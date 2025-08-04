import mysql.connector
from typing import Dict, List, Optional, Any, Tuple


def ensure_connection(func):
    def wrapper(*args, **kwargs):
        if DatabaseManager.connection is None or DatabaseManager.cursor is None:
            DatabaseManager.connect()
        return func(*args, **kwargs)

    return wrapper


class DatabaseManager:
    connection = None
    cursor = None

    @staticmethod
    def connect():
        try:
            DatabaseManager.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="majid6175",
                database="erp"
            )
            DatabaseManager.cursor = DatabaseManager.connection.cursor()
            print("Connected to MySQL Database")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    @staticmethod
    def ensure_connections():
        if DatabaseManager.connection is None or DatabaseManager.cursor is None:
            DatabaseManager.connect()

    @staticmethod
    def create_database() -> bool:
        try:
            query = "CREATE DATABASE erp"
            data_base = DatabaseManager.cursor.execute(query)
            DatabaseManager.connection.commit()
            if data_base:
                print("Database created successfully")
                tabels = """
                USE ERP;
                      -- Table: cart
                CREATE TABLE `cart` (
                  `cart_id` int NOT NULL AUTO_INCREMENT,
                  `customer_id` int NOT NULL,
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  PRIMARY KEY (`cart_id`),
                  KEY `customer_id` (`customer_id`),
                  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: cart_item
                CREATE TABLE `cart_item` (
                  `cart_item_id` int NOT NULL AUTO_INCREMENT,
                  `cart_id` int NOT NULL,
                  `product_id` int NOT NULL,
                  `stock_id` int NOT NULL,
                  `price` float NOT NULL,
                  `quantity` int NOT NULL,
                  `added_at` datetime DEFAULT CURRENT_TIMESTAMP,
                  PRIMARY KEY (`cart_item_id`),
                  KEY `cart_id` (`cart_id`),
                  KEY `product_id` (`product_id`),
                  KEY `cart_item_ibfk_2_idx` (`stock_id`),
                  CONSTRAINT `cart_item_ibfk_1` FOREIGN KEY (`cart_id`) REFERENCES `cart` (`cart_id`),
                  CONSTRAINT `cart_item_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
                  CONSTRAINT `cart_item_ibfk_3` FOREIGN KEY (`stock_id`) REFERENCES `stock` (`stock_id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: coupon
                CREATE TABLE `coupon` (
                  `coupon_id` int NOT NULL AUTO_INCREMENT,
                  `code` varchar(50) NOT NULL,
                  `description` text,
                  `discount_type` enum('percentage','amount') NOT NULL,
                  `discount_value` float NOT NULL,
                  `usage_limit` int DEFAULT NULL,
                  `used_count` int DEFAULT '0',
                  `start_date` datetime NOT NULL,
                  `end_date` datetime NOT NULL,
                  `is_active` tinyint(1) DEFAULT '1',
                  PRIMARY KEY (`coupon_id`),
                  UNIQUE KEY `code` (`code`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: customer
                CREATE TABLE `customer` (
                  `customer_id` int NOT NULL AUTO_INCREMENT,
                  `name` varchar(45) NOT NULL,
                  `family` varchar(45) NOT NULL,
                  `email` varchar(45) DEFAULT NULL,
                  `username` varchar(45) NOT NULL,
                  `password` varchar(255) NOT NULL,
                  `mobile` char(13) NOT NULL,
                  `birthday` varchar(50) NOT NULL,
                  `age` varchar(3) DEFAULT '0',
                  `address` varchar(255) NOT NULL,
                  `city` varchar(100) NOT NULL,
                  `gender` enum('male','female','unisex') NOT NULL,
                  `position` varchar(20) DEFAULT 'customer',
                  `register_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `digital_wallet` int NOT NULL,
                  `loyalty_points` int NOT NULL,
                  `favorite_sellers` json NOT NULL,
                  `order_history` json NOT NULL,
                  `addresses` json NOT NULL,
                  `status` varchar(25) DEFAULT NULL,
                  PRIMARY KEY (`customer_id`),
                  UNIQUE KEY `user_name` (`username`),
                  UNIQUE KEY `mobile` (`mobile`),
                  UNIQUE KEY `email` (`email`)
                ) ENGINE=InnoDB AUTO_INCREMENT=20000006 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: discount
                CREATE TABLE `discount` (
                  `discount_id` int NOT NULL AUTO_INCREMENT,
                  `name` varchar(100) NOT NULL,
                  `description` text,
                  `discount_type` enum('percentage','amount') NOT NULL,
                  `discount_value` float NOT NULL,
                  `start_date` datetime NOT NULL,
                  `end_date` datetime NOT NULL,
                  `is_active` tinyint(1) DEFAULT '1',
                  PRIMARY KEY (`discount_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: employee
                CREATE TABLE `employee` (
                  `employee_id` int NOT NULL AUTO_INCREMENT,
                  `name` varchar(45) NOT NULL,
                  `family` varchar(45) NOT NULL,
                  `email` varchar(45) DEFAULT NULL,
                  `username` varchar(45) NOT NULL,
                  `password` varchar(255) NOT NULL,
                  `mobile` char(13) NOT NULL,
                  `birthday` varchar(50) NOT NULL,
                  `age` int DEFAULT NULL,
                  `address` varchar(255) NOT NULL,
                  `city` varchar(100) NOT NULL,
                  `gender` enum('male','female','unisex') NOT NULL,
                  `position` varchar(20) DEFAULT 'employee',
                  `register_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `salary` float NOT NULL,
                  `department` varchar(50) NOT NULL,
                  `branch` varchar(45) NOT NULL,
                  `hire_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `attendance_records` json NOT NULL,
                  `status` varchar(25) DEFAULT 'active',
                  PRIMARY KEY (`employee_id`),
                  UNIQUE KEY `user_name` (`username`),
                  UNIQUE KEY `mobile` (`mobile`),
                  UNIQUE KEY `email` (`email`)
                ) ENGINE=InnoDB AUTO_INCREMENT=50000005 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: invoice
                CREATE TABLE `invoice` (
                  `invoice_id` int NOT NULL AUTO_INCREMENT,
                  `order_id` int NOT NULL,
                  `customer_id` int NOT NULL,
                  `total_item` int NOT NULL,
                  `total_amount` float NOT NULL,
                  `paid_id` int NOT NULL,
                  `paid_amount` float NOT NULL,
                  `payment_method` varchar(45) NOT NULL,
                  `invoice_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `status` varchar(45) NOT NULL DEFAULT 'pending',
                  PRIMARY KEY (`invoice_id`),
                  KEY `order_id` (`order_id`),
                  KEY `customer_id` (`customer_id`),
                  CONSTRAINT `invoice_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
                  CONSTRAINT `invoice_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: notifiction
                CREATE TABLE `notifiction` (
                  `noti_id` int NOT NULL AUTO_INCREMENT,
                  `user_id` int NOT NULL,
                  `title` varchar(50) NOT NULL,
                  `message` text NOT NULL,
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  PRIMARY KEY (`noti_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: order_item
                CREATE TABLE `order_item` (
                  `order_item_id` int NOT NULL AUTO_INCREMENT,
                  `order_id` int NOT NULL,
                  `product_id` int NOT NULL,
                  `stock_id` int NOT NULL,
                  `quantity` int NOT NULL,
                  `price` float NOT NULL,
                  PRIMARY KEY (`order_item_id`),
                  KEY `order_id` (`order_id`),
                  KEY `product_id` (`product_id`),
                  KEY `stock_id` (`stock_id`),
                  CONSTRAINT `order_item_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
                  CONSTRAINT `order_item_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
                  CONSTRAINT `stock_id` FOREIGN KEY (`stock_id`) REFERENCES `stock` (`stock_id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: orders
                CREATE TABLE `orders` (
                  `order_id` int NOT NULL AUTO_INCREMENT,
                  `cart_id` int NOT NULL,
                  `customer_id` int NOT NULL,
                  `total_items` int NOT NULL,
                  `total_amount` float NOT NULL,
                  `discount_amount` float DEFAULT '0',
                  `coupon_code` varchar(50) DEFAULT 'None',
                  `order_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `status` varchar(45) NOT NULL DEFAULT 'pending',
                  PRIMARY KEY (`order_id`),
                  KEY `cart_id` (`cart_id`),
                  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`cart_id`) REFERENCES `cart` (`cart_id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: payment
                CREATE TABLE `payment` (
                  `payment_id` int NOT NULL AUTO_INCREMENT,
                  `customer_id` int NOT NULL,
                  `order_id` int NOT NULL,
                  `paid_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `status` varchar(30) NOT NULL DEFAULT 'pending',
                  PRIMARY KEY (`payment_id`),
                  KEY `customer_id` (`customer_id`),
                  KEY `order_id` (`order_id`),
                  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
                  CONSTRAINT `payment_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: product
                CREATE TABLE `product` (
                  `product_id` int NOT NULL AUTO_INCREMENT,
                  `name` varchar(60) NOT NULL,
                  `category` varchar(45) NOT NULL,
                  `parent_category` varchar(45) NOT NULL,
                  `brand` varchar(45) NOT NULL,
                  `model` varchar(45) NOT NULL,
                  `description` varchar(255) NOT NULL,
                  `color` varchar(25) NOT NULL,
                  `price` float NOT NULL,
                  `markup` float NOT NULL,
                  `product_spect` json NOT NULL,
                  `sale_price` float NOT NULL,
                  `warranty` int NOT NULL,
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                  `images` json NOT NULL,
                  `status` varchar(25) NOT NULL,
                  PRIMARY KEY (`product_id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=97000004 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: product_group
                CREATE TABLE `product_group` (
                  `group_id` int NOT NULL AUTO_INCREMENT,
                  `name` varchar(100) NOT NULL,
                  `description` text,
                  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
                  PRIMARY KEY (`group_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: product_temp
                CREATE TABLE `product_temp` (
                  `product_temp_id` int NOT NULL AUTO_INCREMENT,
                  `seller_id` int NOT NULL,
                  `name` varchar(60) NOT NULL,
                  `category` varchar(45) NOT NULL,
                  `parent_category` varchar(45) NOT NULL,
                  `brand` varchar(45) NOT NULL,
                  `model` varchar(45) NOT NULL,
                  `color` varchar(25) NOT NULL,
                  `price` float NOT NULL,
                  `markup` float NOT NULL,
                  `product_spect` json NOT NULL,
                  `sale_price` float NOT NULL,
                  `description` varchar(255) NOT NULL,
                  `warranty` int NOT NULL,
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                  `images` json NOT NULL,
                  `status` varchar(25) NOT NULL DEFAULT 'deactive',
                  PRIMARY KEY (`product_temp_id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=92000003 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: seller
                CREATE TABLE `seller` (
                  `seller_id` int NOT NULL AUTO_INCREMENT,
                  `name` varchar(45) NOT NULL,
                  `family` varchar(45) NOT NULL,
                  `email` varchar(45) DEFAULT NULL,
                  `username` varchar(45) NOT NULL,
                  `password` varchar(60) NOT NULL,
                  `mobile` char(13) NOT NULL,
                  `birthday` varchar(50) NOT NULL,
                  `age` varchar(3) DEFAULT NULL,
                  `address` varchar(255) NOT NULL,
                  `city` varchar(100) NOT NULL,
                  `gender` enum('male','female','unisex') NOT NULL,
                  `position` varchar(20) DEFAULT 'seller',
                  `register_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `shop_name` varchar(50) NOT NULL,
                  `business_license` int DEFAULT NULL,
                  `tax_number` int DEFAULT NULL,
                  `bank_account` varchar(45) NOT NULL,
                  `rating` float NOT NULL,
                  `total_sales` float NOT NULL,
                  `status` varchar(25) DEFAULT NULL,
                  PRIMARY KEY (`seller_id`),
                  UNIQUE KEY `user_name` (`username`),
                  UNIQUE KEY `mobile` (`mobile`),
                  UNIQUE KEY `email` (`email`)
                ) ENGINE=InnoDB AUTO_INCREMENT=60000004 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: stock
                CREATE TABLE `stock` (
                  `stock_id` int NOT NULL AUTO_INCREMENT,
                  `product_id` int NOT NULL,
                  `seller_id` int NOT NULL,
                  `warehouse_id` int NOT NULL,
                  `quantity` int NOT NULL DEFAULT '0',
                  `markup_percent` float DEFAULT '0',
                  `discount_percent` float DEFAULT '0',
                  `sale_price` float NOT NULL DEFAULT '0',
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                  `updated_by` int NOT NULL,
                  PRIMARY KEY (`stock_id`),
                  UNIQUE KEY `unique_inventory` (`product_id`,`seller_id`,`warehouse_id`),
                  KEY `seller_id` (`seller_id`),
                  KEY `warehouse_id` (`warehouse_id`),
                  CONSTRAINT `stock_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
                  CONSTRAINT `stock_ibfk_2` FOREIGN KEY (`seller_id`) REFERENCES `seller` (`seller_id`),
                  CONSTRAINT `stock_ibfk_3` FOREIGN KEY (`warehouse_id`) REFERENCES `warehouse` (`warehouse_id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=4002 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                
                -- Table: warehouse
                CREATE TABLE `warehouse` (
                  `warehouse_id` int NOT NULL AUTO_INCREMENT,
                  `name` varchar(100) NOT NULL,
                  `location` varchar(100) DEFAULT NULL,
                  `warehouse_type` enum('central','in_transit','branch','defective') NOT NULL DEFAULT 'central',
                  `branch_name` varchar(45) DEFAULT NULL,
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  PRIMARY KEY (`warehouse_id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                    """
                DatabaseManager.cursor.execute(tabels)
                DatabaseManager.connection.commit()
                DatabaseManager.cursor.close()
                return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    @staticmethod
    def insert_data(table_name, columns, values) -> tuple[bool, Any]:
        DatabaseManager.ensure_connections()
        try:
            placeholders = ', '.join(['%s'] * len(values))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            DatabaseManager.cursor.execute(query, values)
            DatabaseManager.connection.commit()
            last_id = DatabaseManager.cursor.lastrowid
            print(f"Data inserted into {table_name} successfully!")
            print(f"Last ID: {last_id}")
            return True, last_id
        except mysql.connector.Error as err:
            print(f"Insert error: {err}")
            return False, None

    @staticmethod
    @ensure_connection
    def choice_select(id, name, table):
        query = f"SELECT {id},{name} FROM {table};"
        DatabaseManager.cursor.execute(query)
        return DatabaseManager.cursor.fetchall()

    @staticmethod
    @ensure_connection
    def get_last_insert_id():
        DatabaseManager.cursor.execute("SELECT LAST_INSERT_ID();")
        last_id = DatabaseManager.cursor.fetchone()[0]
        return last_id

    @staticmethod
    @ensure_connection
    def read_data(table_name: str, columns: str = '*', condition: str = None) -> list[dict[Any, Any]] | None:
        try:
            query = f"SELECT {columns} FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"
            DatabaseManager.cursor.execute(query)
            col_names = [col[0] for col in DatabaseManager.cursor.description]
            return [dict(zip(col_names, row)) for row in DatabaseManager.cursor.fetchall()]
        except mysql.connector.Error as err:
            print(f"Read error: {err}")
            return None

    @staticmethod
    @ensure_connection
    def update_data(table_name: str, update_values: Dict, condition: str) -> None:
        try:
            set_clause = ', '.join([f"{col} = %s" for col in update_values.keys()])
            values = list(update_values.values())
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            DatabaseManager.cursor.execute(query, values)
            DatabaseManager.connection.commit()
            print(f"Data updated in {table_name} successfully!")
        except mysql.connector.Error as err:
            print(f"Update error: {err}")

    @staticmethod
    @ensure_connection
    def delete_data(table_name: str, condition: str):
        try:
            query = f"DELETE FROM {table_name} WHERE {condition}"
            DatabaseManager.cursor.execute(query)
            DatabaseManager.connection.commit()
            print(f"Data deleted from {table_name} successfully!")
        except mysql.connector.Error as err:
            print(f"Delete error: {err}")

    @staticmethod
    def generic_sql_fetch(table: str = None, columns: list = None, joins: list = None, filters: list = None) -> List[
         Dict[Any, Any]]:
        col_part = ', '.join(columns) if columns else '*'
        query = f"SELECT {col_part} FROM {table}"
        if joins:
            for join_table, condition in joins:
                query += f" JOIN {join_table} ON {condition}"
        if filters:
            query += " WHERE " + " AND ".join(filters)
        DatabaseManager.cursor.execute(query)
        col_names = [desc[0] for desc in DatabaseManager.cursor.description]
        return [dict(zip(col_names, row)) for row in DatabaseManager.cursor.fetchall()]

    @staticmethod
    @ensure_connection
    def update_stock(warehouse_id=None, product_id=None, seller_id=None, updates: dict = None) -> bool:
        if not updates:
            return False
        set_clause = ", ".join([f"{k} = {v}" for k, v in updates.items()])
        filters = []
        if warehouse_id:
            filters.append(f"warehouse_id = {warehouse_id}")
        if product_id:
            filters.append(f"product_id = {product_id}")
        if seller_id:
            filters.append(f"seller_id = {seller_id}")
        where_clause = " AND ".join(filters)
        query = f"UPDATE warehouse_stock SET {set_clause} WHERE {where_clause}"
        try:
            DatabaseManager.cursor.execute(query)
            DatabaseManager.connection.commit()
            print("Stock updated successfully!")
            return True
        except Exception as e:
            print("Stock update failed:", e)
            return False

    @staticmethod
    def close_connection():
        try:
            if DatabaseManager.cursor:
                DatabaseManager.cursor.close()
                DatabaseManager.cursor = None
            if DatabaseManager.connection:
                DatabaseManager.connection.close()
                DatabaseManager.connection = None
            print("Connection closed.")
        except mysql.connector.Error as err:
            print(f"Error while closing connection: {err}")
