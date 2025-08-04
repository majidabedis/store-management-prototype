from Application.services.stock_service import StockService
from Database.db.connection_manager import DatabaseManager

stock_service = StockService()
database_manager = DatabaseManager()
database_manager.connect()
results = DatabaseManager.generic_sql_fetch(
    table="carts",
    columns=[
        "customer.name AS user_name",
        "laptops.name AS product_name",
        "cart_items.quantity",
        "warehouse_stock.sale_price",
        "warehouse_stock.seller_id",
        "seller.name AS seller_name",
        "(cart_items.quantity * warehouse_stock.sale_price) AS total_price"
    ],
    joins=[
        ("customer", "carts.customer_id = customer.customer_id"),
        ("cart_items", "carts.cart_id = cart_items.cart_id"),
        ("laptops", "cart_items.product_id = laptops.laptop_id"),
        ("warehouse_stock", "cart_items.product_id = warehouse_stock.product_id"),
        ("seller", "warehouse_stock.seller_id = seller.seller_id "),

    ],
    filters=["warehouse_stock.stock_id = cart_items.stock_id"]
)
print(results)
