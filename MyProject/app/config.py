import os


class Config:
    DB_URL = os.getenv("DB_URL", "mysql+pymysql://root:pass@localhost/main_db")
    READONLY_DB_URL = os.getenv("READONLY_DB_URL", "mysql+pymysql://readonly_user:pass@localhost/main_db")


DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'majid6175',
    'database': 'online_shop',
    'pool_size': 10,
    'pool_recycle': 3600 ,
    'charset': 'utf8mb4',
}
